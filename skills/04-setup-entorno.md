# Skill 04 — Setup del Entorno Local

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
- El checklist de verificación debe ser concreto: "abre http://localhost:3000/health y deberías ver `{"status":"ok"}`".
