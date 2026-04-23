# Skill 06 — Reglas de Sesión

Estas son las reglas de comportamiento que Claude debe seguir en toda sesión de trabajo con el usuario. Aplícalas desde el inicio de cada sesión.

---

## Comportamiento base de sesión

- Idioma: español siempre, sin excepciones.
- Respuestas: concisas, máximo 100 palabras salvo que el usuario pida detalle explícitamente.
- Código: sin comentarios en líneas no modificadas, sin refactors que no hayan sido pedidos.
- Cambios: solo los archivos que el usuario indique — nunca modificar archivos adicionales "de paso".
- Ambigüedades: preguntar en una sola línea antes de proceder.
- Planes: antes de implementar algo que afecte más de 3 archivos o que cambie la BD, presentar el plan y esperar aprobación explícita.

---

## Comandos slash reconocidos

Cuando el usuario use estos comandos, responde exactamente como se indica:

| Comando | Qué hace Claude |
|---------|-----------------|
| `/fix [archivo:función] — [síntoma]` | Diagnostica causa raíz y propone fix mínimo antes de aplicar |
| `/feature [nombre] — [descripción]` | Presenta plan de implementación y espera aprobación |
| `/refactor [archivo] — [objetivo]` | Solo si el usuario lo pide explícitamente, con alcance limitado |
| `/test [función]` | Genera test unitario con casos normales + casos edge |
| `/review` | Revisa cambios de la sesión buscando bugs reales y vulnerabilidades — ignora estilo |
| `/plan [tarea]` | Genera el plan antes de implementar: archivos, orden, riesgos |
| `/commit` | Genera mensaje de commit semántico para los cambios actuales |
| `/doc` | Actualiza los readmes con lo implementado en la sesión |
| `/status` | Resumen de qué se hizo y qué falta en la sesión actual |

---

## Plantillas de solicitud a interpretar

Cuando el usuario envíe solicitudes en estos formatos, extrae la información correctamente:

### Fix de bug
```
/fix [archivo:línea o función]
Síntoma: [qué pasa]
Esperado: [qué debería pasar]
Error exacto: [líneas relevantes del stack trace]
```
→ Primero diagnostica, luego propone el fix, luego espera aprobación antes de aplicar.

### Feature nuevo
```
/feature [nombre]
Entidad: [campos principales]
Reglas: [lista]
Acceso: [rol]
Patrón de referencia: [módulo existente]
```
→ Genera el plan completo y espera aprobación antes de escribir código.

### Consulta técnica (sin implementar)
```
¿Cuál es la mejor estrategia para [problema]?
Contexto: [stack, restricciones]
```
→ Da 2-3 opciones con pros/contras + recomendación. Sin código hasta que el usuario lo pida.

---

## Continuar una sesión interrumpida

Cuando el usuario retome una sesión, pide o infiere:
- Qué se implementó en la sesión anterior.
- Qué archivos fueron modificados.
- Cuál es la siguiente tarea en `readmes/tareas.md`.

Retoma desde donde quedó sin pedir al usuario que re-explique el contexto del proyecto.

---

## Cuándo pedir plan antes de implementar

Siempre presenta el plan y espera aprobación cuando:
- La tarea afecta más de 3 archivos.
- La tarea requiere una nueva migración de base de datos.
- La tarea cambia la API pública de un módulo ya existente.
- La tarea puede romper funcionalidad existente.

Formato del plan:
```
Archivos a crear/modificar:
1. [archivo] — [qué cambio]
2. [archivo] — [qué cambio]

Orden de ejecución y por qué.
Riesgos o dependencias a considerar.
```
