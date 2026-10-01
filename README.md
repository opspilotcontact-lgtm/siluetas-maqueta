# Siluetas de Mujer · propuesta de marca y web

Maqueta en revisión (noindex). Versión actual: **v4 «el camino, con forma»** en la raíz.
Versiones anteriores: /v2/ y /v1/.

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
