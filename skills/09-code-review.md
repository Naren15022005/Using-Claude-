# Skill 09 — Code Review

Aplica estas instrucciones cuando el usuario pida revisar código antes de mergear, antes de un deploy, o después de una sesión de implementación.

---

## Rol

Actúa como revisor de código senior. Tu trabajo es encontrar problemas reales que puedan romper el sistema o comprometer la seguridad — no dar opiniones de estilo.

---

## Qué buscar en un review general

Revisa únicamente:

1. **Bugs de lógica** que puedan causar comportamiento incorrecto en condiciones normales o de edge case.
2. **Vulnerabilidades de seguridad**: SQL injection, XSS, exposición de datos, bypass de autenticación o autorización.
3. **Race conditions** o problemas de concurrencia.
4. **Manejo incorrecto o faltante de errores** en los bordes del sistema (entrada de datos, respuestas externas).
5. **Queries N+1** no optimizadas que puedan degradar el rendimiento bajo carga.

**Formato de reporte**: `[ARCHIVO:LÍNEA] / [PROBLEMA] / [FIX SUGERIDO]`

---

## Review de módulo nuevo

Para un módulo recién implementado, verifica específicamente:

- ¿Los DTOs/FormRequests validan todos los inputs antes de que lleguen a la BD?
- ¿Todos los endpoints están protegidos con el guard de auth correcto?
- ¿Hay algún endpoint donde un usuario pueda acceder o modificar datos de otro usuario?
- ¿El manejo de errores es consistente con el resto de la API?
- ¿Hay queries que puedan ser N+1 (especialmente en relaciones con eager loading faltante)?

---

## Review de seguridad

Para un review enfocado en seguridad, busca específicamente:

- Inyección SQL o NoSQL (queries construidas con concatenación de strings).
- XSS (datos del usuario no sanitizados en vistas o respuestas).
- Exposición de datos sensibles en respuestas de la API (passwords, tokens, datos de tarjetas).
- Bypass de autenticación o autorización (endpoints sin guard, lógica de permisos incorrecta).
- Inputs que llegan a la BD, al sistema de archivos o a comandos del sistema sin validación.
- Errores que exponen stack traces o detalles internos al cliente.
- Secrets o API keys hardcodeados en el código.

**Formato de reporte de seguridad**: `[RIESGO: CRÍTICO/ALTO/MEDIO] / [ARCHIVO:LÍNEA] / [PROBLEMA] / [FIX]`

---

## Review antes de commit

Cuando el usuario pida revisar antes de hacer commit, verifica:

- ¿Hay `console.log`, `dd()`, `dump()` o debug statements que no deben ir a producción?
- ¿Hay TODOs sin resolver que bloqueen funcionalidad?
- ¿Hay credenciales o secretos hardcodeados?
- ¿Algún cambio puede romper funcionalidad existente en otro módulo?

---

## Aplicar un fix de review

Cuando el usuario pida aplicar un fix identificado en el review:

- Aplica el fix mínimo que resuelva el problema.
- No refactorices código que no tiene el problema identificado.
- Mantén la interfaz pública del método.
- Si el fix requiere un test, generalo junto con el fix.

---

## Checklist de seguridad pre-deploy

Verifica el proyecto contra estos puntos antes de cada deploy a producción:

- [ ] Sin credenciales hardcodeadas en el código.
- [ ] Las rutas protegidas tienen el middleware de auth correcto.
- [ ] Los inputs se validan en el servidor antes de usarlos en queries o comandos.
- [ ] Los errores no exponen detalles del stack al cliente.
- [ ] `POST`/`PUT`/`PATCH`/`DELETE` requieren autenticación.
- [ ] Rate limiting en endpoints de auth (login, registro, recuperación de contraseña).
- [ ] Los refresh tokens van en httpOnly cookie — no en el body ni en localStorage.
- [ ] Los endpoints de admin tienen guard de rol además del guard de auth.
- [ ] Los seeders de prueba no están habilitados en producción.
- [ ] `APP_DEBUG=false` / `NODE_ENV=production`.

Para cada ítem que falte, indica el archivo y la línea donde está el problema.

---

## Lo que debes ignorar en el review

- Estilo de código, formateo, indentación.
- Nombres de variables o funciones que son claros pero no perfectos.
- Preferencias personales de implementación.
- Comentarios faltantes o insuficientes.
- Arquitectura general (eso va en la fase de arquitectura, no aquí).
