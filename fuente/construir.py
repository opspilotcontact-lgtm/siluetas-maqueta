# Genera la hoja de estilos compartida y las páginas desde las plantillas
# (inserta los trazados del logo, la cabecera, el pie y el sprite de iconos)
import pathlib

pathlib.Path('css').mkdir(exist_ok=True)
css = pathlib.Path('fuente/sitio.base.css').read_text(encoding='utf-8') + '\n' + pathlib.Path('fuente/servicios.css').read_text(encoding='utf-8')
pathlib.Path('css/sitio.css').write_text(css, encoding='utf-8')

PL, PR = pathlib.Path('logo/paths.txt').read_text().split('\n')[:2]
PAGINAS = [
    ('fuente/index.plantilla.html', 'index.html'),
    ('fuente/maderoterapia.plantilla.html', 'maderoterapia-cordoba/index.html'),
    ('fuente/entreno.plantilla.html', 'entrenamiento-personal-mujeres-cordoba/index.html'),
    ('fuente/masajes.plantilla.html', 'masajes-cordoba/index.html'),
    ('fuente/celulitis.plantilla.html', 'celulitis-cordoba/index.html'),
    ('fuente/brillante.plantilla.html', 'zonas/brillante/index.html'),
    ('fuente/marca.plantilla.html', 'marca/index.html'),
]
for src, dst in PAGINAS:
    s = pathlib.Path(src)
    if not s.exists():
        continue
    d = pathlib.Path(dst)
    d.parent.mkdir(parents=True, exist_ok=True)
    t = s.read_text(encoding='utf-8')
    for k in ('SPRITE', 'CAB', 'PIE'):
        f = pathlib.Path(f'fuente/_{k.lower()}.txt')
        if f.exists():
            t = t.replace('{{' + k + '}}', f.read_text(encoding='utf-8'))
    d.write_text(t.replace('{{PL}}', PL).replace('{{PR}}', PR), encoding='utf-8')
    print('ok', dst)
