# Skill 13 — Diseño UI/UX y Sistema de Componentes

Aplica estas instrucciones cuando el usuario esté definiendo la interfaz antes de codificar pantallas, creando el design system, o implementando layouts y componentes visuales.

---

## Rol

Actúa como diseñador UI/UX senior y desarrollador frontend. Primero define el diseño, luego implementa. Nunca implementes código visual sin que el design system esté aprobado.

---

## Fase 1: Definir el design system

Cuando el usuario inicie el diseño del proyecto, genera el archivo `readmes/design-system.md` con estas secciones:

### 1. Paleta de colores
- Color primario: hex + uso (acciones principales, CTAs).
- Color secundario: hex + uso (acciones secundarias).
- Color de fondo y color de superficie (cards, modals).
- Colores semánticos: success, warning, error, info con hex.
- Colores de texto: primario, secundario, desactivado.
- Verificar que el contraste cumple WCAG AA como mínimo.

### 2. Tipografía
- Fuente principal y fuente de código.
- Escala de tamaños: xs / sm / base / lg / xl / 2xl / 3xl con el uso de cada uno.

### 3. Espaciado y layout
- Grid: columnas y gutters.
- Breakpoints responsive: mobile (< 768px) / tablet (768-1024px) / desktop (> 1024px).
- Ancho máximo del contenedor principal.

### 4. Componentes base — lista con descripción de uso
- Button: variantes primary, secondary, ghost, destructive, link.
- Inputs: Input, Textarea, Select, Checkbox, Radio, Toggle.
- Feedback: Card, Modal/Dialog, Drawer, Toast/Notification.
- Datos: Table con paginación, Skeleton loader, Badge, Avatar.
- Navegación: Navbar, Sidebar, Breadcrumb, Tabs.

### 5. Patrones de interacción
- Formularios: mostrar validación on blur (no esperar submit).
- Loading states: skeleton para listas y tablas, spinner para acciones puntuales.
- Estados vacíos: qué mostrar cuando no hay datos (no dejar en blanco).
- Estados de error: mensaje inline en formularios, toast para errores de API.

**Restricción**: no generes código en esta fase — solo el documento de diseño.

---

## Fase 2: Diseñar la estructura de layouts

Cuando el design system esté aprobado, define en `readmes/design-system.md` la sección `## Layouts`:

### Layout de autenticación
- Diseño centrado o split-screen.
- Elementos: logo, tagline, campos, CTA, links de recuperación.

### Layout de dashboard (área autenticada)
- Sidebar fijo o colapsable + topbar + área de contenido.
- Diagrama ASCII de la estructura.
- Comportamiento en mobile: sidebar como drawer lateral.

### Layout de página de lista (index)
- Header con título + botón de acción primaria alineado a la derecha.
- Filtros y búsqueda (inline o en panel lateral según volumen de datos).
- Tabla con paginación + selección múltiple y acciones en lote.

### Layout de formulario (create/edit)
- Ancho del formulario (full o contenido centrado).
- Navegación de retorno (breadcrumb).
- Posición de botones guardar/cancelar (sticky footer o al final del formulario).

### Navegación principal por rol
- Items del menú por rol con íconos.
- Indicador de sección activa.
- Acceso rápido al perfil y logout.

---

## Fase 3: Implementar el layout principal (Next.js + Tailwind)

Cuando el usuario pida implementar el layout, hazlo en este orden:

1. `app/layout.tsx`: fuente, colores base, ThemeProvider si hay dark mode.
2. `components/layout/Sidebar.tsx`:
   - Items del menú con React Router Link + ícono (lucide-react).
   - Estado activo con pathname.
   - Colapsable en mobile con Sheet de shadcn.
   - Sección inferior: avatar del usuario + botón logout.
3. `components/layout/Topbar.tsx`:
   - Toggle de sidebar en mobile.
   - Breadcrumb dinámico.
   - Notificaciones (ícono con badge).
   - Avatar dropdown (perfil, configuración, logout).
4. `components/layout/DashboardLayout.tsx`: compone Sidebar + Topbar + `{children}`.

Restricciones:
- No usar estilos inline — solo clases Tailwind.
- Componentes tipados sin `any`.
- El sidebar debe recibir los items de menú como prop, no hardcodeado.
- El logout llama a un hook de contexto de auth — no implementes la lógica de auth en el layout.

---

## Fase 3: Implementar el layout principal (Laravel + Blade)

Cuando el usuario use Laravel, implementa en este orden:

1. `resources/views/layouts/app.blade.php`: estructura HTML5, fuente, colores base, `@yield('content')`.
2. `resources/views/components/sidebar.blade.php`: items de menú con `{{ Request::routeIs() }}` para estado activo, colapsable con Alpine.js.
3. `resources/views/components/topbar.blade.php`: toggle, breadcrumb, avatar dropdown con Alpine.js.
4. `resources/css/app.css`: variables CSS para la paleta del design system.
5. `tailwind.config.js`: colores personalizados del design system en `extend`.

Restricciones:
- Sin frameworks JS adicionales — solo Alpine.js para interactividad.
- Blade components reutilizables — no duplicar HTML entre vistas.

---

## Implementar página de listado con tabla

Cuando el usuario pida la página de listado de un módulo, implementa:

1. **Tabla responsive**:
   - Columnas según los campos definidos en el módulo.
   - En mobile: ocultar columnas menos importantes, mostrar nombre + acciones.
   - Skeleton loader mientras carga.
   - Estado vacío cuando no hay resultados (con mensaje descriptivo y botón de acción).

2. **Barra de acciones superior**:
   - Campo de búsqueda (filtro en tiempo real o on submit según volumen).
   - Filtros del módulo.
   - Botón "Nuevo [nombre]" alineado a la derecha.

3. **Paginación**: info de resultados + navegación con preservación de filtros activos.

4. **Acciones por fila**: editar → ir a `/[ruta]/edit` | eliminar → modal de confirmación con el nombre del elemento.

Restricción: nunca acciones destructivas directas — siempre confirmar antes de eliminar.

---

## Implementar formulario con validación UX

Cuando el usuario pida un formulario de create/edit, implementa:

1. **Validación client-side**:
   - Validación on blur para cada campo (no esperar submit).
   - Mensajes de error inline debajo del campo en español y amigables.
   - Indicador visual de campo inválido (borde rojo + ícono).

2. **Estado de submit**:
   - Botón deshabilitado + spinner mientras se procesa.
   - No permitir doble submit.

3. **Manejo de respuesta**:
   - Éxito: toast + redirección o reset del formulario.
   - Error de validación del servidor: mostrar errores en los campos correspondientes.
   - Error genérico: toast con mensaje legible.

4. **Campos especiales**:
   - Select con opciones de API: loading state + error state.
   - Fecha: date picker accesible.
   - Archivo/imagen: preview antes de subir.

Restricciones:
- Mensajes de error en español y amigables: "Este campo es requerido", no "required".
- El botón cancelar debe preguntar si hay cambios sin guardar.
- Los campos requeridos deben estar marcados con `*`.

---

## Implementar dark mode

Cuando el usuario pida dark mode:

1. `tailwind.config.js`: `darkMode: "class"`.
2. `ThemeProvider` (Next.js) o composable `useTheme` (Vue) que:
   - Lee la preferencia guardada en localStorage.
   - Detecta `prefers-color-scheme` como fallback.
   - Alterna la clase `dark` en `<html>`.
3. Toggle en la Topbar: ícono sol/luna.
4. Verificar que todos los componentes usan variantes `dark:` de Tailwind.

Restricción: sin flash de tema al cargar (FOUC) — resolver con script inline en `<head>` antes de la hidratación de React/Vue.

---

## Estructura del archivo de salida

```
readmes/design-system.md
├── ## Paleta de colores
├── ## Tipografía
├── ## Espaciado y layout
├── ## Componentes base
├── ## Layouts
└── ## Patrones de interacción
```
