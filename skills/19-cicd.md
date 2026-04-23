# Skill 19 — CI/CD: Integración y Entrega Continua

Aplica estas instrucciones cuando el usuario necesite configurar un pipeline de CI/CD, automatizar tests y deploys, definir la estrategia de ramas, o eliminar el proceso de deploy manual.

---

## Rol

Actúa como ingeniero DevOps senior. El objetivo de CI/CD es hacer que cada commit sea potencialmente deployable a producción de forma automatizada, segura y reproducible. Un deploy manual que depende del conocimiento de una sola persona es un riesgo operacional.

---

## Principios que rigen todas las decisiones

- El pipeline falla rápido: los pasos más baratos (lint, tipos) van primero; los más lentos (tests de integración, builds) van después.
- Nunca deployar a producción sin que los tests hayan pasado.
- Los secrets del pipeline viven en las variables del repositorio (GitHub Secrets / GitLab Variables) — nunca en el código del pipeline.
- Cada entorno tiene su propio pipeline o stage: no hay un botón que deploy a producción y staging al mismo tiempo con la misma acción.
- El deploy debe ser reversible: siempre debe existir una forma de volver a la versión anterior en menos de 5 minutos.

---

## Estrategia de ramas recomendada

Cuando el usuario defina la estrategia de ramas, recomienda este modelo según el tamaño del equipo:

### Equipo pequeño (1-3 personas)
```
main         → producción (protegida, solo merge con PR)
develop      → integración continua, staging
feature/*    → features individuales
hotfix/*     → fixes urgentes en producción
```

### Equipo mediano (4+ personas)
```
main         → producción (protegida, requiere review + CI verde)
staging      → staging (protegida)
develop      → integración
feature/*    → features (se mergean a develop)
release/*    → preparación de release (merge a main + develop)
hotfix/*     → fixes urgentes (merge a main + develop)
```

Reglas de protección para la rama `main`:
- Requiere PR aprobado por al menos 1 reviewer.
- El CI/CD debe estar verde antes de permitir merge.
- No permitir force-push.
- No permitir eliminación.

---

## Pipeline base con GitHub Actions (Node.js / NestJS + Next.js)

Cuando el usuario pida configurar CI/CD con GitHub Actions, genera estos archivos:

### `.github/workflows/ci.yml` — se ejecuta en cada PR y push a develop
```yaml
name: CI

on:
  push:
    branches: [develop]
  pull_request:
    branches: [develop, main]

jobs:
  ci:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: app_test
        ports: ['3306:3306']
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
      redis:
        image: redis:7
        ports: ['6379:6379']

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # Backend
      - name: Install backend dependencies
        run: npm ci
        working-directory: ./backend

      - name: Lint
        run: npm run lint
        working-directory: ./backend

      - name: Type check
        run: npm run build --noEmit
        working-directory: ./backend

      - name: Run migrations
        run: npx prisma migrate deploy
        working-directory: ./backend
        env:
          DATABASE_URL: mysql://root:root@localhost:3306/app_test

      - name: Run tests
        run: npm run test:cov
        working-directory: ./backend
        env:
          DATABASE_URL: mysql://root:root@localhost:3306/app_test
          JWT_SECRET: test-secret-for-ci-only
          NODE_ENV: test

      # Frontend
      - name: Install frontend dependencies
        run: npm ci
        working-directory: ./frontend

      - name: Lint frontend
        run: npm run lint
        working-directory: ./frontend

      - name: Build frontend
        run: npm run build
        working-directory: ./frontend
```

### `.github/workflows/deploy-staging.yml` — se ejecuta al hacer merge a develop
```yaml
name: Deploy Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        # Aquí va el comando de deploy según la infraestructura
        # Docker: build + push + SSH al servidor
        # Railway/Render: trigger via webhook
        # VPS: SSH + git pull + restart
        env:
          DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
```

### `.github/workflows/deploy-production.yml` — se ejecuta al hacer merge a main
```yaml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production   # Requiere aprobación manual en GitHub

    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.PROD_DEPLOY_KEY }}
```

---

## Pipeline base con GitHub Actions (Laravel)

Cuando el usuario use Laravel, genera:

### `.github/workflows/ci.yml`
```yaml
name: CI Laravel

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: app_test
        ports: ['3306:3306']
        options: --health-cmd="mysqladmin ping" --health-interval=10s

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          extensions: mbstring, pdo, pdo_mysql, redis
          coverage: xdebug

      - name: Install dependencies
        run: composer install --no-interaction --prefer-dist

      - name: Copy .env
        run: cp .env.example .env.testing

      - name: Generate key
        run: php artisan key:generate --env=testing

      - name: Run migrations
        run: php artisan migrate --env=testing
        env:
          DB_DATABASE: app_test
          DB_USERNAME: root
          DB_PASSWORD: root

      - name: Run tests
        run: php artisan test --coverage
        env:
          DB_DATABASE: app_test
          DB_USERNAME: root
          DB_PASSWORD: root
```

---

## Variables de entorno en el pipeline

Cuando el usuario configure los secrets del pipeline, establece estas reglas:

- En **GitHub**: Settings → Secrets and variables → Actions → separar en `secrets` (sensibles) y `variables` (no sensibles).
- Usar **environments** de GitHub Actions para separar staging de producción — los secrets de producción solo se inyectan en el environment `production`.
- Si el pipeline necesita conectarse a la BD en producción (para migraciones): usar un secret separado de solo escritura en migraciones, no la URL completa de la aplicación.

Secrets mínimos que debe tener el pipeline:

| Secret | Entorno | Para qué |
|--------|---------|---------|
| `DATABASE_URL_TEST` | CI | Tests automatizados |
| `STAGING_DEPLOY_KEY` | Staging | SSH o token de deploy |
| `PROD_DEPLOY_KEY` | Production | SSH o token de deploy |
| `PROD_DATABASE_URL` | Production | Solo para correr migraciones |

---

## Notificaciones de fallos

Cuando el pipeline falle, el equipo debe ser notificado:

### Slack / Discord (webhook)
```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "❌ Pipeline falló en ${{ github.repository }} rama ${{ github.ref_name }}",
        "attachments": [{"text": "Ver: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"}]
      }
```

---

## Estrategia de rollback en CI/CD

Cuando el usuario pregunte cómo revertir un deploy fallido, define la estrategia según la infraestructura:

### Docker (imagen versionada)
```bash
# Volver a la imagen anterior
docker pull registry/app:v1.2.2   # versión anterior
docker stop app-container
docker run -d --name app-container registry/app:v1.2.2
```

### VPS con git
```bash
git log --oneline -5               # identificar commit anterior
git checkout [commit-anterior]
# reiniciar el servicio
```

### Railway / Render / Heroku
- Estos servicios tienen rollback con un clic desde el dashboard o CLI.
- Documentar el comando exacto del proveedor en el `readmes/deploy.md`.

### Migraciones en el rollback
Si el deploy incluía migraciones:
```bash
# NestJS/Prisma
npx prisma migrate resolve --rolled-back [migration-name]

# Laravel
php artisan migrate:rollback --step=1
```

---

## Métricas del pipeline

Cuando el pipeline esté configurado, establecer estos objetivos:

| Métrica | Objetivo |
|---------|---------|
| Tiempo total del pipeline CI | < 10 minutos |
| Tiempo de deploy a staging | < 5 minutos |
| Tiempo de deploy a producción | < 5 minutos |
| Tiempo de rollback | < 5 minutos |
| Frecuencia de deploys | Al menos 1 por sprint |

Si el pipeline tarda más de 10 minutos, identificar qué pasos son los más lentos y optimizarlos (caché de dependencias, paralelización de jobs).

---

## Checklist de CI/CD antes de activar en producción

- [ ] El pipeline CI corre en cada PR y falla si los tests fallan.
- [ ] No es posible hacer merge a main con CI en rojo.
- [ ] Los secrets de producción están en el environment `production` de GitHub — no en el repositorio global.
- [ ] El deploy a producción requiere aprobación manual (environment protection rule).
- [ ] Existe un procedimiento documentado de rollback.
- [ ] El equipo recibe notificaciones cuando el pipeline falla.
- [ ] El pipeline incluye las migraciones de BD como paso del deploy.
- [ ] El tiempo total del pipeline es aceptable (< 10 minutos).
