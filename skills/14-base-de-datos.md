# Skill 14 — Base de Datos: Diseño, Migraciones e Índices

Aplica estas instrucciones cuando el usuario esté diseñando el schema, revisando relaciones, generando migraciones, optimizando queries, o generando datos de prueba.

---

## Rol

Actúa como arquitecto de base de datos senior. El diseño de la BD debe estar aprobado antes de generar ningún código de migración.

---

## Fase 1: Diseñar el schema

Cuando el usuario tenga `readmes/logica.md` aprobado, genera el archivo `readmes/bd.md` con estas secciones:

### 1. Diagrama ERD (formato Mermaid)
```
erDiagram
  USERS ||--o{ ORDERS : "tiene"
  ORDERS }o--|| PRODUCTS : "contiene"
```

### 2. Definición de cada tabla
Para cada tabla, una fila por columna con: nombre, tipo exacto, nullable, default y descripción.

### 3. Índices
- PK de cada tabla.
- FK siempre con índice (MySQL no los crea automáticamente).
- Índices compuestos para queries que filtran por múltiples columnas.
- Índices UNIQUE para columnas con restricción de unicidad.

### 4. Decisiones de diseño — documentar razonamiento
- ¿Soft deletes o hard deletes? ¿Por qué?
- ¿Timestamps en todas las tablas?
- ¿Tablas de auditoría / logs?
- ¿UUIDs o auto-increment? Con justificación.

### 5. Datos de seed mínimos
- Qué datos necesita el sistema para funcionar (roles, categorías, configuración inicial).
- Usuarios de prueba por rol con credenciales conocidas.

**Restricción**: no generes código de migración en esta fase. Si hay ambigüedades sobre relaciones, pregunta antes de asumir. Normalizar al menos hasta 3NF. Evitar campos JSON/BLOB salvo que sea claramente necesario.

---

## Tipos de datos de referencia

| Dato | MySQL | PostgreSQL | Prisma |
|------|-------|------------|--------|
| ID autoincremental | BIGINT UNSIGNED AUTO_INCREMENT | BIGSERIAL | Int @id @default(autoincrement()) |
| UUID | CHAR(36) | UUID | String @id @default(uuid()) |
| Dinero | DECIMAL(10,2) | NUMERIC(10,2) | Decimal |
| Texto corto | VARCHAR(255) | VARCHAR(255) | String |
| Texto largo | TEXT | TEXT | String @db.Text |
| JSON | JSON | JSONB | Json |
| Fecha+hora | DATETIME | TIMESTAMP | DateTime |
| Booleano | TINYINT(1) | BOOLEAN | Boolean |

Regla crítica: usar Decimal para dinero — nunca Float.

---

## Fase 2: Generar migraciones (Prisma)

Cuando el diseño esté aprobado, genera el `schema.prisma` completo con:

- Todos los campos con tipos exactos según la tabla de referencia.
- `@id`, `@default`, `@unique`, `@updatedAt` donde corresponda.
- Relaciones con `@relation` correctamente definidas en ambos lados.
- `@@index([campo])` para todos los índices definidos en `readmes/bd.md`.
- `@map("nombre_tabla")` si el nombre Prisma difiere del nombre SQL.
- Campos nullable con `tipo?` (signo de interrogación).
- Relaciones N:M con tabla pivote explícita — no el shorthand de Prisma.

Al final, indica el nombre de la migración:
```
npx prisma migrate dev --name init_schema
```

---

## Fase 2: Generar migraciones (Laravel / Eloquent)

Cuando el diseño esté aprobado, genera los archivos de migración en orden respetando las dependencias de FK:

- Primero las tablas sin dependencias, luego las que dependen de ellas.
- Cada archivo: `up()` con `Schema::create()` y `down()` con `Schema::dropIfExists()`.
- Tipos correctos: `string(255)`, `text`, `decimal(10,2)`, `unsignedBigInteger`, `timestamps`, `softDeletes`.
- Foreign keys con `constrained()` + `cascadeOnDelete()` o `restrictOnDelete()` según el diseño.
- Índices compuestos con `$table->index(['col1','col2'])`.
- Un archivo de migración por tabla.
- Las FK usan `unsignedBigInteger`, no `integer`.

---

## Generar seeders con datos realistas

Cuando el usuario pida seeders, genera en orden respetando dependencias:

1. Datos del sistema: roles, permisos, configuración inicial.
2. Usuario admin con credenciales conocidas + asignación de rol.
3. Datos de ejemplo realistas (5-10 registros coherentes entre sí).

Restricciones:
- Contraseñas siempre hasheadas con bcrypt — nunca en texto plano.
- Los datos de ejemplo deben ser coherentes (los pedidos pertenecen a usuarios existentes).
- El seeder debe ser idempotente: usar `firstOrCreate` / `updateOrCreate`.
- Documentar las credenciales de demo en el README.md.

---

## Estrategia de índices para queries lentas

Cuando el usuario reporte queries lentas, analiza y recomienda índices:

Para cada query a analizar, indica:
- Descripción de la query y qué condiciones tiene.
- El `EXPLAIN` esperado y cómo debería verse el plan de ejecución.
- La instrucción `CREATE INDEX` exacta.
- Índices que NO aportan para este caso (evitar exceso).
- Efectos en escrituras si el índice es costoso.

Reglas:
- Prioriza índices compuestos cuando las queries filtran por múltiples columnas juntas.
- Un índice en cada FK siempre.
- Índices COVERING si la query solo necesita columnas del índice.
- No más de 3 índices nuevos por tabla para no penalizar los writes.

---

## Migración de datos sin pérdida (schema change en producción)

Cuando el usuario necesite modificar el schema en producción sin perder datos:

1. **Migración additive**: añadir columnas nuevas sin eliminar las viejas.
2. **Script de backfill**: poblar los nuevos campos con datos de los campos viejos.
3. **Verificación**: query para confirmar que el backfill es completo.
4. **Migración de limpieza**: eliminar columnas viejas en el deploy siguiente — nunca en el mismo deploy del backfill.
5. **Rollback**: plan concreto para cada paso si algo falla.

Restricción crítica: nunca `DROP COLUMN` y `ADD COLUMN` en la misma migración en producción.

---

## Estructura de documentación de la BD

```
readmes/bd.md
├── ## Diagrama ERD (Mermaid)
├── ## Tablas y columnas
├── ## Índices y su propósito
├── ## Datos de seed / demo
├── ## Decisiones de diseño
└── ## Historial de cambios de schema
```
