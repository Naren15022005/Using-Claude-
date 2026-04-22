# 📝 Skill 11 — Documentación

> **Fase:** Todo el ciclo de vida  
> **Objetivo:** Mantener la documentación sincronizada con el código real del proyecto en todo momento.

---

## Cuándo usar este skill

- Después de implementar cualquier módulo o feature.
- Al terminar un sprint.
- Al onboardear a un nuevo colaborador.
- Antes de hacer deploy (la documentación refleja el estado real).

---

## Principio central

> **La documentación desactualizada es peor que no tener documentación.**

Cada vez que se implementa algo, se actualiza el documento correspondiente en la misma sesión. No se pospone.

---

## Estructura de documentación por proyecto

```
proyecto/
├── README.md                   ← Punto de entrada: cómo arrancar el proyecto
└── readmes/
    ├── logica.md               ← Lógica de negocio y reglas (skill 01)
    ├── tareas.md               ← Desglose de tareas y sprints (skill 02)
    ├── flujo-final.md          ← Arquitectura y estado real del sistema
    ├── flujo_backend.md        ← Estado e implementación del backend
    ├── flujo_frontend.md       ← Estado e implementación del frontend
    └── bd.md                   ← Diseño y esquema de base de datos
```

---

## Contenido de cada documento

### README.md (portada del proyecto)

```markdown
# [Nombre del Proyecto]

## Descripción
[Una línea describiendo qué hace el sistema]

## Stack
[Lista del stack tecnológico]

## Cómo arrancar

### Prerequisitos
- [versiones de Node, PHP, Docker, etc.]

### Instalación
[Pasos para levantar el entorno desde cero]

### Credenciales de demo
- Admin: admin@demo.com / Admin123!
```

### readmes/flujo_backend.md

```markdown
# Estado del Backend

## ✅ Implementado
- [lista de módulos y endpoints funcionando]

## 🔄 En progreso
- [lo que está a medias]

## ❌ Pendiente
- [tareas de backend sin empezar]

## Porcentaje de avance estimado: [X]%

## Comandos útiles
[comandos frecuentes para esa capa]

## Decisiones de diseño
[por qué se eligió X en lugar de Y]
```

### readmes/flujo_frontend.md

```markdown
# Estado del Frontend

## ✅ Implementado
- [lista de páginas y componentes funcionando]

## 🔄 En progreso
- [lo que está a medias]

## ❌ Pendiente
- [páginas/componentes sin implementar]

## Porcentaje de avance estimado: [X]%

## Rutas del sistema
| Ruta | Componente | Rol requerido |
|------|-----------|---------------|
| /admin/productos | ProductosIndex | administrador |
```

### readmes/bd.md

```markdown
# Base de Datos

## Schema actual
[Lista de tablas con columnas principales]

## Relaciones
[Diagrama ASCII o descripción de relaciones]

## Migraciones aplicadas
[Lista de migraciones en orden]

## Datos de seed
[Qué datos crea el seeder y para qué]
```

---

## Prompt para actualizar documentación después de implementar

```
Actualiza readmes/flujo_backend.md con lo que se implementó en esta sesión:
- Módulo: [nombre]
- Lo que se creó: [lista de archivos]
- Endpoints nuevos: [lista]
- Mueve las tareas correspondientes de "Pendiente" a "Implementado"
- Actualiza el porcentaje de avance estimado
No cambies secciones que no correspondan a esta sesión.
```

---

## Prompt para generar README.md inicial

```
Genera el README.md principal del proyecto con:
- Descripción de una línea
- Stack tecnológico (ver readmes/flujo-final.md)
- Instrucciones de instalación desde cero (ver readmes/flujo-final.md para comandos)
- Credenciales de demo del seeder
- Estructura de carpetas simplificada
Formato: markdown limpio, orientado a un developer que clona el repo por primera vez.
```

---

## Convenciones de documentación

| Aspecto | Convención |
|---------|-----------|
| Idioma | Español |
| Nombres de archivos | snake_case (`flujo_backend.md`) |
| Estado de tareas | ✅ Hecho / 🔄 En progreso / ❌ Pendiente |
| Porcentaje de avance | Estimación honesta, actualizada en cada sesión |
| Comandos | Siempre en bloques de código con el shell correcto |
| Decisiones técnicas | Registrar el por qué, no solo el qué |

---

## Documentar decisiones de diseño

Cuando se toma una decisión técnica importante, registrarla en el documento de flujo correspondiente:

```markdown
## Decisiones de diseño

### Por qué Redis para locks de concurrencia
El sistema permite múltiples usuarios comprando el mismo producto simultáneamente.
Se eligió Redis locks en lugar de transacciones DB porque las transacciones en MySQL
no previenen race conditions entre procesos distintos con el mismo dato.
Fecha: [fecha]
```

---

## Reglas al usar este skill

- ✅ Actualizar la documentación en la misma sesión en que se implementa algo.
- ✅ El README.md debe permitir a cualquier desarrollador levantar el proyecto desde cero.
- ✅ Registrar el *por qué* de las decisiones técnicas importantes.
- ❌ No documentar código obvio — documentar decisiones y comportamientos no evidentes.
- ❌ No tener documentación que contradiga el código actual.
