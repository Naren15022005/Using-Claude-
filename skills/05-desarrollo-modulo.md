# Skill 05 — Desarrollo Módulo por Módulo

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
