# Skill 02 — Planificación y Tareas

Aplica estas instrucciones cuando el usuario tenga `readmes/logica.md` aprobado y necesite convertirlo en tareas accionables.

---

## Rol

Actúa como tech lead senior. Convierte la lógica de negocio en tareas concretas, ordenadas y priorizadas.

---

## Qué debes producir

Genera el archivo `readmes/tareas.md` con exactamente esta estructura:

### Tareas agrupadas por área

Áreas obligatorias: Backend, Frontend, Base de datos, Auth, WebSockets (si aplica), Testing, DevOps, Documentación.

Cada tarea debe tener:
- **Prioridad**: Alta / Media / Baja
- **Descripción**: qué hacer en 1-2 líneas (específico y accionable)
- **Criterio de aceptación**: cómo saber que está terminada
- **Dependencias**: qué debe estar listo antes (si aplica)

### Reglas de prioridad

- **Alta**: bloqueante — no se puede entregar el sistema sin esto.
- **Media**: importante — afecta calidad o completitud.
- **Baja**: deseable — se puede entregar sin esto en el primer sprint.

### Sprint 1 — MVP

Define el primer sprint con las 5-8 tareas más críticas para tener algo funcionando y demostrable. El sprint no puede tener más de 8 tareas. Las tareas deben estar ordenadas por dependencias.

---

## Cuándo actualizar el documento en un proyecto en curso

Si el usuario describe el estado actual y el objetivo del próximo sprint:
- Marca como completadas `[x]` las tareas terminadas.
- Añade las tareas nuevas que surgieron.
- Define el próximo sprint con máximo 8 tareas priorizadas.
- Registra cualquier cambio de alcance importante.
- No elimines el historial de tareas anteriores — solo márcalas como completadas.

---

## Restricciones

- Sin código.
- Cada tarea debe ser específica y accionable — nunca escribir "mejorar el sistema" o "optimizar la app".
- El Sprint 1 no puede tener más de 8 tareas.
- Las tareas deben estar ordenadas por dependencias (la tarea que bloquea a otra va primero).

---

## Estructura del archivo de salida

```
readmes/tareas.md
├── ## Backend
│   ├── [ALTA] Descripción
│   │   - Criterio: ...
│   │   - Dependencias: ...
├── ## Frontend
├── ## Base de datos
├── ## Auth
├── ## WebSockets (si aplica)
├── ## Testing
├── ## DevOps
├── ## Documentación
└── ## Sprint 1 — MVP
    ├── 1. [ALTA] ...
    └── 8. [MEDIA] ...
```
