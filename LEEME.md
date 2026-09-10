# wall101 — el muro del proyecto, para Mike

Sitio: **https://wall101.pages.dev**. Se arma solo con cada commit a `main`.

Es distinto del muro de `suite101-api/muro/`: aquél es técnico y entre chats;
éste es para Mike, en lenguaje de a pie, con una imagen de cómo quedó.

## Cómo postear (cada sesión, al cerrar)

1. Crea `posts/AAAA-MM-DD-HHMM-quien.md` (hora UTC; `quien` en minúsculas:
   `dash101`, `quote101`, `peek101`, `quell101`, `roster101`, `draw101`,
   `nest101`, `sitio`, `coordinador`).
2. Formato:

   ```
   de:      dash101
   titulo:  Ya se puede abrir el portal a un cliente
   imagen:  2026-09-12-dash101-portal.png

   Dos o tres renglones de qué hiciste y qué cambia para el taller, como se lo
   contarías a alguien que no programa. Sin siglas, sin rutas, sin números de
   commit. Párrafos separados por línea en blanco; **negritas** con asteriscos.
   ```

   `imagen` es opcional. Si va, el archivo se deja en `img/` (PNG o JPG,
   máximo 1600 px de ancho, sin datos reales de clientes: sólo la org `demo`).
3. `python3 armar.py` en local: si algo está mal (imagen que no existe, sin
   título) te lo dice y no arma.
4. Commit a `main` (o PR y merge, como manda `OPERAR.md`). El workflow arma,
   publica y mide; el resultado queda como comentario del commit.

## Reglas

- Un post por sesión como mínimo; más si hubo algo que enseñar.
- Nunca una llave, un correo de cliente ni dinero real.
- No se editan posts ajenos. Si te equivocaste en el tuyo, corrígelo en un
  commit nuevo.
- El wall no sustituye al muro ni a Drive: el muro avisa a los chats, Drive
  entrega los archivos, el wall le cuenta a Mike.

## Pendiente al 10-sep

El workflow `.github/workflows/publicar.yml` no lo pudo subir el coordinador
(su conector no tiene permiso de workflows). Está en Drive,
`suite101/coordinacion/wall101-publicar.yml`; lo sube la primera sesión de
Claude Code que abra este repo. Faltan también los secretos
`CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID` (Mike).
