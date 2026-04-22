# ✅ Skill 08 — Testing y Verificación

> **Fase:** Durante y al finalizar el desarrollo  
> **Objetivo:** Verificar que cada cambio funciona correctamente antes de considerar una tarea terminada.

---

## Cuándo usar este skill

- Después de implementar cualquier módulo o feature.
- Antes de hacer commit de cambios importantes.
- Al corregir un bug (escribir el test que lo reproduce primero).
- En el cierre de proyecto para validación final.

---

## Niveles de verificación

| Nivel | Cuándo | Herramienta |
|-------|--------|-------------|
| Manual | Siempre, después de cada módulo | Navegador / Postman |
| Unitario | Funciones de lógica de negocio | Jest / PHPUnit |
| Integración | Endpoints completos | Supertest / Laravel Feature Tests |
| Aceptación | Flujos completos del usuario | Manual por rol |

---

## Verificación manual (flujo estándar)

Después de implementar cualquier módulo:

```
1. Iniciar sesión con el rol que usa ese módulo
2. Probar CRUD completo:
   - Listar registros (index)
   - Crear nuevo registro (create + store)
   - Ver detalle (show)
   - Editar (edit + update)
   - Eliminar (destroy)
3. Verificar que los permisos funcionan:
   - Con rol que tiene acceso → funciona
   - Con rol sin acceso → redirige o da 403
4. Probar casos edge:
   - Campos vacíos
   - Valores inválidos
   - Registros que no existen (404)
```

---

## Tests de aceptación: cómo definirlos

Antes de implementar un feature, define los criterios de aceptación:

```markdown
Feature: Crear producto
- ✅ Con datos válidos → producto creado, aparece en listado
- ✅ Sin nombre → error de validación "El nombre es requerido"
- ✅ Precio negativo → error de validación "El precio debe ser mayor a 0"
- ✅ Usuario sin rol admin → 403 Forbidden
- ✅ Stock en 0 → producto creado, se muestra como "sin stock"
```

---

## Cómo pedir tests a Claude

### Test unitario (función de lógica de negocio)

```
Genera test unitario para la función calcularDescuento en src/services/pricing.service.ts.
Casos a cubrir:
- Descuento del 10% sobre precio de 100 → 90
- Descuento del 0% → precio sin cambio
- Descuento del 100% → 0
- Precio negativo → lanzar excepción
Usa Jest con TypeScript.
```

### Test de integración (endpoint)

```
Genera test de integración para POST /api/productos.
Casos:
- Con datos válidos → 201 + objeto creado en respuesta
- Sin campo nombre → 400 con mensaje de error
- Sin token de auth → 401
- Con rol no administrador → 403
Usa Supertest + Jest. El endpoint está en src/modules/productos/productos.controller.ts
```

### Test que reproduce un bug

```
Escribe un test que reproduzca el bug:
- Bug: processPayment retorna undefined cuando provider está caído
- Archivo: src/services/payment.service.ts
- El test debe FALLAR antes del fix y PASAR después.
```

---

## Flujo TDD para bugs

```
1. Escribir test que reproduce el bug (falla)
   ↓
2. Verificar que el test falla por la razón correcta
   ↓
3. Aplicar el fix mínimo
   ↓
4. Verificar que el test pasa
   ↓
5. Verificar que los otros tests siguen pasando
```

---

## Comandos de testing por stack

### Node.js / NestJS

```powershell
npm run test                    # todos los tests
npm run test:watch              # modo watch
npm run test:cov                # con cobertura
npm run test -- payment.service # solo un archivo
```

### Laravel

```powershell
php artisan test                           # todos
php artisan test --filter=ProductoTest     # solo un test
php artisan test tests/Feature/ProductoTest.php
./vendor/bin/phpunit --testdox             # output legible
```

---

## Checklist de QA mínima antes de commit

- [ ] El feature/fix funciona manualmente en el navegador o Postman
- [ ] No hay errores en consola (frontend y backend)
- [ ] Los permisos de rol se aplican correctamente
- [ ] Los tests existentes siguen pasando
- [ ] Si se añadió lógica de negocio nueva: hay al menos 1 test unitario
- [ ] Los casos edge más obvios están cubiertos

---

## Verificación final de proyecto

Antes del deploy:

```powershell
# Node.js
npm run test
npm run build          # debe terminar sin errores
npm run lint           # sin errores de lint

# Laravel
php artisan migrate:fresh --seed   # partida limpia sin errores
php artisan test                    # todos los tests en verde
npm run build                       # frontend compilado para producción
```

---

## Reglas al usar este skill

- ✅ Prueba manual después de cada módulo, sin excepción.
- ✅ Los bugs se verifican con tests antes de corregirse.
- ✅ Los criterios de aceptación se definen antes de implementar.
- ❌ No hacer commit de cambios que no hayas verificado manualmente.
- ❌ No omitir la prueba de permisos por rol.

---

## Siguiente paso

→ [`09-code-review.md`](09-code-review.md) — Revisión de código asistida por Claude.
