# 🗣️ Skill 06 — Comunicación con el Agente

> **Fase:** Todo el ciclo de vida  
> **Objetivo:** Pedir trabajo a Claude de forma eficiente: clara, concisa y sin desperdiciar tokens.

---

## Principios de comunicación

| Principio | Descripción |
|-----------|------------|
| **Directo** | No "¿puedes ayudarme con X?" → "Haz X" |
| **Específico** | Indicar archivo, función, línea, comportamiento esperado |
| **Contexto mínimo** | Solo lo que Claude necesita para decidir, nada más |
| **Idioma** | Siempre en español |
| **Sin rodeos** | Sin introducciones ni agradecimientos — ir al punto |
| **Plan antes de ejecutar** | Para cambios grandes: ver el plan primero, aprobar, luego implementar |

---

## Plantilla de solicitud estándar

```
Objetivo: [qué quiero lograr en una frase]
Archivos: [lista de paths exactos]
Comportamiento esperado: [cómo debe funcionar cuando termine]
Restricciones: [qué no tocar, qué versiones respetar]
```

**Ejemplo:**
```
Objetivo: Corregir validación de email en el formulario de registro
Archivos: src/modules/auth/dto/register.dto.ts, src/modules/auth/auth.service.ts
Comportamiento esperado: rechazar emails sin dominio válido con error 400
Restricciones: no cambiar la estructura del DTO, mantener los tests existentes
```

---

## Tipos de solicitud y cómo hacerlas

### Fix puntual (bug conocido)
```
Fix en [archivo, línea/función]: [descripción del bug].
Síntoma: [qué pasa].
Esperado: [qué debería pasar].
```

### Feature nuevo (módulo o funcionalidad)
```
Implementa [nombre del feature].
Stack: [tecnología].
Entidad: [campos].
Reglas de negocio: [lista].
Acceso: [rol/permisos].
Usa los patrones de [módulo de referencia].
```

### Refactor
```
Refactoriza [archivo o función].
Problema actual: [descripción].
Objetivo: [qué debe mejorar].
No cambiar: [qué debe quedar igual].
```

### Documentación
```
Genera/actualiza [readmes/flujo_backend.md] con:
- Qué se implementó en esta sesión
- Qué falta pendiente
- Comandos útiles actualizados
```

### Consulta técnica
```
¿Cuál es la mejor estrategia para [problema]?
Contexto: [stack, restricciones, volumen].
Dame: 2-3 opciones con pros/contras y tu recomendación.
```

---

## Comandos slash (para tareas comunes)

```
/fix [archivo:línea] — [descripción del bug]
/refactor [archivo] — [qué mejorar]
/doc [archivo] — genera JSDoc/PHPDoc para funciones públicas
/test [función] — genera test unitario
/review — revisa los cambios de esta sesión
/plan — genera plan antes de implementar
/commit — genera mensaje de commit semántico para los cambios actuales
```

---

## Cuándo pedir plan antes de implementar

Pide siempre el plan primero cuando:

- La tarea afecta más de 3 archivos.
- Hay cambios en la base de datos (nuevas migraciones).
- Se cambia la arquitectura de un módulo existente.
- No tienes certeza de qué archivos están involucrados.

```
Antes de implementar, dame el plan:
- Lista de archivos a crear/modificar
- Orden de los cambios
- Riesgos o dependencias a considerar
Cuando apruebe, procede.
```

---

## Dar contexto eficiente

### ✅ Correcto — referencia por path y líneas
```
Revisa src/services/payment.service.ts líneas 45-80.
El método processPayment falla cuando el proveedor retorna error 503.
```

### ❌ Incorrecto — pegar código completo
```
[pegar 300 líneas de código]
Arréglalo.
```

### ✅ Adjuntar solo el fragmento relevante
```
Función afectada:
async processPayment(orderId: string) {
  const result = await provider.charge(...)  // falla aquí con 503
  return result;
}
```

---

## Iteración cuando algo no funciona

```
El fix anterior no resolvió el problema.
Nuevo contexto: [error actualizado / comportamiento observado]
Stack trace: [solo las líneas relevantes]
¿Qué cambio de estrategia propones?
```

**Regla:** Si Claude intenta el mismo enfoque dos veces sin resultado, pedir explícitamente un replanteo de estrategia.

---

## Aprobación antes de ejecutar

Para planes grandes o cambios estructurales:

```
1. "Dame el plan detallado para [tarea]"
   → Claude presenta lista de pasos
2. "Aprobado. Procede con el paso 1."
   → Claude implementa
3. "Aprobado. Continúa."
   → Claude sigue
```

No dar aprobación global de todo el plan de una vez si implica cambios en múltiples capas.

---

## Formato de respuesta esperado

Si necesitas una respuesta estructurada:
```
Dame el resultado como: [CAUSA] / [SOLUCIÓN] / [ARCHIVOS AFECTADOS]
```

Si solo necesitas el cambio:
```
Solo el código modificado, sin explicaciones.
```

Si quieres verificar:
```
Al terminar, dame los comandos para verificar que funciona correctamente.
```

---

## Reglas al usar este skill

- ✅ Instrucciones directas: "Haz X" no "¿podrías hacer X?"
- ✅ Siempre incluir el path exacto del archivo.
- ✅ Pedir confirmación antes de cambios destructivos.
- ❌ No pegar código que Claude no necesita leer.
- ❌ No pedir explicaciones de cada paso si solo necesitas el resultado.
- ❌ No hacer preguntas abiertas del tipo "¿qué crees que debería hacer?"

---

## Referencia rápida: estimación de tokens

| Contenido | Tokens aprox. |
|-----------|--------------|
| Prompt de una línea | 20-40 |
| Plantilla de solicitud completa | 80-150 |
| Archivo de contexto compacto | ~150 |
| Stack trace típico | 200-400 |
| 100 líneas de código | ~800 |

**Objetivo:** cada prompt bajo 500 tokens siempre que sea posible.
