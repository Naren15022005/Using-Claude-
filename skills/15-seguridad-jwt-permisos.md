# Skill 15 — Seguridad, JWT y Permisos

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
permissions:      { id, name, description }  ← formato "recurso:accion", ej: "users:create"
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
