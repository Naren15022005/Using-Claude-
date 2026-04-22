# Using-Claude

Base de conocimiento personal para sacarle el máximo provecho a Claude Code minimizando el consumo de tokens. Cubre skills, agentes, patrones de prompts y flujos de trabajo para desarrollo y tareas cotidianas.

---

## Filosofía central

Claude es un sistema de razonamiento, no un chatbot. El objetivo es delegarle trabajo complejo con contexto preciso.

- **Precisión > verbosidad** — prompts cortos y concretos superan a los largos y vagos
- **Reutilizar contexto** — estructurar sesiones para no repetir información
- **Componer skills** — herramientas especializadas en lugar de un solo prompt que lo hace todo
- **Evitar ruido** — sin confirmaciones innecesarias ni explicaciones de lo obvio

---

## Contenido

| Documento | Qué encontrarás |
|-----------|----------------|
| [iniciandoclaude.md](iniciandoclaude.md) | Guía completa: filosofía, estructura, estrategias de tokens, skills, agentes, workflows y anti-patrones |

### Secciones clave de la guía

- **[Estrategias para ahorrar tokens](iniciandoclaude.md#-estrategias-para-ahorrar-tokens)** — prompts compactos, instrucciones por referencia, batching, respuestas estructuradas
- **[Uso de Skills](iniciandoclaude.md#-uso-de-skills)** — qué skills existen, cuándo y cómo invocarlos
- **[Tipos de agentes](iniciandoclaude.md#-tipos-de-agentes-y-cuándo-usarlos)** — Explore, Task, general-purpose, code-review y cuándo delegar
- **[Patrones de prompts](iniciandoclaude.md#-patrones-de-prompts-de-alto-rendimiento)** — ROLE+TASK+FORMAT, contexto mínimo viable, patrón iterativo
- **[Anti-patrones a evitar](iniciandoclaude.md#-anti-patrones-a-evitar)** — errores comunes que desperdician tokens

---

## Estructura del workspace

```
Using-Claude-/
├── README.md                ← Esta portada
├── iniciandoclaude.md       ← Guía principal
├── prompts/                 ← Plantillas de prompts reutilizables
├── skills/                  ← Definiciones de skills personalizados
├── workflows/               ← Flujos para tareas recurrentes
├── context/                 ← Archivos de contexto persistente por proyecto
└── sessions/                ← Notas y artefactos de sesiones anteriores
```

---

## Quick start

**1. Carga contexto al inicio de cada sesión** en lugar de re-explicar el proyecto:
```
ROL: Eres un desarrollador senior full-stack.
STACK: TypeScript, Node.js, Azure, MongoDB.
REGLAS: Respuestas máx. 100 palabras salvo que pida detalle.
```

**2. Usa comandos directos en una línea** en vez de preguntas abiertas:
```
/fix bug en validateToken — retorna undefined cuando el token expira
/refactor useUserStore para separar lógica de API
```

**3. Referencia archivos, no pegues código:**
```
# ❌  pegar 200 líneas
# ✅  "revisa src/auth/login.ts líneas 45-80 y optimiza el manejo de errores"
```

**4. Agrupa tareas relacionadas en un solo mensaje** para reducir rondas:
```
En un solo paso: (1) añade validación de email, (2) actualiza el test, (3) documenta el cambio en CHANGELOG.md
```

---

*Documento vivo — actualizar conforme evolucionen los flujos de trabajo.*
