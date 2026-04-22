# 🏗️ Skill 03 — Arquitectura y Stack Tecnológico

> **Fase:** Definición técnica  
> **Objetivo:** Documentar el stack, la estructura de carpetas y las decisiones de arquitectura antes de escribir código.

---

## Cuándo usar este skill

- Al iniciar un proyecto nuevo.
- Al añadir una nueva capa o servicio al sistema existente.
- Cuando hay que tomar decisiones de arquitectura que afectan múltiples módulos.

---

## Stacks de referencia

### Stack Node.js / TypeScript (proyectos modernos)

| Capa | Tecnología |
|------|-----------|
| Frontend | Next.js + TypeScript + Tailwind CSS |
| Backend | NestJS + TypeScript + Prisma ORM |
| Base de datos | MySQL / MariaDB (Docker) |
| Cache / Locks | Redis |
| Auth | JWT (backend) + NextAuth.js (frontend) |
| Real-time | Socket.IO |
| Pagos | Wompi / Stripe |
| HTTP Client | Axios centralizado en `lib/api.ts` |
| Infraestructura | Docker Compose (local) + Terraform (cloud) |

### Stack Laravel / PHP (proyectos legacy / rápidos)

| Capa | Tecnología |
|------|-----------|
| Backend | Laravel 11 + PHP 8.2 |
| Frontend | Blade + Vue 3 + Tailwind CSS + Bootstrap 5 |
| Build | Vite |
| Base de datos | MySQL |
| ORM | Eloquent / Prisma |
| Auth | Laravel UI + JWT |
| Permisos | Spatie Laravel Permission |
| PDF | barryvdh/laravel-dompdf |
| OS | Windows + PowerShell |

---

## Estructura de carpetas estándar

### Node.js / Monorepo

```
proyecto/
├── backend/
│   ├── src/
│   │   ├── modules/       ← un módulo por dominio
│   │   ├── common/        ← guards, interceptors, decorators
│   │   ├── config/        ← configuración centralizada
│   │   └── main.ts
│   ├── prisma/
│   │   ├── schema.prisma
│   │   ├── migrations/
│   │   └── seed.ts
│   └── .env
├── frontend/
│   ├── app/               ← rutas (Next.js App Router)
│   ├── components/
│   ├── lib/
│   │   └── api.ts         ← Axios centralizado
│   └── .env.local
├── infra/                 ← Terraform, Docker
├── readmes/               ← Documentación por capa
└── docker-compose.yml
```

### Laravel

```
proyecto/
├── app/
│   ├── Http/Controllers/  ← Resource controllers por módulo
│   ├── Models/
│   ├── Services/          ← Lógica de negocio extraída
│   └── helpers.php        ← Funciones globales pequeñas
├── resources/views/
│   ├── Admin/             ← Vistas por rol
│   │   ├── Cliente/
│   │   ├── Productos/
│   │   └── Configuracion/
│   ├── Recepcionista/
│   └── layouts/
├── routes/web.php          ← Grupos de rutas por rol
├── database/
│   ├── migrations/
│   └── seeders/
└── readmes/
```

---

## Convenciones técnicas clave

| Aspecto | Convención |
|---------|-----------|
| Idioma en comentarios y docs | Español |
| TypeScript | Estricto, sin `any` si es evitable |
| Variables de entorno | `.env` en cada capa + `.env.example` documentado |
| Nombres de archivos de docs | snake_case |
| Nombres de rutas (Laravel) | snake_case con prefijo de rol (`admin.modulo.index`) |
| Concurrencia | Transacciones DB + Redis locks cuando aplica |
| Seguridad | OWASP Top 10, HMAC en webhooks, rate limiting en endpoints sensibles |
| Estructura de rutas (Laravel) | Grupos con `prefix`, `as`, `middleware` desde el inicio |

---

## Documento de salida: flujo-final.md

```markdown
# Arquitectura del Sistema — [Proyecto]

## Stack
...

## Estructura de carpetas
...

## Decisiones de diseño
- Por qué X en lugar de Y: [justificación]
...

## Diagrama de flujo de datos
...

## Variables de entorno requeridas
...
```

---

## Prompt para arquitectura con Claude

```
Basándote en readmes/logica.md y readmes/tareas.md, genera readmes/flujo-final.md con:
- Stack tecnológico justificado
- Estructura de carpetas del proyecto
- Decisiones de diseño clave con justificación
- Variables de entorno necesarias (.env.example)
- Diagrama ASCII del flujo de datos principal
Usa el stack: [lista tu stack preferido]
```

---

## Reglas al usar este skill

- ✅ Definir el stack antes de crear cualquier archivo de código.
- ✅ Documentar el *por qué* de cada decisión técnica importante.
- ✅ Crear `.env.example` desde el inicio con todas las variables necesarias.
- ❌ No cambiar el stack a mitad del proyecto sin actualizar este documento.
- ❌ No mezclar convenciones de dos frameworks en el mismo módulo.

---

## Siguiente paso

→ [`04-setup-entorno.md`](04-setup-entorno.md) — Levantar el entorno local.
