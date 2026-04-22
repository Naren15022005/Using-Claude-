# 🧠 Iniciando con Claude — Guía de uso inteligente

> Contexto principal: sacarle el máximo provecho a Claude minimizando el consumo de tokens, usando skills, agentes y estructuras de prompts eficientes.

---

## 📌 Filosofía central

Claude no es solo un chatbot — es un **sistema de razonamiento** que puede actuar como desarrollador, arquitecto, investigador y gestor de proyectos. El objetivo es **delegarle trabajo complejo** con contexto preciso, no hacerle preguntas simples que consumen tokens innecesariamente.

**Principios:**
- 🎯 **Precisión sobre verbosidad** — prompts cortos y concretos superan a los largos y vagos
- 🔁 **Reutilización de contexto** — estructurar sesiones para no repetir información
- 🧩 **Composición de skills** — combinar herramientas especializadas en lugar de pedirle todo a un solo prompt
- 🚫 **Evitar el ruido** — no pedir confirmaciones innecesarias ni explicaciones de lo obvio

---

## 🗂️ Estructura del workspace

```
Using-Claude-/
├── iniciandoclaude.md       ← Esta guía
├── README.md                ← Descripción general del proyecto
├── prompts/                 ← Plantillas de prompts reutilizables
├── skills/                  ← Definiciones de skills personalizados
├── workflows/               ← Flujos de trabajo para tareas recurrentes
├── context/                 ← Archivos de contexto persistente por proyecto
└── sessions/                ← Notas y artefactos de sesiones anteriores
```

---

## ⚡ Estrategias para ahorrar tokens

### 1. Prompts de sistema compactos
En lugar de explicar el contexto en cada mensaje, usa un **archivo de contexto** que se carga al inicio de la sesión:
```
ROL: Eres un desarrollador senior full-stack.
STACK: TypeScript, Node.js, Azure, MongoDB.
REGLAS: Respuestas máx. 100 palabras salvo que pida detalle. Sin comentarios obvios.
```

### 2. Instrucciones por referencia, no por copia
En vez de pegar código completo, referencia archivos:
```
// ❌ Malo — pegar 200 líneas de código
// ✅ Bueno — "revisa src/auth/login.ts líneas 45-80 y optimiza el manejo de errores"
```

### 3. Comandos en una línea (slash-style)
Diseña prompts como comandos:
```
/fix bug en función validateToken — retorna undefined cuando el token expira
/refactor useUserStore para separar lógica de API
/doc genera JSDoc para todas las funciones públicas de utils/date.ts
```

### 4. Respuestas estructuradas
Pide siempre formato definido para evitar explicaciones redundantes:
```
Dame el resultado como: [PROBLEMA] / [CAUSA] / [SOLUCIÓN]
```

### 5. Batching de tareas
Agrupa tareas relacionadas en un solo mensaje:
```
En un solo paso: (1) añade validación de email, (2) actualiza el test correspondiente, 
(3) documenta el cambio en CHANGELOG.md
```

---

## 🛠️ Uso de Skills

Los skills son agentes especializados que Claude puede invocar automáticamente. Cada skill tiene un dominio específico y evita que tengas que explicar el contexto desde cero.

### Skills disponibles en este workspace

| Skill | Cuándo usarlo |
|-------|--------------|
| `typescript-setup` | Iniciar proyectos TypeScript desde cero |
| `agent-customization` | Crear/editar instructions, prompts y agentes personalizados |
| `troubleshoot` | Investigar comportamiento inesperado de Claude o herramientas |
| `mongodb-connection` | Configurar conexiones y pools en MongoDB |
| `mongodb-schema-design` | Diseñar esquemas, patrones embed/reference |
| `mongodb-natural-language-querying` | Generar queries MongoDB con lenguaje natural |
| `mongodb-query-optimizer` | Optimizar queries lentos e índices |
| `mongodb-search-and-ai` | Atlas Search, Vector Search, búsqueda semántica |

### Cómo invocar un skill eficientemente
No es necesario nombrarlo explícitamente — Claude lo detecta por contexto. Pero si quieres forzarlo:
```
[usa el skill mongodb-schema-design]
Necesito modelar una relación entre usuarios y pedidos con historial de estados.
```

---

## 🤖 Tipos de agentes y cuándo usarlos

| Agente | Uso ideal |
|--------|-----------|
| `explore` | Investigar múltiples partes del codebase en paralelo |
| `task` | Ejecutar builds, tests, lints — solo necesito saber si pasó o falló |
| `general-purpose` | Tareas complejas de múltiples pasos con alta calidad de razonamiento |
| `code-review` | Revisar cambios — solo reporta bugs reales, ignora estilo |

**Regla de oro:** usa agentes cuando la tarea se puede delegar completamente. No los uses para búsquedas simples que puedes hacer tú mismo con grep/glob.

---

## 📋 Flujos de trabajo recomendados

### Flujo: Iniciar un nuevo feature
```
1. /context → carga el archivo de contexto del proyecto
2. /plan → Claude genera un plan estructurado antes de codificar
3. /implement → implementa siguiendo el plan
4. /review → code-review agent revisa los cambios
5. /commit → commit con mensaje semántico
```

### Flujo: Debug de un bug
```
1. Describe el síntoma + adjunta stack trace (no el código completo)
2. Pide: [DIAGNÓSTICO] / [HIPÓTESIS] / [FIX MÍNIMO]
3. Valida el fix antes de aplicar
```

### Flujo: Refactor de módulo
```
1. "Analiza src/X.ts y lista los problemas sin corregirlos aún"
2. Aprueba la lista
3. "Ahora aplica los fixes en orden de impacto"
```

---

## 🧩 Patrones de prompts de alto rendimiento

### El patrón ROLE + TASK + FORMAT
```
Actúa como arquitecto de software.
Tarea: revisa este diseño de API REST y detecta violaciones de REST principles.
Formato: lista numerada, máx. 5 puntos, cada uno con [PROBLEMA] y [CORRECCIÓN].
```

### El patrón CONTEXTO MÍNIMO VIABLE
Solo incluye lo que Claude necesita para decidir — nada más:
```
Función: calcularDescuento(precio, porcentaje)
Problema: retorna NaN cuando porcentaje es 0
Fix: en una línea
```

### El patrón ITERATIVO
En lugar de un mega-prompt, divide en pasos con aprobación:
```
Paso 1: "Propón la estructura de carpetas para este microservicio"
→ Apruebo
Paso 2: "Genera el boilerplate para esa estructura"
→ Apruebo
Paso 3: "Añade la lógica de autenticación"
```

---

## 🚫 Anti-patrones a evitar

| ❌ Anti-patrón | ✅ Alternativa |
|----------------|---------------|
| Pegar 500 líneas de código y pedir "arréglalo" | Señalar el archivo, función y líneas exactas |
| Pedir explicación de cada paso | Pedir solo el resultado final |
| Re-explicar el proyecto en cada sesión | Usar un archivo de contexto persistente |
| Usar Claude para búsquedas simples de texto | Usar grep/glob directamente |
| Mega-prompts de una sola vez | Flujos iterativos con aprobación |
| "¿Puedes ayudarme con X?" | "Haz X" — instrucciones directas |

---

## 📏 Referencia rápida: estimación de tokens

| Contenido | Tokens aprox. |
|-----------|--------------|
| Esta guía completa | ~1.200 |
| 100 líneas de código TypeScript | ~800 |
| Un archivo de contexto compacto | ~150 |
| Un prompt de comando en una línea | ~20-40 |
| Stack trace típico | ~200-400 |

**Objetivo:** mantener cada prompt bajo los 500 tokens siempre que sea posible.

---

## 🔗 Recursos relacionados

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Claude Model Context Window](https://docs.anthropic.com/en/docs/about-claude/models/overview)
- `README.md` — descripción general de este workspace

---

*Este documento es un artefacto vivo — actualízalo conforme evolucionen tus flujos de trabajo con Claude.*

---

## 📚 READMEs recomendados por uso de Claude (por contexto)

Para mejorar la experiencia con Claude Code y otros modos de uso, mantener varios README específicos ayuda a estandarizar prompts, reducir tokens y acelerar flujos. Crea estos archivos en la raíz o en carpetas relacionadas.

- README-claude-code.md — Uso intensivo de Claude para generación y refactor de código
  - Contenido: plantillas de comandos slash, ejemplos de prompts para refactor, políticas de chunking (cómo dividir archivos grandes), checklist de QA mínima, snippets de tests.
  - Cuando usar: workflows de pair-programming y generación de código.

- README-claude-cowork.md — Coworking con colaboradores (comentarios, revisiones, sesiones)
  - Contenido: protocolo de sesiones (roles, normas de comunicación), cómo compartir contexto (archivos a cargar), formato de entregables y seguimiento de decisiones.
  - Cuando usar: sesiones en vivo o asincrónicas con otros humanos y Claude.

- README-prompts.md — Biblioteca de prompts y plantillas reutilizables
  - Contenido: ROLE+TASK+FORMAT, prompts para debugging, prompts para documentación, prompts compactos para ahorrar tokens.
  - Cuando usar: al redactar prompts nuevos o estandarizar equipo.

- README-skills-and-agents.md — Guía de skills disponibles y patrones de invocación
  - Contenido: listado de skills, ejemplo de triggers, policy para elegir agente (explore/task/general-purpose), anti-patrones al invocar agents.
  - Cuando usar: decidir delegación a agentes o diseñar nuevos skills.

- README-token-management.md — Estrategias y métricas para minimizar tokens
  - Contenido: límites recomendados por prompt, ejemplos de chunking, cómo resumir contexto, herramientas para medir consumo aproximado.
  - Cuando usar: optimización de costes y context window planning.

- README-examples.md — Ejemplos completos: before/after (fixes, refactors, tests)
  - Contenido: casos reales reducidos con prompts, outputs esperados, tests asociados.
  - Cuando usar: aprendizaje y onboarding, referencia rápida.

- README-context-persistence.md — Cómo organizar y versionar archivos de contexto
  - Contenido: normas para context/*, cuándo regenerar contexto, obsolescencia y TTL de contexto.
  - Cuando usar: mantener contexto actualizado sin duplicar tokens.

- README-security-privacy.md — Manejo de datos sensibles y políticas de privacidad
  - Contenido: qué no enviar a Claude, redacción de redacted snippets, reglas para compartir secretos y archivos con terceros.
  - Cuando usar: cualquier intercambio de logs, trazas, o datos de usuarios.

- README-automation.md — Scripts y workflows automáticos (CI / hooks) para usar Claude
  - Contenido: ejemplos de hooks pre-commit que generan PR descriptions, CI jobs que ejecutan agents para generar changelogs, plantillas de commit.
  - Cuando usar: integración de Claude en pipelines de desarrollo.

- README-contrib.md — Cómo contribuir a los prompts, skills y workflows del workspace
  - Contenido: convenciones de naming, formato de PR para nuevos prompts/skills, revisión y testing mínimo.
  - Cuando usar: abrir o revisar contribuciones del equipo.


### Sugerencia de implementación rápida
1. Crear una plantilla mínima para cada README con secciones: Propósito / Cuándo usar / Ejemplos / Plantillas / Buenas prácticas.
2. Añadir cross-links en iniciandoclaude.md a los READMEs relevantes.
3. Versionar los READMEs y actualizar según feedback de sesiones.

---

*Este documento es un artefacto vivo — actualízalo conforme evolucionen tus flujos de trabajo con Claude.*
