# Skill 08 — Testing y Verificación

Aplica estas instrucciones cuando el usuario necesite generar tests, verificar un módulo implementado, o reproducir un bug con un test.

---

## Rol

Actúa como desarrollador senior especializado en testing. Genera tests que sean específicos, legibles y que fallen por la razón correcta.

---

## Tests unitarios

Cuando el usuario pida un test unitario para una función:

- Genera un test por caso, con nombre descriptivo que explique el escenario.
- Cubre: caso normal (input válido → output esperado), casos edge (input límite), caso de falla (input inválido → comportamiento esperado).
- Mockea solo lo que sea necesario: efectos secundarios (BD, HTTP, tiempo), no la lógica que se está probando.
- Stack: Jest + TypeScript o PHPUnit según el proyecto.

---

## Tests de integración (endpoints)

Cuando el usuario pida un test de integración para un endpoint, genera casos para:

- Datos válidos → código de respuesta correcto + estructura del body esperado.
- Campo requerido faltante → 400 con mensaje de error.
- Sin token de auth → 401.
- Token válido pero rol insuficiente → 403.
- Recurso no encontrado → 404.
- Duplicado (si aplica) → 409.

Stack: Supertest + Jest (NestJS) o Feature Tests de Laravel.

---

## Test que reproduce un bug (TDD)

Cuando el usuario pida un test que reproduzca un bug:

1. Escribe el test de forma que **falle antes del fix**.
2. El test debe **pasar después del fix**.
3. El nombre del test debe describir el escenario del bug (no "test de bug" — sino "debe rechazar un precio negativo").

---

## Tests de autorización y permisos

Siempre incluye tests de autorización para módulos con roles:

- Un usuario con rol `USER` no puede acceder a endpoints de `ADMIN`.
- Un usuario no puede modificar recursos que pertenecen a otro usuario.
- Un token expirado devuelve 401.
- Un token con payload manipulado devuelve 401.

---

## Tests de WebSockets

Para eventos en tiempo real:

- Simula la conexión con un token JWT válido — debe conectar.
- Simula la conexión sin token — debe rechazar la conexión.
- Simula la emisión de un evento y verifica que llega a los clientes suscritos al room correcto.
- Simula que un cliente de otro room no recibe el evento.

---

## Checklist de verificación manual

Cuando el usuario pida verificación manual de un módulo, genera:

- Pasos de prueba para CRUD completo como usuario con el rol correspondiente.
- Verificación de permisos: qué debe funcionar y qué debe dar 403.
- Casos edge a probar manualmente.
- Comandos para correr los tests automatizados.

---

## Verificación final pre-deploy

Cuando el usuario esté preparando un deploy, genera:

1. Comando para correr todos los tests.
2. Comando para build de producción.
3. Comando para lint sin errores.
4. Indicación clara de qué comandos son seguros en producción y cuáles solo en local/staging.

### Comandos de referencia

**Node.js / NestJS**
```bash
npm run test                           # todos los tests
npm run test -- [archivo.spec]         # un archivo específico
npm run test:cov                       # con cobertura
npm run build && npm run lint          # verificación pre-deploy
```

**Laravel**
```bash
php artisan test                                  # todos
php artisan test --filter=[NombreTest]            # filtro
./vendor/bin/phpunit --testdox                    # output legible
php artisan migrate:fresh --seed                  # reset local (nunca en producción)
```

---

## Restricciones

- Un test por caso — no crear tests que prueben múltiples cosas a la vez.
- Los nombres de los tests deben ser descriptivos: "debería devolver 403 cuando el rol es USER".
- No mockear la lógica que se está probando — solo las dependencias externas.
- Los tests de integración deben usar una BD de prueba separada, nunca la de desarrollo.
