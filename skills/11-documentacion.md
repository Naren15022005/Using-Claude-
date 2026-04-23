# Skill 11 — Documentación

Aplica estas instrucciones cuando el usuario haya implementado un módulo, al terminar una sesión, o antes de un deploy. La documentación debe actualizarse en la misma sesión en que se implementa algo.

---

## Rol

Actúa como desarrollador senior que mantiene la documentación técnica al día. Documenta solo lo que realmente existe en el código — nunca inventes funcionalidad.

---

## Actualizar docs después de implementar un módulo

Cuando el usuario indique qué se implementó en la sesión, actualiza:

### `readmes/flujo_backend.md`
- Mueve las tareas correspondientes de "Pendiente" a "Implementado".
- Añade los endpoints nuevos con formato: `MÉTODO /ruta — descripción`.
- Actualiza el porcentaje de avance estimado (ser honesto — no inflar).

### `readmes/bd.md`
- Añade las tablas nuevas con sus columnas principales.
- Actualiza las relaciones si cambiaron.
- Registra los índices añadidos.

### `readmes/tareas.md`
- Marca como completadas `[x]` las tareas terminadas.
- Añade las tareas nuevas que surgieron durante la implementación.

**Restricción**: no modifiques secciones que no correspondan a lo implementado en esta sesión. No añadas información sobre funcionalidad no implementada.

---

## Generar README.md inicial del proyecto

Cuando el usuario pida el README principal del proyecto, genera un documento que permita a un desarrollador que clona el repo levantar el proyecto desde cero sin preguntar nada.

Estructura obligatoria:

1. Nombre y descripción en una línea.
2. Stack tecnológico (lista simple con versiones).
3. Prerequisitos (versiones necesarias de Node/PHP/Docker).
4. Instalación paso a paso (comandos exactos y ejecutables).
5. Credenciales de demo del seeder (usuario admin + contraseña).
6. Estructura de carpetas simplificada (solo niveles principales).
7. Comandos de uso frecuente (levantar, migrar, testear, buildear).

Formato: markdown limpio, sin emojis, comandos en bloques de código con el shell correcto.

---

## Actualizar docs al terminar un sprint

Cuando el usuario indique que terminó un sprint, actualiza:

1. `readmes/tareas.md` — marca completadas, añade nuevas si surgieron.
2. `readmes/flujo_backend.md` — estado actualizado del backend.
3. `readmes/flujo_frontend.md` — estado actualizado del frontend (si aplica).

Para cada decisión técnica importante tomada durante el sprint, regístrala en el documento correspondiente con:
- Qué se decidió.
- Por qué (la razón técnica o de negocio).
- Fecha de la decisión.

---

## Estructura de documentación del proyecto

Mantén siempre esta estructura en el proyecto:

```
proyecto/
├── README.md                   → Cómo arrancar (orientado a developer nuevo)
└── readmes/
    ├── logica.md               → Dominio, reglas y endpoints (skill 01)
    ├── tareas.md               → Tareas y sprints (skill 02)
    ├── flujo-final.md          → Arquitectura y decisiones técnicas
    ├── flujo_backend.md        → Estado del backend
    ├── flujo_frontend.md        → Estado del frontend
    ├── bd.md                   → Schema y relaciones de BD
    └── design-system.md        → Paleta, tipografía, componentes y layouts
```

---

## Estados estándar para los docs

Usa siempre estos estados para indicar el avance de cada sección:

```
✅ Implementado y funcionando
🔄 En progreso / parcialmente implementado
❌ Pendiente, no empezado
```

El porcentaje de avance debe ser una estimación honesta del avance real del módulo o proyecto.
