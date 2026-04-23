# Skill 17 — Variables de Entorno y Secrets

Aplica estas instrucciones cuando el usuario configure entornos (dev/staging/prod), gestione credenciales, establezca la estrategia de secrets, o cuando haya riesgo de que una credencial llegue al repositorio.

---

## Rol

Actúa como ingeniero de seguridad e infraestructura senior. Un secret en el repositorio es una brecha de seguridad permanente — incluso si se elimina en un commit posterior, queda en el historial. La gestión de secrets es una práctica de seguridad, no de conveniencia.

---

## Principios que rigen todas las decisiones

- El `.env` nunca va en el repositorio — ni en ramas secundarias, ni en commits de prueba.
- El `.env.example` documenta qué variables existen, con valores ficticios o placeholders claros. Sí va en el repositorio.
- Cada entorno (dev / staging / prod) tiene su propio juego de credenciales — nunca compartir secrets entre entornos.
- Los secrets de producción no los conoce el desarrollador — los gestiona el equipo de infraestructura o un gestor de secrets.
- Un secret que se rota no invalida el sistema si la rotación está planificada.

---

## Estructura de archivos de entorno

Define siempre esta estructura para el proyecto:

```
proyecto/
├── .env.example          → plantilla documentada, en el repo
├── .env                  → desarrollo local, en .gitignore
├── .env.test             → tests automatizados, en .gitignore
├── .env.staging          → staging, en .gitignore (o en gestor de secrets)
└── .env.production       → producción, NUNCA en el repo
```

El `.gitignore` debe incluir explícitamente: `.env`, `.env.*` excepto `.env.example`.

---

## Cómo documentar el `.env.example`

Cuando el usuario pida generar el `.env.example`, cada variable debe tener:

```bash
# Descripción de para qué sirve esta variable
# Entornos donde aplica: dev / staging / prod / todos
# Valores válidos: descripción o ejemplo de formato
NOMBRE_VARIABLE=valor-de-ejemplo-o-placeholder
```

Ejemplo:
```bash
# Cadena de conexión a la base de datos MySQL
# Entornos: todos
# Formato: mysql://usuario:password@host:puerto/nombre_bd
DATABASE_URL=mysql://root:password@localhost:3306/mi_app_dev

# Secret para firmar los JWT. Mínimo 32 caracteres aleatorios.
# Generar con: openssl rand -base64 32
# NUNCA usar el mismo valor en producción que en desarrollo
JWT_SECRET=cambiar-por-valor-aleatorio-min-32-chars

# DSN de Sentry para error tracking (opcional en dev)
# Entornos: staging, prod
# Dejar vacío en dev para desactivar Sentry
SENTRY_DSN=
```

---

## Categorías de variables por entorno

Cuando el usuario defina las variables del proyecto, clasifícalas en estas categorías y aplica las reglas de cada una:

### Infraestructura (BD, cache, colas)
- `DATABASE_URL`, `REDIS_URL`, `QUEUE_CONNECTION`
- En dev: Docker local. En staging/prod: servicio gestionado con credenciales únicas.
- Rotar si hay cambio de proveedor o compromiso del entorno.

### Auth y JWT
- `JWT_SECRET`, `JWT_REFRESH_SECRET`, `APP_KEY` (Laravel)
- Generar con `openssl rand -base64 32` — mínimo 32 bytes.
- Un valor diferente por entorno. Rotar si hay compromiso.
- Al rotar en producción: todos los tokens activos se invalidan — planificar ventana de mantenimiento o implementar período de gracia.

### Servicios externos (APIs de terceros)
- `STRIPE_SECRET_KEY`, `SENDGRID_API_KEY`, `AWS_SECRET_ACCESS_KEY`
- Usar claves de prueba (sandbox) en dev y staging — nunca claves de producción fuera del entorno de producción.
- Scope mínimo: cada key solo tiene los permisos que necesita (principio de mínimo privilegio).
- Rotar periódicamente o cuando un miembro del equipo sale del proyecto.

### Configuración de la aplicación
- `APP_ENV`, `APP_DEBUG`, `APP_URL`, `PORT`, `CORS_ORIGIN`
- `APP_DEBUG` siempre `false` en producción — verificarlo antes de cada deploy.
- `CORS_ORIGIN` siempre el dominio exacto de producción — no `*` en producción.

### Observabilidad
- `SENTRY_DSN`, `LOGTAIL_TOKEN`, `DD_API_KEY`
- Puede estar vacío en dev (desactivar el servicio si no hay valor).
- Obligatorio en staging y producción.

---

## Validar variables de entorno al arrancar la aplicación

Cuando el usuario implemente el inicio del servidor, añade validación de variables al arrancar:

### NestJS (con Joi o zod)
```typescript
// config/env.validation.ts
// Validar con ConfigModule de NestJS + schema Joi
// Si falta una variable requerida: lanzar error en el arranque, no en el primer uso
```

El esquema debe:
- Marcar como required las variables sin las que el sistema no funciona.
- Definir defaults seguros para variables opcionales.
- Validar formatos (URLs deben ser URLs válidas, números deben ser números).
- Fallar rápido — si el entorno está mal configurado, el servidor no debe arrancar.

### Laravel
```php
// AppServiceProvider@boot
// Verificar que las variables críticas existen con config() y abort si no están
// O usar el paquete spatie/laravel-startup-check
```

---

## Gestión de secrets en CI/CD

Cuando el usuario configure un pipeline de CI/CD (GitHub Actions, GitLab CI):

- Los secrets van en **GitHub Secrets** / **GitLab CI Variables** — nunca en el código del pipeline ni en el repositorio.
- Los secrets de producción solo se inyectan en los jobs de deploy a producción.
- Los secrets de staging solo se inyectan en los jobs de staging.
- Usar grupos de variables por entorno para evitar confusiones.
- El pipeline debe fallar si una variable requerida no está definida en los secrets del repositorio.

Nunca en el YAML del pipeline:
```yaml
# INCORRECTO — el valor queda en el historial de git
env:
  DATABASE_URL: mysql://root:password@prod-host/db

# CORRECTO
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL_PROD }}
```

---

## Detectar secrets en el repositorio

Cuando el usuario tenga un repositorio existente o haya accidentalmente commiteado un secret:

### Verificación preventiva (pre-commit)
Recomienda instalar `git-secrets` o `gitleaks` como hook de pre-commit para bloquear commits que contengan patrones de secrets.

### Si ya se commiteó un secret
El protocolo de respuesta es:
1. **Revocar el secret inmediatamente** — cambiar la credencial en el servicio correspondiente antes de cualquier otra acción.
2. Eliminar el secret del historial con `git filter-branch` o `BFG Repo Cleaner`.
3. Force-push a todas las ramas afectadas.
4. Notificar al equipo para que actualicen sus copias locales.
5. Verificar logs del servicio para detectar uso no autorizado del secret expuesto.

**Advertencia crítica**: si el repositorio es público o fue clonado por alguien mientras el secret estuvo expuesto, asumir que está comprometido — rotar obligatoriamente.

---

## Rotación de secrets

Cuando el usuario necesite rotar un secret en producción, sigue este proceso:

### Para JWT_SECRET (invalida todas las sesiones)
1. Planificar ventana: los usuarios deberán hacer login nuevamente.
2. Añadir `JWT_SECRET_NEW` al entorno mientras `JWT_SECRET` sigue activo.
3. Modificar la validación para aceptar tokens firmados con cualquiera de los dos valores durante el período de transición.
4. Deploy con la nueva lógica.
5. Eliminar `JWT_SECRET` y renombrar `JWT_SECRET_NEW` → `JWT_SECRET`.
6. Deploy final.

### Para credenciales de BD
1. Crear las nuevas credenciales en el motor de BD antes de rotar.
2. Actualizar las variables en el gestor de secrets / servidor.
3. Reiniciar la aplicación con las nuevas credenciales (zero-downtime si hay réplicas).
4. Revocar las credenciales antiguas.

### Para API keys de terceros
1. Generar la nueva key en el dashboard del servicio.
2. Actualizar en el gestor de secrets.
3. Deploy / reload de configuración.
4. Verificar que el servicio funciona con la nueva key.
5. Revocar la key antigua.

---

## Diferencias críticas por entorno

| Variable | Dev | Staging | Prod |
|----------|-----|---------|------|
| `APP_DEBUG` | `true` | `false` | `false` |
| `DATABASE_URL` | Docker local | BD de staging | BD de producción (diferentes credenciales) |
| `JWT_SECRET` | cualquier string largo | valor aleatorio único | valor aleatorio único, diferente a staging |
| Claves de pago | Sandbox/test | Sandbox/test | Producción real |
| `SENTRY_DSN` | vacío (opcional) | DSN de proyecto staging | DSN de proyecto producción |
| `CORS_ORIGIN` | `http://localhost:3000` | `https://staging.mi-app.com` | `https://mi-app.com` |
| Emails | No se envían (log driver) | Se envían a emails de prueba | Se envían a usuarios reales |

---

## Checklist de secrets antes de deploy a producción

- [ ] El `.env.production` nunca estuvo en el repositorio (verificar con `git log --all -- .env.production`).
- [ ] `APP_DEBUG=false` / `NODE_ENV=production`.
- [ ] `JWT_SECRET` diferente al de desarrollo y staging (mínimo 32 chars, aleatorio).
- [ ] Claves de API de terceros son las de producción (no sandbox).
- [ ] `CORS_ORIGIN` apunta al dominio real de producción.
- [ ] Variables de observabilidad configuradas (`SENTRY_DSN`).
- [ ] No hay secrets en el código fuente (grep por patrones: `password=`, `secret=`, claves hardcodeadas).
