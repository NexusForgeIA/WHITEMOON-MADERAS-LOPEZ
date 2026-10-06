# WHITEMOON-MADERAS-LOPEZ

Propuesta de demo de una página web, preparada por WhiteMoon Agencia IA para Maderas López, una serrería de eucalipto y pino de Arzúa (A Coruña).

**No es la web oficial de Maderas López.** La página lo dice en el pie, lleva la etiqueta «Propuesta de demo» sobre el logo y no usa el logo, las fotos ni la tipografía de la empresa. El logo de la cabecera es también una propuesta, hecha para esta demo.

## Qué hay

- `index.html` — la página, de una sola pantalla larga: hero, productos, cortes a medida, cómo consultar y pie con el contacto y el aviso legal.
- `assets/css/style.css` — estilos. Los colores son variables en `:root`; los puntos de corte son 900 px y 600 px.
- `assets/js/config.js` — los datos de contacto y los de la burbuja de WhatsApp, en una sola constante.
- `assets/js/main.js` — pinta esos datos en la página, el menú móvil, el marcado de la sección activa y la entrada de las secciones al hacer scroll.
- `assets/fonts/` — Bricolage Grotesque variable (licencia OFL), subset latin, auto-hospedada.
- `assets/img/` — fotografías en JPG y WebP, a dos anchos, y el logo de la cabecera a 1x y 2x.
- `assets/logo-maderas-lopez.jpeg` — original del logo propuesto, del que salen los de `assets/img/`.
- `scripts/verifica-contraste.py` — mide el contraste de la paleta.

HTML, CSS y JavaScript puros, sin frameworks, sin dependencias y sin peticiones a terceros. No hay formularios, cookies ni analítica: la página no recoge datos.

## Burbuja de WhatsApp

El botón flotante lleva al WhatsApp de **WhiteMoon Agencia IA**, no al de Maderas López. La etiqueta «Demo: este WhatsApp es de WhiteMoon Agencia IA» está siempre visible a su lado y el aviso legal del pie lo repite. Los contactos de la serrería que muestra la página son el teléfono y el correo.

Es un enlace directo a una conversación (`wa.me`) con un mensaje prellenado. El número y el texto están en `config.js`; el enlace completo también está escrito en `index.html` para quien navega sin JavaScript, así que si se cambia uno hay que cambiar el otro.

## Indexación

La página lleva `<meta name="robots" content="noindex, nofollow">` y no tiene `robots.txt`, sitemap, canonical, datos estructurados ni etiquetas Open Graph. Es una propuesta y no debe aparecer en buscadores como si fuera la web de la empresa.

## Probar en local

```
python -m http.server 8765
```

y abrir `http://localhost:8765/`.

## Cómo se comprueba

**Contraste.** Necesita Pillow (`pip install pillow`):

```
python scripts/verifica-contraste.py
```

Comprueba que todo el texto supera 4,5:1 (WCAG AA) y que los contornos y el foco superan 3:1. Mide los pares de la paleta, el peor píxel real de la foto bajo el texto del hero a diez tamaños de pantalla, el mismo velo sobre una foto blanca pura, la burbuja de WhatsApp sobre fondos claros y oscuros, y el logo sobre su pastilla blanca. Sale con código 1 si algo falla. Los colores y el velo del hero están duplicados en el script: si se tocan en `style.css`, hay que tocarlos ahí también.

**Resto.** Con Lighthouse en modo móvil y con el navegador:

- Rendimiento, accesibilidad y buenas prácticas de Lighthouse. La nota de SEO sale baja a propósito, por el `noindex`.
- Sin desplazamiento horizontal y sin mensajes en la consola entre 320 px y 1440 px de ancho.
- Foco de teclado visible sobre fondo claro y sobre fondo oscuro.
- Enlaces y botones con al menos 44 px de alto; la burbuja mide 56 px.
- Todas las imágenes con `width`, `height` y `alt`.
- El enlace de la burbuja es el mismo con y sin JavaScript.

En local, `main.js` avisa por consola si la página se desborda en horizontal.

## Limitación conocida

En pantallas de menos de unos 740 px de alto, la burbuja de WhatsApp puede quedar sobre la parte baja del hero hasta que se hace scroll.

## Imágenes

Fotografías de Pexels, bajo licencia Pexels. Son imágenes de ambiente: no representan instalaciones ni productos de Maderas López.

- [Mark Stebnicki](https://www.pexels.com/photo/pile-of-wood-planks-inside-a-warehouse-12278570/) — hero.
- [Mark Stebnicki](https://www.pexels.com/photo/layers-of-lumber-in-close-up-photography-12278590/) — banda de cortes a medida.
- [Valentin Ivantsov](https://www.pexels.com/photo/close-up-of-natural-wooden-chips-texture-35687997/) y [Ron Lach](https://www.pexels.com/photo/close-up-shot-of-sawdust-8817844/) — bloque de subproductos.

## Publicación

Sitio estático: se sirve tal cual desde la raíz de la rama `main`, sin paso de compilación.
