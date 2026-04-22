# 🔨 Skill 05 — Desarrollo Módulo por Módulo

> **Fase:** Desarrollo activo  
> **Objetivo:** Implementar cada módulo de forma completa y ordenada antes de pasar al siguiente.

---

## Cuándo usar este skill

- Al comenzar la implementación de cualquier módulo nuevo.
- Al retomar un módulo que quedó incompleto.
- Como referencia para mantener el orden y no saltarse pasos.

---

## El ciclo de desarrollo (orden obligatorio)

### Node.js / NestJS

```
Schema (Prisma) → Migración → Módulo NestJS → Servicio → Controller → DTOs → Rutas → Frontend → Prueba manual → Fix → Siguiente módulo
```

### Laravel

```
Migración → Modelo → Resource Controller → Rutas → Vistas Blade → Prueba manual → Fix → Siguiente módulo
```

---

## Ciclo detallado: Laravel

### Paso 1 — Migración

```powershell
php artisan make:migration create_productos_table
```

```php
Schema::create('productos', function (Blueprint $table) {
    $table->id();
    $table->string('nombre');
    $table->decimal('precio', 10, 2);
    $table->integer('stock')->default(0);
    $table->foreignId('categoria_id')->constrained();
    $table->timestamps();
    $table->softDeletes();
});
```

### Paso 2 — Modelo

```php
class Producto extends Model {
    use SoftDeletes;
    protected $fillable = ['nombre', 'precio', 'stock', 'categoria_id'];
    protected $casts = ['precio' => 'decimal:2'];
    
    public function categoria() { return $this->belongsTo(Categoria::class); }
}
```

### Paso 3 — Resource Controller

```powershell
php artisan make:controller Admin/ProductoController --resource --model=Producto
```

Métodos a implementar: `index`, `create`, `store`, `show`, `edit`, `update`, `destroy`.

### Paso 4 — Rutas en el grupo de rol

```php
Route::group([
    'middleware' => ['auth', 'role:administrador'],
    'as' => 'admin.',
    'prefix' => 'admin'
], function () {
    Route::resource('productos', ProductoController::class);
});
```

### Paso 5 — Vistas Blade

Orden: `index.blade.php` → `create.blade.php` → `edit.blade.php` → `show.blade.php`

Estructura de carpeta:
```
resources/views/Admin/Productos/
├── index.blade.php
├── create.blade.php
├── edit.blade.php
└── show.blade.php
```

### Paso 6 — Prueba manual

1. Abrir el navegador
2. Iniciar sesión con el rol correspondiente
3. Probar cada acción: listar, crear, editar, eliminar
4. Verificar que los permisos de rol se aplican correctamente

---

## Ciclo detallado: NestJS

### Paso 1 — Schema Prisma

```prisma
model Producto {
  id          Int       @id @default(autoincrement())
  nombre      String
  precio      Decimal   @db.Decimal(10, 2)
  stock       Int       @default(0)
  categoriaId Int
  categoria   Categoria @relation(fields: [categoriaId], references: [id])
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
}
```

```powershell
npx prisma migrate dev --name add_productos
```

### Paso 2 — Módulo NestJS

```
src/modules/productos/
├── productos.module.ts
├── productos.controller.ts
├── productos.service.ts
└── dto/
    ├── create-producto.dto.ts
    └── update-producto.dto.ts
```

### Paso 3 — DTOs con validación

```typescript
export class CreateProductoDto {
  @IsString() @IsNotEmpty() nombre: string;
  @IsNumber() @Min(0) precio: number;
  @IsInt() @Min(0) stock: number;
}
```

---

## Prompt para pedir un módulo completo a Claude

```
Implementa el módulo Productos para [Laravel/NestJS]:
- Entidad: [campos de la migración]
- Relaciones: [relaciones con otras entidades]
- Acceso: solo rol administrador
- Incluye: migración + modelo + controller + rutas + vistas básicas (index, create, edit)
- Usa los patrones existentes del proyecto (ver src/modules/usuarios como referencia)
No modifiques archivos que no sean de este módulo.
```

---

## Gestión de interdependencias

Cuando un módulo toca múltiples capas (controller + vista + modelo + ruta), pedir que se trabaje todo junto para no romper nada:

```
Modifica en un solo paso:
1. src/modules/productos/productos.service.ts — añadir método buscarPorCategoria
2. src/modules/productos/productos.controller.ts — nuevo endpoint GET /productos/categoria/:id
3. frontend/src/app/productos/page.tsx — filtro por categoría en la UI
```

---

## Cómo extender una funcionalidad existente

1. Pedir a Claude que lea primero los archivos del módulo a extender.
2. Identificar qué ya existe para no duplicar lógica.
3. Extender usando los patrones ya establecidos (misma estructura, mismos nombres).
4. Verificar que no se rompen módulos existentes.
5. Si la extensión afecta la BD: crear nueva migración, nunca modificar migraciones ya corridas.

---

## Señales de que el módulo está terminado

- [ ] Migración aplicada sin errores
- [ ] CRUD completo funciona manualmente
- [ ] Permisos de rol verificados
- [ ] Sin errores en consola ni en logs
- [ ] Documento de flujo actualizado con lo implementado

---

## Reglas al usar este skill

- ✅ Un módulo completo antes de empezar el siguiente.
- ✅ Prueba manual después de cada módulo.
- ✅ El mismo estilo de código que el resto del proyecto.
- ❌ No empezar otro módulo si hay bugs conocidos en el actual.
- ❌ No modificar migraciones ya aplicadas en producción — crear nueva migración.

---

## Siguiente paso

→ [`06-comunicacion-agente.md`](06-comunicacion-agente.md) — Cómo pedir trabajo a Claude de forma eficiente.
