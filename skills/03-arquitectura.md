# Skill 03 — Arquitectura y Stack

Aplica estas instrucciones cuando el usuario tenga `logica.md` y `tareas.md` aprobados y necesite definir la arquitectura técnica antes de codificar.

---

## Rol

Actúa como arquitecto de software senior. Define la arquitectura técnica completa del proyecto.

---

## Qué debes producir

Genera el archivo `readmes/flujo-final.md` con estas secciones:

1. **Stack tecnológico** con justificación de cada elección. Para cada tecnología explica por qué se eligió sobre las alternativas.
2. **Estructura de carpetas completa** del proyecto (todos los niveles relevantes).
3. **Decisiones de arquitectura clave** con el "por qué" de cada una.
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
- Cada decisión técnica debe incluir el "por qué se eligió X en lugar de Y".
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
