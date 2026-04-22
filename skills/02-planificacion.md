# 📋 Skill 02 — Planificación y Gestión de Tareas

> **Fase:** Antes de codificar  
> **Objetivo:** Convertir la lógica de negocio en tareas accionables, priorizadas y con criterios de aceptación claros.

---

## Cuándo usar este skill

- Justo después de tener `logica.md` aprobado.
- Al iniciar un nuevo sprint o iteración.
- Cuando el alcance del proyecto cambia o crece.

---

## Estructura de tareas

Las tareas se agrupan por área. Cada tarea tiene: descripción, prioridad y criterio de aceptación.

### Áreas estándar

| Área | Prioridad típica |
|------|-----------------|
| Backend (API, modelos, servicios) | Alta |
| Frontend (vistas, componentes, UX) | Alta |
| Base de datos (migraciones, seeds) | Alta |
| Auth y permisos | Alta |
| Testing | Media |
| DevOps / Infraestructura | Media |
| Seguridad | Media |
| Rendimiento / Escalado | Baja (inicial) |
| Documentación | Baja (continua) |
| Scripts auxiliares | Baja |

---

## Formato de tarea

```markdown
### [ÁREA] — [Nombre de la tarea]
- **Prioridad:** Alta / Media / Baja
- **Descripción:** Qué hay que hacer y por qué.
- **Archivos implicados:** lista de paths relevantes (si ya se sabe)
- **Criterio de aceptación:** cómo sé que esta tarea está terminada
- **Dependencias:** qué debe estar listo antes
```

---

## Prompt para generar tareas.md con Claude

```
Basándote en readmes/logica.md, genera un archivo tareas.md con:
- Tareas agrupadas por área (Backend, Frontend, BD, Auth, Testing, DevOps, Docs)
- Cada tarea con: prioridad (Alta/Media/Baja), descripción de 1-2 líneas, criterio de aceptación
- Un primer sprint con las 5-8 tareas más críticas para tener algo funcionando
- Ordenadas por dependencias (qué debe ir primero)
Sin código, solo la lista de tareas.
```

---

## Gestión de prioridades

**Regla principal:** No avanzar a una tarea de menor prioridad si hay bloqueantes pendientes en las de mayor prioridad.

```
Alta   → Bloqueante. No se puede entregar sin esto.
Media  → Importante. Afecta calidad o completitud.
Baja   → Deseable. Se puede entregar sin esto en el primer sprint.
```

### Señales de que hay que replantear prioridades

- Una tarea "media" bloquea otra "alta" → sube a alta.
- Una tarea "alta" lleva más de 2 días bloqueada → escalar o rediseñar.
- El primer sprint tiene más de 10 tareas → está sobreestimado, reducir.

---

## Definir el primer sprint

El primer sprint debe producir algo **demostrable y funcional**, aunque incompleto:

```markdown
## Sprint 1 — MVP funcional

Objetivo: sistema corriendo con auth y módulo principal básico.

Tareas:
1. [ALTA] Crear migraciones de tablas principales
2. [ALTA] Configurar roles y permisos (Spatie)
3. [ALTA] Endpoint de autenticación (login/logout)
4. [ALTA] CRUD básico del módulo principal
5. [ALTA] Vistas básicas del módulo principal
6. [MEDIA] Seeders con datos de demo
```

---

## Seguimiento durante el proyecto

Mantener `tareas.md` actualizado conforme avanza el proyecto:

- Marcar tareas completadas con `[x]`
- Añadir tareas emergentes que aparezcan durante el desarrollo
- Registrar decisiones importantes que afecten el alcance

---

## Reglas al usar este skill

- ✅ Toda tarea tiene criterio de aceptación antes de ejecutarse.
- ✅ El primer sprint es pequeño y demostrable.
- ✅ Las dependencias entre tareas están explícitas.
- ❌ No crear tareas ambiguas tipo "mejorar el sistema" — siempre específicas.
- ❌ No poner más de 8-10 tareas en un sprint.

---

## Siguiente paso

→ [`03-arquitectura.md`](03-arquitectura.md) — Definir el stack y la estructura técnica.
