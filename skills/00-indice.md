# 📂 Skills de Desarrollo — Índice

> Ciclo completo desde la idea inicial hasta la entrega exitosa de un proyecto, usando Claude/Copilot como asistente principal.

---

## Mapa del ciclo de vida

```
💡 IDEA
  └─► 01-idea-y-negocio.md          Definir el dominio, entidades y reglas
        └─► 02-planificacion.md      Desglosar tareas, prioridades, sprints
              └─► 03-arquitectura.md Elegir stack, estructura de carpetas
                    └─► 04-setup-entorno.md   Levantar entorno local
                          └─► 05-desarrollo-modulo.md  Ciclo CRUD por módulo
                                ├─► 06-comunicacion-agente.md  Prompts eficientes
                                ├─► 07-debugging.md             Resolver problemas
                                ├─► 08-testing.md               Verificar cambios
                                └─► 09-code-review.md           Revisar con Claude
                                      └─► 10-deploy-entrega.md  Pre-deploy y entrega
                                            ├─► 11-documentacion.md  Mantener docs
                                            └─► 12-tokens-prompts.md Optimizar tokens
✅ ENTREGA
```

---

## Archivos del directorio

| # | Archivo | Propósito |
|---|---------|-----------|
| 00 | `00-indice.md` | Este índice con el mapa del ciclo |
| 01 | `01-idea-y-negocio.md` | Definición del dominio, entidades, actores y reglas de negocio |
| 02 | `02-planificacion.md` | Desglose de tareas, prioridades, sprints y gestión con Claude |
| 03 | `03-arquitectura.md` | Decisiones de stack, estructura de carpetas y convenciones técnicas |
| 04 | `04-setup-entorno.md` | Levantar el entorno local paso a paso (Docker, migraciones, seeds) |
| 05 | `05-desarrollo-modulo.md` | Ciclo de desarrollo módulo por módulo (CRUD completo) |
| 06 | `06-comunicacion-agente.md` | Cómo pedir trabajo a Claude de forma eficiente |
| 07 | `07-debugging.md` | Flujo para diagnosticar y resolver bugs con Claude |
| 08 | `08-testing.md` | Estrategias de verificación, tests de aceptación y QA |
| 09 | `09-code-review.md` | Revisión de código asistida por Claude |
| 10 | `10-deploy-entrega.md` | Checklist de cierre, configuración producción y deploy |
| 11 | `11-documentacion.md` | Convenciones para mantener docs actualizados en paralelo al código |
| 12 | `12-tokens-prompts.md` | Patrones de prompts y estrategias para minimizar consumo de tokens |

---

## Cómo usar estos skills

1. **Proyecto nuevo** → empieza por `01` y avanza en orden.
2. **Proyecto en curso** → abre el skill correspondiente a la fase activa.
3. **Problema puntual** → ve directamente al skill relevante (`07` para bugs, `09` para review, etc.).
4. **Optimizar uso de Claude** → `06` y `12` son de consulta frecuente.

---

*Basado en los flujos reales de trabajo documentados en `recopilandologicasdetrabajo.md`.*
