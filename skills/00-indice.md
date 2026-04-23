# Skills de Desarrollo — Índice de Instrucciones para Claude

Estos archivos son instrucciones directas para Claude, no prompts para el usuario. Cada skill define el rol, los entregables, las restricciones y el comportamiento exacto que Claude debe adoptar en esa situación.

---

## Regla fundamental

Cuando el usuario mencione una fase, tarea o situación que coincida con uno de estos skills, **aplicar ese skill inmediatamente** sin esperar que el usuario lo pida explícitamente. El skill 06 aplica siempre, en toda sesión.

---

## Skills siempre activos

Estos skills no son de fase — se aplican en cualquier momento de la sesión:

| Skill | Cuándo se activa |
|-------|-----------------|
| **06-comunicacion-agente** | Siempre. Define el idioma (español), tono, longitud de respuestas y comandos `/fix`, `/plan`, `/commit`, etc. Es la capa base de toda sesión. |
| **12-tokens-prompts** | Cuando la sesión se vuelve larga, el contexto crece, o el usuario pide compactar la información. |

---

## Mapa del ciclo de vida completo

```
[INICIO DEL PROYECTO]
  │
  ├─ ¿Necesita estimar o presupuestar? ──────────────► 20-estimacion-presupuesto
  │
  ▼
01-idea-y-negocio       → readmes/logica.md
  │
  ▼
02-planificacion        → readmes/tareas.md
  │
  ▼
03-arquitectura         → readmes/flujo-final.md
  │   └── relacionado con: 14 (schema), 15 (JWT/RBAC), 17 (variables)
  │
  ▼
04-setup-entorno        → comandos y archivos de setup
  │   └── relacionado con: 17 (variables de entorno), 19 (CI/CD)
  │
  ▼
05-desarrollo-modulo    → código del módulo completo
  │   └── relacionado con: 13 (UI), 14 (BD), 15 (auth), 16 (errores), 17 (secrets)
  │
  ├─► 07-debugging          (en cualquier momento del desarrollo)
  ├─► 08-testing            (al terminar cada módulo o al reproducir un bug)
  ├─► 09-code-review        (antes de abrir un PR o antes de deploy)
  ├─► 11-documentacion      (al terminar cada sesión o módulo)
  │
  ▼
[PRE-DEPLOY]
  ├─► 18-migraciones-produccion   (si hay cambios de schema)
  ├─► 09-code-review              (revisión de seguridad)
  └─► 19-cicd                     (si el pipeline no existe o hay que modificarlo)
  │
  ▼
10-deploy-entrega       → checklist de deploy y validación

[POST-DEPLOY]
  └─► 11-documentacion   → actualizar readmes con lo entregado
```

---

## Tabla de referencia completa

| # | Skill | Aplicar cuando... | Entregables |
|---|-------|-------------------|-------------|
| 01 | idea-y-negocio | El usuario describe un proyecto nuevo o quiere formalizar una idea | `readmes/logica.md` con dominio, entidades, reglas, endpoints, matriz de permisos, eventos WebSocket |
| 02 | planificacion | Se tiene `logica.md` y hay que convertirlo en tareas concretas | `readmes/tareas.md` con tareas priorizadas y sprint MVP |
| 03 | arquitectura | Se tienen las tareas y hay que decidir el stack y la estructura | `readmes/flujo-final.md` con stack justificado, estructura de carpetas, decisiones de JWT y WebSocket |
| 04 | setup-entorno | Hay que levantar el entorno de desarrollo desde cero | Comandos exactos de instalación, docker-compose, migraciones, seeds y checklist de verificación |
| 05 | desarrollo-modulo | Hay que implementar un módulo, feature o endpoint específico | Código completo del módulo: controller, service, entity/model, validaciones, guard, tests básicos |
| 06 | comunicacion-agente | **Siempre** — toda sesión | Reglas de sesión activas, comandos slash disponibles |
| 07 | debugging | El usuario reporta un error, comportamiento inesperado o el código no funciona como se espera | Diagnóstico de causa raíz + propuesta de fix (sin aplicarlo hasta aprobación) |
| 08 | testing | Hay que escribir tests para código existente, reproducir un bug, o añadir cobertura antes de deploy | Tests unitarios, de integración o e2e para el módulo indicado |
| 09 | code-review | El usuario pide revisar código, antes de un PR, antes de deploy, o cuando hay sospechas de bugs de seguridad | Lista de problemas encontrados (bugs, vulnerabilidades, N+1, race conditions) ordenada por severidad |
| 10 | deploy-entrega | El proyecto o un módulo está listo para ir a producción | Checklist de deploy personalizado + comandos de deploy + validación post-deploy |
| 11 | documentacion | Al terminar una sesión, al entregar un módulo, o cuando los readmes están desactualizados | `readmes/` actualizados, README.md del repo, resumen del sprint |
| 12 | tokens-prompts | La sesión es larga, el contexto está saturado, o el usuario quiere compactar información | Contexto compactado, anti-patrones identificados, plan de sesión eficiente |
| 13 | disenio-ui-ux | Hay que diseñar o implementar interfaces de usuario (componentes, layouts, páginas, formularios) | Design system definido, layouts implementados, componentes de lista y formulario |
| 14 | base-de-datos | Hay que diseñar el schema, crear migraciones, seeders, o definir índices | Schema diseñado, archivos de migración (Prisma o Laravel), seeders, estrategia de índices |
| 15 | seguridad-jwt-permisos | Hay que implementar autenticación, autorización, roles o hardening de seguridad | JWT completo (access + refresh), RBAC con guards/decorators, logs de auditoría, checklist de seguridad |
| 16 | errores-y-logging | Hay que implementar manejo de errores, logging estructurado, Sentry o request IDs | Jerarquía de errores, filtros de excepción globales, configuración de logs por entorno, integración Sentry |
| 17 | variables-y-secrets | Hay que estructurar variables de entorno, documentar `.env.example`, validar secrets al inicio o detectar leaks | `.env` estructurado por categorías, startup validation, procedimiento de rotación de secrets |
| 18 | migraciones-produccion | Hay que ejecutar una migración en producción, hay riesgo de pérdida de datos, o el cambio afecta tablas con muchos registros | Plan de migración con patrón expand-contract, script de backfill en lotes, rollback definido, checklist |
| 19 | cicd | Hay que configurar un pipeline de CI/CD, automatizar tests o deploys, o definir la estrategia de ramas | Archivos de GitHub Actions, configuración de environments, estrategia de ramas documentada |
| 20 | estimacion-presupuesto | El usuario necesita calcular cuánto cobrar, hacer una propuesta a un cliente, o gestionar cambios de alcance | Desglose de horas por módulo, precio calculado con multiplicadores y buffer, propuesta económica en formato Markdown |

---

## Guía de decisión rápida

Cuando el usuario diga o pregunte algo, aplicar el skill correspondiente:

| Si el usuario dice / pregunta... | Skill a aplicar |
|----------------------------------|-----------------|
| "Tengo una idea para una app / quiero hacer un proyecto de..." | 01 |
| "¿Cómo organizamos las tareas? / ¿Por dónde empezamos?" | 02 |
| "¿Qué stack usamos? / ¿Cómo estructuramos el proyecto?" | 03 |
| "Ayúdame a levantar el entorno / cómo instalo el proyecto" | 04 |
| "Implementa el módulo de X / necesito el endpoint Y" | 05 |
| "/fix, /feature, /plan, /commit, /review" | 06 |
| "No funciona / hay un bug / este error sale al..." | 07 |
| "Escribe los tests / agrega cobertura / hay un bug que quiero reproducir" | 08 |
| "Revisa este código / está bien implementado esto?" | 09 |
| "Vamos a hacer deploy / el proyecto está listo" | 10 |
| "Actualiza el README / documenta lo que hicimos" | 11 |
| "El contexto es muy largo / compacta esto" | 12 |
| "Diseña la UI / implementa esta pantalla / crea este componente" | 13 |
| "Diseña la base de datos / crea las migraciones" | 14 |
| "Implementa el login / los roles / los permisos" | 15 |
| "Implementa logging / manejo de errores / Sentry" | 16 |
| "Configura las variables de entorno / gestión de secrets" | 17 |
| "Voy a migrar la BD en producción / cómo hago este cambio sin downtime" | 18 |
| "Configura el CI/CD / automatiza el deploy / GitHub Actions" | 19 |
| "¿Cuánto cobro por esto? / Necesito un presupuesto / el cliente pide precio" | 20 |

---

## Combinaciones de skills para escenarios frecuentes

### Iniciar un proyecto nuevo desde cero
Orden: **01 → 02 → 03 → 14 → 15 → 04 → 17 → 19**
1. Definir dominio y lógica (01).
2. Planificar tareas (02).
3. Decidir arquitectura (03).
4. Diseñar schema de BD (14).
5. Planificar autenticación y permisos (15).
6. Levantar entorno (04).
7. Configurar variables de entorno (17).
8. Configurar CI/CD (19).

### Implementar un nuevo módulo
Orden: **05 → 08 → 09 → 11**
1. Implementar el módulo (05).
2. Escribir tests (08).
3. Code review (09).
4. Documentar (11).

### Preparar un deploy a producción
Orden: **09 → 18 → 10 → 11**
1. Code review de seguridad (09).
2. Plan de migraciones si hay cambios de schema (18).
3. Checklist de deploy (10).
4. Documentar el release (11).

### Resolver un bug en producción
Orden: **07 → 08 → 09 → 10**
1. Diagnosticar y proponer fix (07).
2. Escribir test que reproduzca el bug (08).
3. Revisar el fix antes de deployar (09).
4. Deploy de emergencia (10).

### Cotizar un proyecto a un cliente
Orden: **01 → 20**
1. Formalizar la idea con todas las funcionalidades (01) — este documento es la base de la estimación.
2. Descomponer en horas y calcular precio (20).

### Añadir seguridad y observabilidad a un proyecto existente
Orden: **15 → 16 → 17 → 09**
1. Implementar JWT y RBAC si no existe (15).
2. Añadir logging estructurado y manejo de errores (16).
3. Auditar y estructurar las variables de entorno (17).
4. Code review de seguridad (09).

---

## Skills relacionados entre sí

Cuando apliques uno de estos skills, considera si el relacionado también aplica:

| Skill aplicado | Considerar también |
|---------------|--------------------|
| 14 (base de datos) | 18 (si hay datos en producción) |
| 15 (seguridad) | 09 (code review) + 16 (logging de intentos fallidos) |
| 05 (desarrollo) | 16 (manejo de errores en el módulo) + 17 (si usa secrets nuevos) |
| 10 (deploy) | 18 (migraciones) + 19 (pipeline) |
| 03 (arquitectura) | 14 (schema) + 15 (auth) + 17 (env vars) |
| 04 (setup) | 17 (variables de entorno) + 19 (CI/CD) |

---

## Estructura de archivos de referencia del proyecto

Todos los skills asumen que el proyecto mantiene esta estructura de documentación:

```
readmes/
  logica.md         → generado por skill 01: dominio, entidades, reglas, endpoints
  tareas.md         → generado por skill 02: tareas priorizadas por módulo
  flujo-final.md    → generado por skill 03: stack, estructura, decisiones técnicas
  bd.md             → generado/actualizado por skills 14 y 18: schema, migraciones ejecutadas
  deploy.md         → generado/actualizado por skill 10: historial de deploys, comandos
README.md           → generado/actualizado por skill 11: descripción pública del proyecto
.env.example        → mantenido por skill 17: variables documentadas sin valores reales
```

Si alguno de estos archivos no existe cuando se aplica un skill que lo requiere, generarlo primero antes de continuar con la tarea principal.
