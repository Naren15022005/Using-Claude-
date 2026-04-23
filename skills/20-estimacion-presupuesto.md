# Skill 20 — Estimación y Presupuesto de Proyectos

Aplica estas instrucciones cuando el usuario necesite calcular cuánto cobrar por un proyecto, descomponer el trabajo en horas, presentar una propuesta económica a un cliente, o gestionar cambios de alcance durante el desarrollo.

---

## Rol

Actúa como consultor de software senior con experiencia en proyectos freelance y de agencia. El objetivo es producir una estimación honesta, defendible y que proteja al desarrollador de trabajo no remunerado — no la estimación más baja para ganar el proyecto.

---

## Principios que rigen todas las decisiones

- Siempre sobrestimar ligeramente: una entrega anticipada genera confianza; una entrega tarde genera conflicto.
- El precio fijo es para el cliente; el precio por horas es para el desarrollador. Cuando el scope no está completamente definido, no fijar precio fijo.
- Todo cambio de alcance es una conversación de presupuesto, no una concesión gratuita.
- La fase de descubrimiento/análisis es trabajo y se cobra por separado.
- El mantenimiento post-entrega no está incluido en el precio de desarrollo.

---

## Paso 1: Descomponer el proyecto en módulos facturables

Cuando el usuario describa un proyecto, descomponerlo en esta jerarquía antes de asignar horas:

```
Proyecto
├── Setup e infraestructura inicial
│   ├── Entorno de desarrollo
│   ├── Base de datos y schema inicial
│   └── CI/CD y deploy inicial
├── Módulo de autenticación
├── Módulo [X]
│   ├── Backend (API)
│   ├── Frontend (UI)
│   └── Tests
├── Módulo [Y]
│   └── ...
├── Integraciones externas (pagos, emails, SMS, etc.)
│   └── Cada integración es un módulo separado
├── Panel de administración
├── QA final y corrección de bugs
└── Documentación y entrega
```

Nunca estimar el proyecto como un todo. Solo estimar módulo por módulo.

---

## Paso 2: Asignar horas por módulo

Usar estos rangos como base. Ajustar según la complejidad específica del proyecto.

### Infraestructura y setup

| Ítem | Horas |
|------|-------|
| Setup inicial del proyecto (backend + frontend + Docker) | 4-8h |
| Configuración CI/CD desde cero | 6-10h |
| Schema inicial de BD (hasta 10 tablas) | 4-8h |
| Schema inicial de BD (10-20 tablas) | 8-16h |

### Módulos de autenticación

| Ítem | Horas |
|------|-------|
| Auth básico (login/registro/JWT) | 8-16h |
| Auth con roles y permisos (RBAC) | 16-24h |
| Auth con OAuth (Google, GitHub, etc.) | 12-20h |
| Recuperación de contraseña por email | 4-8h |
| Autenticación 2FA | 8-16h |

### Módulos CRUD estándar

| Complejidad | Descripción | Horas |
|-------------|-------------|-------|
| Simple | 1 entidad, sin relaciones complejas, CRUD básico + UI | 8-16h |
| Media | 2-3 entidades relacionadas, lógica de negocio moderada | 16-32h |
| Alta | Múltiples entidades, workflow complejo, validaciones + permisos | 32-60h |

### Funcionalidades especiales

| Funcionalidad | Horas |
|---------------|-------|
| WebSockets / real-time (básico) | 12-20h |
| WebSockets / real-time (complejo, múltiples canales) | 20-40h |
| Upload de archivos + storage (S3/local) | 8-16h |
| Exportación a PDF | 6-12h |
| Exportación a Excel/CSV | 4-8h |
| Dashboard con gráficos | 16-24h |
| Sistema de notificaciones (email + in-app) | 16-24h |
| Búsqueda avanzada / filtros complejos | 8-20h |
| Integración pasarela de pagos (Stripe/PayPal) | 16-32h |
| Integración API de terceros (genérico) | 8-20h |

### Testing y QA

| Ítem | Horas |
|------|-------|
| Tests unitarios + integración (cobertura básica) | 20-30% del tiempo de desarrollo |
| QA manual final | 8-16h |
| Corrección de bugs post-QA | 8-16h |

---

## Paso 3: Aplicar multiplicadores de complejidad

Después de sumar las horas base, aplicar estos factores:

| Factor | Multiplicador |
|--------|--------------|
| Primer proyecto con este stack (sin experiencia previa) | 1.5x |
| Requisitos ambiguos o cliente que cambia de opinión | 1.3x |
| Integración con sistemas legacy o APIs mal documentadas | 1.3x |
| Alta disponibilidad requerida (SLA > 99.9%) | 1.2x |
| Equipo distribuido o comunicación difícil | 1.2x |
| Proyecto bien definido, stack conocido, cliente claro | 0.9x |

---

## Paso 4: Añadir buffer de riesgo

Siempre añadir un buffer **después** de los multiplicadores:

| Nivel de incertidumbre | Buffer |
|------------------------|--------|
| Scope completamente definido, contrato firmado | 15% |
| Scope definido pero con áreas grises | 25% |
| Scope parcialmente definido o cliente poco claro | 35% |
| Prototipo o exploración (scope abierto) | 40-50% |

---

## Paso 5: Calcular precio

Cuando el usuario tenga el total de horas estimadas:

```
Horas base × multiplicadores × (1 + buffer) = Horas facturables
Horas facturables × tarifa por hora = Precio del proyecto
```

Para presentar al cliente, redondear al alza al siguiente múltiplo de 500 o 1000 (según la moneda).

**Si el cliente pide precio fijo**: el precio fijo se calcula sobre las horas del **escenario pesimista**, no del promedio. La diferencia entre optimista y pesimista es la ganancia si todo va bien.

---

## Estructura de la propuesta económica

Cuando el usuario necesite presentar un presupuesto, generar una propuesta con esta estructura:

```markdown
## Propuesta de Desarrollo — [Nombre del Proyecto]

### Resumen ejecutivo
[2-3 párrafos explicando qué se va a construir y el valor para el cliente]

### Alcance incluido
- [Lista de módulos y funcionalidades que SÍ están incluidas]

### No incluido en este presupuesto
- Mantenimiento post-entrega
- Contenido (textos, imágenes, datos iniciales)
- Diseño UI/UX (si aplica)
- Infraestructura/hosting (si aplica)
- [Cualquier ítem que el cliente podría asumir que está incluido]

### Desglose por módulo
| Módulo | Descripción | Horas estimadas |
|--------|-------------|-----------------|
| Setup e infraestructura | ... | X horas |
| Módulo de auth | ... | X horas |
| [Módulo N] | ... | X horas |
| QA y entrega | ... | X horas |
| **Total** | | **X horas** |

### Precio total
**[Moneda] [Precio]** (precio fijo, pago por hitos)

### Hitos y pagos
| Hito | Entregable | Pago |
|------|-----------|------|
| Inicio | Contrato firmado | 30% |
| Hito 1 | [Módulos X, Y entregados] | 30% |
| Hito 2 | [Módulos Z entregados] | 20% |
| Entrega final | Proyecto en producción | 20% |

### Plazos
- Inicio: [fecha estimada de inicio]
- Entrega estimada: [N semanas desde el inicio]
- Los plazos asumen disponibilidad del cliente para revisiones en < 48 horas

### Cambios de alcance
Cualquier funcionalidad no listada en "Alcance incluido" será cotizada por separado antes de implementarse. El tiempo estimado para cotizar cambios es de 24-48 horas hábiles.

### Validez de la propuesta
Esta propuesta es válida por 30 días desde la fecha de emisión.
```

---

## Gestión de cambios de alcance durante el proyecto

Cuando el cliente pida algo que no estaba en el scope original:

1. **No decir "lo hago"** sin antes revisar el alcance firmado.
2. Identificar si el cambio está dentro del scope acordado o es nuevo.
3. Si es nuevo: estimar las horas adicionales y comunicar el costo antes de implementar.
4. Documentar el cambio por escrito (email / mensaje / orden de cambio).
5. Nunca absorber cambios de scope como "buena voluntad" más de una vez — establece un precedente difícil de revertir.

Texto para comunicar un cambio de alcance al cliente:

> "Este cambio no estaba incluido en el alcance original. Lo implementamos con gusto — el costo adicional sería de [X horas × tarifa = $Y]. ¿Confirmás que procedemos?"

---

## Fase de descubrimiento (cobrable)

Cuando el cliente no tiene el proyecto completamente definido, recomendar una fase de descubrimiento paga antes de dar el presupuesto final:

| Tamaño del proyecto | Duración del descubrimiento | Costo |
|--------------------|----------------------------|-------|
| Pequeño (< 3 meses de desarrollo) | 4-8 horas | Tarifa normal |
| Mediano (3-6 meses) | 8-20 horas | Tarifa normal |
| Grande (6+ meses) | 20-40 horas | Tarifa normal o tarifa reducida |

El entregable del descubrimiento es el equivalente a `readmes/logica.md` + `readmes/tareas.md`: un documento de especificación funcional que define con precisión el scope del proyecto. Este documento se usa como base del contrato.

---

## Alertas que indican un proyecto problemático

Cuando el usuario describa la situación del cliente, alertar si aparece alguno de estos:

- El cliente "ya tiene todo definido" pero no puede explicarlo con claridad.
- El cliente pide precio fijo pero los requisitos cambian en cada reunión.
- El cliente compara el precio con plataformas de freelancers de bajo costo.
- "Es un proyecto sencillo, solo necesito X" — y X implica semanas de trabajo.
- El pago depende del éxito del negocio del cliente ("te pago cuando empiece a vender").
- El cliente quiere empezar sin contrato.
- No hay un interlocutor claro con poder de decisión.

Ante cualquiera de estas señales: o resolver la situación antes de aceptar, o aumentar el buffer de riesgo significativamente.
