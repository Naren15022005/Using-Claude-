# 🚀 Skill 10 — Deploy y Entrega

> **Fase:** Cierre de proyecto o sprint  
> **Objetivo:** Asegurar que el sistema está listo para producción y entregar sin errores.

---

## Cuándo usar este skill

- Al finalizar un proyecto o sprint.
- Al preparar el primer deploy a producción.
- Al hacer un deploy de actualización a un sistema existente.

---

## Checklist de cierre (antes de deploy)

### Código y calidad

- [ ] Todos los tests pasan (`npm run test` / `php artisan test`)
- [ ] Build de producción sin errores (`npm run build`)
- [ ] Sin errores de lint (`npm run lint`)
- [ ] No hay `console.log`, `dd()`, `dump()` ni debug statements
- [ ] No hay credenciales hardcodeadas en el código
- [ ] No hay TODOs críticos sin resolver

### Base de datos

- [ ] Todas las migraciones aplicadas y schema actualizado
- [ ] Seeders de producción preparados (solo roles y datos esenciales, sin datos de prueba)
- [ ] Backup de la BD de producción tomado antes del deploy
- [ ] Migraciones probadas en entorno de staging

### Configuración de producción

- [ ] Variables de entorno de producción configuradas en el servidor/proveedor
- [ ] `APP_ENV=production` / `NODE_ENV=production`
- [ ] `APP_DEBUG=false` (nunca exponer stack traces en producción)
- [ ] `APP_KEY` generado correctamente (Laravel)
- [ ] Credenciales de BD de producción configuradas
- [ ] Configuración de mail de producción
- [ ] Secrets rotados (no usar los mismos de desarrollo)

### Seguridad

- [ ] Secrets y API keys almacenados en variables de entorno, no en código
- [ ] HTTPS configurado
- [ ] Rate limiting en endpoints sensibles
- [ ] Logs de errores configurados (sin exponer datos sensibles)

### Documentación

- [ ] README principal actualizado con instrucciones de arranque
- [ ] Documentos de flujo actualizados al 100%
- [ ] Changelog actualizado con los cambios del sprint/release
- [ ] `.env.example` actualizado con todas las variables nuevas

---

## Variables de entorno por stack

### Node.js / NestJS

```env
# Producción
NODE_ENV=production
DATABASE_URL=mysql://user:pass@host:3306/db_prod
REDIS_URL=redis://host:6379
JWT_SECRET=secreto-largo-y-aleatorio-produccion
PORT=3000
CORS_ORIGIN=https://mi-dominio.com
```

### Laravel

```env
APP_ENV=production
APP_DEBUG=false
APP_KEY=base64:...
APP_URL=https://mi-dominio.com

DB_CONNECTION=mysql
DB_HOST=db-servidor-produccion
DB_PORT=3306
DB_DATABASE=db_produccion
DB_USERNAME=db_user
DB_PASSWORD=db_pass_seguro

MAIL_MAILER=smtp
MAIL_HOST=smtp.proveedor.com
MAIL_PORT=587
MAIL_USERNAME=no-reply@mi-dominio.com
MAIL_PASSWORD=pass_mail
```

---

## Proceso de deploy

### Node.js (Docker)

```bash
# 1. Build de la imagen
docker build -t mi-app:v1.0.0 .

# 2. Probar la imagen localmente
docker run --env-file .env.production -p 3000:3000 mi-app:v1.0.0

# 3. Push al registry
docker push registry/mi-app:v1.0.0

# 4. Deploy en el servidor (o usar CI/CD)
docker pull registry/mi-app:v1.0.0
docker-compose -f docker-compose.prod.yml up -d
```

### Laravel (VPS/Servidor)

```bash
# Desde el servidor, sobre rama limpia sin commits pendientes
git pull origin main
composer install --no-dev --optimize-autoloader
npm run build
php artisan migrate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan queue:restart
```

---

## Prueba de partida limpia (staging)

Antes del deploy de producción, hacer en staging:

```powershell
# Laravel
php artisan migrate:fresh --seed --env=staging
php artisan test

# Node.js
npx prisma migrate deploy    # sin fresh en producción
npm run test
```

---

## Verificación post-deploy

```
1. Acceder a la URL de producción
2. Hacer login con usuario real
3. Probar los flujos críticos del sistema:
   - Login / logout de cada rol
   - El módulo principal (crear, listar)
   - El flujo de mayor valor (checkout, reserva, etc.)
4. Revisar logs en tiempo real por 5 minutos
5. Verificar que no hay errores 5xx en los logs
```

---

## Rollback si algo falla

```bash
# Docker — volver a la versión anterior
docker pull registry/mi-app:v0.9.0
docker-compose up -d

# Laravel — revertir última migración
php artisan migrate:rollback
git revert HEAD
git push origin main
```

---

## Checklist de cierre post-deploy

- [ ] Sistema accesible en producción
- [ ] Login funciona con credenciales reales
- [ ] Flujos críticos verificados manualmente
- [ ] Sin errores 5xx en logs
- [ ] Monitoreo activo (si existe: Datadog, Sentry, etc.)
- [ ] Equipo notificado del deploy exitoso
- [ ] Documentación de la versión actualizada

---

## Prompt para generar checklist personalizado

```
Genera el checklist de deploy para este proyecto.
Stack: [tecnología]
Módulos implementados: [lista]
Servicios externos: [pagos, email, webhooks, etc.]
Incluye los pasos específicos para nuestro stack y los riesgos particulares de este release.
```

---

## Reglas al usar este skill

- ✅ El deploy siempre parte de una rama limpia (sin commits pendientes).
- ✅ Backup de BD antes de cualquier deploy con migraciones.
- ✅ Verificar manualmente después de cada deploy.
- ❌ Nunca `migrate:fresh` en producción.
- ❌ No deployar sin pasar el checklist de cierre.
- ❌ No deployar si hay tests fallando.

---

## Siguiente paso

→ [`11-documentacion.md`](11-documentacion.md) — Mantener la documentación actualizada.
