# WHITEMOON-MADERAS-LOPEZ

Propuesta de demo preparada por WhiteMoon Agencia IA para Serrería Maderas López, S.L. (Arzúa, A Coruña), una serrería de eucalipto y pino.

**No es la web oficial de la empresa** y no debe poder confundirse con ella: no usa su logo, sus fotos ni su tipografía, lleva `noindex, nofollow` y no tiene sitemap, `robots.txt`, `llms.txt`, canonical, JSON-LD ni `og:image`.

GitHub Pages está desactivado hasta que Cris lo confirme.

## Pendiente de confirmar con la empresa

- **Texto de su web (empresa familiar, más de 50 años), confirmar con la empresa antes de enseñar.** Es lo único que la página afirma sobre su historia.
- **FSC y NIMF 15: pendiente de confirmar con la empresa.** Hasta entonces no aparecen en la página, ni esas ni ninguna otra certificación.

## Reglas de contenido

- Solo los datos que dio Cris: razón social, dirección, teléfono, correo y la lista de productos. Nada más.
- Sin precios, plazos, stock, volúmenes, clientes, testimonios, certificaciones ni cifras. La única cifra es «más de 50 años».
- Sin «prestigio», «a nivel nacional» ni superlativos.
- Sin chatbot, sin formularios, sin Supabase y sin claves de ningún tipo en el cliente.
- Las fotos son de Pexels y van como ambiente: no representan instalaciones ni productos de Maderas López, y ninguna se rotula como eucalipto, pino, tabla limpia ni tabla de carpintería.

## Qué hay

- `index.html`, `assets/css/style.css`, `assets/js/` — HTML, CSS y JS puros, sin frameworks ni dependencias.
- `assets/js/config.js` — datos de contacto de la serrería y, aparte, el WhatsApp de WhiteMoon Agencia IA (número y texto prellenado) en una sola constante. El HTML lleva los mismos valores como respaldo para quien navega sin JavaScript: si se cambia uno, se cambia el otro.
- `assets/fonts/` — Bricolage Grotesque variable (licencia OFL), subset latin, auto-hospedada.
- `scripts/verifica-contraste.py` — mide el contraste AA de la paleta y el peor píxel real de la foto bajo el texto del hero.

## Probar en local

```
python -m http.server 8765
python scripts/verifica-contraste.py
```

El script necesita Pillow (`pip install pillow`). Si se toca la paleta o el velo del hero en `style.css`, hay que tocarlos igual en el script.

## Imágenes

Fotografías de Pexels, bajo licencia Pexels, revisadas a tamaño completo: sin personas y sin rótulos ni marcas legibles.

- Hero: [Mark Stebnicki](https://www.pexels.com/photo/pile-of-wood-planks-inside-a-warehouse-12278570/).
- Cortes a medida: [Mark Stebnicki](https://www.pexels.com/photo/layers-of-lumber-in-close-up-photography-12278590/).
- Astilla: [Valentin Ivantsov](https://www.pexels.com/photo/close-up-of-natural-wooden-chips-texture-35687997/).
- Serrín: [Ron Lach](https://www.pexels.com/photo/close-up-shot-of-sawdust-8817844/).

## Burbuja de WhatsApp

Es la única captación y lleva al WhatsApp de **WhiteMoon Agencia IA**, no al de Maderas López: la etiqueta «Demo: este WhatsApp es de WhiteMoon Agencia IA» está siempre visible y el aviso legal lo repite. Ningún texto de la página invita a escribir por WhatsApp a la empresa; sus CTA son el teléfono y el correo.

Es un enlace directo a una conversación (`wa.me`), sin nada más detrás. El `href` completo está escrito en `index.html` como respaldo sin JavaScript; si se cambia el número o el texto en `config.js`, hay que cambiarlo también ahí.
