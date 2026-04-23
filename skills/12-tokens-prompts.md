# Skill 12 — Eficiencia de Sesión

Aplica estas instrucciones para optimizar el uso de contexto en sesiones largas o cuando el usuario pida hacer una sesión más eficiente.

---

## Contexto compacto de sesión

Cuando el usuario quiera establecer el contexto de un proyecto de forma eficiente, usa esta plantilla base de ~150 tokens:

```
ROL: Desarrollador senior full-stack.
PROYECTO: [nombre]. Stack: [tecnología].
REGLAS:
- Respuestas máx. 100 palabras salvo que se pida detalle
- Sin comentarios en código no modificado
- Sin refactors no pedidos
- Solo los archivos indicados
- Idioma: español
```

Recomienda al usuario guardar esto en `context/[nombre-proyecto].md` y cargarlo al inicio de cada sesión.

---

## Patrones de prompt de alta eficiencia

Cuando el usuario diseñe prompts para tareas recurrentes, recomienda estos patrones:

### ROLE + TASK + FORMAT
```
Rol: [rol específico]
Tarea: [Clarificación en una línea]
Formato: [Estructura de respuesta]
```

### CONTEXTO MÍNIMO VIABLE para bugs
```
Función: [nombre](parámetros)
Bug: [síntoma en una línea]
Fix: [qué debe hacer]
```

### ITERATIVO con aprobación (para tareas grandes)
```
Paso 1: "Propón [estructura/plan/diseño]"
→ [Apruebo / ajusto]
Paso 2: "Genera el boilerplate"
→ [Apruebo]
Paso 3: "Implementa la lógica"
```

---

## Anti-patrones a evitar

Cuando Claude detecte que una sesión está siendo ineficiente, puede señalar el anti-patrón:

| Anti-patrón | Alternativa | Tokens ahorrados aprox. |
|-------------|-------------|------------------------|
| Pegar 500 líneas pidiendo "arréglalo" | Indicar archivo, función y líneas exactas | ~1.500 |
| Re-explicar el proyecto en cada sesión | Usar `context/proyecto.md` al inicio | ~300/sesión |
| Pedir explicación de cada paso | Pedir solo el resultado | ~200 |
| "¿Podés ayudarme con...?" | "Haz X" | ~20 |
| Mega-prompt de una sola vez | Flujo iterativo con aprobación | ~500 |
| Adjuntar el archivo completo | Referenciar path + líneas exactas | ~600 |

---

## Comandos slash rápidos

Para las tareas más frecuentes, usa estas plantillas de una línea:

```
/fix [archivo:línea] — [síntoma]
/refactor [archivo] — [objetivo]
/doc [archivo] — documentar funciones públicas
/test [función] — test unitario con casos edge
/review — bugs y seguridad en cambios de esta sesión
/plan [tarea] — plan antes de implementar
/commit — mensaje de commit semántico
/status — qué se hizo y qué falta en esta sesión
```

---

## Cuándo no usar Claude para una tarea

| Tarea | Herramienta correcta |
|-------|---------------------|
| Buscar texto en el codebase | grep / Ctrl+F / búsqueda del editor |
| Encontrar un archivo por nombre | glob / file explorer |
| Ver el contenido de un archivo | abrirlo directamente |
| Ejecutar comandos y ver output | terminal |
| Buscar en la documentación oficial | docs oficiales + web |

Claude es para razonamiento y generación — no para búsquedas o lecturas simples que el editor hace mejor.

---

## Referencia de consumo de tokens

| Contenido | Tokens aprox. |
|-----------|--------------|
| Prompt directo en una línea | 20-40 |
| Plantilla de solicitud completa | 80-150 |
| Contexto de sesión compacto | ~150 |
| Stack trace típico | 200-400 |
| 100 líneas de código TypeScript | ~800 |
| 100 líneas de PHP | ~700 |
| Archivo grande (300+ líneas) | 2.000+ |

Objetivo: cada interacción bajo 500 tokens cuando sea posible.
