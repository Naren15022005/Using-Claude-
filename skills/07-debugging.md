# 🐛 Skill 07 — Debugging y Resolución de Problemas

> **Fase:** Durante el desarrollo  
> **Objetivo:** Diagnosticar y resolver bugs de forma sistemática, atacando siempre la causa raíz.

---

## Cuándo usar este skill

- Cuando algo no funciona como se esperaba.
- Cuando hay un error en consola, en logs o en la UI.
- Cuando un test falla sin razón aparente.
- Cuando el comportamiento del sistema cambió después de un commit.

---

## Flujo de debugging

```
1. REPRODUCIR → confirmar que el bug existe y es consistente
       ↓
2. DESCRIBIR → síntoma exacto + contexto + error exacto
       ↓
3. AISLAR → identificar la capa, archivo o función responsable
       ↓
4. DIAGNOSTICAR → Claude lee el código y propone causa raíz
       ↓
5. APLICAR FIX → cambio mínimo sobre los archivos afectados
       ↓
6. VERIFICAR → confirmar que el fix resuelve sin efectos secundarios
       ↓
7. ITERAR si no resuelve → más contexto, nuevo enfoque
```

---

## Cómo reportar un bug a Claude

### Plantilla de reporte

```
Bug: [descripción de una línea]
Contexto: qué hice antes de que apareciera el error
Esperado: qué debería pasar
Observado: qué pasa en realidad
Error exacto: [pegar solo las líneas relevantes del stack trace]
Archivo/función: [path exacto donde crees que está el problema]
```

### Ejemplo concreto

```
Bug: la función de pago retorna undefined cuando el proveedor está caído
Contexto: ejecuto POST /api/checkout con datos válidos
Esperado: respuesta 503 con mensaje "servicio no disponible"
Observado: respuesta 500 y error "Cannot read properties of undefined"
Error: TypeError: Cannot read properties of undefined (reading 'status')
       at PaymentService.processPayment (payment.service.ts:67)
Archivo: src/services/payment.service.ts, línea 67
```

---

## Qué adjuntar al reporte

| Incluir | No incluir |
|---------|-----------|
| Stack trace (solo líneas relevantes) | Stack trace completo de 200 líneas |
| El fragmento de función afectada | El archivo entero |
| Código de respuesta HTTP | Todos los headers de la request |
| Variables de entorno relevantes (sin secretos) | Todo el .env |

---

## Señales para identificar la capa del problema

| Síntoma | Capa probable |
|---------|--------------|
| Error 4xx al llamar la API | Validación o autenticación en backend |
| Error 5xx | Lógica de negocio o DB |
| UI no actualiza pero API responde bien | Estado frontend o caching |
| Error de migración al arrancar | Schema de DB desincronizado |
| Test falla después de un commit | Cambio en dependencias o contratos de función |
| Comportamiento incorrecto sin error visible | Lógica de negocio o condición edge case |

---

## Resolución con Claude

### Diagnóstico (leer antes de modificar)

```
Lee src/services/payment.service.ts y diagnostica:
- Causa raíz del error en línea 67
- Por qué falla cuando el proveedor retorna undefined
- Propón el fix mínimo sin cambiar la interfaz pública del método
```

### Aplicar fix

```
Aplica el fix en src/services/payment.service.ts:
- Manejar el caso en que provider.charge() retorna undefined o lanza excepción
- Retornar error estructurado en lugar de propagar la excepción cruda
No cambiar la firma del método ni los DTOs.
```

### Verificar

```
Dame los comandos para verificar que el fix funciona:
- Test unitario que cubra el escenario del bug
- Curl/comando de prueba manual
```

---

## Cuando el primer fix no funciona

```
El fix anterior no resolvió el bug.
Nuevo contexto: [descripción actualizada]
Nuevo error: [error actualizado]
¿Qué cambió y qué no cambió?
Propón una estrategia diferente — no insistir en el mismo enfoque.
```

**Regla:** Si después de dos intentos con el mismo enfoque no se resuelve, pedir un paso atrás y replantear la estrategia completa.

---

## Fixes que no se aceptan

- ❌ Silenciar el error con `try/catch` vacío.
- ❌ Poner `|| {}` o `|| []` para evitar el undefined sin entender por qué llega undefined.
- ❌ Añadir un `if` de guarda sin corregir la causa que genera el estado inválido.
- ❌ Comentar el código problemático.

**Lo que sí se acepta:**
- ✅ Identificar por qué el estado inválido existe y prevenirlo en origen.
- ✅ Validar en los bordes del sistema (entrada de datos) para que el estado inválido nunca llegue a la lógica interna.
- ✅ Manejar explícitamente los casos de error con mensajes claros.

---

## Debugging de migraciones (Laravel / Prisma)

### Laravel

```powershell
php artisan migrate:status          # Ver estado de migraciones
php artisan migrate --pretend       # Simular sin ejecutar
php artisan migrate:fresh --seed    # Reset completo (solo local)
```

### Prisma

```powershell
npx prisma migrate status           # Ver estado
npx prisma db push                  # Aplicar sin crear migration (solo dev)
npx prisma studio                   # GUI para inspeccionar datos
```

---

## Debugging de autenticación / permisos

Checklist cuando aparece 401 o el usuario no puede acceder a algo que debería:

- [ ] El token se está enviando en el header `Authorization: Bearer <token>`
- [ ] El token no ha expirado
- [ ] El rol del usuario está asignado correctamente en la BD
- [ ] El middleware del endpoint está configurado para el rol correcto
- [ ] El seed creó el usuario con el rol correcto

---

## Reglas al usar este skill

- ✅ Siempre atacar la causa raíz, no el síntoma.
- ✅ Adjuntar el error exacto — nunca describirlo de memoria.
- ✅ Indicar el archivo y línea exacta si se conoce.
- ❌ No aceptar fixes que solo ocultan el problema.
- ❌ No insistir en el mismo enfoque más de dos veces.
