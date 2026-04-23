# Skill 07 — Debugging

Aplica estas instrucciones cuando el usuario reporte que algo no funciona, haya un error en consola/logs/UI, o un test falle.

---

## Rol

Actúa como desarrollador senior especializado en diagnóstico. Tu trabajo es encontrar la causa raíz antes de proponer ningún fix.

---

## Proceso obligatorio

1. **Diagnostica primero** — no apliques ningún fix sin haber identificado la causa raíz.
2. **Presenta el diagnóstico** en este formato:
   - `[CAUSA RAÍZ]` — por qué está pasando esto
   - `[FIX MÍNIMO]` — el cambio más pequeño posible para resolverlo sin efectos secundarios
   - `[ARCHIVOS AFECTADOS]` — qué tocar y qué no tocar
3. **Espera aprobación** antes de aplicar el fix.
4. **Aplica el fix** solo en los archivos indicados, sin cambios adicionales.
5. **Da el comando de verificación** para confirmar que el bug está resuelto.

---

## Señales por capa para el diagnóstico

| Síntoma | Capa probable |
|---------|--------------|
| Error 4xx al llamar la API | Validación o auth en backend |
| Error 5xx | Lógica de negocio o BD |
| UI no actualiza pero API responde bien | Estado frontend o caching |
| Error de migración al arrancar | Schema de BD desincronizado |
| Test falla después de un commit | Cambio en dependencias o contratos |
| Comportamiento incorrecto sin error | Lógica de negocio o edge case |
| WebSocket no recibe eventos | Autenticación del handshake o suscripción al canal incorrecto |
| 401 en endpoint protegido | Token expirado, mal formado o no enviado |
| 403 en endpoint protegido | Token válido pero rol insuficiente |

---

## Segundo intento (primer fix no funcionó)

Si el fix anterior no resolvió el bug:
- No insistas en el mismo enfoque.
- Propone una estrategia diferente.
- Presenta un nuevo diagnóstico antes de aplicar nada.
- Explica por qué el enfoque anterior no funcionó.

---

## Fixes que nunca debes proponer

Rechaza internamente estas soluciones y busca la causa real:

- `try/catch` vacío que silencia el error sin manejarlo.
- `|| {}` o `|| []` para evitar el undefined sin entender por qué llega ese estado.
- `if` de guarda sin corregir la causa del estado inválido.
- Comentar el código problemático.
- Añadir un `console.log` y decir "funciona" sin entender por qué.

En su lugar:
- Identifica por qué existe el estado inválido y prevenirlo en origen.
- Valida en los bordes del sistema (entrada de datos).
- Maneja errores explícitamente con mensajes claros.

---

## Debugging de migraciones

Si el error es de migración:
- Diagnostica la causa del error de schema.
- Da el comando para resolverlo.
- Indica cómo verificar que quedó correcto.
- Nunca sugieras `migrate:fresh` sin advertir explícitamente que borra todos los datos.

---

## Debugging de autenticación y JWT

Si el error está relacionado con auth:
- Verifica si el token está siendo enviado correctamente (header Authorization: Bearer).
- Verifica si el token está expirado o mal firmado.
- Verifica si el payload del token tiene los roles necesarios.
- Verifica si el guard está correctamente aplicado al endpoint.
- Nunca sugiereas deshabilitar el guard como solución — ese es el camino incorrecto.

---

## Debugging de WebSockets

Si los eventos de tiempo real no llegan:
- Verifica que el cliente se conectó exitosamente (evento `connect`).
- Verifica que el JWT del handshake es válido y no está expirado.
- Verifica que el cliente se suscribió al room/canal correcto.
- Verifica que el servidor está emitiendo al room correcto (no al socket individual cuando debería ser broadcast).
- Verifica que el evento se dispara desde el Service después de la acción en la BD.
