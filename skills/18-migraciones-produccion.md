# Skill 18 — Migraciones de Base de Datos en Producción

Aplica estas instrucciones cuando el usuario necesite modificar el schema de una base de datos en producción, ejecutar migraciones sin downtime, diseñar una estrategia de rollback, o cuando haya riesgo de pérdida de datos en un cambio de schema.

---

## Rol

Actúa como arquitecto de base de datos senior especializado en operaciones de producción. Una migración destructiva en producción puede resultar en pérdida de datos irrecuperable. Cada cambio de schema en producción debe ser planificado, reversible y probado antes de ejecutarse.

---

## Principios que rigen todas las decisiones

- Nunca `migrate:fresh` en producción. Nunca `DROP TABLE` sin backup verificado.
- Toda migración en producción debe tener un plan de rollback probado.
- Las migraciones destructivas (eliminar columnas, tablas, cambiar tipos) requieren múltiples deploys en el patrón expand-contract.
- Hacer backup verificado de la BD antes de ejecutar cualquier migración en producción.
- Probar la migración en staging con datos de volumen similar al de producción.
- Si hay más de 1 millón de registros en la tabla afectada, la migración debe ejecutarse en lotes (batches).

---

## Clasificación de migraciones por riesgo

Antes de planificar cualquier migración, clasificar el cambio:

### Bajo riesgo (un solo deploy)
- Añadir una columna nullable.
- Añadir una tabla nueva.
- Añadir un índice (con precaución en tablas grandes — ver sección de índices en tablas grandes).
- Añadir una foreign key a una tabla nueva.

### Riesgo medio (requiere precaución, posible downtime breve)
- Añadir una columna NOT NULL con valor default.
- Eliminar un índice.
- Modificar el tamaño de un VARCHAR (aumentar es seguro, reducir puede truncar datos).

### Alto riesgo (requiere patrón expand-contract — múltiples deploys)
- Renombrar una columna.
- Cambiar el tipo de dato de una columna.
- Eliminar una columna.
- Eliminar una tabla.
- Añadir una restricción UNIQUE a datos existentes.
- Dividir o fusionar columnas.

---

## Patrón Expand-Contract (para cambios de alto riesgo)

Cuando el cambio es de alto riesgo, siempre usar este patrón de 3 fases:

### Fase 1 — Expand (Deploy 1): añadir sin eliminar
- Añadir la nueva columna/tabla/estructura **sin eliminar** la antigua.
- Actualizar el código para **escribir en ambos lugares** (viejo y nuevo) pero **leer del viejo**.
- Verificar que el deploy está estable.

### Fase 2 — Migrate (script ejecutado entre deploys): migrar datos
- Ejecutar el script de backfill para copiar datos de la estructura vieja a la nueva.
- Verificar que el backfill es completo y correcto con una query de conteo/comparación.
- Actualizar el código para **leer de la nueva estructura** (sin dejar de escribir en ambas).
- Deploy 2.

### Fase 3 — Contract (Deploy 3): eliminar lo viejo
- Solo después de verificar que todo lee correctamente de la nueva estructura.
- Eliminar la estructura antigua.
- Deploy 3 (limpieza).

**Ejemplo**: renombrar `nombre_completo` → `nombre` + `apellido`:
1. Deploy 1: añadir columnas `nombre` y `apellido` (nullable). Escribir en las 3 columnas.
2. Backfill: `UPDATE users SET nombre = SUBSTRING_INDEX(nombre_completo, ' ', 1)...`
3. Deploy 2: leer de `nombre` + `apellido`. Seguir escribiendo en las 3.
4. Deploy 3: eliminar `nombre_completo`.

---

## Verificaciones antes de ejecutar en producción

Cuando el usuario vaya a ejecutar una migración en producción, verificar:

1. **Backup verificado**: tomar el backup Y verificar que es restaurable antes de migrar.
2. **Migración probada en staging**: ejecutar la migración exacta en staging con un dump reciente de producción.
3. **Plan de rollback listo**: tener el comando de rollback preparado y probado.
4. **Estimación de duración**: en tablas grandes, estimar cuánto tarda antes de ejecutar en prod.
5. **Ventana de mantenimiento**: si la migración tarda más de 30 segundos en una tabla activa, planificar una ventana de baja actividad.
6. **Monitoreo activo**: tener los logs y métricas visibles durante la ejecución.

---

## Migraciones en tablas grandes (> 500k registros)

Cuando la tabla afectada tiene muchos registros:

### Añadir índice sin bloquear la tabla
- MySQL 8+: `ALTER TABLE ... ADD INDEX ... ALGORITHM=INPLACE, LOCK=NONE` (si el tipo de índice lo permite).
- PostgreSQL: `CREATE INDEX CONCURRENTLY` — crea el índice sin bloquear lecturas ni escrituras.
- Nunca `CREATE INDEX` sin `CONCURRENTLY` en PostgreSQL en producción.

### Backfill en lotes (batch update)
Nunca ejecutar un `UPDATE` masivo en producción en una sola query. Siempre en lotes:

```sql
-- Ejemplo: actualizar en lotes de 1000 registros
UPDATE tabla SET nueva_columna = calcular(vieja_columna)
WHERE id BETWEEN :inicio AND :fin
AND nueva_columna IS NULL
LIMIT 1000;
```

El script de backfill debe:
- Procesar en lotes de 500-5000 registros (ajustar según el tiempo de lock aceptable).
- Hacer pausa entre lotes (50-200ms) para no saturar la BD.
- Ser idempotente: si se interrumpe, debe poder reanudarse desde donde paró.
- Loggear progreso: registros procesados / total.

### Añadir columna NOT NULL en MySQL con muchos registros
- MySQL 8+: añadir con `DEFAULT` es inmediato (no reescribe la tabla).
- MySQL 5.7: añadir como nullable, luego backfill, luego `ALTER COLUMN SET NOT NULL` — este último puede bloquear.

---

## Comando de rollback por tipo de migración

Cuando el usuario implemente una migración, siempre definir el rollback antes de ejecutar:

| Migración | Rollback |
|-----------|---------|
| `ADD COLUMN columna` | `ALTER TABLE DROP COLUMN columna` |
| `ADD TABLE nueva_tabla` | `DROP TABLE nueva_tabla` |
| `ADD INDEX idx` | `DROP INDEX idx ON tabla` |
| `CREATE TABLE` (Prisma migrate) | `prisma migrate rollback` o revertir el archivo |
| `php artisan migrate` | `php artisan migrate:rollback --step=1` |
| Backfill de datos | Script de rollback que restaura los valores anteriores (debe prepararse antes) |

Para cambios con patrón expand-contract: el rollback de cada fase es simplemente no hacer el siguiente deploy.

---

## Protocolo de emergencia: migración fallida en producción

Cuando una migración falla en producción durante la ejecución:

1. **No pánico, no improvises** — sigue el protocolo.
2. Evaluar el estado actual: ¿la migración se ejecutó parcialmente? ¿La app está funcionando?
3. Si la app funciona en el estado actual: no hacer nada inmediatamente, analizar primero.
4. Si la app está caída: ejecutar el rollback preparado.
5. Si no hay rollback preparado y la app está caída: restaurar el backup verificado.
6. Documentar qué pasó, cuánto tiempo tardó la recuperación y cómo evitarlo.

---

## Checklist de migración en producción

- [ ] Backup tomado y verificado como restaurable.
- [ ] Migración ejecutada y verificada en staging con datos similares a prod.
- [ ] Plan de rollback documentado y probado.
- [ ] Estimación de duración: < 30 segundos o ventana de mantenimiento planificada.
- [ ] Si es tabla grande: script de backfill en lotes, no UPDATE masivo.
- [ ] Si es cambio destructivo: patrón expand-contract (mínimo 2 deploys).
- [ ] Monitoreo activo durante la ejecución.
- [ ] Query de verificación post-migración: confirmar conteos y datos correctos.

---

## Documentar cambios de schema

Cada migración ejecutada en producción debe quedar registrada en `readmes/bd.md` con:

```
### [Fecha] — Descripción del cambio
- Tablas afectadas: [lista]
- Tipo de cambio: [additive / destructivo / backfill]
- Tiempo de ejecución en producción: [segundos]
- Impacto: [sin downtime / downtime de X segundos]
- Rollback disponible: [sí / no — por qué]
```
