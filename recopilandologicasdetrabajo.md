# Mi Flujo de Trabajo con GitHub Copilot

> Documento personal que describe cómo trabajo con el agente de IA, cómo inicio y finalizo proyectos, y cómo resuelvo problemas durante el desarrollo.

---

## 1. Cómo me comunico con el agente

- **Idioma:** Siempre en español. El agente responde en español.
- **Tono directo:** Pido lo que necesito de forma concisa y específica, sin rodeos.
- **Aprobación antes de ejecutar:** Cuando hay un plan grande o cambios importantes, primero le pido que me explique el plan y yo lo apruebo antes de que empiece a modificar archivos.
- **Pido detalles cuando algo no está claro:** Si el agente propone algo que no entiendo o no me convence, pregunto antes de seguir.
- **Actualización de documentación en paralelo:** Cuando se implementa algo, también le pido que actualice los readmes del proyecto para que el estado documentado sea siempre real.

---

## 2. Cómo inicio un proyecto

### 2.1 Definición de la lógica de negocio
Lo primero es escribir (o pedirle al agente que me ayude a escribir) un documento de lógica de negocio (`logica.md` o similar). Este documento incluye:

- Propósito del proyecto y stakeholders (quién lo usa y para qué).
- Requisitos clave y reglas de negocio.
- Modelado de datos: entidades, relaciones, enumeraciones.
- Lógica crítica (transacciones, atomicidad, concurrencia).
- Endpoints REST propuestos con descripción.
- Flujo de frontend: páginas, acciones del usuario.

### 2.2 Desglose de tareas
Con la lógica clara, creo un `tareas.md` que desglosa todo en tareas accionables agrupadas por área:

- **Backend** (prioridad alta)
- **Frontend** (prioridad alta)
- **DevOps / Infraestructura**
- **Testing**
- **Seguridad / Operaciones**
- **Rendimiento / Escalado**
- **Documentación**
- **Scripts auxiliares**

Cada grupo tiene tareas numeradas, y al final defino el **primer sprint** con las tareas más críticas.

### 2.3 Stack tecnológico definido desde el inicio
Siempre dejo claro el stack en un documento de arquitectura (`flujo-final.md`):

- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: NestJS + TypeScript + Prisma ORM
- Base de datos: MySQL/MariaDB vía Docker
- Cache / Locks: Redis
- Auth: JWT (backend) + NextAuth.js (frontend)
- Real-time: Socket.IO
- Pagos: Wompi (o proveedor externo)
- Infraestructura: Docker Compose para local, Terraform para cloud

### 2.4 Levantar entorno local
Siempre comienzo con Docker para la base de datos y servicios auxiliares:

```powershell
docker-compose up -d
```

Luego instalo dependencias y ejecuto migraciones:

```powershell
cd backend
npm install
npx prisma migrate dev --name init
npx prisma generate
npx ts-node -r dotenv/config prisma/seed.ts
```

```powershell
cd frontend
npm install
npm run dev
```

---

## 3. Cómo trabajo mientras el proyecto avanza

### 3.1 Documentos de estado por capa
Mantengo un documento por capa del proyecto que describe:

- Qué se implementó (lista concisa de lo hecho).
- Qué falta (pendientes concretos y priorizados).
- Porcentaje de avance estimado.
- Comandos útiles para esa capa.
- Notas importantes sobre decisiones de diseño.

Documentos típicos:
- `readmes/flujo_backend.md`
- `readmes/flujo_frontend.md`
- `readmes/bd.md`
- `readmes/flujo-final.md`

### 3.2 Trabajo por prioridades
Siempre trabajo con prioridades explícitas: **alta**, **media**, **baja**. Las tareas de alta prioridad se completan primero. No avanzo a una tarea de menor prioridad si hay bloqueantes pendientes en las de mayor prioridad.

### 3.3 Cómo le pido trabajo al agente
- Soy específico: indico qué archivo, qué función, qué comportamiento quiero.
- Cuando es una tarea grande, pido primero el plan y luego la implementación.
- Cuando es un fix puntual, pido directamente el cambio.
- Cuando no sé cómo algo debería funcionar, le pregunto opciones y él me da la recomendación con justificación.

### 3.4 Revisión de cambios
Después de que el agente implementa algo importante:

1. Reviso los archivos modificados.
2. Pruebo manualmente o con scripts de prueba.
3. Si algo no funciona, lo reporto con el error exacto (mensaje de error, stack trace, comportamiento observado vs. esperado).

### 3.5 Resolución de problemas
Cuando hay un bug o algo no funciona, sigo este flujo:

1. **Describir el problema** con contexto: qué hice, qué esperaba, qué pasó.
2. **Adjuntar el error exacto** si lo hay (stack trace, mensaje de consola, código de respuesta HTTP).
3. **Indicar el archivo o capa** donde cree que está el problema (o pregunto si no sé).
4. El agente diagnostica, propone la causa raíz y el fix.
5. Apruebo el fix y el agente lo aplica directamente sobre los archivos.
6. Si el fix no resuelve, itero con más contexto.

---

## 4. Cómo finalizo un proyecto

### 4.1 Revisión final de pendientes
Antes de cerrar, reviso todos los `tareas.md` y los documentos de flujo para asegurarme de que:

- No quedan bugs conocidos sin resolver.
- Los tests críticos están en verde.
- La documentación refleja el estado real del código.

### 4.2 Checklist de cierre
- [ ] Migraciones aplicadas y schema en producción actualizado.
- [ ] Variables de entorno de producción configuradas (`.env.production`, secrets en el proveedor).
- [ ] Docker image construida y probada.
- [ ] CI/CD ejecutando sin errores (lint, tests, build).
- [ ] README principal actualizado con instrucciones de arranque.
- [ ] Documentos de flujo actualizados al 100%.
- [ ] Secrets rotados y no expuestos en el repo.

### 4.3 Deploy
El proceso de deploy usa scripts del proyecto (`backend/deploy.sh`, `Procfile`) y se documenta en `readmes/`. Siempre se despliega sobre una rama limpia y sin commits pendientes.

---

## 5. Convenciones y preferencias técnicas

| Aspecto | Preferencia |
|---------|-------------|
| ORM | Prisma |
| Base de datos | MySQL / MariaDB en Docker |
| Auth | JWT en backend, NextAuth.js en frontend |
| Estilo de código | TypeScript estricto, sin `any` si es evitable |
| HTTP Client (frontend) | Axios centralizado en `lib/api.ts` |
| Variables de entorno | `.env` en cada capa, `.env.example` documentado |
| Estructura de carpetas | Backend en `backend/`, Frontend en `frontend/`, Infra en `infra/`, Docs en `readmes/` |
| Nombres de archivos de docs | Snake_case en inglés o español según contexto |
| Idioma en comentarios y docs | Español |
| Gestión de concurrencia | Transacciones DB + locks Redis cuando aplica |
| Seguridad | OWASP Top 10 como referencia, HMAC en webhooks, rate limiting en endpoints sensibles |

---

## 6. Estructura de documentación de cada proyecto

```
proyecto/
├── readmes/
│   ├── logica.md          # Lógica de negocio y requisitos
│   ├── tareas.md          # Desglose de tareas y sprints
│   ├── flujo-final.md     # Arquitectura y estado real del sistema
│   ├── flujo_backend.md   # Estado e implementación del backend
│   ├── flujo_frontend.md  # Estado e implementación del frontend
│   └── bd.md              # Diseño y esquema de base de datos
└── README.md              # Punto de entrada general
```

---

## 7. Reglas generales que sigo con el agente

1. **No generar archivos innecesarios.** Solo creo archivos que realmente se usan.
2. **No hacer refactors no pedidos.** El agente solo cambia lo que se le pide.
3. **No agregar comentarios ni docstrings al código que no fue modificado.**
4. **Cambios reversibles primero.** Para acciones destructivas (drop de tablas, reset de datos, force push) siempre pido confirmación explícita.
5. **Contexto antes de implementar.** El agente lee los archivos relevantes antes de modificarlos.
6. **Errores con causa raíz.** No aceptar fixes superficiales que oculten el problema real.
7. **Actualizar el estado documentado.** Cada vez que se implementa algo, actualizar el readme correspondiente.

---

## 8. Cómo escalo o extiendo una funcionalidad existente

1. Leer el documento de flujo de la capa que voy a tocar (`flujo_backend.md`, `flujo_frontend.md`).
2. Entender qué ya existe para no duplicar.
3. Pedir al agente que extienda usando los patrones ya establecidos en el código (mismos nombres de servicios, misma estructura de carpetas, mismo estilo).
4. Verificar que no rompe endpoints o componentes existentes.
5. Actualizar el documento de flujo con lo nuevo.

---

*Documento generado a partir de la observación del flujo real de trabajo en el proyecto ArisRifas.*


_____________________________________________


# Mi Flujo de Trabajo con Copilot / Asistente

Este documento resume cómo me gusta trabajar y cómo pido y gestiono tareas al asistente (Copilot). Está basado en la manera en que trabajamos en este repositorio y en las convenciones y prácticas que sigo al solicitar cambios, empezar y terminar proyectos, y durante el desarrollo.

## Propósito
- Documentar mi forma de pedir y recibir trabajo del asistente.
- Establecer un flujo reproducible para iniciar, ejecutar y cerrar tareas.
- Facilitar que cualquier colaborador o asistente siga mis expectativas al trabajar en este proyecto.

## Lenguaje y tono
- Preferencia de idioma: español.
- Respuestas: concisas, directas y orientadas a la acción.
- Mostrar solo lo necesario para avanzar; preguntar cuando falte contexto.

## Cómo pido trabajo al asistente
- Proporciono contexto relevante (archivos, fragmentos, .env, rutas).
- Indico claramente el objetivo y el alcance (qué modificar, dónde y por qué).
- Especifico si quiero acciones automáticas (crear/editar archivos) o solo sugerencias.
- Si hay restricciones (no tocar tests, no cambiar configuración global), las indico al inicio.
- Ejemplo de petición efectiva: "Corrige la validación de `src/api/checkout.ts` para manejar pagos fallidos; crea test unitario y actualiza README si corresponde."

## Qué espero que haga el asistente al recibir una tarea
- Presentar un plan breve (TODOs) cuando la tarea sea multi-paso.
- Antes de ejecutar herramientas, enviar un preámbulo muy corto explicando la acción siguiente.
- Ejecutar acciones concretas (crear/editar archivos) usando cambios mínimos y localizados.
- Si se edita código, usar parches pequeños y coherentes, y no reformatar innecesariamente.
- Ejecutar pruebas o comprobaciones rápidas si están disponibles y el usuario lo autoriza.

## Inicio de un proyecto o tarea (pasos)
1. Definir alcance: objetivo, criterios de aceptación, y archivos implicados.
2. Crear una lista de tareas (TODO) con pasos claros y estados.
3. Pedir al asistente que confirme entendimiento o solicite aclaraciones.
4. Autorizar al asistente a editar archivos y a ejecutar pruebas si procede.

## Flujo durante el trabajo
- El asistente debe: 
  - Enviar preámbulos cortos antes de usar herramientas.
  - Hacer cambios mínimos y documentarlos.
  - Proveer actualizaciones de progreso cada 3–5 acciones o después de cambios grandes.
  - Pedir confirmación para cambios de diseño o cuando encuentre ambigüedades.
- Comunicación: uso de mensajes cortos y directos; cuando sea necesario, incluir ejemplos de prompts o snippets.

## Cómo entrego contexto útil (mejor práctica)
- Seleccionar y compartir fragmentos de archivo (líneas relevantes) o adjuntar el archivo completo si es pequeño.
- Indicar rutas exactas dentro del repo (p. ej. `src/components/Cart.tsx`) y el propósito del archivo.
- Incluir variables de entorno relevantes cuando afecten al comportamiento (sin exponer secretos en repositorios públicos).

## Edición de archivos: buenas prácticas que sigo
- Preferir cambios pequeños, revisables y atómicos.
- Usar parches (diffs) en lugar de reescrituras completas cuando sea posible.
- Mantener el estilo y convenciones del repositorio (TypeScript, Tailwind, Prisma, etc.).
- Añadir tests básicos para cambios lógicos (unitarios o integrados) cuando aplique.

## Finalización de la tarea / Proyecto
- Ejecutar pruebas unitarias y/o integradas si existen.
- Actualizar documentación mínima: README, notas de implementación o comentarios clave.
- Generar un resumen de cambios aplicados y pasos para verificar localmente.
- Preguntar si deseo que se: commit, cree PR, o despliegue (si corresponde).

## Manejo de incidencias y regresiones
- Si aparece un error, el asistente debe:
  - Reproducir el fallo localmente cuando sea posible.
  - Proponer la causa raíz y una solución alternativa rápida (hotfix) si necesario.
  - Priorizar correcciones que no introduzcan riesgos a otras partes.

## Ejemplos concretos de interacción (prompts recomendados)
- "Crea un archivo `miflujotrabajo.md` fuera del proyecto con mi flujo de trabajo." (Esperar: plan -> preámbulo -> archivo creado -> confirmación).
- "Corrige la migración en `prisma/migrations/...` y añade test que falle antes y pase después." (Esperar: plan con pasos, edición, test, ejecución de test).
- "Haz un patch pequeño que cambie solo la validación en `src/api/user.ts` y dime cómo probarlo." (Esperar: patch + instrucciones de prueba).

## Reglas de colaboración con el asistente (resumidas)
- Usar la lista de tareas (`TODO list`) para trabajos multi-paso.
- Recibir preámbulos antes de llamadas a herramientas automáticas.
- Mantener las ediciones pequeñas y con foco.
- Pedir confirmación para las decisiones de diseño que afecten la arquitectura.
- Entregar siempre instrucciones de verificación (comandos para correr tests o pasos manuales).

## Checklist de cierre (qué revisar antes de dar por terminada la tarea)
- [ ] Tests relevantes pasan.
- [ ] Cambios mínimos y atómicos en el repo.
- [ ] Documentación actualizada si aplica.
- [ ] Resumen de cambios y comandos de verificación entregados.
- [ ] Pregunta final al usuario: ¿Quiero que haga commit/PR/despliegue?

---

________________________-------------___________

# Mi Flujo de Trabajo con GitHub Copilot (Alfon)

> Documento personal que resume cómo trabajo, cómo le pido ayuda a la IA, mi proceso desde que inicio hasta que entrego un proyecto, y cómo resuelvo problemas en el camino.

---

## Stack tecnológico habitual

| Capa | Tecnología |
|---|---|
| Backend | Laravel 11, PHP 8.2 |
| Frontend | Blade + Vue 3 + Tailwind CSS + Bootstrap 5 |
| Build | Vite |
| Base de datos | MySQL |
| Permisos | Spatie Laravel Permission |
| PDF | barryvdh/laravel-dompdf |
| Autenticación | Laravel UI (Auth scaffolding) |
| Editor | VS Code con GitHub Copilot |
| OS | Windows (PowerShell) |

---

## 1. Cómo me comunico con el agente

- **Idioma:** Siempre en español. El agente responde en español.
- **Tono directo:** Pido lo que necesito sin rodeos. No quiero opciones ni sugerencias si no las pedí.
- **Implementación directa:** No pido que me diga cómo hacerlo, pido que lo haga. El agente lee el código, entiende el contexto y aplica los cambios.
- **Aprobación antes de ejecutar:** Para planes grandes o cambios estructurales importantes, primero veo el plan y lo apruebo antes de que toque archivos.
- **Pido detalles cuando algo no está claro:** Si el agente propone algo que no entiendo, pregunto antes de seguir.
- **Respuestas breves:** Si el código es claro, no necesito un ensayo explicativo. Prefiero confirmaciones cortas.

---

## 2. Cómo inicio un proyecto

### 2.1 Definición del dominio de negocio
Lo primero que hago antes de tocar código es definir las entidades del sistema:
- ¿Quiénes son los actores? (roles: administrador, recepcionista, etc.)
- ¿Qué entidades maneja el sistema? (clientes, productos, ventas, membresías, personal, flujos de caja, etc.)
- ¿Qué puede hacer cada rol?
- ¿Cuáles son las relaciones entre entidades?

### 2.2 Migraciones y modelos desde el inicio
Con el dominio claro, creo migraciones y modelos para cada entidad antes de escribir cualquier lógica. Prefiero tener el schema definido y sólido desde el principio.

### 2.3 Roles y permisos desde el principio (Spatie)
Configuro `spatie/laravel-permission` desde el inicio del proyecto. Defino los roles, los middlewares y los grupos de rutas antes de empezar a implementar módulos. Así todo lo que se construya ya respeta la estructura de acceso.

### 2.4 Estructura de rutas por rol
Organizo las rutas en grupos con `prefix`, `as` y `middleware` desde el inicio:

```php
Route::group([
    'middleware' => ['auth', 'role:administrador'],
    'as' => 'admin.',
    'prefix' => 'admin'
], function () {
    Route::resource('modulo', ModuloController::class);
});
```

### 2.5 Seeders iniciales
Creo seeders para dejar el sistema listo: roles, permisos, usuario administrador y datos de prueba esenciales.

### 2.6 Levantar el entorno local

```powershell
composer install
npm install
php artisan migrate:fresh --seed
npm run dev
php artisan serve
```

---

## 3. Cómo trabajo mientras el proyecto avanza

### 3.1 Desarrollo módulo por módulo (CRUD completo)
Trabajo un módulo completo antes de pasar al siguiente. El orden siempre es:

```
Migración → Modelo → Controller → Rutas → Vistas → Prueba manual → Fix si hay bugs → Siguiente módulo
```

### 3.2 Estructura de vistas por rol y módulo
Las vistas están organizadas por rol y módulo para no mezclar contextos:

```
resources/views/
├── Admin/
│   ├── Cliente/
│   ├── Productos/
│   ├── Membresias/
│   ├── flujos/
│   ├── users/
│   └── Configuracion/
├── Recepcionista/
│   └── ...
└── layouts/
```

### 3.3 Cómo le pido trabajo al agente
- Soy específico: indico qué archivo, qué función, qué módulo, qué comportamiento espero.
- Para tareas grandes: primero le pido el plan, lo apruebo, y luego implementa.
- Para fixes puntuales: pido el cambio directo sin explicaciones largas.
- Cuando no sé cómo debería funcionar algo: le pregunto y me da la recomendación con justificación corta.
- Cuando algo tiene muchas partes interdependientes (controller + vista + modelo + ruta), pido que trabaje todo junto para no romper nada.

### 3.4 Revisión de cambios
Después de que el agente implementa algo importante:
1. Reviso los archivos modificados.
2. Pruebo manualmente en el navegador.
3. Si algo no funciona, reporto el error exacto y el comportamiento observado vs. el esperado.

### 3.5 Helpers globales
Uso `app/helpers.php` (autoloaded vía composer) para funciones pequeñas que se repiten en múltiples partes del sistema y no justifican una clase propia.

### 3.6 API interna con Vue
Cuando el frontend necesita datos dinámicos con Vue 3, uso rutas bajo `/api` con middleware `cors` en el backend y Axios en el frontend:

```php
Route::prefix('api')->group(function () {
    Route::group(['middleware' => ['cors']], function () {
        Route::get('/productos', [ProductoAPIController::class, 'index']);
    });
});
```

---

## 4. Cómo resuelvo problemas

1. **Describo el síntoma exacto**: qué hice, qué esperaba que pasara, qué pasó en realidad.
2. **Adjunto el error exacto** si lo hay: mensaje de error, stack trace, código de respuesta HTTP, salida de consola.
3. **Indico el archivo o módulo** donde creo que está el problema. Si no sé, le pregunto al agente.
4. El agente lee el código, diagnostica la causa raíz y aplica el fix directamente.
5. Si el fix no resuelve, doy más contexto e itero. No acepto fixes superficiales que oculten el problema real.
6. Si el agente intenta dos enfoques distintos sin resultado, pedimos juntos un paso atrás y replanteo la estrategia.

---

## 5. Cómo finalizo un proyecto

### 5.1 Revisión de rutas y accesos
Verifico que todos los módulos tengan sus rutas definidas correctamente, con los middlewares de rol que corresponden, y que ningún endpoint quede accesible sin autenticación.

### 5.2 Seeders finales
Me aseguro de que los seeders dejen el sistema listo para una demo o entrega:
- Roles creados y asignados
- Usuario administrador funcional
- Datos de prueba realistas en las entidades principales

### 5.3 Prueba de partida limpia

```powershell
php artisan migrate:fresh --seed
```

Esto confirma que el sistema arranca desde cero sin errores de migración ni de seeding.

### 5.4 Revisión de permisos
Cada usuario solo ve y puede hacer lo que corresponde a su rol. Pruebo con sesiones de distintos roles.

### 5.5 Build de frontend para producción

```powershell
npm run build
```

### 5.6 Revisión visual manual
Recorro cada pantalla de cada rol verificando que nada esté roto visualmente ni funcionalmente.

### 5.7 Configuración del `.env` para producción
- `APP_ENV=production`
- `APP_DEBUG=false`
- Credenciales de base de datos de producción
- Configuración de mail
- `APP_KEY` generado correctamente

---

## 6. Flujo visual del desarrollo

```
[Nuevo módulo o feature]
         │
         ▼
Migración + Modelo (relaciones, fillable, casts)
         │
         ▼
Resource Controller (index, create, store, show, edit, update, destroy)
         │
         ▼
Rutas en el grupo de rol correspondiente
         │
         ▼
Vistas Blade: index → create → edit → show
         │
         ▼
Prueba manual en el navegador (por cada rol)
         │
         ▼
¿Hay bugs? → Sí: fix → volver a probar
         │ No
         ▼
Siguiente módulo
```

---

## 7. Convenciones y preferencias técnicas

| Aspecto | Preferencia |
|---|---|
| Controladores | Resource controllers estándar de Laravel |
| Validaciones | `FormRequest` para lógica compleja, `validate()` inline para casos simples |
| Helpers | `app/helpers.php` para funciones globales pequeñas |
| Permisos | Spatie con middleware `role:` y `permission:` en grupos de rutas |
| Frontend dinámico | Vue 3 con Vite, solo donde se necesita interactividad real |
| Estilos | Tailwind CSS + Bootstrap 5 combinados |
| PDF | `barryvdh/laravel-dompdf` desde controladores |
| Idioma en código y docs | Español |
| Nombres de rutas | snake_case con prefijo de rol (`admin.modulo.index`) |
| Estructura de vistas | Carpetas por rol, subcarpetas por módulo |
| OS y terminal | Windows + PowerShell |

---

## 8. Reglas generales que sigo con el agente

1. **No generar archivos innecesarios.** Solo se crean archivos que realmente se usan.
2. **No hacer refactors no pedidos.** El agente cambia únicamente lo que se le pide.
3. **No agregar comentarios ni docstrings al código que no fue modificado.**
4. **No agregar manejo de errores para escenarios imposibles.** Solo validación en los bordes del sistema.
5. **Leer antes de modificar.** El agente lee los archivos relevantes antes de tocarlos.
6. **Causa raíz, no parches.** No acepto fixes que oculten el problema real.
7. **Acciones destructivas: confirmación previa.** Para `migrate:fresh`, borrar archivos, resetear datos, etc., siempre pido confirmación explícita primero.
8. **Si un enfoque falla dos veces, cambiar de estrategia.** No insistir en el mismo camino.

---

## 9. Cómo extiendo una funcionalidad existente

1. Le pido al agente que lea primero los archivos relacionados con lo que voy a tocar.
2. Le pido que entienda qué ya existe para no duplicar lógica.
3. Le pido que extienda usando los patrones ya establecidos en el proyecto: misma estructura de carpetas, mismos nombres de controladores y vistas, mismo estilo de rutas.
4. Verifico que los cambios no rompan módulos existentes.
5. Si la extensión afecta la base de datos, creo una nueva migración (nunca modifico migraciones ya corridas en producción).

---

______________________________________________________

# Mi flujo de trabajo

## 1) Cómo solicito tareas
- Defino un objetivo claro y práctico (por ejemplo: probar carga, validar flujo completo).
- Comparto contexto técnico: repositorio, archivos involucrados, entorno y comandos.
- Pido cambios accionables (scripts, ajustes, documentación y próximos pasos).
- Valoro respuestas con resultados medibles (creados/fallidos, `avg`, `p95`, errores HTTP).

## 2) Cómo abordo y resuelvo problemas
- Empiezo con una hipótesis simple y reproducible.
- Ejecuto pruebas controladas con parámetros de concurrencia.
- Identifico bloqueos funcionales (ejemplo: `401` por falta de token en endpoints protegidos).
- Separo hallazgos en:
  - Lo que funciona (creación de pedidos).
  - Lo que requiere condiciones adicionales (transiciones autenticadas).
- Convierto hallazgos en acciones concretas para la siguiente iteración.

## 3) Cómo inicio proyectos o pruebas
- Preparo un script base y lo adapto al objetivo.
- Configuro variables necesarias (`API_TOKEN`, URL base, workers, pedidos por cliente).
- Documento desde el inicio:
  - Objetivo
  - Ambiente
  - Procedimiento
  - Criterios de éxito

## 4) Cómo cierro proyectos o iteraciones
- Registro resultados cuantitativos y cualitativos.
- Dejo evidencia de ejecución (comandos y extractos de salida).
- Enumero limitaciones detectadas y riesgos.
- Propongo siguientes pasos priorizados (más carga, monitoreo, validación de consistencia).
- Mantengo trazabilidad de archivos modificados y conclusión final.

## 5) Mi proceso de trabajo (resumen)
1. Definir objetivo y alcance.
2. Preparar/ajustar herramienta de ejecución.
3. Ejecutar prueba con parámetros controlados.
4. Analizar métricas y errores.
5. Documentar hallazgos y recomendaciones.
6. Planificar siguiente iteración con mayor realismo (autenticación, monitoreo, mayor concurrencia).

## 6) Estilo operativo
- Iterativo, orientado a evidencia.
- Enfoque en reproducibilidad y claridad.
- Decisiones basadas en datos observables.
- Documentación como parte obligatoria del resultado.

______________________________________________________

# Mi Flujo de Trabajo

Este documento describe, en detalle, cómo me pides trabajo, cómo resuelvo problemas, cómo comienzo y finalizo proyectos, y cómo trabajo durante el desarrollo. Está pensado para que cualquier colaborador (o la IA asistente) entienda y reproduzca mi forma de trabajar.

---

## 1. Principios generales

- Enfoque en la causa raíz: siempre buscar y arreglar el origen del problema, no aplicar parches superficiales.
- Cambios mínimos y claros: aplicar la modificación más pequeña que resuelva el problema y mantener el estilo existente.
- Comunicación concisa: preámbulos breves antes de acciones automatizadas (1–2 frases) y actualizaciones de progreso cortas.
- Reproducibilidad: dejar pasos claros para reproducir, probar y verificar cualquier cambio.

## 2. Cómo me pides que trabaje (plantilla de solicitud)

Cuando solicites trabajo, incluye al menos:

- Objetivo claro: qué quieres lograr en una sola frase.
- Archivos/paths: lista de archivos o rutas exactas a modificar (si aplica).
- Comportamiento esperado: ejemplos de entrada/salida o criterios de aceptación.
- Restricciones: versiones, dependencias a no tocar, formato, tiempos.
- Tests de aceptación (opcionales pero preferidos): comandos o pasos para verificar que funciona.

Ejemplo corto:
- Objetivo: "Corregir fallo X al subir factura"
- Archivos: `app/Services/InvoiceService.php`
- Resultado esperado: "Al subir archivo con formato Y, no se produce la excepción Z"
- Tests: pasos para reproducir o tests unitarios a añadir.

## 3. Inicio de un proyecto/tarea (checklist)

- 1) Leer la solicitud y confirmar ambigüedades.
- 2) Explorar el repo: identificar puntos relevantes (buscar filenames y llamadas).
- 3) Crear un plan/todo con pasos (usar `manage_todo_list`).
- 4) Crear rama/entorno (si aplica): rama descriptiva y aislada.
- 5) Preparar pruebas mínimas para reproducir el problema.

## 4. Mientras trabajo: prácticas y herramienta preferidas

- Preambulo breve antes de ejecutar acciones automáticas (ej.: "Voy a aplicar un parche y ejecutar tests unitarios").
- Ediciones de código:
  - Para modificar archivos existentes: usar `apply_patch` (o equivalente) y hacer cambios pequeños, atómicos.
  - Para crear archivos nuevos: usar `create_file` con contenido completo y razonable.
- Tests y verificación:
  - Ejecutar sólo los tests necesarios localmente primero, luego correr la suite completa si pasa.
  - Usar `execution_subagent` o la herramienta de terminal apropiada para correr comandos y presentar salida relevante.
- Mensajes de progreso: cada 3–5 acciones significativas, publicar un breve estado.
- Evitar cambios masivos: no reformatear ficheros enteros a menos que sea requerido.

## 5. Resolución de problemas

- Reproducir primero: obtener pasos exactos para replicar el bug.
- Inspeccionar logs/errores y aislar la función o módulo responsable.
- Escribir un test que reproduzca el fallo, si es posible.
- Implementar la corrección mínima y volver a ejecutar los tests.
- Si la corrección es riesgosa, proponer alternativas y pedir aprobación antes de aplicar grandes refactors.

## 6. Finalización del proyecto/tarea (checklist)

- 1) Verificar que todos los tests relevantes pasan.
- 2) Actualizar o añadir tests de aceptación si procede.
- 3) Añadir notas en el commit y en el PR explicando la causa raíz y la solución.
- 4) Ejecutar un chequeo rápido de calidad (linters o php-cs-fixer si aplica) sin reformatar archivos no relacionados.
- 5) Cerrar el TODO correspondiente y notificar con un resumen de cambios y pasos para validar.

## 7. Convenciones de commit y ramas

- Ramas: `feature/<descripcion>`, `fix/<descripcion>`, `chore/<descripcion>`.
- Commits: mensajería clara con referencia a issue o ticket si existe. Primer línea corta (50 chars aprox.), cuerpo explicativo con la causa raíz.
- Commits atómicos: un cambio lógico por commit.

## 8. Comunicación y formato en PRs/tareas

- Resumen breve del cambio: qué se cambió y por qué.
- Pasos para probar localmente.
- Riesgos y notas (migraciones, cambios en DB, etc.).
- Enlaces a tickets o discusiones previas.

## 9. Plantilla rápida para pedir cambios a la IA o a un compañero

- Título: breve
- Objetivo: 1 frase
- Archivos a tocar: lista
- Comportamiento esperado: bullets con ejemplos
- Restricciones: bullets
- Tests de aceptación: pasos o comandos

## 10. Ejemplo de flujo (resumido)

1. Recibo solicitud con la plantilla.
2. Confirma/aclara dudas.
3. Creo TODO y rama.
4. Reproduzco bug y escribo test.
5. Aplico cambio mínimo con `apply_patch`.
6. Corro tests necesarios.
7. Formulo PR con descripción y cierro TODO.

## 11. Notas finales y expectativas hacia la IA asistente

- Preambulo corto antes de usar herramientas.
- Usa `manage_todo_list` al iniciar tareas multi-paso.
- Prioriza arreglar la causa raíz.
- No hagas cambios masivos sin permiso.
- Resume los pasos realizados y por hacer al terminar.

---
