# 💡 Skill 01 — Idea y Lógica de Negocio

> **Fase:** Inicio de proyecto  
> **Objetivo:** Transformar una idea en un documento de dominio sólido antes de tocar código.

---

## Cuándo usar este skill

- Al iniciar un proyecto desde cero.
- Al añadir un módulo nuevo que no estaba contemplado.
- Cuando el equipo no tiene claridad sobre qué construir exactamente.

---

## Proceso

### Paso 1 — Definir el propósito y los actores

Antes de escribir código, responde estas preguntas:

```
¿Para qué existe este sistema?
¿Quién lo usa? (roles: administrador, recepcionista, cliente, etc.)
¿Qué problema resuelve concretamente?
¿Quiénes son los stakeholders? ¿Qué esperan?
```

### Paso 2 — Identificar las entidades del dominio

Lista todas las entidades que el sistema maneja:

```
Entidades principales: Usuario, Producto, Pedido, Membresía, ...
Relaciones: Un Usuario tiene muchos Pedidos. Un Pedido tiene muchos Productos.
Enumeraciones: Estado del pedido (pendiente, activo, cerrado), Rol (admin, recepcionista)
```

### Paso 3 — Definir reglas de negocio

Las reglas más importantes a documentar:

```
- Un pedido solo puede cancelarse si está en estado "pendiente".
- Solo el administrador puede acceder al módulo de configuración.
- El stock se descuenta al confirmar el pedido, no al crearlo.
- Las transacciones de pago deben ser atómicas (todo o nada).
```

### Paso 4 — Mapear los flujos principales

Describe en texto simple el flujo de cada actor:

```
Flujo de compra:
1. Cliente selecciona productos
2. Sistema valida stock
3. Cliente confirma y paga
4. Sistema descuenta stock y genera orden
5. Admin ve la orden en el panel
```

### Paso 5 — Proponer endpoints REST (si aplica)

```
GET    /api/products          → listar productos
POST   /api/orders            → crear orden
PATCH  /api/orders/:id/status → cambiar estado
DELETE /api/orders/:id        → cancelar (solo si pendiente)
```

---

## Prompt para pedir esto a Claude

```
Voy a iniciar un proyecto: [descripción breve].
Actores: [lista de roles].
Entidades principales: [lista].
Genera un documento logica.md con:
- Propósito y stakeholders
- Entidades, relaciones y enumeraciones
- Reglas de negocio principales
- Flujos de los actores principales
- Endpoints REST propuestos
Formato: markdown estructurado, sin código aún.
```

---

## Documento de salida esperado

Archivo: `readmes/logica.md` (o `docs/logica.md`)

```markdown
# Lógica de Negocio — [Nombre del Proyecto]

## Propósito
...

## Actores y roles
...

## Entidades y relaciones
...

## Reglas de negocio
...

## Flujos principales
...

## Endpoints propuestos
...
```

---

## Reglas al usar este skill

- ✅ Primero el documento, después el código.
- ✅ Si algo no está claro en el dominio, pregunta antes de asumir.
- ✅ Las reglas de negocio deben ser verificables (criterios de aceptación concretos).
- ❌ No modelar la base de datos en este paso — eso va en el skill de arquitectura.
- ❌ No empezar a generar migraciones hasta tener este documento aprobado.

---

## Siguiente paso

→ [`02-planificacion.md`](02-planificacion.md) — Convertir la lógica en tareas accionables.
