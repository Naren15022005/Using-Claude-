# 🔍 Skill 09 — Code Review con Claude

> **Fase:** Antes de mergear o desplegar  
> **Objetivo:** Detectar bugs reales, problemas de seguridad y errores de lógica antes de que lleguen a producción.

---

## Cuándo usar este skill

- Antes de hacer merge de una rama de feature.
- Antes de hacer deploy.
- Al revisar código de un colaborador.
- Después de una sesión larga de implementación para detectar errores introducidos.

---

## Qué busca el code review

| ✅ Revisar | ❌ No es scope del review |
|-----------|--------------------------|
| Bugs de lógica | Estilo de código (indentación, nombres) |
| Vulnerabilidades de seguridad | Formateo y espacios |
| Race conditions / concurrencia | Preferencias personales |
| Manejo incorrecto de errores | Si se podría "hacer de otra forma" |
| Datos sensibles expuestos | Comentarios en el código |
| Queries N+1 | Nombres de variables |
| Validaciones faltantes en bordes del sistema | |

---

## Prompt de code review básico

```
Revisa los cambios en [archivo o rama]:
Solo reporta:
1. Bugs de lógica que puedan causar comportamiento incorrecto
2. Vulnerabilidades de seguridad (SQL injection, XSS, exposición de datos, etc.)
3. Race conditions o problemas de concurrencia
4. Manejo incorrecto o faltante de errores

Para cada issue: [ARCHIVO:LÍNEA] / [PROBLEMA] / [FIX SUGERIDO]
Ignora estilo, formateo y preferencias.
```

---

## Tipos de review por contexto

### Review de un módulo nuevo

```
Revisa el módulo recién implementado en src/modules/productos/:
- ¿Hay validaciones faltantes en los DTOs?
- ¿Los endpoints están protegidos con el middleware de auth correcto?
- ¿Hay algún caso donde un usuario pueda acceder a datos de otro?
- ¿El manejo de errores es consistente con el resto de la API?
Solo issues reales, no sugerencias de mejora.
```

### Review de seguridad

```
Haz un review de seguridad de [archivo]:
- Busca: inyección SQL, XSS, exposición de datos sensibles, bypass de autenticación
- Verifica: que los inputs se validan antes de llegar a la base de datos
- Verifica: que los errores no exponen stack traces ni detalles internos al cliente
```

### Review de rendimiento

```
Revisa [archivo] en busca de:
- Queries N+1 (Eloquent: eager loading faltante, Prisma: include faltante)
- Operaciones costosas dentro de loops
- Requests a servicios externos dentro de transacciones de DB
```

### Review de cambios antes de commit

```
Revisa los cambios de esta sesión antes de hacer commit:
- ¿Hay debug logs o console.log que no deberían estar?
- ¿Se introdujo algún TODO sin resolver?
- ¿Hay credenciales o secretos hardcodeados?
- ¿Algún cambio puede romper funcionalidad existente?
```

---

## Checklist de seguridad

Antes de cualquier deploy, verificar:

- [ ] No hay credenciales hardcodeadas en el código
- [ ] Las rutas protegidas tienen middleware de auth
- [ ] Los inputs de usuario se validan antes de usarlos en queries
- [ ] Los errores no exponen detalles del stack al cliente
- [ ] Los endpoints que mutan datos (POST/PUT/PATCH/DELETE) requieren autenticación
- [ ] HMAC o firma verificada en webhooks externos
- [ ] Rate limiting en endpoints de auth (login, registro)

---

## Cómo reportar y resolver un issue de review

```
Issue encontrado en code review:
Archivo: src/modules/auth/auth.service.ts, línea 89
Problema: el error de login expone si el email existe o no en el sistema
Riesgo: permite enumerar usuarios registrados
Fix: retornar siempre el mismo mensaje genérico independientemente de si el email existe
Aplica el fix.
```

---

## Review con el agente code-review

Para sesiones largas o ramas con muchos cambios, usar el agente especializado:

```
Inicia un code review de la rama feature/checkout-module.
Enfócate en:
- Lógica de negocio del proceso de checkout
- Manejo de errores del procesador de pagos
- Concurrencia al actualizar stock
Solo bugs y riesgos reales.
```

---

## Reglas al usar este skill

- ✅ El review es el último paso antes del deploy.
- ✅ Cada issue reportado tiene archivo, línea, problema y fix sugerido.
- ✅ Los issues de seguridad se resuelven antes de mergear.
- ❌ No bloquear el merge por estilo o preferencias personales.
- ❌ No hacer review de archivos que no cambiaron en el PR.

---

## Siguiente paso

→ [`10-deploy-entrega.md`](10-deploy-entrega.md) — Checklist de cierre y deploy a producción.
