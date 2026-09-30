# Inserta los trazados del logo en las plantillas y genera las páginas
import pathlib
PL,PR=pathlib.Path('logo/paths.txt').read_text().split('\n')[:2]
for src,dst in [('fuente/index.plantilla.html','index.html'),('fuente/celulitis.plantilla.html','celulitis-cordoba/index.html'),('fuente/brillante.plantilla.html','zonas/brillante/index.html'),('fuente/marca.plantilla.html','marca/index.html')]:
    s=pathlib.Path(src)
    if not s.exists(): continue
    d=pathlib.Path(dst); d.parent.mkdir(parents=True,exist_ok=True)
    t=s.read_text(encoding='utf-8')
    for k in ('CSS','SPRITE','CAB','PIE'):
        f=pathlib.Path(f'fuente/_{k.lower()}.txt')
        if f.exists(): t=t.replace('{{'+k+'}}',f.read_text(encoding='utf-8'))
    d.write_text(t.replace('{{PL}}',PL).replace('{{PR}}',PR),encoding='utf-8')
    print('ok',dst)
