# ⚙️ Skill 04 — Setup del Entorno Local

> **Fase:** Antes del primer commit de código  
> **Objetivo:** Levantar el entorno de desarrollo local de forma reproducible desde cero.

---

## Cuándo usar este skill

- Al clonar un proyecto por primera vez.
- Al incorporar un nuevo desarrollador al proyecto.
- Al resetear el entorno local por corrupción o cambios de schema.

---

## Setup Node.js / NestJS + Next.js

### 1. Servicios de infraestructura (Docker)

```bash
# Levantar base de datos y Redis
docker-compose up -d

# Verificar que los contenedores están corriendo
docker ps
```

`docker-compose.yml` mínimo:
```yaml
services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: app_dev
    ports:
      - "3306:3306"
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### 2. Backend (NestJS)

```powershell
cd backend
npm install
cp .env.example .env          # Configurar variables de entorno
npx prisma migrate dev --name init
npx prisma generate
npx ts-node -r dotenv/config prisma/seed.ts
npm run start:dev
```

### 3. Frontend (Next.js)

```powershell
cd frontend
npm install
cp .env.example .env.local    # Configurar NEXT_PUBLIC_API_URL
npm run dev
```

---

## Setup Laravel + PHP

### 1. Instalar dependencias

```powershell
composer install
npm install
cp .env.example .env
php artisan key:generate
```

### 2. Configurar base de datos en .env

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=nombre_proyecto
DB_USERNAME=root
DB_PASSWORD=tu_password
```

### 3. Migraciones y seeds

```powershell
php artisan migrate:fresh --seed
```

> ⚠️ `migrate:fresh` borra y recrea todas las tablas. Solo usar en local.

### 4. Levantar servidor de desarrollo

```powershell
npm run dev        # Vite en paralelo
php artisan serve  # Servidor PHP
```

---

## Checklist de verificación post-setup

- [ ] Todos los servicios Docker corriendo (`docker ps`)
- [ ] Backend responde en `localhost:3000` (o puerto configurado)
- [ ] Frontend carga en `localhost:3001` (o `localhost:3000` para Next.js)
- [ ] Login funciona con el usuario semilla
- [ ] Migraciones aplicadas sin errores
- [ ] Seeds ejecutados con datos de demo visibles

---

## Variables de entorno críticas

### Backend Node.js
```env
DATABASE_URL="mysql://root:root@localhost:3306/app_dev"
REDIS_URL="redis://localhost:6379"
JWT_SECRET="secreto-local-no-produccion"
PORT=3000
NODE_ENV=development
```

### Laravel
```env
APP_ENV=local
APP_DEBUG=true
APP_KEY=base64:...
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
MAIL_MAILER=log
```

---

## Roles y usuario administrador por defecto (seeds)

El seeder debe crear siempre:
- Roles del sistema (admin, usuario, etc.)
- Un usuario administrador funcional con credenciales conocidas
- Datos de prueba realistas en las entidades principales

```typescript
// Ejemplo seed Node.js / Prisma
await prisma.user.create({
  data: {
    email: 'admin@demo.com',
    password: await bcrypt.hash('Admin123!', 10),
    role: 'ADMIN',
  }
})
```

```php
// Ejemplo seed Laravel
User::create([
    'name' => 'Administrador',
    'email' => 'admin@demo.com',
    'password' => Hash::make('Admin123!'),
])->assignRole('administrador');
```

---

## Resolución de problemas comunes

| Problema | Solución |
|---------|---------|
| `ECONNREFUSED` en DB | Verificar que Docker está corriendo: `docker ps` |
| Error de migración | Revisar `schema.prisma` o migrations, ejecutar `migrate:fresh` en local |
| `401 Unauthorized` | El seed no creó el usuario o las credenciales son incorrectas |
| Puerto ocupado | Cambiar `PORT` en `.env` o detener el proceso que ocupa el puerto |
| `prisma generate` falla | Verificar que `DATABASE_URL` es accesible |

---

## Reglas al usar este skill

- ✅ Siempre usar `.env.example` para documentar qué variables se necesitan.
- ✅ Los seeds deben dejar el sistema listo para demo sin configuración adicional.
- ✅ Documentar en `readmes/bd.md` si el schema cambia.
- ❌ Nunca poner credenciales reales en `.env.example`.
- ❌ Nunca ejecutar `migrate:fresh` en producción.

---

## Siguiente paso

→ [`05-desarrollo-modulo.md`](05-desarrollo-modulo.md) — Ciclo de desarrollo módulo por módulo.
