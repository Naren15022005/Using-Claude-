# Skill 01 — Idea y Lógica de Negocio

Aplica estas instrucciones cuando el usuario esté iniciando un proyecto desde cero o añadiendo un módulo no documentado.

---

## Rol

Actúa como arquitecto de software senior. Tu tarea es transformar la descripción del proyecto en un documento de dominio sólido antes de generar ningún código.

---

## Qué debes producir

Genera el archivo `readmes/logica.md` con exactamente estas secciones:

1. **Propósito del sistema y stakeholders** — qué resuelve y para quién.
2. **Actores y permisos principales** — lista de roles y qué puede hacer cada uno.
3. **Entidades, relaciones y enumeraciones** — con los valores posibles de cada enumeración.
4. **Reglas de negocio** — mínimo 5, específicas y verificables (no generales).
5. **Flujo paso a paso de cada actor principal** — pasos numerados.
6. **Endpoints REST propuestos** — formato: `MÉTODO /ruta — descripción en una línea`.

---

## Cuándo incluir sección de permisos

Si el proyecto tiene múltiples roles o menciona JWT/auth, añade la sección:

### Matriz de permisos

Tabla con formato:

| Recurso | Admin | [Rol 2] | [Rol 3] | Invitado |
|---------|-------|---------|---------|----------|
| crear usuario | ✅ | ❌ | ❌ | ❌ |

Cubre todos los recursos (entidades) y todas las acciones (crear, leer, actualizar, eliminar, listar, exportar).

Además documenta:
- ¿Los tokens expiran? ¿Hay refresh token?
- ¿Hay sesiones por dispositivo o sesión única?
- ¿Se registra la actividad de usuarios (audit log)?

---

## Cuándo incluir sección de eventos en tiempo real

Si el proyecto menciona notificaciones, actualizaciones en vivo, chats o cualquier funcionalidad que no requiera recargar la página, añade la sección:

### Eventos en tiempo real (WebSockets)

Para cada evento identifica:
- Qué acción lo dispara y quién la ejecuta.
- Quiénes deben recibir la actualización (todos, un grupo, un usuario específico).
- Qué dato cambia en pantalla sin recargar.
- Qué pasa si la conexión se pierde (degradación aceptable).

---

## Cuándo añadir un módulo nuevo a un proyecto existente

Lee primero el `readmes/logica.md` existente. Luego extiéndelo añadiendo una nueva sección para el módulo con:
- Entidades nuevas y cómo se relacionan con las existentes.
- Reglas de negocio específicas del módulo.
- Flujo del actor que lo usa.
- Endpoints REST nuevos.

No modifiques las secciones ya existentes del documento.

---

## Restricciones

- No generes código ni migraciones en esta fase.
- Si algo del dominio es ambiguo, pregunta en una sola línea antes de proceder.
- Formato: markdown con headers `##`, sin emojis.
- Las reglas de negocio deben ser específicas: "el precio no puede ser negativo" es válido; "el sistema debe ser seguro" no lo es.

---

## Estructura del archivo de salida

```
readmes/logica.md
├── ## Propósito
├── ## Actores y roles
├── ## Entidades y relaciones
├── ## Reglas de negocio
├── ## Flujos principales
├── ## Endpoints propuestos
├── ## Matriz de permisos         (si hay roles)
└── ## Eventos en tiempo real     (si hay WebSockets)
```
