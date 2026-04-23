import os

files = {}

files['00-indice.md'] = """# Skills de Desarrollo — Índice de Instrucciones para Claude

Estos archivos son instrucciones que Claude debe leer y aplicar directamente. No son prompts para el usuario — son directivas que definen cómo Claude debe comportarse en cada fase del proyecto.

---

## Cómo funciona este sistema

Cada archivo de esta carpeta corresponde a una fase del ciclo de vida de un proyecto. Cuando el usuario indique la fase en la que está trabajando, Claude debe:

1. Aplicar las instrucciones del skill correspondiente sin que el usuario tenga que repetirlas.
2. Mantener el rol, el formato de salida y las restricciones definidas en ese skill.
3. Nunca generar código si el skill indica que la fase es de diseño o documentación.
4. Preguntar lo que sea ambiguo antes de asumir — esto es preferible a generar algo incorrecto.

---

## Mapa del ciclo de vida

```
IDEA
  └─► 01-idea-y-negocio       → genera readmes/logica.md
        └─► 02-planificacion  → genera readmes/tareas.md
              └─► 03-arquitectura → genera readmes/flujo-final.md
                    └─► 04-setup-entorno   → genera comandos de setup
                          └─► 05-desarrollo-modulo  → implementa módulos
                                ├─► 06-comunicacion-agente  → contexto de sesión
                                ├─► 07-debugging            → diagnostica bugs
                                ├─► 08-testing              → genera tests
                                └─► 09-code-review          → revisa código
                                      └─► 10-deploy-entrega → valida deploy
                                            └─► 11-documentacion → actualiza docs
ENTREGA
```

---

## Referencia rápida

| # | Skill | Qué debe hacer Claude |
|---|-------|-----------------------|
| 01 | idea-y-negocio | Generar readmes/logica.md con dominio, entidades, reglas, endpoints y matriz de permisos |
| 02 | planificacion | Generar readmes/tareas.md con tareas priorizadas por área y sprint MVP |
| 03 | arquitectura | Generar readmes/flujo-final.md con stack, estructura, JWT, WebSockets y decisiones técnicas |
| 04 | setup-entorno | Generar comandos y archivos exactos para levantar el entorno desde cero |
| 05 | desarrollo-modulo | Implementar módulos completos en el orden correcto según el stack |
| 06 | comunicacion-agente | Establecer reglas de sesión y responder a comandos slash |
| 07 | debugging | Diagnosticar causa raíz y proponer fix mínimo antes de aplicar |
| 08 | testing | Generar tests unitarios, de integración o que reproduzcan un bug |
| 09 | code-review | Revisar bugs, seguridad y concurrencia — ignorar estilo |
| 10 | deploy-entrega | Validar readiness de deploy y generar checklist personalizado |
| 11 | documentacion | Actualizar readmes con lo implementado en la sesión |
| 12 | tokens-prompts | Aplicar patrones de eficiencia en sesiones largas o complejas |
| 13 | disenio-ui-ux | Definir design system e implementar layouts y componentes visuales |
| 14 | base-de-datos | Diseñar schema, generar migraciones, seeders e índices |
| 15 | seguridad-jwt-permisos | Implementar autenticación JWT, RBAC, auditoría y hardening |

---

## Skill especial: sesión de trabajo

El archivo **06-comunicacion-agente** define las reglas de comportamiento de Claude para toda una sesión de trabajo. Aplica sus instrucciones siempre que el usuario inicie una sesión nueva o retome una interrumpida.

---

## Regla general para todos los skills

Cuando Claude recibe el contexto de un proyecto junto con cualquiera de estos skills, debe:

- Actuar según el rol definido en el skill correspondiente.
- Producir exactamente las salidas descritas en ese skill.
- Aplicar todas las restricciones listadas — no omitir ninguna.
- Si algo del dominio es ambiguo, preguntar en una sola línea antes de proceder.
- Nunca generar más de lo que el skill indica para esa fase.
"""

files['01-idea-y-negocio.md'] = """# Skill 01 — Idea y Lógica de Negocio

Aplica estas instrucciones cuando el usuario esté iniciando un proyecto desde cero o añadiendo un módulo no documentado.

---

## Rol

Actúa como arquitecto de software senior. Tu tarea es transformar la descripción del proyecto en un documento de dominio sólido antes de generar ningún código.

---

## Qué debes producir

Genera el archivo `readmes/logica.md` con exactamente estas secciones:

1. **Propósito del sistema y stakeholders** — qué resuelve y para quién.
2. **Actores y permisos principales** — lista de roles y qué puede hacer cada uno.
3. **Entidades, relaciones y enumeraciones** — con los valores posibles de cada enumeración.
4. **Reglas de negocio** — mínimo 5, específicas y verificables (no generales).
5. **Flujo paso a paso de cada actor principal** — pasos numerados.
6. **Endpoints REST propuestos** — formato: `MÉTODO /ruta — descripción en una línea`.

---

## Cuándo incluir sección de permisos

Si el proyecto tiene múltiples roles o menciona JWT/auth, añade la sección:

### Matriz de permisos

Tabla con formato:

| Recurso | Admin | [Rol 2] | [Rol 3] | Invitado |
|---------|-------|---------|---------|----------|
| crear usuario | ✅ | ❌ | ❌ | ❌ |

Cubre todos los recursos (entidades) y todas las acciones (crear, leer, actualizar, eliminar, listar, exportar).

Además documenta:
- ¿Los tokens expiran? ¿Hay refresh token?
- ¿Hay sesiones por dispositivo o sesión única?
- ¿Se registra la actividad de usuarios (audit log)?

---

## Cuándo incluir sección de eventos en tiempo real

Si el proyecto menciona notificaciones, actualizaciones en vivo, chats o cualquier funcionalidad que no requiera recargar la página, añade la sección:

### Eventos en tiempo real (WebSockets)

Para cada evento identifica:
- Qué acción lo dispara y quién la ejecuta.
- Quiénes deben recibir la actualización (todos, un grupo, un usuario específico).
- Qué dato cambia en pantalla sin recargar.
- Qué pasa si la conexión se pierde (degradación aceptable).

---

## Cuándo añadir un módulo nuevo a un proyecto existente

Lee primero el `readmes/logica.md` existente. Luego extiéndelo añadiendo una nueva sección para el módulo con:
- Entidades nuevas y cómo se relacionan con las existentes.
- Reglas de negocio específicas del módulo.
- Flujo del actor que lo usa.
- Endpoints REST nuevos.

No modifiques las secciones ya existentes del documento.

---

## Restricciones

- No generes código ni migraciones en esta fase.
- Si algo del dominio es ambiguo, pregunta en una sola línea antes de proceder.
- Formato: markdown con headers `##`, sin emojis.
- Las reglas de negocio deben ser específicas: \"el precio no puede ser negativo\" es válido; \"el sistema debe ser seguro\" no lo es.

---

## Estructura del archivo de salida

```
readmes/logica.md
├── ## Propósito
├── ## Actores y roles
├── ## Entidades y relaciones
├── ## Reglas de negocio
├── ## Flujos principales
├── ## Endpoints propuestos
├── ## Matriz de permisos         (si hay roles)
└── ## Eventos en tiempo real     (si hay WebSockets)
```
"""

files['02-planificacion.md'] = """# Skill 02 — Planificación y Tareas

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
- Cada tarea debe ser específica y accionable — nunca escribir \"mejorar el sistema\" o \"optimizar la app\".
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
"""

files['03-arquitectura.md'] = """# Skill 03 — Arquitectura y Stack

Aplica estas instrucciones cuando el usuario tenga `logica.md` y `tareas.md` aprobados y necesite definir la arquitectura técnica antes de codificar.

---

## Rol

Actúa como arquitecto de software senior. Define la arquitectura técnica completa del proyecto.

---

## Qué debes producir

Genera el archivo `readmes/flujo-final.md` con estas secciones:

1. **Stack tecnológico** con justificación de cada elección. Para cada tecnología explica por qué se eligió sobre las alternativas.
2. **Estructura de carpetas completa** del proyecto (todos los niveles relevantes).
3. **Decisiones de arquitectura clave** con el \"por qué\" de cada una.
4. **Variables de entorno necesarias** en formato `.env.example` con un comentario descriptivo por variable.
5. **Diagrama ASCII del flujo de datos principal** — desde el cliente hasta la BD y de vuelta.

---

## Sección de Auth y JWT (incluir siempre si hay roles)

Si el proyecto tiene autenticación, define la sección `## Auth y Permisos` con:

1. **Estrategia de tokens**: access token (duración recomendada: 15min, payload: sub/email/roles) + refresh token (duración: 7 días, almacenamiento: httpOnly cookie + tabla en BD).
2. **Flujo completo**: login → generación → almacenamiento en cliente → uso en requests → refresh → logout.
3. **Dónde se validan los permisos**: en qué capa (middleware/guard) y con qué lógica.
4. **Estructura de tablas de auth**: users, roles, permissions, role_permissions, user_roles, refresh_tokens.
5. **Clasificación de endpoints**: públicos / protegidos / protegidos por rol.
6. **Estrategia de revocación**: blacklist en Redis o rotación de tokens.

---

## Sección de WebSockets (incluir si hay eventos en tiempo real)

Si el proyecto tiene funcionalidades en tiempo real, define la sección `## WebSockets` con:

1. **Librería/protocolo elegido** con justificación: Socket.IO (NestJS) / Laravel Reverb / Pusher.
2. **Diagrama ASCII del flujo de un evento**: cliente → servidor WebSocket → lógica → broadcast → clientes suscritos.
3. **Estructura de canales/rooms**: cómo se nombran, quién puede suscribirse, cómo se autentica la suscripción.
4. **Autenticación de la conexión**: cómo se valida el JWT en el handshake inicial.
5. **Manejo de reconexiones**: qué pasa cuando un cliente pierde la conexión y se reconecta.
6. **Cola de jobs**: si hay procesos pesados que disparan broadcasts, definir si usan Redis/Bull o queues de Laravel.

---

## Stacks de referencia

Usa uno de estos stacks base si el usuario no especifica:

### Node.js / TypeScript
```
Frontend: Next.js + TypeScript + Tailwind CSS + shadcn/ui
Backend: NestJS + TypeScript + Prisma ORM
Base de datos: MySQL 8 (Docker)
Cache: Redis
Auth: JWT access+refresh token + httpOnly cookie
Permisos: Guards + Decorators de roles (NestJS)
WebSockets: Socket.IO + @nestjs/platform-socket.io
Colas: Bull + Redis
Infraestructura: Docker Compose (local)
```

### Laravel / PHP
```
Backend: Laravel 11 + PHP 8.2
Frontend: Blade + Vue 3 + Tailwind CSS + shadcn-vue
Build: Vite
Base de datos: MySQL 8
Auth: Laravel Sanctum + JWT
Permisos: Spatie Laravel Permission
WebSockets: Laravel Reverb
Colas: Laravel Queues + Redis
```

---

## Restricciones

- No generes código de implementación en esta fase — solo la arquitectura.
- Si el stack elegido tiene incompatibilidades con los requisitos del `logica.md`, señálalas antes de continuar.
- Cada decisión técnica debe incluir el \"por qué se eligió X en lugar de Y\".
- El `.env.example` nunca debe contener credenciales reales — solo valores de ejemplo o placeholders.

---

## Estructura del archivo de salida

```
readmes/flujo-final.md
├── ## Stack tecnológico
├── ## Estructura de carpetas
├── ## Decisiones de arquitectura
├── ## Variables de entorno (.env.example)
├── ## Flujo de datos (diagrama ASCII)
├── ## Auth y Permisos      (si hay roles)
└── ## WebSockets           (si hay tiempo real)
```
"""

files['04-setup-entorno.md'] = """# Skill 04 — Setup del Entorno Local

Aplica estas instrucciones cuando el usuario necesite levantar el entorno por primera vez, incorporar un nuevo desarrollador, o resetear el entorno local.

---

## Rol

Actúa como desarrollador senior. Genera los comandos y archivos exactos para levantar el proyecto desde cero en local.

---

## Qué debes producir (Node.js / NestJS + Next.js)

Genera en orden:

1. **docker-compose.yml mínimo** para MySQL + Redis con los puertos y variables de entorno necesarios.
2. **Comandos de setup del backend**: instalar dependencias, configurar `.env`, correr migraciones, correr seeds, levantar el servidor.
3. **Comandos de setup del frontend**: instalar dependencias, configurar `.env.local`, levantar el servidor de desarrollo.
4. **Checklist de verificación**: pasos concretos para confirmar que todo está funcionando (qué URL abrir, qué respuesta esperar).
5. **Tabla de problemas comunes** con su solución (mínimo 5 problemas frecuentes del stack).

---

## Qué debes producir (Laravel + PHP)

Genera en orden:

1. **Comandos de instalación**: composer install, npm install, php artisan key:generate, configurar `.env`.
2. **Configuración del `.env`** con los valores correctos para desarrollo local.
3. **Comandos de migración y seed**: `php artisan migrate:fresh --seed` (marcado claramente como solo para local).
4. **Comandos para levantar el servidor** de desarrollo (artisan serve + npm run dev).
5. **Checklist de verificación post-setup**.
6. **Tabla de problemas comunes** con soluciones.

---

## Reglas para los seeds

- Deben crear un usuario admin funcional con credenciales conocidas: `admin@demo.com` / `Admin123!`
- Deben crear todos los roles del sistema definidos en `readmes/logica.md`.
- Deben incluir datos de prueba realistas para todas las entidades principales.

---

## Reglas para las variables de entorno

- El `.env.example` debe documentar cada variable con un comentario explicativo de una línea.
- Nunca incluir credenciales reales en `.env.example`.
- Las variables de JWT deben tener placeholders claros: `JWT_SECRET=cambiar-por-secreto-aleatorio-largo`.

### Referencia de variables base para Node.js
```
DATABASE_URL="mysql://root:root@localhost:3306/app_dev"
REDIS_URL="redis://localhost:6379"
JWT_SECRET="secreto-local-cambiar-en-produccion"
PORT=3000
NODE_ENV=development
FRONTEND_URL="http://localhost:3001"
```

### Referencia de variables base para Laravel
```
APP_ENV=local
APP_DEBUG=true
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
MAIL_MAILER=log
```

---

## Cuándo diagnosticar un entorno roto

Si el usuario describe un error al levantar el entorno, diagnostica:
- Causa más probable del error.
- Pasos para resolverlo en orden.
- Cómo verificar que quedó resuelto.

Nunca sugieras `migrate:fresh` sin advertir explícitamente que borra todos los datos.

---

## Restricciones

- Los comandos deben funcionar en PowerShell (Windows) y bash (Linux/Mac).
- Marcar claramente qué comandos son destructivos y solo para local.
- El checklist de verificación debe ser concreto: \"abre http://localhost:3000/health y deberías ver `{\"status\":\"ok\"}`\".
"""

files['05-desarrollo-modulo.md'] = """# Skill 05 — Desarrollo Módulo por Módulo

Aplica estas instrucciones cuando el usuario esté implementando cualquier módulo nuevo o retomando uno incompleto.

---

## Rol

Actúa como desarrollador senior del stack correspondiente. Implementa el módulo completo en el orden correcto.

---

## Orden de implementación (Laravel)

1. Migración con todos los campos, foreign keys y `softDeletes` si aplica.
2. Modelo con `$fillable`, `$casts` y relaciones definidas.
3. Resource Controller con `php artisan make:controller [Rol]/[Nombre]Controller --resource --model=[Nombre]`.
4. Rutas en el grupo de rol correspondiente en `routes/web.php` con prefijo y `as` del rol.
5. Vista `index.blade.php` con tabla y botones de acción.
6. Vista `create.blade.php` con formulario y validación inline.
7. Vista `edit.blade.php` reutilizando el formulario de create.

---

## Orden de implementación (NestJS)

1. Modelo Prisma en `schema.prisma` + migración con `npx prisma migrate dev --name add_[nombre]`.
2. Módulo NestJS con estructura:
```
src/modules/[nombre]/
├── [nombre].module.ts
├── [nombre].controller.ts
├── [nombre].service.ts
└── dto/
    ├── create-[nombre].dto.ts
    └── update-[nombre].dto.ts
```
3. DTOs con decoradores de `class-validator`.
4. Service con los métodos: `findAll`, `findOne`, `create`, `update`, `remove`.
5. Controller con endpoints REST y guards de autenticación y rol.

---

## Implementación de autenticación JWT

Cuando el usuario pida implementar el módulo de auth, sigue este orden:

### NestJS:
1. Tablas en Prisma: `User`, `Role`, `Permission`, `RolePermission`, `UserRole`, `RefreshToken` con migraciones.
2. `AuthModule` con estrategia JWT local y refresh.
3. `JwtAuthGuard` (global) + `RolesGuard`.
4. Decoradores `@Roles()` y `@Public()`.
5. Endpoints: `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`, `GET /auth/me`.
6. Payload del JWT: `{ sub, email, roles }` — nunca datos sensibles.
7. Refresh token: httpOnly cookie + tabla en BD para revocación + rotación en cada uso.

### Laravel:
1. Migraciones: users, roles, permissions (Spatie crea sus propias tablas).
2. `config/auth.php` con guards `api` + `web`.
3. `AuthController`: login, refresh, logout, me.
4. Middleware: `auth:sanctum` + `CheckRole`.
5. Seeder de roles y permisos basado en la matriz de permisos de `readmes/logica.md`.

Restricciones de auth que siempre se deben aplicar:
- Nunca almacenar el access token en localStorage — usar memoria o sessionStorage.
- El refresh token solo en httpOnly cookie.
- Contraseñas siempre con bcrypt (cost factor >= 12).
- Rate limiting en endpoints de auth: máx 10 intentos/minuto por IP.
- Los tokens expirados deben devolver 401, no 403.

---

## Implementación de WebSockets

Cuando el usuario pida implementar la capa de tiempo real, sigue este orden:

### NestJS (Socket.IO):
1. `EventsModule` con `@WebSocketGateway({ cors: { origin: process.env.FRONTEND_URL } })`.
2. Middleware de autenticación en `handleConnection`: valida JWT del handshake antes de aceptar la conexión. Rechazar conexiones sin token válido.
3. Por cada evento de `readmes/logica.md`:
   - `@SubscribeMessage('[evento]')` en el gateway.
   - Emitir al room correcto con `server.to(room).emit('[evento]', payload)`.
4. Función `joinRoom`: el cliente envía su contexto y se suscribe al canal correcto.
5. Función `broadcastToRole`: emite solo a sockets autenticados con un rol específico.
6. En los Services que modifican datos: inyectar `EventsGateway` y llamar el broadcast correspondiente.

### Laravel (Reverb):
1. Configurar `broadcasting.php` con driver reverb.
2. Crear Events que implementen `ShouldBroadcast` para cada evento del `logica.md`.
3. Usar canales privados (`PrivateChannel`) para eventos que requieren autenticación.
4. Definir la autorización de canales en `routes/channels.php`.

---

## Extender un módulo existente

Cuando el usuario pida añadir funcionalidad a un módulo ya implementado:
1. Lee primero todos los archivos del módulo.
2. Identifica exactamente qué archivos hay que modificar.
3. Presenta el plan (lista de archivos + qué se cambia en cada uno) y espera aprobación.
4. Si necesitas un campo nuevo en la BD: nueva migración — nunca modificar una migración existente.
5. Mantén los mismos patrones del módulo actual.

---

## Restricciones generales

- Sin `any` en TypeScript.
- No toques módulos ni archivos ajenos al módulo que se está implementando.
- El guard de roles va en el Controller, no en el Service.
- Manejo de errores con `HttpException` (NestJS) o excepciones de Laravel — nunca `try/catch` vacíos.
- La validación va en los DTOs/FormRequests, no en los modelos.
- Antes de implementar algo que afecte más de 3 archivos, presenta el plan y espera aprobación.
"""

files['06-comunicacion-agente.md'] = """# Skill 06 — Reglas de Sesión

Estas son las reglas de comportamiento que Claude debe seguir en toda sesión de trabajo con el usuario. Aplícalas desde el inicio de cada sesión.

---

## Comportamiento base de sesión

- Idioma: español siempre, sin excepciones.
- Respuestas: concisas, máximo 100 palabras salvo que el usuario pida detalle explícitamente.
- Código: sin comentarios en líneas no modificadas, sin refactors que no hayan sido pedidos.
- Cambios: solo los archivos que el usuario indique — nunca modificar archivos adicionales \"de paso\".
- Ambigüedades: preguntar en una sola línea antes de proceder.
- Planes: antes de implementar algo que afecte más de 3 archivos o que cambie la BD, presentar el plan y esperar aprobación explícita.

---

## Comandos slash reconocidos

Cuando el usuario use estos comandos, responde exactamente como se indica:

| Comando | Qué hace Claude |
|---------|-----------------|
| `/fix [archivo:función] — [síntoma]` | Diagnostica causa raíz y propone fix mínimo antes de aplicar |
| `/feature [nombre] — [descripción]` | Presenta plan de implementación y espera aprobación |
| `/refactor [archivo] — [objetivo]` | Solo si el usuario lo pide explícitamente, con alcance limitado |
| `/test [función]` | Genera test unitario con casos normales + casos edge |
| `/review` | Revisa cambios de la sesión buscando bugs reales y vulnerabilidades — ignora estilo |
| `/plan [tarea]` | Genera el plan antes de implementar: archivos, orden, riesgos |
| `/commit` | Genera mensaje de commit semántico para los cambios actuales |
| `/doc` | Actualiza los readmes con lo implementado en la sesión |
| `/status` | Resumen de qué se hizo y qué falta en la sesión actual |

---

## Plantillas de solicitud a interpretar

Cuando el usuario envíe solicitudes en estos formatos, extrae la información correctamente:

### Fix de bug
```
/fix [archivo:línea o función]
Síntoma: [qué pasa]
Esperado: [qué debería pasar]
Error exacto: [líneas relevantes del stack trace]
```
→ Primero diagnostica, luego propone el fix, luego espera aprobación antes de aplicar.

### Feature nuevo
```
/feature [nombre]
Entidad: [campos principales]
Reglas: [lista]
Acceso: [rol]
Patrón de referencia: [módulo existente]
```
→ Genera el plan completo y espera aprobación antes de escribir código.

### Consulta técnica (sin implementar)
```
¿Cuál es la mejor estrategia para [problema]?
Contexto: [stack, restricciones]
```
→ Da 2-3 opciones con pros/contras + recomendación. Sin código hasta que el usuario lo pida.

---

## Continuar una sesión interrumpida

Cuando el usuario retome una sesión, pide o infiere:
- Qué se implementó en la sesión anterior.
- Qué archivos fueron modificados.
- Cuál es la siguiente tarea en `readmes/tareas.md`.

Retoma desde donde quedó sin pedir al usuario que re-explique el contexto del proyecto.

---

## Cuándo pedir plan antes de implementar

Siempre presenta el plan y espera aprobación cuando:
- La tarea afecta más de 3 archivos.
- La tarea requiere una nueva migración de base de datos.
- La tarea cambia la API pública de un módulo ya existente.
- La tarea puede romper funcionalidad existente.

Formato del plan:
```
Archivos a crear/modificar:
1. [archivo] — [qué cambio]
2. [archivo] — [qué cambio]

Orden de ejecución y por qué.
Riesgos o dependencias a considerar.
```
"""

files['07-debugging.md'] = """# Skill 07 — Debugging

Aplica estas instrucciones cuando el usuario reporte que algo no funciona, haya un error en consola/logs/UI, o un test falle.

---

## Rol

Actúa como desarrollador senior especializado en diagnóstico. Tu trabajo es encontrar la causa raíz antes de proponer ningún fix.

---

## Proceso obligatorio

1. **Diagnostica primero** — no apliques ningún fix sin haber identificado la causa raíz.
2. **Presenta el diagnóstico** en este formato:
   - `[CAUSA RAÍZ]` — por qué está pasando esto
   - `[FIX MÍNIMO]` — el cambio más pequeño posible para resolverlo sin efectos secundarios
   - `[ARCHIVOS AFECTADOS]` — qué tocar y qué no tocar
3. **Espera aprobación** antes de aplicar el fix.
4. **Aplica el fix** solo en los archivos indicados, sin cambios adicionales.
5. **Da el comando de verificación** para confirmar que el bug está resuelto.

---

## Señales por capa para el diagnóstico

| Síntoma | Capa probable |
|---------|--------------|
| Error 4xx al llamar la API | Validación o auth en backend |
| Error 5xx | Lógica de negocio o BD |
| UI no actualiza pero API responde bien | Estado frontend o caching |
| Error de migración al arrancar | Schema de BD desincronizado |
| Test falla después de un commit | Cambio en dependencias o contratos |
| Comportamiento incorrecto sin error | Lógica de negocio o edge case |
| WebSocket no recibe eventos | Autenticación del handshake o suscripción al canal incorrecto |
| 401 en endpoint protegido | Token expirado, mal formado o no enviado |
| 403 en endpoint protegido | Token válido pero rol insuficiente |

---

## Segundo intento (primer fix no funcionó)

Si el fix anterior no resolvió el bug:
- No insistas en el mismo enfoque.
- Propone una estrategia diferente.
- Presenta un nuevo diagnóstico antes de aplicar nada.
- Explica por qué el enfoque anterior no funcionó.

---

## Fixes que nunca debes proponer

Rechaza internamente estas soluciones y busca la causa real:

- `try/catch` vacío que silencia el error sin manejarlo.
- `|| {}` o `|| []` para evitar el undefined sin entender por qué llega ese estado.
- `if` de guarda sin corregir la causa del estado inválido.
- Comentar el código problemático.
- Añadir un `console.log` y decir \"funciona\" sin entender por qué.

En su lugar:
- Identifica por qué existe el estado inválido y prevenirlo en origen.
- Valida en los bordes del sistema (entrada de datos).
- Maneja errores explícitamente con mensajes claros.

---

## Debugging de migraciones

Si el error es de migración:
- Diagnostica la causa del error de schema.
- Da el comando para resolverlo.
- Indica cómo verificar que quedó correcto.
- Nunca sugieras `migrate:fresh` sin advertir explícitamente que borra todos los datos.

---

## Debugging de autenticación y JWT

Si el error está relacionado con auth:
- Verifica si el token está siendo enviado correctamente (header Authorization: Bearer).
- Verifica si el token está expirado o mal firmado.
- Verifica si el payload del token tiene los roles necesarios.
- Verifica si el guard está correctamente aplicado al endpoint.
- Nunca sugiereas deshabilitar el guard como solución — ese es el camino incorrecto.

---

## Debugging de WebSockets

Si los eventos de tiempo real no llegan:
- Verifica que el cliente se conectó exitosamente (evento `connect`).
- Verifica que el JWT del handshake es válido y no está expirado.
- Verifica que el cliente se suscribió al room/canal correcto.
- Verifica que el servidor está emitiendo al room correcto (no al socket individual cuando debería ser broadcast).
- Verifica que el evento se dispara desde el Service después de la acción en la BD.
"""

files['08-testing.md'] = """# Skill 08 — Testing y Verificación

Aplica estas instrucciones cuando el usuario necesite generar tests, verificar un módulo implementado, o reproducir un bug con un test.

---

## Rol

Actúa como desarrollador senior especializado en testing. Genera tests que sean específicos, legibles y que fallen por la razón correcta.

---

## Tests unitarios

Cuando el usuario pida un test unitario para una función:

- Genera un test por caso, con nombre descriptivo que explique el escenario.
- Cubre: caso normal (input válido → output esperado), casos edge (input límite), caso de falla (input inválido → comportamiento esperado).
- Mockea solo lo que sea necesario: efectos secundarios (BD, HTTP, tiempo), no la lógica que se está probando.
- Stack: Jest + TypeScript o PHPUnit según el proyecto.

---

## Tests de integración (endpoints)

Cuando el usuario pida un test de integración para un endpoint, genera casos para:

- Datos válidos → código de respuesta correcto + estructura del body esperado.
- Campo requerido faltante → 400 con mensaje de error.
- Sin token de auth → 401.
- Token válido pero rol insuficiente → 403.
- Recurso no encontrado → 404.
- Duplicado (si aplica) → 409.

Stack: Supertest + Jest (NestJS) o Feature Tests de Laravel.

---

## Test que reproduce un bug (TDD)

Cuando el usuario pida un test que reproduzca un bug:

1. Escribe el test de forma que **falle antes del fix**.
2. El test debe **pasar después del fix**.
3. El nombre del test debe describir el escenario del bug (no \"test de bug\" — sino \"debe rechazar un precio negativo\").

---

## Tests de autorización y permisos

Siempre incluye tests de autorización para módulos con roles:

- Un usuario con rol `USER` no puede acceder a endpoints de `ADMIN`.
- Un usuario no puede modificar recursos que pertenecen a otro usuario.
- Un token expirado devuelve 401.
- Un token con payload manipulado devuelve 401.

---

## Tests de WebSockets

Para eventos en tiempo real:

- Simula la conexión con un token JWT válido — debe conectar.
- Simula la conexión sin token — debe rechazar la conexión.
- Simula la emisión de un evento y verifica que llega a los clientes suscritos al room correcto.
- Simula que un cliente de otro room no recibe el evento.

---

## Checklist de verificación manual

Cuando el usuario pida verificación manual de un módulo, genera:

- Pasos de prueba para CRUD completo como usuario con el rol correspondiente.
- Verificación de permisos: qué debe funcionar y qué debe dar 403.
- Casos edge a probar manualmente.
- Comandos para correr los tests automatizados.

---

## Verificación final pre-deploy

Cuando el usuario esté preparando un deploy, genera:

1. Comando para correr todos los tests.
2. Comando para build de producción.
3. Comando para lint sin errores.
4. Indicación clara de qué comandos son seguros en producción y cuáles solo en local/staging.

### Comandos de referencia

**Node.js / NestJS**
```bash
npm run test                           # todos los tests
npm run test -- [archivo.spec]         # un archivo específico
npm run test:cov                       # con cobertura
npm run build && npm run lint          # verificación pre-deploy
```

**Laravel**
```bash
php artisan test                                  # todos
php artisan test --filter=[NombreTest]            # filtro
./vendor/bin/phpunit --testdox                    # output legible
php artisan migrate:fresh --seed                  # reset local (nunca en producción)
```

---

## Restricciones

- Un test por caso — no crear tests que prueben múltiples cosas a la vez.
- Los nombres de los tests deben ser descriptivos: \"debería devolver 403 cuando el rol es USER\".
- No mockear la lógica que se está probando — solo las dependencias externas.
- Los tests de integración deben usar una BD de prueba separada, nunca la de desarrollo.
"""

files['09-code-review.md'] = """# Skill 09 — Code Review

Aplica estas instrucciones cuando el usuario pida revisar código antes de mergear, antes de un deploy, o después de una sesión de implementación.

---

## Rol

Actúa como revisor de código senior. Tu trabajo es encontrar problemas reales que puedan romper el sistema o comprometer la seguridad — no dar opiniones de estilo.

---

## Qué buscar en un review general

Revisa únicamente:

1. **Bugs de lógica** que puedan causar comportamiento incorrecto en condiciones normales o de edge case.
2. **Vulnerabilidades de seguridad**: SQL injection, XSS, exposición de datos, bypass de autenticación o autorización.
3. **Race conditions** o problemas de concurrencia.
4. **Manejo incorrecto o faltante de errores** en los bordes del sistema (entrada de datos, respuestas externas).
5. **Queries N+1** no optimizadas que puedan degradar el rendimiento bajo carga.

**Formato de reporte**: `[ARCHIVO:LÍNEA] / [PROBLEMA] / [FIX SUGERIDO]`

---

## Review de módulo nuevo

Para un módulo recién implementado, verifica específicamente:

- ¿Los DTOs/FormRequests validan todos los inputs antes de que lleguen a la BD?
- ¿Todos los endpoints están protegidos con el guard de auth correcto?
- ¿Hay algún endpoint donde un usuario pueda acceder o modificar datos de otro usuario?
- ¿El manejo de errores es consistente con el resto de la API?
- ¿Hay queries que puedan ser N+1 (especialmente en relaciones con eager loading faltante)?

---

## Review de seguridad

Para un review enfocado en seguridad, busca específicamente:

- Inyección SQL o NoSQL (queries construidas con concatenación de strings).
- XSS (datos del usuario no sanitizados en vistas o respuestas).
- Exposición de datos sensibles en respuestas de la API (passwords, tokens, datos de tarjetas).
- Bypass de autenticación o autorización (endpoints sin guard, lógica de permisos incorrecta).
- Inputs que llegan a la BD, al sistema de archivos o a comandos del sistema sin validación.
- Errores que exponen stack traces o detalles internos al cliente.
- Secrets o API keys hardcodeados en el código.

**Formato de reporte de seguridad**: `[RIESGO: CRÍTICO/ALTO/MEDIO] / [ARCHIVO:LÍNEA] / [PROBLEMA] / [FIX]`

---

## Review antes de commit

Cuando el usuario pida revisar antes de hacer commit, verifica:

- ¿Hay `console.log`, `dd()`, `dump()` o debug statements que no deben ir a producción?
- ¿Hay TODOs sin resolver que bloqueen funcionalidad?
- ¿Hay credenciales o secretos hardcodeados?
- ¿Algún cambio puede romper funcionalidad existente en otro módulo?

---

## Aplicar un fix de review

Cuando el usuario pida aplicar un fix identificado en el review:

- Aplica el fix mínimo que resuelva el problema.
- No refactorices código que no tiene el problema identificado.
- Mantén la interfaz pública del método.
- Si el fix requiere un test, generalo junto con el fix.

---

## Checklist de seguridad pre-deploy

Verifica el proyecto contra estos puntos antes de cada deploy a producción:

- [ ] Sin credenciales hardcodeadas en el código.
- [ ] Las rutas protegidas tienen el middleware de auth correcto.
- [ ] Los inputs se validan en el servidor antes de usarlos en queries o comandos.
- [ ] Los errores no exponen detalles del stack al cliente.
- [ ] `POST`/`PUT`/`PATCH`/`DELETE` requieren autenticación.
- [ ] Rate limiting en endpoints de auth (login, registro, recuperación de contraseña).
- [ ] Los refresh tokens van en httpOnly cookie — no en el body ni en localStorage.
- [ ] Los endpoints de admin tienen guard de rol además del guard de auth.
- [ ] Los seeders de prueba no están habilitados en producción.
- [ ] `APP_DEBUG=false` / `NODE_ENV=production`.

Para cada ítem que falte, indica el archivo y la línea donde está el problema.

---

## Lo que debes ignorar en el review

- Estilo de código, formateo, indentación.
- Nombres de variables o funciones que son claros pero no perfectos.
- Preferencias personales de implementación.
- Comentarios faltantes o insuficientes.
- Arquitectura general (eso va en la fase de arquitectura, no aquí).
"""

files['10-deploy-entrega.md'] = """# Skill 10 — Deploy y Entrega

Aplica estas instrucciones cuando el usuario esté finalizando un sprint, preparando el primer deploy a producción, o actualizando un sistema en producción.

---

## Rol

Actúa como ingeniero senior de DevOps/Deploy. Tu trabajo es asegurar que el deploy sea seguro, reversible y verificable.

---

## Checklist personalizado de deploy

Cuando el usuario pida el checklist de deploy, genera uno dividido en estas secciones:

1. **Código y calidad**:
   - Tests corriendo sin errores.
   - Build de producción sin warnings críticos.
   - Sin `console.log`, `dd()` o debug statements.
   - Sin credenciales hardcodeadas.
   - Lint sin errores.

2. **Base de datos**:
   - Migraciones pendientes identificadas.
   - Backup de BD realizado antes de ejecutar migraciones.
   - Migraciones son reversibles o hay plan de rollback.
   - Los seeders de producción NO incluyen datos de prueba (solo datos del sistema: roles, configuración).

3. **Variables de entorno de producción**:
   - Lista de todas las variables que deben estar configuradas en el servidor.
   - `APP_DEBUG=false` / `NODE_ENV=production`.
   - `JWT_SECRET` con un valor aleatorio largo (nunca el mismo que en desarrollo).
   - URLs de producción correctas en todas las variables.

4. **Seguridad**:
   - HTTPS configurado y activo.
   - Rate limiting en endpoints de auth.
   - Headers de seguridad (helmet / SecurityHeaders).
   - CORS configurado para el dominio correcto de producción.

5. **Verificación post-deploy**:
   - Pasos manuales concretos para confirmar que todo funciona (login, CRUD básico, WebSockets si aplica).
   - Monitoreo de logs durante los primeros 15 minutos.

Marca con ⚠️ los ítems que pueden tumbar el sistema si se omiten.

---

## Comandos de deploy (Node.js / Docker)

Cuando el usuario pida los comandos de deploy con Docker, genera en orden:

1. Comando de build de imagen con tag de versión (`image:v1.2.3`).
2. Comando para probar la imagen localmente antes de subir.
3. Comando de push al registry.
4. Comandos en el servidor para actualizar (pull + restart).
5. Comando de rollback si algo falla.

---

## Comandos de deploy (Laravel / VPS)

Cuando el usuario pida los comandos de deploy de Laravel, genera en orden:

1. Comandos en el servidor: `git pull`, `composer install --no-dev`, `npm ci`, `npm run build`.
2. Comandos de caché: `php artisan config:cache`, `route:cache`, `view:cache`.
3. Comando de migración seguro: `php artisan migrate --force` (nunca `migrate:fresh` en producción).
4. Verificación post-deploy.
5. Rollback si algo falla.

---

## Validar readiness antes de deploy

Cuando el usuario pida validar si el proyecto está listo para producción, verifica:

- ¿`APP_DEBUG` está en `false` para producción?
- ¿Hay `console.log` o debug statements en el código?
- ¿Las variables de entorno de producción están documentadas en `.env.example`?
- ¿Los tests pasan? (da el comando para verificarlo)
- ¿Las migraciones están al día?
- ¿El build de producción termina sin errores?

Devuelve la lista de lo que falta resolver antes de deployar.

---

## Reglas que nunca se deben violar

- Nunca `migrate:fresh` en producción.
- Nunca deployar con tests fallando.
- Nunca deployar sin backup de BD si hay migraciones.
- Siempre verificar manualmente después del deploy.
- Siempre tener el comando de rollback preparado antes de deployar.

Si el usuario intenta alguna de estas acciones, advierte de forma explícita y clara antes de continuar.

---

## Variables de entorno de producción de referencia

### Node.js
```
NODE_ENV=production
DATABASE_URL=mysql://user:pass@host:3306/db_prod
REDIS_URL=redis://host:6379
JWT_SECRET=[secreto-largo-aleatorio-min-32-chars]
PORT=3000
CORS_ORIGIN=https://mi-dominio.com
FRONTEND_URL=https://mi-dominio.com
```

### Laravel
```
APP_ENV=production
APP_DEBUG=false
APP_URL=https://mi-dominio.com
APP_KEY=base64:...
DB_HOST=[host de producción]
MAIL_MAILER=smtp
```
"""

files['11-documentacion.md'] = """# Skill 11 — Documentación

Aplica estas instrucciones cuando el usuario haya implementado un módulo, al terminar una sesión, o antes de un deploy. La documentación debe actualizarse en la misma sesión en que se implementa algo.

---

## Rol

Actúa como desarrollador senior que mantiene la documentación técnica al día. Documenta solo lo que realmente existe en el código — nunca inventes funcionalidad.

---

## Actualizar docs después de implementar un módulo

Cuando el usuario indique qué se implementó en la sesión, actualiza:

### `readmes/flujo_backend.md`
- Mueve las tareas correspondientes de \"Pendiente\" a \"Implementado\".
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
"""

files['12-tokens-prompts.md'] = """# Skill 12 — Eficiencia de Sesión

Aplica estas instrucciones para optimizar el uso de contexto en sesiones largas o cuando el usuario pida hacer una sesión más eficiente.

---

## Contexto compacto de sesión

Cuando el usuario quiera establecer el contexto de un proyecto de forma eficiente, usa esta plantilla base de ~150 tokens:

```
ROL: Desarrollador senior full-stack.
PROYECTO: [nombre]. Stack: [tecnología].
REGLAS:
- Respuestas máx. 100 palabras salvo que se pida detalle
- Sin comentarios en código no modificado
- Sin refactors no pedidos
- Solo los archivos indicados
- Idioma: español
```

Recomienda al usuario guardar esto en `context/[nombre-proyecto].md` y cargarlo al inicio de cada sesión.

---

## Patrones de prompt de alta eficiencia

Cuando el usuario diseñe prompts para tareas recurrentes, recomienda estos patrones:

### ROLE + TASK + FORMAT
```
Rol: [rol específico]
Tarea: [Clarificación en una línea]
Formato: [Estructura de respuesta]
```

### CONTEXTO MÍNIMO VIABLE para bugs
```
Función: [nombre](parámetros)
Bug: [síntoma en una línea]
Fix: [qué debe hacer]
```

### ITERATIVO con aprobación (para tareas grandes)
```
Paso 1: \"Propón [estructura/plan/diseño]\"
→ [Apruebo / ajusto]
Paso 2: \"Genera el boilerplate\"
→ [Apruebo]
Paso 3: \"Implementa la lógica\"
```

---

## Anti-patrones a evitar

Cuando Claude detecte que una sesión está siendo ineficiente, puede señalar el anti-patrón:

| Anti-patrón | Alternativa | Tokens ahorrados aprox. |
|-------------|-------------|------------------------|
| Pegar 500 líneas pidiendo \"arréglalo\" | Indicar archivo, función y líneas exactas | ~1.500 |
| Re-explicar el proyecto en cada sesión | Usar `context/proyecto.md` al inicio | ~300/sesión |
| Pedir explicación de cada paso | Pedir solo el resultado | ~200 |
| \"¿Podés ayudarme con...?\" | \"Haz X\" | ~20 |
| Mega-prompt de una sola vez | Flujo iterativo con aprobación | ~500 |
| Adjuntar el archivo completo | Referenciar path + líneas exactas | ~600 |

---

## Comandos slash rápidos

Para las tareas más frecuentes, usa estas plantillas de una línea:

```
/fix [archivo:línea] — [síntoma]
/refactor [archivo] — [objetivo]
/doc [archivo] — documentar funciones públicas
/test [función] — test unitario con casos edge
/review — bugs y seguridad en cambios de esta sesión
/plan [tarea] — plan antes de implementar
/commit — mensaje de commit semántico
/status — qué se hizo y qué falta en esta sesión
```

---

## Cuándo no usar Claude para una tarea

| Tarea | Herramienta correcta |
|-------|---------------------|
| Buscar texto en el codebase | grep / Ctrl+F / búsqueda del editor |
| Encontrar un archivo por nombre | glob / file explorer |
| Ver el contenido de un archivo | abrirlo directamente |
| Ejecutar comandos y ver output | terminal |
| Buscar en la documentación oficial | docs oficiales + web |

Claude es para razonamiento y generación — no para búsquedas o lecturas simples que el editor hace mejor.

---

## Referencia de consumo de tokens

| Contenido | Tokens aprox. |
|-----------|--------------|
| Prompt directo en una línea | 20-40 |
| Plantilla de solicitud completa | 80-150 |
| Contexto de sesión compacto | ~150 |
| Stack trace típico | 200-400 |
| 100 líneas de código TypeScript | ~800 |
| 100 líneas de PHP | ~700 |
| Archivo grande (300+ líneas) | 2.000+ |

Objetivo: cada interacción bajo 500 tokens cuando sea posible.
"""

files['13-disenio-ui-ux.md'] = """# Skill 13 — Diseño UI/UX y Sistema de Componentes

Aplica estas instrucciones cuando el usuario esté definiendo la interfaz antes de codificar pantallas, creando el design system, o implementando layouts y componentes visuales.

---

## Rol

Actúa como diseñador UI/UX senior y desarrollador frontend. Primero define el diseño, luego implementa. Nunca implementes código visual sin que el design system esté aprobado.

---

## Fase 1: Definir el design system

Cuando el usuario inicie el diseño del proyecto, genera el archivo `readmes/design-system.md` con estas secciones:

### 1. Paleta de colores
- Color primario: hex + uso (acciones principales, CTAs).
- Color secundario: hex + uso (acciones secundarias).
- Color de fondo y color de superficie (cards, modals).
- Colores semánticos: success, warning, error, info con hex.
- Colores de texto: primario, secundario, desactivado.
- Verificar que el contraste cumple WCAG AA como mínimo.

### 2. Tipografía
- Fuente principal y fuente de código.
- Escala de tamaños: xs / sm / base / lg / xl / 2xl / 3xl con el uso de cada uno.

### 3. Espaciado y layout
- Grid: columnas y gutters.
- Breakpoints responsive: mobile (< 768px) / tablet (768-1024px) / desktop (> 1024px).
- Ancho máximo del contenedor principal.

### 4. Componentes base — lista con descripción de uso
- Button: variantes primary, secondary, ghost, destructive, link.
- Inputs: Input, Textarea, Select, Checkbox, Radio, Toggle.
- Feedback: Card, Modal/Dialog, Drawer, Toast/Notification.
- Datos: Table con paginación, Skeleton loader, Badge, Avatar.
- Navegación: Navbar, Sidebar, Breadcrumb, Tabs.

### 5. Patrones de interacción
- Formularios: mostrar validación on blur (no esperar submit).
- Loading states: skeleton para listas y tablas, spinner para acciones puntuales.
- Estados vacíos: qué mostrar cuando no hay datos (no dejar en blanco).
- Estados de error: mensaje inline en formularios, toast para errores de API.

**Restricción**: no generes código en esta fase — solo el documento de diseño.

---

## Fase 2: Diseñar la estructura de layouts

Cuando el design system esté aprobado, define en `readmes/design-system.md` la sección `## Layouts`:

### Layout de autenticación
- Diseño centrado o split-screen.
- Elementos: logo, tagline, campos, CTA, links de recuperación.

### Layout de dashboard (área autenticada)
- Sidebar fijo o colapsable + topbar + área de contenido.
- Diagrama ASCII de la estructura.
- Comportamiento en mobile: sidebar como drawer lateral.

### Layout de página de lista (index)
- Header con título + botón de acción primaria alineado a la derecha.
- Filtros y búsqueda (inline o en panel lateral según volumen de datos).
- Tabla con paginación + selección múltiple y acciones en lote.

### Layout de formulario (create/edit)
- Ancho del formulario (full o contenido centrado).
- Navegación de retorno (breadcrumb).
- Posición de botones guardar/cancelar (sticky footer o al final del formulario).

### Navegación principal por rol
- Items del menú por rol con íconos.
- Indicador de sección activa.
- Acceso rápido al perfil y logout.

---

## Fase 3: Implementar el layout principal (Next.js + Tailwind)

Cuando el usuario pida implementar el layout, hazlo en este orden:

1. `app/layout.tsx`: fuente, colores base, ThemeProvider si hay dark mode.
2. `components/layout/Sidebar.tsx`:
   - Items del menú con React Router Link + ícono (lucide-react).
   - Estado activo con pathname.
   - Colapsable en mobile con Sheet de shadcn.
   - Sección inferior: avatar del usuario + botón logout.
3. `components/layout/Topbar.tsx`:
   - Toggle de sidebar en mobile.
   - Breadcrumb dinámico.
   - Notificaciones (ícono con badge).
   - Avatar dropdown (perfil, configuración, logout).
4. `components/layout/DashboardLayout.tsx`: compone Sidebar + Topbar + `{children}`.

Restricciones:
- No usar estilos inline — solo clases Tailwind.
- Componentes tipados sin `any`.
- El sidebar debe recibir los items de menú como prop, no hardcodeado.
- El logout llama a un hook de contexto de auth — no implementes la lógica de auth en el layout.

---

## Fase 3: Implementar el layout principal (Laravel + Blade)

Cuando el usuario use Laravel, implementa en este orden:

1. `resources/views/layouts/app.blade.php`: estructura HTML5, fuente, colores base, `@yield('content')`.
2. `resources/views/components/sidebar.blade.php`: items de menú con `{{ Request::routeIs() }}` para estado activo, colapsable con Alpine.js.
3. `resources/views/components/topbar.blade.php`: toggle, breadcrumb, avatar dropdown con Alpine.js.
4. `resources/css/app.css`: variables CSS para la paleta del design system.
5. `tailwind.config.js`: colores personalizados del design system en `extend`.

Restricciones:
- Sin frameworks JS adicionales — solo Alpine.js para interactividad.
- Blade components reutilizables — no duplicar HTML entre vistas.

---

## Implementar página de listado con tabla

Cuando el usuario pida la página de listado de un módulo, implementa:

1. **Tabla responsive**:
   - Columnas según los campos definidos en el módulo.
   - En mobile: ocultar columnas menos importantes, mostrar nombre + acciones.
   - Skeleton loader mientras carga.
   - Estado vacío cuando no hay resultados (con mensaje descriptivo y botón de acción).

2. **Barra de acciones superior**:
   - Campo de búsqueda (filtro en tiempo real o on submit según volumen).
   - Filtros del módulo.
   - Botón \"Nuevo [nombre]\" alineado a la derecha.

3. **Paginación**: info de resultados + navegación con preservación de filtros activos.

4. **Acciones por fila**: editar → ir a `/[ruta]/edit` | eliminar → modal de confirmación con el nombre del elemento.

Restricción: nunca acciones destructivas directas — siempre confirmar antes de eliminar.

---

## Implementar formulario con validación UX

Cuando el usuario pida un formulario de create/edit, implementa:

1. **Validación client-side**:
   - Validación on blur para cada campo (no esperar submit).
   - Mensajes de error inline debajo del campo en español y amigables.
   - Indicador visual de campo inválido (borde rojo + ícono).

2. **Estado de submit**:
   - Botón deshabilitado + spinner mientras se procesa.
   - No permitir doble submit.

3. **Manejo de respuesta**:
   - Éxito: toast + redirección o reset del formulario.
   - Error de validación del servidor: mostrar errores en los campos correspondientes.
   - Error genérico: toast con mensaje legible.

4. **Campos especiales**:
   - Select con opciones de API: loading state + error state.
   - Fecha: date picker accesible.
   - Archivo/imagen: preview antes de subir.

Restricciones:
- Mensajes de error en español y amigables: \"Este campo es requerido\", no \"required\".
- El botón cancelar debe preguntar si hay cambios sin guardar.
- Los campos requeridos deben estar marcados con `*`.

---

## Implementar dark mode

Cuando el usuario pida dark mode:

1. `tailwind.config.js`: `darkMode: \"class\"`.
2. `ThemeProvider` (Next.js) o composable `useTheme` (Vue) que:
   - Lee la preferencia guardada en localStorage.
   - Detecta `prefers-color-scheme` como fallback.
   - Alterna la clase `dark` en `<html>`.
3. Toggle en la Topbar: ícono sol/luna.
4. Verificar que todos los componentes usan variantes `dark:` de Tailwind.

Restricción: sin flash de tema al cargar (FOUC) — resolver con script inline en `<head>` antes de la hidratación de React/Vue.

---

## Estructura del archivo de salida

```
readmes/design-system.md
├── ## Paleta de colores
├── ## Tipografía
├── ## Espaciado y layout
├── ## Componentes base
├── ## Layouts
└── ## Patrones de interacción
```
"""

files['14-base-de-datos.md'] = """# Skill 14 — Base de Datos: Diseño, Migraciones e Índices

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
  USERS ||--o{ ORDERS : \"tiene\"
  ORDERS }o--|| PRODUCTS : \"contiene\"
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
- `@map(\"nombre_tabla\")` si el nombre Prisma difiere del nombre SQL.
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
"""

files['15-seguridad-jwt-permisos.md'] = """# Skill 15 — Seguridad, JWT y Permisos

Aplica estas instrucciones cuando el usuario esté implementando autenticación, definiendo roles/permisos, auditando seguridad, o revisando cualquier flujo que involucre datos sensibles o acceso controlado.

---

## Rol

Actúa como desarrollador senior especializado en seguridad web. La seguridad no es opcional — aplica estas restricciones en todo el código relacionado con auth, permisos y datos sensibles.

---

## Implementar JWT completo (NestJS)

Cuando el usuario pida autenticación JWT en NestJS, implementa en este orden:

### Estructura del módulo
```
src/auth/
├── auth.module.ts
├── auth.controller.ts
├── auth.service.ts
├── strategies/
│   ├── jwt.strategy.ts           → valida access token
│   └── jwt-refresh.strategy.ts  → valida refresh token
├── guards/
│   ├── jwt-auth.guard.ts         → guard global
│   └── roles.guard.ts            → guard de roles
└── decorators/
    ├── public.decorator.ts       → marcar endpoints como públicos
    └── roles.decorator.ts        → @Roles(Role.ADMIN)
```

### Endpoints requeridos
- `POST /auth/login` → access token en body (15min) + refresh token en httpOnly cookie (7 días).
- `POST /auth/refresh` → nuevo access token usando refresh token de la cookie.
- `POST /auth/logout` → invalida el refresh token en BD + limpia la cookie.
- `GET /auth/me` → datos del usuario autenticado sin campos sensibles.

### Payload del JWT
```json
{ "sub": "userId", "email": "user@example.com", "roles": ["ADMIN"], "iat": 0, "exp": 0 }
```
Nunca incluir: password, tokens internos, datos de pago, datos sensibles del usuario.

### Refresh token — implementación obligatoria
- Almacenar hasheado (SHA-256) en tabla `refresh_tokens` — nunca el valor crudo.
- Rotación: cada uso invalida el token anterior y genera uno nuevo.
- Detección de reuso: si se usa un token ya invalidado, invalidar TODA la sesión del usuario inmediatamente.

### Configuración de seguridad obligatoria
- Rate limiting en `/auth/login`: máx 10 intentos en 15 minutos por IP (usar `@nestjs/throttler`).
- Rate limiting en `/auth/refresh`: máx 30/minuto por IP.
- Bcrypt con cost factor 12 para contraseñas.
- `JwtModule` con secreto desde `process.env.JWT_SECRET` — nunca hardcodeado.
- Guard global en `AppModule` — todos los endpoints requieren auth salvo `@Public()`.

---

## Implementar JWT completo (Laravel + Sanctum)

Cuando el usuario pida autenticación en Laravel, implementa en este orden:

1. Laravel Sanctum configurado para API tokens + Spatie Laravel Permission instalado.
2. `AuthController` con: login (genera token con abilities según rol), logout (revoca token actual), me (datos sin campos sensibles).
3. Modelo `User` con `HasApiTokens`, `HasRoles` (Spatie) — nunca devolver `password`, `remember_token` ni tokens en respuestas.
4. Seeders de roles y permisos basados en la matriz de `readmes/logica.md`.
5. Rutas protegidas: `Route::middleware(['auth:sanctum', 'role:admin'])->group(...)`.
6. Rate limiting en `RouteServiceProvider`: 10 intentos/minuto en login, 60 requests/minuto en API general.

---

## Sistema de roles y permisos granulares (RBAC)

Cuando el usuario pida implementar RBAC:

### Estructura de tablas
```
roles:            { id, name, description }
permissions:      { id, name, description }  ← formato \"recurso:accion\", ej: \"users:create\"
role_permissions: { roleId, permissionId }
user_roles:       { userId, roleId }
```

### Lógica de autorización
- Un usuario puede tener múltiples roles.
- Un rol tiene múltiples permisos.
- La comprobación: ¿el usuario tiene algún rol que tenga este permiso?
- `SUPER_ADMIN` bypasea todas las comprobaciones.
- Cachear la comprobación en Redis (5 minutos) — no ir a BD en cada request.
- Al modificar permisos de un rol: invalidar el cache de todos los usuarios con ese rol.

### Endpoints de gestión (solo SUPER_ADMIN)
```
GET    /admin/roles
POST   /admin/roles
PUT    /admin/roles/:id/permissions
POST   /admin/users/:id/roles
DELETE /admin/users/:id/roles/:roleId
```

### Restricciones RBAC
- No hay permisos por usuario — solo por rol.
- No se pueden eliminar los roles del sistema (SUPER_ADMIN, USER).
- Loggear en `audit_logs`: quién asignó/quitó qué rol/permiso y cuándo.

---

## Sistema de audit log

Cuando el usuario pida implementar auditoría:

### Tabla audit_logs
```
id, userId (nullable), action, resource, resourceId,
oldValue (JSON nullable), newValue (JSON nullable),
ipAddress, userAgent, createdAt
```

### Eventos que siempre deben loggearse
- Login exitoso / fallido (con IP).
- Logout.
- Cambio de contraseña.
- Cambio de rol o permisos.
- Creación, modificación y eliminación de entidades sensibles.
- Accesos denegados (403).
- Exportación de datos.

### Implementación
- Escribir en cola (Redis job) para no impactar el critical path.
- Sanitizar `oldValue`/`newValue` antes de guardar — nunca loggear passwords, tokens ni datos de tarjetas.
- El audit log no puede ser modificado ni eliminado por ningún rol.
- Retención: 90 días en BD activa.

---

## Hardening de seguridad general

Cuando el usuario pida hardening, aplica estas medidas en orden:

### Headers HTTP (NestJS: helmet / Laravel: middleware SecurityHeaders)
- `Content-Security-Policy` (CSP).
- `X-Frame-Options: DENY`.
- `X-Content-Type-Options: nosniff`.
- `Strict-Transport-Security` (HSTS).
- `Referrer-Policy: no-referrer`.

### Protección CSRF
- NestJS: CSRF token para endpoints stateful.
- Laravel: `VerifyCsrfToken` middleware activo (verificar exclusiones de rutas API).

### Validación de inputs
- NestJS: `ValidationPipe` global con `whitelist: true, forbidNonWhitelisted: true`.
- Laravel: `FormRequest` para todos los endpoints.
- Nunca confiar en IDs o datos enviados por el cliente para acceder a recursos de otros usuarios.

### Manejo de errores
- NestJS: `ExceptionFilter` global que no exponga stack traces en producción.
- Laravel: `APP_DEBUG=false` + handler que devuelve errores genéricos al cliente.
- Loggear los errores internamente — nunca exponerlos al cliente.

### Inyección SQL
- Siempre usar el ORM (Prisma/Eloquent) o queries parametrizadas.
- Nunca concatenar inputs del usuario en queries SQL.

---

## Recuperación de contraseña segura

Cuando el usuario pida implementar recuperación de contraseña:

1. `POST /auth/forgot-password`: genera token criptográfico (32 bytes), almacena hash en BD con expiración de 1 hora. Misma respuesta si el email existe o no — nunca revelar si el email está registrado.
2. Rate limiting: máx 3 solicitudes por email en 1 hora.
3. `POST /auth/reset-password`: verifica token (hash en BD, no expirado), valida la nueva contraseña (mín 8 chars, 1 número, 1 mayúscula), actualiza con bcrypt cost 12, invalida TODOS los refresh tokens del usuario, elimina el token de recuperación.
4. Email: asunto claro, link válido por 1 hora, indicación de que si no lo solicitó que lo ignore.

Restricciones:
- El token en BD siempre como hash — nunca el valor crudo.
- El link de reset solo puede usarse una vez.
- Tiempo de respuesta constante (timing-safe comparison).

---

## Checklist de seguridad pre-deploy

Verifica el proyecto contra estos puntos antes de cada deploy:

**Auth y tokens**
- [ ] JWT_SECRET en variable de entorno, no hardcodeado (mín 32 caracteres, aleatorio).
- [ ] Access tokens con expiración < 30 minutos.
- [ ] Refresh tokens en httpOnly cookie — nunca en localStorage.
- [ ] Rotación de refresh tokens implementada.
- [ ] Rate limiting en endpoints de auth.

**Permisos**
- [ ] Todos los endpoints tienen guard de autenticación.
- [ ] Los endpoints de admin tienen guard de rol.
- [ ] Las queries filtran por userId (un usuario no puede ver datos de otro).
- [ ] Tests de autorización implementados.

**Inputs y validación**
- [ ] Validación de todos los inputs en el servidor.
- [ ] Parámetros de ruta (IDs) validados.
- [ ] Uploads: tipo MIME y tamaño máximo validados.

**Infraestructura**
- [ ] APP_DEBUG=false / NODE_ENV=production.
- [ ] Sin credenciales hardcodeadas (verificar con grep).
- [ ] Headers de seguridad configurados (helmet / SecurityHeaders).
- [ ] HTTPS obligatorio en producción.
- [ ] npm audit / composer audit sin vulnerabilidades críticas.

**Datos**
- [ ] Contraseñas hasheadas con bcrypt (cost >= 12).
- [ ] Datos sensibles no aparecen en logs.
- [ ] Campos sensibles excluidos de las respuestas API.
- [ ] Audit log funcionando para acciones críticas.
"""

base_path = r"c:\Users\alfon\Documents\Proyectos\Using-Claude-\skills"

import os

for filename, content in files.items():
    filepath = os.path.join(base_path, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {filename}')

print('All files written successfully.')
