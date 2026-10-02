# Siluetas de Mujer · propuesta de marca y web

Maqueta en revisión (noindex). Versión actual: **v7** en la raíz («Arma tus 4 semanas» con los precios de Carmen del 2-oct: individual 360 € y grupo 200 € cada 4 semanas, gimnasio incluido) + tarjeta regalo en /tarjeta-regalo/. Dominio: siluetasdemujer.es (archivo CNAME, no borrar).
Versiones anteriores: /v6/, /v5/, /v4/, /v2/ y /v1/.

## Cómo se construye la versión actual

```
python fuente/v3/generar.py          # genera la web en _v3/ (vista previa)
```

Para publicar, copiar el contenido de `_v3/` a la raíz del repo.
El generador lleva todas las páginas con sus componentes compartidos (cabecera, pie,
el camino, los 3 pasos, las fotos). Estilos: `fuente/v3/estilo.css` (sistema)
+ `fuente/v3/modulos.css` (los objetos de cada sección).
Fotos: `fuente/fotos/ia-*.jpg`, generadas con IA (Gemini) y marcadas como ilustrativas.

`fuente/construir.py` es el constructor de la v2: escribe en la raíz y pisaría la v4.
No usarlo salvo para regenerar /v2/.

Fuentes: Figtree y DM Serif Display, esta solo en el logotipo (SIL OFL).
