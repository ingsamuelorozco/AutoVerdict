# Portada: barra superior, hero, buscador y características

Rediseño de la parte superior de la portada a partir de una referencia de diseño (barra oscura sobre el hero, buscador que se superpone al hero y sección de características con un auto central).

## Colores (rol de la referencia → token del proyecto)

| Rol en la referencia | Token |
|---|---|
| Fondo oscuro principal | `--velo` (negro del lienzo M) |
| Acento (botones, activo, puntos) | `--acento` (azul), `--acento-hondo` en hover |
| Acento como texto sobre fondo oscuro | `--acento-texto` (azul aclarado para contraste AA) |
| Blanco y grises | `--papel`, `--suave`, `--superficie`, `--linea`, `--tenue` |

`--m-rojo` sigue reservado para la franja M: nunca es relleno ni acción.

## Tipografía y forma

- Títulos y cifras: Inter 700 en mayúsculas (la fuente de títulos del sistema) en lugar de una condensada.
- Texto: Inter 300/400, igual que el resto del sitio.
- Radio binario del sistema: todo rectangular; solo los controles circulares (puntos del hero, manijas del rango) usan `rounded-full`.

## Alcance

1. Barra superior con menú desplegable de herramientas.
2. Hero con titular, párrafo, botón, dato destacado, auto y puntos interactivos.
3. Buscador rápido que se superpone al borde inferior del hero.
4. Sección de características: seis ítems alrededor de un auto visto desde arriba.

El resto de la portada (método, calculadoras, actualizados, alertas rojas y cierre) se mantiene.

## Contenido

- Menú: Inicio, Actualizados, Buscar, Comparador, Reviews y Herramientas (el desplegable lista las cinco calculadoras).
- Derecha de la barra: ajustes regionales (moneda, TRM y ciudad), favoritos y el botón Comparar a toda la altura.
- Hero: titular "Precio & verdad", sublema del sitio y conteo real del catálogo.
- Buscador: carrocería, marca y ciudad reales; rango de precio en calle en COP; lleva a `/buscar` con los filtros.
- Características: seis funciones reales del producto.

## Puntos de quiebre

- Barra completa desde 1280 px (`nav`): por debajo, menú hamburguesa con Herramientas plegable. Con seis secciones, ajustes, favoritos y Comparar no cabe en 992 px sin apretarse. Entre 1280 y 1440 px se ocultan la cifra de la TRM y parte del espaciado.
- Hero: titular de 38/52/64 px; por debajo de 1024 px el dato del catálogo pasa bajo el botón y el auto ocupa el 92 % (móvil) o el 72 % (tableta) del ancho.
- Buscador: una columna por debajo de 768 px y botón a todo el ancho.
- Características: el auto va primero; dos columnas en tableta y tres desde 1024 px.

## Imágenes

Viven en `frontend/src/assets/images/` y sus créditos en `CREDITS.md`.

- Fondos: fotos libres de Wikimedia Commons, redimensionadas y sin metadatos.
- Autos: fotos reales de Wikimedia Commons con el fondo eliminado y exportadas como PNG transparente (`hero-car.png`, `car-top-view.png`).
