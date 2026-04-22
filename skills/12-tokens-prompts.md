# ⚡ Skill 12 — Tokens y Optimización de Prompts

> **Fase:** Todo el ciclo de vida  
> **Objetivo:** Maximizar la calidad del output de Claude minimizando el consumo de tokens.

---

## Cuándo usar este skill

- Al diseñar prompts nuevos para tareas recurrentes.
- Cuando las sesiones se están volviendo lentas o costosas.
- Al estandarizar cómo el equipo se comunica con Claude.
- Como referencia rápida antes de escribir un prompt complejo.

---

## Referencia de consumo estimado

| Contenido | Tokens aprox. |
|-----------|--------------|
| Prompt directo de una línea | 20-40 |
| Plantilla de solicitud completa | 80-150 |
| Archivo de contexto compacto | ~150 |
| Stack trace típico | 200-400 |
| 100 líneas de código TypeScript | ~800 |
| 100 líneas de PHP | ~700 |
| Esta guía completa | ~1.200 |
| Archivo grande (300+ líneas) | 2.000+ |

**Objetivo:** mantener cada prompt bajo 500 tokens cuando sea posible.

---

## Los 3 patrones de prompt de alta eficiencia

### Patrón 1 — ROLE + TASK + FORMAT

Para obtener respuestas estructuradas y accionables:

```
Rol: arquitecto de software senior.
Tarea: revisa este diseño de API REST y detecta violaciones de principios REST.
Formato: lista numerada, máx. 5 puntos, cada uno como [PROBLEMA] / [CORRECCIÓN].
```

### Patrón 2 — CONTEXTO MÍNIMO VIABLE

Solo incluir lo que Claude necesita para decidir:

```
Función: calcularDescuento(precio, porcentaje)
Bug: retorna NaN cuando porcentaje es 0
Fix mínimo: solo esa función, en una línea si es posible
```

### Patrón 3 — ITERATIVO con aprobación

En lugar de un mega-prompt, dividir en pasos:

```
Paso 1: "Propón la estructura de carpetas para el módulo de pagos"
→ [Apruebo la estructura]
Paso 2: "Genera el boilerplate de esa estructura"
→ [Apruebo el boilerplate]
Paso 3: "Implementa la lógica de procesamiento de pagos"
```

---

## Estrategias de ahorro de tokens

### 1. Archivo de contexto persistente (cargar al inicio de sesión)

En lugar de re-explicar el proyecto en cada mensaje:

```
ROL: Eres un desarrollador senior full-stack.
PROYECTO: Sistema de gestión [nombre]. Stack: Laravel 11 + Vue 3 + MySQL.
REGLAS:
- Respuestas máx. 100 palabras salvo que pida detalle.
- Sin comentarios en código no modificado.
- Sin refactors no pedidos.
- Idioma: español.
```

Guardar como `context/proyecto-nombre.md` y cargarlo al inicio de cada sesión.

### 2. Referencia por path, no por copia

```
❌ [pegar 200 líneas de código]
✅ "Revisa src/auth/login.ts líneas 45-80 y optimiza el manejo de errores"
```

### 3. Batching de tareas relacionadas

```
En un solo paso:
1. Añade validación de email en src/modules/auth/dto/register.dto.ts
2. Actualiza el test en src/modules/auth/auth.service.spec.ts
3. Documenta el cambio en readmes/flujo_backend.md
```

### 4. Respuestas estructuradas sin relleno

```
Dame solo: [CAUSA] / [FIX] / [ARCHIVOS AFECTADOS]
Sin explicaciones adicionales.
```

### 5. Limitar el alcance explícitamente

```
Solo modifica src/services/payment.service.ts.
No toques tests ni otros archivos en esta iteración.
```

---

## Anti-patrones que desperdician tokens

| ❌ Anti-patrón | ✅ Alternativa | Ahorro aprox. |
|----------------|---------------|---------------|
| Pegar 500 líneas y pedir "arréglalo" | Señalar archivo, función y líneas | -1.500 tokens |
| Re-explicar el proyecto en cada sesión | Usar archivo de contexto | -300 tokens/sesión |
| Pedir explicación de cada paso | Pedir solo el resultado | -200 tokens |
| Preguntas abiertas ("¿qué crees?") | Instrucciones directas ("Haz X") | -100 tokens |
| Mega-prompts de una sola vez | Flujos iterativos con aprobación | -500 tokens |
| "¿Puedes ayudarme con...?" | "Haz X" | -20 tokens |

---

## Comandos slash para tareas frecuentes

Diseñar los prompts más usados como comandos cortos:

```
/fix [archivo:función] — [síntoma en una línea]
/refactor [archivo] — [objetivo del refactor]
/doc [archivo] — JSDoc/PHPDoc para funciones públicas
/test [función] — test unitario con casos edge
/review — revisa cambios de esta sesión (solo bugs reales)
/plan [tarea] — plan antes de implementar
/commit — mensaje de commit semántico para cambios actuales
/update-docs — actualiza el README del módulo activo
```

---

## Cómo estructurar el contexto de una sesión

### Al iniciar una sesión nueva

```
Contexto: estoy trabajando en [proyecto].
Stack: [lista].
Hoy voy a: [objetivo de la sesión].
Archivos relevantes: [lista de paths].
Restricciones: [qué no tocar].
```

### Al continuar una sesión interrumpida

```
Continuamos donde quedamos.
Estado actual: [qué se implementó].
Próxima tarea: [siguiente en la lista].
```

---

## Cuándo no usar Claude (para ahorrar tokens)

| Tarea | Herramienta mejor |
|-------|------------------|
| Buscar texto en el codebase | grep / ripgrep |
| Encontrar archivos por nombre | glob |
| Ver el contenido de un archivo | view (directo) |
| Ejecutar comandos y ver output | terminal directamente |
| Buscar en documentación | docs oficiales / web |

Claude es para **razonamiento y generación**, no para búsquedas simples.

---

## Medición del uso de tokens en una sesión

Estimación por tipo de sesión:

| Tipo de sesión | Tokens esperados |
|----------------|-----------------|
| Fix puntual (1 bug) | 200-500 |
| Feature nuevo (módulo completo) | 2.000-5.000 |
| Refactor de módulo existente | 1.000-3.000 |
| Code review | 500-1.500 |
| Sesión de planificación | 500-1.000 |
| Setup inicial de proyecto | 3.000-8.000 |

Si una sesión supera lo esperado, revisar si se están aplicando los anti-patrones de la tabla anterior.

---

## Reglas al usar este skill

- ✅ Cargar el archivo de contexto al inicio de cada sesión.
- ✅ Prompts directos: "Haz X", no "¿podrías hacer X?"
- ✅ Batching: agrupar tareas relacionadas en un solo mensaje.
- ❌ No pegar código que Claude no necesita leer.
- ❌ No pedir explicaciones si solo necesitas el resultado.
- ❌ No usar Claude para búsquedas de texto en el codebase.
