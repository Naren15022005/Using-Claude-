# Skill 16 — Gestión de Errores y Logging

Aplica estas instrucciones cuando el usuario implemente manejo de errores, configure logging, integre herramientas de observabilidad, o cuando el sistema llegue a producción sin visibilidad sobre lo que falla.

---

## Rol

Actúa como ingeniero de confiabilidad (SRE) senior. Un sistema sin logging estructurado y sin manejo de errores explícito es un sistema que no se puede operar en producción. Ningún error debe silenciarse — debe manejarse, loggearse o propagarse hacia arriba con contexto suficiente para diagnosticarlo.

---

## Principios que rigen todas las decisiones

- Los errores se manejan en el borde del sistema (entrada de requests, respuestas externas, jobs). En el interior, se propagan hacia arriba con contexto añadido.
- Los logs son para máquinas primero, para humanos segundo. Deben ser estructurados (JSON) en producción.
- Nunca loggear datos sensibles: passwords, tokens, números de tarjeta, datos personales completos.
- El cliente nunca ve detalles internos de un error — ve un mensaje genérico + un `errorId` para rastrear en los logs.
- Los errores operacionales (validación, not found, auth) se devuelven con códigos HTTP correctos. Los errores de programación (excepciones inesperadas) se loggean como `error` y devuelven 500.

---

## Jerarquía de errores

Define siempre esta jerarquía antes de implementar el manejo de errores:

| Tipo | Código HTTP | Log level | Ejemplo |
|------|-------------|-----------|---------|
| Validación de input | 400 | `warn` | Campo requerido faltante |
| No autenticado | 401 | `warn` | Token expirado |
| Sin permisos | 403 | `warn` | Rol insuficiente |
| Recurso no encontrado | 404 | `info` | ID inexistente |
| Conflicto de datos | 409 | `warn` | Email duplicado |
| Error interno | 500 | `error` | Excepción no manejada |
| Servicio externo caído | 503 | `error` | API de pagos no responde |

---

## Implementar manejo de errores global (NestJS)

Cuando el usuario pida manejo de errores en NestJS, implementa en este orden:

### 1. Clase base de errores de dominio
```
src/common/exceptions/
├── app.exception.ts          → clase base con errorId + contexto
├── not-found.exception.ts    → extends AppException, HTTP 404
├── forbidden.exception.ts    → extends AppException, HTTP 403
└── conflict.exception.ts     → extends AppException, HTTP 409
```

La clase base debe incluir:
- `errorId`: UUID generado en el constructor — permite correlacionar el error en logs con la respuesta al cliente.
- `context`: objeto con datos relevantes para el diagnóstico (nunca datos sensibles).
- `message`: mensaje técnico para logs.
- `userMessage`: mensaje amigable para el cliente (en español).

### 2. ExceptionFilter global
- Captura todas las excepciones no manejadas.
- Loggea con `logger.error()` incluyendo: `errorId`, `stack`, `context`, `path`, `method`, `userId` (si está autenticado).
- Devuelve al cliente: `{ error: true, errorId, message: userMessage, statusCode }`.
- En producción (`NODE_ENV=production`): nunca incluir `stack` en la respuesta.
- En desarrollo: incluir `stack` en la respuesta para facilitar el debugging.

### 3. Registro en AppModule
```typescript
APP_FILTER con AllExceptionsFilter como global
APP_INTERCEPTOR con LoggingInterceptor para loggear request/response time
```

---

## Implementar manejo de errores global (Laravel)

Cuando el usuario pida manejo de errores en Laravel, configura en este orden:

### 1. `app/Exceptions/Handler.php`
- `register()`: define handlers para cada tipo de excepción del dominio.
- Para `ModelNotFoundException`: devuelve 404 con mensaje genérico.
- Para `AuthenticationException`: devuelve 401.
- Para `AuthorizationException`: devuelve 403.
- Para excepciones de dominio propias: usar su código y mensaje definido.
- Para cualquier otra excepción: loggear con contexto + devolver 500 con `errorId`.

### 2. Excepciones de dominio propias
```
app/Exceptions/
├── DomainException.php       → clase base con errorId
├── NotFoundException.php
├── ConflictException.php
└── BusinessRuleException.php
```

### 3. Formato de respuesta de error consistente
```json
{
  "error": true,
  "errorId": "uuid-para-rastrear",
  "message": "Mensaje legible para el usuario",
  "statusCode": 404
}
```
En producción: nunca incluir `trace` ni detalles del framework en la respuesta.

---

## Configurar logging estructurado (NestJS / Winston o Pino)

Cuando el usuario pida configurar logging en Node.js:

### Configuración base
- Usar **Pino** (preferido por performance) o **Winston**.
- Formato JSON en producción, formato legible (pretty) en desarrollo.
- Incluir en cada log: `timestamp`, `level`, `service` (nombre del servicio), `requestId` (UUID por request), `userId` (si está disponible).

### Niveles y cuándo usarlos
- `error`: excepciones inesperadas, errores de servicios externos, fallos críticos.
- `warn`: errores operacionales recurrentes (auth fallida, validación), comportamiento degradado.
- `info`: eventos importantes del negocio (usuario creado, pedido completado, job procesado).
- `debug`: flujo de ejecución detallado — solo activo en desarrollo, nunca en producción.

### Request ID propagation
- Generar un UUID al inicio de cada request.
- Propagar ese ID en todos los logs de ese request usando `AsyncLocalStorage` o un interceptor.
- Incluir el mismo ID en la respuesta como header `X-Request-Id`.

---

## Configurar logging (Laravel / Monolog)

Cuando el usuario pida configurar logging en Laravel:

### `config/logging.php`
- Channel `stack` por defecto: combina `daily` (archivo) + canal externo (Sentry, Logtail).
- Formato JSON en producción: usar `JsonFormatter` de Monolog.
- Retención local: 14 días máximo.

### Contexto compartido por request
- En un `ServiceProvider`, bindear el `RequestId` (UUID) en el contexto de Monolog con `Log::withContext(['requestId' => $id])`.
- Incluir `userId` y `userRole` en el contexto cuando el usuario esté autenticado.

---

## Integrar Sentry (error tracking)

Cuando el usuario pida integrar tracking de errores en producción:

### NestJS
1. Instalar `@sentry/node` + `@sentry/tracing`.
2. Inicializar antes de que arranque la app con `dsn`, `environment`, `tracesSampleRate` (0.1 en producción para no saturar la cuota).
3. En el `AllExceptionsFilter`: capturar excepciones 5xx con `Sentry.captureException(error)` + incluir el `Sentry.lastEventId()` como `errorId` en la respuesta.
4. No capturar errores operacionales esperados (4xx) — solo los inesperados (5xx).

### Laravel
1. Instalar `sentry/sentry-laravel`.
2. Configurar en `config/sentry.php` con `dsn` desde variable de entorno `SENTRY_DSN`.
3. En `Handler.php`: reportar solo excepciones que no sean instancias de las excepciones operacionales propias.

---

## Logs que nunca deben existir

Rechaza o elimina cualquier log que contenga:

- Passwords, hashes de passwords.
- Tokens JWT, access tokens, refresh tokens, API keys.
- Números de tarjeta o datos de pago.
- Datos personales completos (DNI, número de teléfono completo, dirección completa).
- Stack traces completos en respuestas al cliente.
- Consultas SQL con datos de usuario interpolados.

Si un log necesita identificar a un usuario, usar solo el `userId` (ID numérico o UUID) — nunca el email ni el nombre.

---

## Alertas y umbrales

Cuando el usuario configure alertas en producción, define estas reglas base:

| Métrica | Umbral de alerta | Severidad |
|---------|-----------------|-----------|
| Tasa de errores 5xx | > 1% de requests en 5 min | Crítica |
| Tiempo de respuesta p95 | > 2 segundos | Alta |
| Jobs fallidos en cola | > 5 jobs fallidos | Alta |
| Intentos de login fallidos | > 50/minuto | Media |
| Espacio en disco | < 20% libre | Media |

---

## Estructura de archivos de salida

```
src/common/exceptions/         (NestJS)
├── app.exception.ts
├── not-found.exception.ts
├── forbidden.exception.ts
└── conflict.exception.ts

src/common/filters/
└── all-exceptions.filter.ts

src/common/interceptors/
└── logging.interceptor.ts

app/Exceptions/                (Laravel)
├── Handler.php
├── DomainException.php
└── [otras excepciones de dominio]

config/logging.php             (Laravel)
```
