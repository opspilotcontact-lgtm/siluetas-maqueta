"""Siluetas de Mujer · v6 (v4 «el camino, con forma» + audios de Carmen del 1-oct + «Arma tu semana»).

v3 dio el SISTEMA (una paleta, una letra, el camino, una plantilla) y el fundador
lo aprobó; le faltaba personalidad: «texto y más texto». La v4 mantiene el sistema
y da a cada contenido su propio objeto: el mapa de la silueta, la conversación de
WhatsApp, la balanza grande, las dos curvas, la lámina, el recibo, la ficha...

    python fuente/v3/generar.py [salida]      (por defecto: _v3/)

Datos reales: Figueras Wellness (precios), audios de Carmen del 30-sep
(valoración gratis, sin pack, «certificada», «desaparece la retención»).
Fotos: generadas con Gemini el 1-oct, provisionales e «ilustrativas».
"""
import html
import pathlib
import shutil
import sys
from urllib.parse import quote

from PIL import Image, ImageEnhance

RAIZ = pathlib.Path(__file__).resolve().parents[2]
SALIDA = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / '_v3'
FUENTE = RAIZ / 'fuente'

TEL = '646 437 371'
PL, PR = (RAIZ / 'logo' / 'paths.txt').read_text().split('\n')[:2]
SIL = f'<svg viewBox="0 0 100 152" aria-hidden="true"><path fill="#D93A7A" d="{PL}"/><path fill="#16A39A" d="{PR}"/></svg>'


def wa(txt):
    return 'https://wa.me/34646437371?text=' + quote(txt)


# ── Fotos: una serie, un tratamiento ────────────────────────────────────────
FOTOS = {
    'maderoterapia': 'Manos pasando un rodillo de madera de esferas sobre el muslo, en camilla',
    'entreno': 'Mujer de unos 50 años haciendo una sentadilla a un cajón con goma',
    'grupo': 'Grupo pequeño de mujeres entrenando con gomas en una sala luminosa',
    'descarga': 'Manos haciendo un masaje de descarga en hombros y espalda',
    'piernas': 'Piernas descansando en alto sobre un cojín al final del día',
    'cuesta': 'Mujer subiendo una cuesta empedrada entre casas encaladas',
    'pesa': 'Manos de una mujer agarrando una pesa rusa pequeña',
}


def preparar_fotos():
    dst = SALIDA / 'img' / 'fotos'
    dst.mkdir(parents=True, exist_ok=True)
    arena = Image.new('RGB', (1, 1), (243, 235, 224))
    for n in FOTOS:
        im = Image.open(FUENTE / 'fotos' / f'ia-{n}.jpg').convert('RGB')
        im = ImageEnhance.Color(im).enhance(.88)          # misma serie: algo menos de color
        im = Image.blend(im, arena.resize(im.size), .06)   # y un velo de arena
        for w in (1200, 640):
            c = im.copy()
            c.thumbnail((w, w))
            c.save(dst / f'{n}-{w}.webp', 'WEBP', quality=72, method=6)
        c = im.copy()
        s = min(c.size)
        c = c.crop(((c.width - s) // 2, (c.height - s) // 2, (c.width + s) // 2, (c.height + s) // 2)).resize((160, 160))
        c.save(dst / f'{n}-mini.webp', 'WEBP', quality=70)


def foto(n, base, ar=None, carga='lazy', sizes='(max-width: 820px) 100vw, 45vw'):
    estilo = f' style="--ar:{ar}"' if ar else ''
    prio = ' fetchpriority="high"' if carga == 'eager' else ''
    return (f'<figure class="foto"{estilo}><img src="{base}img/fotos/{n}-1200.webp" '
            f'srcset="{base}img/fotos/{n}-640.webp 640w, {base}img/fotos/{n}-1200.webp 1200w" '
            f'sizes="{sizes}" width="1200" height="805" alt="{FOTOS[n]}" '
            f'loading="{carga}" decoding="async"{prio}><figcaption>Imagen ilustrativa</figcaption></figure>')


# ── Datos compartidos ───────────────────────────────────────────────────────
AYUDAS = [  # slug, en palabras de la clienta, gancho, ramas, foto, zona del mapa (y en la silueta)
    ('espalda-cuello-cargados-cordoba', 'Cargo la espalda y el cuello', 'Primero soltar. Después, que no vuelva.', 'mv', 'descarga', 18),
    ('menopausia-fuerza-cordoba', 'Con la menopausia, mi cuerpo ya no es el mismo', 'Cintura, energía y fuerza: lo que se puede hacer.', 'vm', 'pesa', 58),
    ('celulitis-cordoba', 'La piel de naranja me quita las ganas de ponerme según qué', 'Qué puede hacer la maderoterapia, y qué no.', 'mv', 'maderoterapia', 92),
    ('piernas-cansadas-retencion-cordoba', 'Acabo el día con las piernas pesadas', 'Pesadez, tobillos marcados, peor con el calor.', 'mv', 'piernas', 128),
    ('empezar-a-entrenar-cordoba', 'Quiero empezar a moverme, pero no estoy en forma', 'Empezamos desde donde estás hoy.', 'v', 'cuesta', None),
]
ZONA = {'espalda-cuello-cargados-cordoba': 'Espalda y cuello', 'menopausia-fuerza-cordoba': 'Cintura y abdomen',
        'celulitis-cordoba': 'Cadera y glúteo', 'piernas-cansadas-retencion-cordoba': 'Piernas'}
SERVICIOS = [
    ('maderoterapia-cordoba', 'Maderoterapia'),
    ('entrenamiento-personal-mujeres-cordoba', 'Entrenamiento'),
    ('masajes-cordoba', 'Masajes'),
]
RAMA = {'m': '<span class="rama m">Con las manos</span>', 'v': '<span class="rama v">Con el movimiento</span>'}


# ── Componentes compartidos ─────────────────────────────────────────────────
def cabecera(base, actual=''):
    nav = [(f'{base}#empieza', 'Empieza aquí', '')] + [(f'{base}{u}/', t, u) for u, t in SERVICIOS] + [(f'{base}#donde', 'Dónde', '')]
    cur = ' aria-current="page"'
    enl = ''.join(f'<a href="{h}"{cur if u and u == actual else ""}>{t}</a>' for h, t, u in nav)
    return f'''<a class="salta" href="#contenido">Saltar al contenido</a>
<div class="franja">Propuesta de web para Siluetas de Mujer, en revisión (v6). Las imágenes son ilustrativas, generadas con IA. <a href="{base}v5/">Ver la v5</a></div>
<header class="cab"><div class="wrap">
  <a class="marca" href="{base}" aria-label="Siluetas de Mujer, inicio"><img src="{base}img/silueta.svg" alt="" width="20" height="30"><span><i>Siluetas</i> de Mujer</span></a>
  <nav class="nav" aria-label="Principal">{enl}</nav>
  <a class="btn" href="{wa('Hola Mari Carmen, te escribo desde la web de Siluetas de Mujer')}">WhatsApp</a>
</div></header>'''


def pie(base):
    ay = ''.join(f'<li><a href="{base}{u}/">{t}</a></li>' for u, t, *_ in AYUDAS)
    se = ''.join(f'<li><a href="{base}{u}/">{t}</a></li>' for u, t in SERVICIOS)
    return f'''<footer class="pie"><div class="wrap">
  <div><a class="marca" href="{base}"><img src="{base}img/silueta-arena.svg" alt="" width="20" height="30"><span><i>Siluetas</i> de Mujer</span></a>
    <p style="margin-top:1rem">Masaje, maderoterapia y entrenamiento para mujeres en Córdoba. Por Mari Carmen Figueras, entrenadora personal certificada y masajista.</p></div>
  <div><h2>Te ayudo con</h2><ul>{ay}</ul></div>
  <div><h2>Servicios</h2><ul>{se}</ul></div>
  <div><h2>Contacto</h2><ul><li><a href="{wa('Hola Mari Carmen')}">WhatsApp {TEL}</a></li><li>Lunes a viernes, de 10:00 a 20:00</li><li>En mi sala o en tu casa, en Córdoba capital</li></ul></div>
  <div class="legal"><span>© 2026 Siluetas de Mujer</span><span>Aviso legal · Privacidad · Cookies</span></div>
</div></footer>'''


def pasos(titulo='Tus 3 pasos para empezar', texto='Sin compromiso. La valoración es gratis y el plan lo decides tú.', msg='Hola Mari Carmen, quiero mi valoración gratuita'):
    """El bloque común: los 3 pasos sobre los dos trazos del logo. Cierra TODAS las páginas."""
    return f'''<section class="seccion" id="pasos"><div class="wrap">
  <div class="pasos-cab"><div class="tit-sec"><h2>{titulo}</h2><p>{texto}</p></div>
    <a class="btn" href="{wa(msg)}">Pedir mi valoración gratuita</a></div>
  <ol class="pasos-h">
    <li><div><h3>Me escribes</h3><p>Por WhatsApp, con tus palabras: qué notas y desde cuándo. Te respondo yo.</p></div></li>
    <li><div><h3>Valoración gratis</h3><p>Te mido, hablamos de tu salud y de lo que quieres conseguir. Sin prisas.</p></div></li>
    <li><div><h3>Tu plan</h3><p>Manos, movimiento o las dos cosas. Tú decides, y cada pocas semanas lo revisamos juntas.</p></div></li>
  </ol>
</div></section>'''


# ── «Tu semana con Carmen»: el programa como un calendario que se arma ────
# Carmen (audio 1-oct 18:44): lo que vende es el PROGRAMA (movimiento + manos), no piezas
# sueltas, y quiere el precio POR SEMANA. El fundador (2-oct): niveles que se suman.
# PRECIOS PROVISIONALES (fundador 2-oct, pasados de mes a semana) · A VALIDAR CON CARMEN.
PRECIO = {'base': 12, 'grupo': 9, 'manos': 28}   # €/semana: app y seguimiento · cada entreno en grupo · cada sesión de manos
PLANES = [('casa', 'En casa, con la app', 0, 0), ('deporte', 'Deporte', 2, 0), ('manos', 'Deporte y manos', 2, 1)]
SEM_DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']


def semana(base, plan='manos', titulo='Arma tu semana.', texto='Elige cómo quieres empezar y mira cómo queda tu semana. Mueve las sesiones al día que te venga mejor, añade o quita, y verás cuánto te sale. Luego lo hablamos.'):
    """El planificador: plan → semana tipo con sus sesiones → mover / añadir → precio semanal → WhatsApp.
    Solo visual: no reserva nada; el plan exacto se cierra con Carmen en la valoración gratis."""
    planes = ''.join(f'<button type="button" data-plan="{k}" data-g="{g}" data-m="{m}" aria-pressed="{str(k == plan).lower()}">'
                     f'<b>{n}</b><small>desde {PRECIO["base"] + g * PRECIO["grupo"] + m * PRECIO["manos"]} €/sem.</small></button>'
                     for k, n, g, m in PLANES)
    dias = ''.join(f'<div class="dia" data-d="{i}"><button type="button" class="dia-cab" data-mover="{i}" aria-label="Mover la sesión elegida al {d.lower()}">'
                   f'<span class="anilla" aria-hidden="true"></span><small>{d[:3]}</small><b></b></button><div class="huecos"></div></div>'
                   for i, d in enumerate(SEM_DIAS))
    return f'''<section class="seccion semana-sec" id="reserva"><div class="wrap">
  <div class="semana">
    <div class="semana-txt">
      <h2>{titulo}</h2>
      <p>{texto}</p>
      <p class="semana-paso"><b>1</b>¿Cómo quieres empezar?</p>
      <div class="planes" role="group" aria-label="Plan">{planes}</div>
    </div>
    <div class="semana-cal">
      <p class="semana-paso"><b>2</b>Tu semana <span class="mes" aria-live="polite"></span></p>
      <div class="dias">{dias}</div>
      <p class="pista" aria-live="polite">Toca una sesión y después el día al que quieres moverla.</p>
      <div class="ley-sem"><span class="rama v">Entreno en grupo</span><span class="rama m">Masaje o maderoterapia</span><span class="app-ley">App: tu entreno en casa</span></div>
      <p class="semana-paso"><b>3</b>¿Quieres más?</p>
      <div class="mas">
        <div class="cont" data-t="g"><span class="rama v">Entrenos en grupo</span><button type="button" data-menos="g" aria-label="Un entreno menos">−</button><output data-n="g">2</output><button type="button" data-mas="g" aria-label="Un entreno más">+</button></div>
        <div class="cont" data-t="m"><span class="rama m">Sesiones de manos</span><button type="button" data-menos="m" aria-label="Una sesión de manos menos">−</button><output data-n="m">1</output><button type="button" data-mas="m" aria-label="Una sesión de manos más">+</button></div>
      </div>
      <p class="suave por-separado">¿Solo una cosa? También puedes hacer cada una por separado: <a href="{base}maderoterapia-cordoba/">maderoterapia</a>, <a href="{base}masajes-cordoba/">masajes</a> o <a href="{base}entrenamiento-personal-mujeres-cordoba/">entrenamiento</a>.</p>
      <div class="cuenta">
        <div class="total"><span>Te saldría por unos</span><b><output id="sem-precio">58</output> €</b><span>a la semana</span></div>
        <ul id="sem-desglose"></ul>
        <a class="btn" id="sem-wa" href="{wa('Hola Mari Carmen, quiero empezar el programa de Siluetas de Mujer. ¿Lo vemos en la valoración?')}">Hablar con Carmen</a>
        <small>Precio aproximado, para orientarte. Tu plan exacto lo cerramos en la valoración, que es gratis.</small>
      </div>
    </div>
  </div>
</div></section>'''


SEMANA_JS = '''(function(){
  var d=document,root=d.querySelector('.semana');if(!root)return;
  var P=%s,D=['lunes','martes','miércoles','jueves','viernes'],M=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
  var ORDEN={g:[1,3,0,2,4],m:[4,2,0,1,3]},MAX={g:5,m:3},N={g:'Entreno en grupo',m:'Masaje o maderoterapia'};
  var cols=[].slice.call(root.querySelectorAll('.dia')),planes=[].slice.call(root.querySelectorAll('[data-plan]'));
  var ses=[],sel=null,pista=root.querySelector('.pista');
  var hoy=new Date();hoy.setHours(0,0,0,0);var lun=new Date(hoy);lun.setDate(lun.getDate()-((hoy.getDay()+6)%%7)+7);
  cols.forEach(function(c,i){var f=new Date(lun);f.setDate(lun.getDate()+i);c.querySelector('.dia-cab b').textContent=f.getDate()});
  root.querySelector('.mes').textContent='· semana del '+lun.getDate()+' de '+M[lun.getMonth()];
  function cuenta(t){return ses.filter(function(s){return s.t===t}).length}
  function enDia(i){return ses.filter(function(s){return s.d===i}).length}
  function libre(t){var o=ORDEN[t];for(var k=0;k<2;k++)for(var j=0;j<o.length;j++)if(enDia(o[j])<=k&&!ses.some(function(s){return s.d===o[j]&&s.t===t}))return o[j];for(j=0;j<5;j++)if(enDia(j)<2)return j;return -1}
  function poner(t,n){while(cuenta(t)<n){var x=libre(t);if(x<0)break;ses.push({t:t,d:x})}while(cuenta(t)>n){for(var i=ses.length-1;i>=0;i--)if(ses[i].t===t){ses.splice(i,1);break}}}
  function plan(b){ses=[];sel=null;poner('g',+b.dataset.g);poner('m',+b.dataset.m);pinta()}
  planes.forEach(function(b){b.onclick=function(){plan(b)}});
  [].forEach.call(root.querySelectorAll('[data-mas],[data-menos]'),function(b){b.onclick=function(){var t=b.dataset.mas||b.dataset.menos,n=cuenta(t)+(b.dataset.mas?1:-1);
    poner(t,Math.max(0,Math.min(MAX[t],n)));sel=null;pinta()}});
  cols.forEach(function(c,i){c.querySelector('[data-mover]').onclick=function(){if(sel===null)return;if(enDia(i)>=2&&ses[sel].d!==i){pista.textContent='Ese día ya tiene dos sesiones. Elige otro.';return}
    ses[sel].d=i;sel=null;pinta()}});
  function pinta(){
    var g=cuenta('g'),m=cuenta('m');
    planes.forEach(function(b){b.setAttribute('aria-pressed',+b.dataset.g===g&&+b.dataset.m===m)});
    root.querySelector('[data-n="g"]').textContent=g;root.querySelector('[data-n="m"]').textContent=m;
    cols.forEach(function(c,i){var h=c.querySelector('.huecos');h.innerHTML='';
      ses.forEach(function(s,k){if(s.d!==i)return;var b=d.createElement('button');b.type='button';b.className='ses '+s.t;b.setAttribute('aria-pressed',sel===k);
        b.innerHTML='<span>'+(s.t==='g'?'Entreno':'Manos')+'</span>';b.setAttribute('aria-label',N[s.t]+' el '+D[i]+'. Tocar para moverla');
        b.onclick=function(){sel=sel===k?null:k;pinta()};h.appendChild(b)});
      if(!enDia(i)){var a=d.createElement('span');a.className='app';a.textContent='app';h.appendChild(a)}
      c.classList.toggle('destino',sel!==null&&ses[sel].d!==i&&enDia(i)<2)});
    pista.textContent=sel===null?'Toca una sesión y después el día al que quieres moverla.':'Ahora toca el día al que la quieres llevar.';
    var e=P.base+g*P.grupo+m*P.manos;root.querySelector('#sem-precio').textContent=e;
    var li=['<li><span>App, entrenos en casa y mi seguimiento</span><b>'+P.base+' €</b></li>'];
    if(g)li.push('<li><span>'+g+' entreno'+(g>1?'s':'')+' en grupo</span><b>'+g*P.grupo+' €</b></li>');
    if(m)li.push('<li><span>'+m+' sesión'+(m>1?'es':'')+' de manos</span><b>'+m*P.manos+' €</b></li>');
    li.push('<li class="mes-eq"><span>Más o menos al mes</span><b>'+Math.round(e*52/12/5)*5+' €</b></li>');
    root.querySelector('#sem-desglose').innerHTML=li.join('');
    var dias=[];ses.slice().sort(function(a,b){return a.d-b.d}).forEach(function(s){dias.push(D[s.d]+': '+(s.t==='g'?'entreno en grupo':'masaje o maderoterapia'))});
    var p=planes.filter(function(b){return b.getAttribute('aria-pressed')==='true'})[0];
    var txt='Hola Mari Carmen, he montado mi semana en la web de Siluetas de Mujer'+(p?' ('+p.querySelector('b').textContent+')':'')+':\\n'+
      (dias.length?dias.join('\\n'):'solo la app, entrenando en casa')+'\\nMe sale por unos '+e+' € a la semana. ¿Lo vemos en la valoración?';
    root.querySelector('#sem-wa').href='https://wa.me/34646437371?text='+encodeURIComponent(txt)}
  plan(planes.filter(function(b){return b.getAttribute('aria-pressed')==='true'})[0]||planes[0]);
})();''' % ('{"base":%d,"grupo":%d,"manos":%d}' % (PRECIO['base'], PRECIO['grupo'], PRECIO['manos']))


def pagina(base, titulo, desc, cuerpo, actual='', extra_js='', ld=''):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{titulo}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="{base}img/silueta.svg" type="image/svg+xml">
<link rel="preload" href="{base}fonts/figtree-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}css/v3.css">
{ld}
</head>
<body>
{cabecera(base, actual)}
<main id="contenido">
{cuerpo}
</main>
{pie(base)}
<script>
(function(){{
  var d=document;d.documentElement.classList.add('js');
  var els=d.querySelectorAll('.camino,.pasos-h,.hilo,.sube');
  if(!('IntersectionObserver' in window)){{els.forEach(function(e){{e.classList.add('visto')}});return}}
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('visto');io.unobserve(e.target)}}}})}},{{rootMargin:'0px 0px -12% 0px'}});
  els.forEach(function(e){{io.observe(e)}});
}})();
{SEMANA_JS}
{extra_js}
</script>
</body>
</html>
'''


# ── Portada ─────────────────────────────────────────────────────────────────
MAPA_JS = '''(function(){
  var d=document,zs=[].slice.call(d.querySelectorAll('[data-z]')),ps=[].slice.call(d.querySelectorAll('.panel'));if(!zs.length)return;
  function ver(z){ps.forEach(function(p){p.hidden=p.id!=='p-'+z});
    zs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.z===z)})}
  zs.forEach(function(b){b.setAttribute('aria-controls','p-'+b.dataset.z);b.onclick=function(){ver(b.dataset.z)}});
  ver(zs[3].dataset.z);
})();'''


def portada():
    b = ''
    zonas, extra, paneles = '', '', ''
    for i, (u, t, g, rr, f, y) in enumerate(AYUDAS, 1):
        if y is not None:
            zonas += f'<button class="zona" type="button" data-z="{u}" style="left:50%;top:{y / 152 * 100:.1f}%"><i>{i}</i><span>{ZONA[u]}</span></button>'
        else:
            extra += f'<button type="button" data-z="{u}"><i>{i}</i>No es una zona: quiero empezar a moverme</button>'
        paneles += (f'<div class="panel" id="p-{u}">{foto(f, b)}<div><p class="suave" style="margin:0">{i} · {ZONA.get(u, "Empezar")}</p>'
                    f'<h3 class="globo-h">{t}<small>Lo que me escribís</small></h3><p class="lead">{g}</p>'
                    f'<div class="mini-bal" style="--p:{AYUDA[u]["p"]}%"><div class="barra"><i></i><i></i></div>'
                    f'<p><span class="rama m">Manos {AYUDA[u]["p"]} %</span><span class="rama v">Movimiento {100 - AYUDA[u]["p"]} %</span></p></div>'
                    f'<a class="btn" href="{u}/">Ver cómo te ayudo</a></div></div>')
    extra += f'<a href="{wa("Hola Mari Carmen, no tengo claro por dónde empezar. ¿Me orientas?")}"><i>6</i>No lo tengo claro: oriéntame tú por WhatsApp</a>'
    cuerpo = f'''
<section class="portada">
  <div class="firma">
    <h1>
      <span class="lado izq">Tu silueta, por fuera<small>con las manos</small></span>
      <span class="sil" aria-hidden="true">{SIL}<span class="tapa"></span></span>
      <span class="lado der">y por dentro.<small>con el movimiento</small></span>
    </h1>
  </div>
  <div class="bajo">
    <p class="lead">Soy Mari Carmen Figueras. Masaje, maderoterapia y entrenamiento para mujeres en Córdoba, en mi sala o en tu casa.</p>
    <div class="acciones"><a class="btn" href="#empieza">Empieza por aquí</a><a class="btn linea" href="{wa('Hola Mari Carmen, quiero mi valoración gratuita')}">Pedir valoración gratis</a></div>
    <p class="dato">Lunes a viernes, de 10:00 a 20:00 · Córdoba capital</p>
  </div>
  <div class="tira">{foto('maderoterapia', b, sizes='40vw')}{foto('grupo', b, sizes='33vw')}{foto('piernas', b, sizes='45vw')}</div>
</section>

<section class="seccion"><div class="wrap">
  <p class="frase-xl"><span class="nw"><u class="m">Las manos</u><img class="en-linea" src="img/fotos/maderoterapia-mini.webp" alt="" width="160" height="160" loading="lazy"></span>, para lo que notas pronto. <span class="nw"><u class="v">El movimiento</u><img class="en-linea" src="img/fotos/grupo-mini.webp" alt="" width="160" height="160" loading="lazy"></span>, para lo que se queda.</p>
  <p>Lo que se deshincha con las manos vuelve si el cuerpo no se mueve. Por eso trabajo las dos cosas, con la misma persona siguiéndote.</p>
</div></section>

<section class="seccion" id="empieza"><div class="wrap">
  <div class="tit-sec"><h2>Señálame dónde lo notas.</h2><p>No hace falta que sepas cómo se llama el tratamiento. Toca la zona y te cuento qué haría.</p></div>
  <div class="mapa">
    <div><div class="mapa-sil">{SIL}{zonas}</div><div class="mapa-extra">{extra}</div></div>
    <div>{paneles}</div>
  </div>
</div></section>

{pasos('Así empezamos: tres pasos, siempre los mismos.', 'Antes de vender nada, te miro. La valoración es gratis y sales con tu plan hecho.')}

<section class="ramas2" aria-label="Las dos maneras de trabajar">
  <a class="rama2" href="maderoterapia-cordoba/">{foto('descarga', b, sizes='(max-width: 760px) 100vw, 50vw')}
    <div class="dentro">{RAMA['m']}<h3>Por fuera, con las manos</h3>
      <div class="tarifas"><div><span>Maderoterapia · según zona</span><b>45–65 €</b></div><div><span>Masaje de descarga · 60 min</span><b>35 €</b></div><div><span>Masaje tailandés · 60 min</span><b>40 €</b></div></div>
      <span class="ver">Con bono, desde 40 € la sesión</span></div></a>
  <a class="rama2" href="entrenamiento-personal-mujeres-cordoba/">{foto('entreno', b, sizes='(max-width: 760px) 100vw, 50vw')}
    <div class="dentro">{RAMA['v']}<h3>Por dentro, con el movimiento</h3>
      <div class="tarifas"><div><span>Grupos reducidos</span><b>hasta 5</b></div><div><span>Entrenamiento</span><b>1 a 1</b></div><div><span>En tu casa o en la sala</span><b>+ app</b></div></div>
      <span class="ver">Ver el entrenamiento</span></div></a>
</section>

<section class="seccion honesta"><div class="wrap">
  <div class="tit-sec"><h2>Lo que vas a oír por ahí, y lo que te digo yo.</h2><p>Sin milagros. Con constancia y alguien que te acompaña.</p></div>
  <div class="frases">
    <div class="frase"><s>Elimina la celulitis</s><p>Mejora su aspecto con constancia. <b>Eliminarla, no.</b></p></div>
    <div class="frase"><s>Quema la grasa localizada</s><p>La grasa no se funde con un rodillo. <b>Se pierde con movimiento, comida y tiempo.</b></p></div>
    <div class="frase"><s>Elimina toxinas</s><p>De eso se encargan tu hígado y tus riñones. <b>Lo que sí notas es que desaparece la retención.</b></p></div>
  </div>
</div></section>

<section class="sobre-foto" id="donde">{foto('cuesta', b, sizes='100vw')}
  <div class="wrap"><div class="tarjeta">
    <h2>En mi sala o en tu casa.</h2>
    <p>En Córdoba capital, de lunes a viernes de 10:00 a 20:00.</p>
    <ul class="lista">
      <li><span><b>En la sala</b><br>Un espacio cubierto y tranquilo, con grupos de hasta 5.</span></li>
      <li><span><b>A domicilio</b><br>Llevo la camilla o el material. Solo necesitas un hueco de 2 o 3 metros. En casa el precio cambia según la zona: pregúntame.</span></li>
    </ul>
    <p class="suave" style="margin:1.2rem 0 0">¿No sabes si llego a tu barrio? <a href="{wa('Hola Mari Carmen, ¿llegas a mi barrio?')}">Pregúntame</a>.</p>
  </div></div>
</section>

<section class="seccion"><div class="wrap dos-col">
  <div class="tit-sec"><h2>Lo que me preguntáis antes de venir.</h2><p>Las cuatro dudas que más me llegan.</p>
    <a class="duda" href="{wa('Hola Mari Carmen, tengo una duda: ')}"><span class="globo">¿Y si mi duda no está?</span><span class="globo yo">Escríbeme y te contesto yo, no un bot.<small>Carmen</small></span></a></div>
  <div class="faq">
    <details><summary>¿La valoración es gratis de verdad?</summary><p>Sí. Te miro, hablamos de lo que buscas y te hago tu plan en ese momento. Después decides.</p></details>
    <details><summary>¿Duele la maderoterapia?</summary><p>No debería doler. Puedes notar presión en las zonas más cargadas: uso la que requiere cada zona, ni más ni menos, y me vas diciendo.</p></details>
    <details><summary>¿Tengo que estar en forma para entrenar?</summary><p>No. Empezamos desde donde estás. En grupos de hasta 5 te puedo corregir a ti.</p></details>
    <details><summary>¿Puedo hacer solo masaje o solo entreno?</summary><p>Claro. Cada cosa funciona sola. Juntas se nota más, y te diré con honestidad cuándo te conviene una u otra.</p></details>
  </div>
</div></section>

{semana(b, 'manos', 'Arma tu semana conmigo.')}'''
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"HealthAndBeautyBusiness","name":"Siluetas de Mujer",'
          '"founder":{"@type":"Person","name":"Mari Carmen Figueras"},"description":"Masaje, maderoterapia y entrenamiento para mujeres en Córdoba, en sala o a domicilio.",'
          '"telephone":"+34646437371","areaServed":{"@type":"City","name":"Córdoba"},"address":{"@type":"PostalAddress","addressLocality":"Córdoba","addressCountry":"ES"},'
          '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"10:00","closes":"20:00"}]}</script>')
    return pagina('', 'Siluetas de Mujer · Masaje, maderoterapia y entrenamiento para mujeres en Córdoba',
                  'Mari Carmen Figueras: masaje, maderoterapia y entrenamiento para mujeres en Córdoba, en su sala o a domicilio. Valoración gratis y un plan hecho para ti.',
                  cuerpo, extra_js=MAPA_JS, ld=ld)


# ── Páginas de ayuda: UNA plantilla, sus objetos ───────────────────────────
AYUDA = {
    'piernas-cansadas-retencion-cordoba': dict(
        titulo='Piernas cansadas e hinchadas al final del día',
        seo='Piernas cansadas y retención de líquidos en Córdoba · Siluetas de Mujer',
        lead='Si los tobillos se marcan con el calcetín y por la tarde las piernas pesan el doble, no estás exagerando.',
        foto='piernas',
        charla=['Hola Carmen. Llego a la noche con las piernas como dos piedras.',
                'Y los tobillos se me marcan con el calcetín. Con este calor, peor.',
                'Trabajo muchas horas de pie. ¿Eso tiene arreglo?'],
        respuesta='Tiene mucho que ver. Con tantas horas de pie, al líquido le cuesta subir, y la pantorrilla, que hace de bomba, se mueve poco. <b>Primero lo aliviamos con las manos, y luego hacemos que la pierna se ayude sola.</b>',
        manos='Maderoterapia y maniobras de drenaje linfático. Desaparece la retención y se nota pronto.',
        mov='Fuerza de piernas y rutinas cortas para que la pantorrilla trabaje y la circulación no dependa solo del masaje.',
        p=62, nota='Al principio pesan más las manos. Después, el movimiento lo sostiene.',
        tiempos=[('Pronto', 'Ligereza', 'Menos hinchazón en pocas sesiones.'),
                 ('Semanas', 'Piernas que aguantan', 'Llegas a la tarde con menos peso.'),
                 ('Se queda', 'Con movimiento', 'Cuando el movimiento entra en tu semana.')],
        aviso='Si la hinchazón es de una sola pierna, duele, está caliente o aparece de golpe, ve antes a tu médico.',
        servicio=('maderoterapia-cordoba', 'La maderoterapia, con precios')),
    'celulitis-cordoba': dict(
        titulo='Celulitis: lo que la maderoterapia puede hacer, y lo que no',
        seo='Celulitis en Córdoba: qué hace de verdad la maderoterapia · Siluetas de Mujer',
        lead='Mejora el aspecto de la piel y la sensación de volumen. No la elimina. Lo que cambia la forma es el músculo de debajo.',
        foto='maderoterapia',
        charla=['Carmen, ¿la maderoterapia quita la celulitis?',
                'Me he gastado un dineral en cremas y nada.',
                'A partir de los 45 se me marca más, y no he cambiado nada.'],
        respuesta='Te digo la verdad: <b>eliminarla, no te la elimina nadie.</b> La tiene casi todo el mundo, y con las hormonas se marca más. La madera mejora mucho cómo se ve y se siente la piel. Y si fortalecemos glúteo y pierna, cambia la forma de la zona.',
        manos='Maderoterapia sobre piernas, glúteos y abdomen, con drenaje antes de empezar. Piel más suave y uniforme, y menos volumen si hay retención.',
        mov='Un glúteo y una pierna más fuertes cambian la forma de la zona. Sentadillas, puentes y escalones, 2 o 3 días por semana.',
        p=50, nota='Aquí van a partes iguales.',
        tiempos=[('Pronto', 'Ligereza', 'Menos volumen si hay retención.'),
                 ('Semanas', 'Piel más uniforme', 'Con constancia en las manos.'),
                 ('8-12 semanas', 'La forma de la zona', 'Con fuerza sostenida.')],
        aviso='No es para ti si estás embarazada, tienes varices importantes, has tenido una trombosis, tomas anticoagulantes o tienes heridas en la zona. Te pregunto siempre por tu salud.',
        servicio=('maderoterapia-cordoba', 'La maderoterapia, con precios')),
    'menopausia-fuerza-cordoba': dict(
        titulo='Menopausia: el cuerpo cambia, y la fuerza es tu mejor aliada',
        seo='Menopausia y entrenamiento de fuerza para mujeres en Córdoba · Siluetas de Mujer',
        lead='La cintura que se ensancha, menos energía, la ropa que cae distinta. No lo estás haciendo peor: el cuerpo cambia. Y se puede hacer mucho.',
        foto='pesa',
        charla=['Carmen, como lo mismo de siempre y la barriga no deja de crecer.',
                'Estoy más cansada y me cuesta hasta levantarme del sofá.',
                '¿Me apunto a algo de cardio y ya?'],
        respuesta='Con la menopausia se pierden músculo y hueso más deprisa, y la grasa se va más al abdomen. <b>No es que lo hagas peor.</b> Lo que mejor lo frena es la fuerza, dos días por semana, cuidando el suelo pélvico. El cardio suma, pero no basta.',
        manos='Masaje y maderoterapia para la hinchazón y la tensión. Te ayudan a sentirte mejor mientras lo demás se construye.',
        mov='Fuerza de cuerpo entero dos días por semana, cuidando el suelo pélvico en cada sesión.',
        p=30, nota='Aquí manda el movimiento. Te lo digo aunque te vendiera más masajes.',
        tiempos=[('Semanas', 'Más fuerza', 'Al cargar la compra o levantarte de la silla.'),
                 ('2-3 meses', 'Más firmeza', 'La ropa empieza a caer distinta.'),
                 ('Se queda', 'Músculo y hábito', 'Lo que construyes, se mantiene.')],
        aviso='Si tienes osteoporosis, artrosis o alguna lesión, lo hablamos en la valoración y, si hace falta, con tu médico o tu fisio.',
        servicio=('entrenamiento-personal-mujeres-cordoba', 'El entrenamiento')),
    'espalda-cuello-cargados-cordoba': dict(
        titulo='Espalda y cuello cargados',
        seo='Espalda y cuello cargados: masaje de descarga en Córdoba · Siluetas de Mujer',
        lead='Hombros subidos, un cuello que no gira y una espalda que avisa al final del día. Primero, soltar. Después, que no vuelva.',
        foto='descarga',
        charla=['Tengo los hombros por las orejas, Carmen.',
                'Me doy un masaje, mejoro, y a la semana estoy igual.',
                '¿Hay algo que dure?'],
        respuesta='Lo que cuentas es muy típico: horas en la misma postura y el estrés van al mismo sitio. <b>El masaje suelta lo que ya está cargado. Para que no vuelva, la espalda necesita fuerza y movilidad.</b> Las dos cosas las llevo yo.',
        manos='Masaje de descarga en camilla (35 €) o tailandés en colchoneta y vestida (40 €). Suelta la tensión y ayuda a descansar.',
        mov='Movilidad y fuerza de espalda para que la postura aguante sola y la tensión no vuelva a la semana.',
        p=62, nota='Al principio, manos. Después, el movimiento lo sostiene.',
        tiempos=[('1.ª sesión', 'Alivio', 'Y mejor descanso esa misma noche.'),
                 ('Semanas', 'Se carga menos', 'Con movilidad en tu semana.'),
                 ('Se queda', 'Una espalda que aguanta', 'Con fuerza, no solo con masaje.')],
        aviso='Si el dolor baja por el brazo o la pierna, notas hormigueo o viene de un golpe, ve antes a tu médico.',
        servicio=('masajes-cordoba', 'Los masajes, con precios')),
    'empezar-a-entrenar-cordoba': dict(
        titulo='Quiero empezar a moverme, pero no estoy en forma',
        seo='Empezar a entrenar sin estar en forma: entrenadora para mujeres en Córdoba · Siluetas de Mujer',
        lead='No hace falta. Empezamos desde donde estás hoy, no desde donde estabas hace veinte años.',
        foto='cuesta',
        charla=['Carmen, hace años que no hago nada de deporte.',
                'Un gimnasio lleno de gente me da muchísimo corte.',
                'Lo intenté una vez, me pasé y lo dejé a las dos semanas.'],
        respuesta='Casi siempre se deja por empezar demasiado fuerte o sola. <b>El primer día te mido y ajusto cada ejercicio a ti.</b> En grupos de hasta 5, te corrijo a ti, no a una fila. Y si no te apetece sala, voy a tu casa.',
        manos='Si llegas con el cuerpo cargado, una sesión de masaje a tiempo hace que el entreno se lleve mejor.',
        mov='Grupo de hasta 5, 1 a 1 o en tu casa. Dos días de fuerza a la semana para empezar, y tus entrenos en la app.',
        p=20, nota='Aquí el movimiento lleva casi todo el peso.',
        tiempos=[('Día 1', 'Valoración gratis', 'Te mido y ajustamos cada ejercicio a ti.'),
                 ('Semanas', 'Aprendes sin prisa', 'Los movimientos, la carga y tu ritmo.'),
                 ('2-3 meses', 'Fuerza y ganas', 'Subes la Cuesta del Bailío sin pararte.')],
        aviso='Si tienes alguna lesión o tomas medicación, lo hablamos el primer día para adaptar cada ejercicio.',
        servicio=('entrenamiento-personal-mujeres-cordoba', 'El entrenamiento')),
}


def curvas(p):
    """Dos curvas: lo que hacen las manos (pronto) y lo que construye el movimiento (se queda).
    p = peso de las manos al principio (0-100)."""
    a = 40 - p * .32           # altura inicial de las manos (más p → más alta)
    m0 = 40 - (100 - p) * .12  # el movimiento arranca bajo y sube
    manos = f'M0 40 L0 {a:.1f} C 60 {a - 4:.1f}, 110 {a + 6:.1f}, 300 {min(36, a + 16):.1f} L300 40Z'
    mov = f'M0 40 L0 {m0:.1f} C 80 {m0 - 2:.1f}, 150 14, 300 4 L300 40Z'
    return f'''<div class="curvas">
  <div class="ley">{RAMA['m']}{RAMA['v']}</div>
  <svg viewBox="0 0 300 40" preserveAspectRatio="none" role="img" aria-label="Las manos se notan pronto; el movimiento crece y se queda"><path d="{mov}" fill="#16A39A" opacity=".85"/><path d="{manos}" fill="#D93A7A" opacity=".8"/></svg>'''


def ayuda(slug):
    a = AYUDA[slug]
    b = '../'
    hilo = ''.join(f'<p class="globo">{t}<small>12:4{i}</small></p>' for i, t in enumerate(a['charla'], 1))
    hilo += f'<p class="globo yo">{a["respuesta"]}<small>Carmen · 12:52</small></p>'
    ejes = ''.join(f'<div><b>{t}</b><h3>{h}</h3><p>{p}</p></div>' for t, h, p in a['tiempos'])
    otras = ''.join(f'<li><a href="{b}{u}/"><img src="{b}img/fotos/{f}-mini.webp" alt="" width="80" height="80" loading="lazy"><span>{t}</span></a></li>'
                    for u, t, _, _, f, _ in AYUDAS if u != slug)
    su, st = a['servicio']
    p = a['p']
    cuerpo = f'''
<section class="abre">{foto(a['foto'], b, carga='eager', sizes='100vw')}
  <div class="wrap">
    <p class="miga"><a href="{b}">Inicio</a> · <a href="{b}#empieza">Te ayudo con</a></p>
    <h1>{a['titulo']}</h1>
    <p class="lead">{a['lead']}</p>
    <div class="acciones"><a class="btn" href="{wa('Hola Mari Carmen, te escribo por: ' + a['titulo'].lower())}">Cuéntame qué notas</a><a class="btn linea" href="#pasos">Cómo empezamos</a></div>
  </div>
</section>

<section class="seccion"><div class="wrap charla">
  <div class="tit-sec"><h2>Lo que me contáis, y lo que os digo.</h2><p>Así empiezan casi todas las conversaciones por WhatsApp. Y así respondo.</p></div>
  <div class="hilo"><p class="quien">Hoy</p>{hilo}</div>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Qué hacemos: por fuera y por dentro.</h2><p>Lo que cambia es cuánto pesa cada lado en tu caso.</p></div>
  <div class="balanza-xl" style="--p:{p}%">
    <div class="lado-b m"><span class="pc">{p}%</span></div><div class="lado-b v"><span class="pc">{100 - p}%</span></div>
    <div class="barra" aria-hidden="true"><i></i><i></i></div>
    <div class="lado-b m">{RAMA['m']}<p>{a['manos']}</p></div><div class="lado-b v">{RAMA['v']}<p>{a['mov']}</p></div>
  </div>
  <p class="balanza-nota">{a['nota']} Es orientativo: en la valoración lo ajustamos a ti.</p>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Cuándo se nota.</h2><p>Las manos se notan pronto. El movimiento tarda más, pero es lo que se queda.</p></div>
  {curvas(p)}
  <div class="ejes">{ejes}</div></div>
  <div class="aviso"><p>{a['aviso']}</p></div>
  <p style="margin-top:1.5rem"><a class="enlace" href="{b}{su}/">{st}</a></p>
</div></section>

{pasos()}
{semana(b, 'deporte' if su.startswith('entrenamiento') else 'manos')}

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2 style="font-size:1.6rem">Otras cosas en las que te ayudo</h2></div>
  <ul class="otras-ay">{otras}</ul>
</div></section>'''
    return pagina(b, a['seo'], a['lead'], cuerpo)


# ── Servicios ───────────────────────────────────────────────────────────────
LAMINA = [
    ('Rodillo de esferas', 'La pieza más versátil: piernas, glúteos, abdomen o brazos, según lo que pida cada zona.',
     '<g class="f"><circle cx="46" cy="46" r="13"/><circle cx="72" cy="46" r="13"/><circle cx="98" cy="46" r="13"/><circle cx="124" cy="46" r="13"/><circle cx="150" cy="46" r="13"/><circle cx="176" cy="46" r="13"/></g><g class="l"><circle cx="46" cy="46" r="13"/><circle cx="72" cy="46" r="13"/><circle cx="98" cy="46" r="13"/><circle cx="124" cy="46" r="13"/><circle cx="150" cy="46" r="13"/><circle cx="176" cy="46" r="13"/><path d="M30 46h-4v14q0 6 6 6h78v30"/><path d="M192 46h4v14q0 6-6 6h-78"/><rect x="102" y="96" width="16" height="34" rx="7"/></g>'),
    ('Copa sueca', 'Un efecto de succión parecido al de la ventosa, para trabajar la piel de naranja.',
     '<path class="f" d="M100 16h20v14c0 6 5 9 5 15 0 14 30 34 30 62 0 8-5 13-12 13H77c-7 0-12-5-12-13 0-28 30-48 30-62 0-6 5-9 5-15z"/><path class="l" d="M100 16h20v14c0 6 5 9 5 15 0 14 30 34 30 62 0 8-5 13-12 13H77c-7 0-12-5-12-13 0-28 30-48 30-62 0-6 5-9 5-15z"/><path class="l" d="M68 106h84"/><ellipse class="l" cx="110" cy="16" rx="10" ry="3.5"/>'),
    ('Tabla moldeadora', 'Su perfil de ondas cubre zonas amplias, como el abdomen y los costados.',
     '<path class="f" d="M24 86c10-22 20-22 30 0s20 22 30 0 20-22 30 0 20 22 30 0 20-22 30 0 16 18 22 6v18H24z"/><path class="l" d="M24 86c10-22 20-22 30 0s20 22 30 0 20-22 30 0 20 22 30 0 20-22 30 0 16 18 22 6"/><path class="l" d="M24 86v18h172v-18"/><path class="l" d="M84 104v14q0 6 6 6h40q6 0 6-6v-14"/>'),
]


def madero():
    b = '../'
    lam = ''.join(f'<div class="pieza"><svg viewBox="0 0 220 140" aria-hidden="true">{s}</svg><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d, s in LAMINA)
    sem = [['1', '2'], ['3', '4'], ['5', '6'], ['7', '8'], ['9'], [], ['10'], [], ['M'], [], ['M'], []]
    cal = ''.join('<div class="sem"><small>S' + str(i) + '</small>' +
                  ''.join(f'<i class="{"mant" if x == "M" else ("ya" if x in ("3", "4") else "")}">{x}</i>' for x in s) + '</div>'
                  for i, s in enumerate(sem, 1))
    cuerpo = f'''
<div class="wrap cabeza">
  <div>
    <p class="miga"><a href="{b}">Inicio</a> · Con las manos</p>
    <h1>Maderoterapia en Córdoba, explicada sin humo</h1>
    <p class="lead">Trabajo manual con piezas de madera sobre piernas, glúteos, abdomen y, si quieres, brazos. Para aliviar la pesadez y mejorar el aspecto de la piel.</p>
    <div class="cifras-xl"><div><b>Gratis</b><span>la valoración</span></div><div><b>45–65 €</b><span>la sesión, según la zona</span></div><div><b>40 €</b><span>desde, con bono de 10</span></div></div>
    <div class="acciones" style="margin-top:1.8rem"><a class="btn" href="{wa('Hola Mari Carmen, quiero mi valoración gratuita de maderoterapia')}">Pedir mi valoración gratuita</a><a class="btn linea" href="#precios">Precios y bonos</a></div>
  </div>
  {foto('maderoterapia', b, carga='eager')}
</div>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Tres maderas, tres maniobras.</h2><p>Manual y no invasiva: sin máquinas ni productos químicos. Son mis tres piezas principales, no las únicas: según la zona y lo que necesite, uso otras.</p></div>
  <div class="lamina">{lam}</div>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Te lo digo antes de que reserves.</h2></div>
  <div class="sino">
    <div class="si"><h3>Lo que vas a notar</h3><ul>
      <li><span><b>Piel más suave</b><span>con mejor textura, con constancia.</span></span></li>
      <li><span><b>Ligereza</b><span>sobre todo en las piernas.</span></span></li>
      <li><span><b>Menos hinchazón</b><span>desaparece la retención.</span></span></li>
      <li><span><b>Una hora para ti</b><span>sin prisas y con el móvil lejos.</span></span></li></ul></div>
    <div class="no"><h3>Lo que no es</h3><ul>
      <li><span><b>Un milagro de una sesión</b><span>los cambios van poco a poco.</span></span></li>
      <li><span><b>Un sustituto de moverte</b><span>ni de comer bien: los complementa.</span></span></li>
      <li><span><b>Un tratamiento médico</b><span>no cura ninguna enfermedad.</span></span></li>
      <li><span><b>Igual para todas</b><span>cada cuerpo responde a su ritmo.</span></span></li></ul></div>
  </div>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Así es tu sesión.</h2><p>Siempre en este orden. Lo que dura depende de las zonas que trabajemos, en la sala o en tu casa.</p></div>
  <div class="regla" style="--cols:5fr 9fr 4fr 30fr 6fr">
    <div class="regla-barra" aria-hidden="true"><span style="background:#16323F">Hablamos</span><span style="background:#B8295F">Drenaje</span><span style="background:#16323F">Aceite</span><span style="background:#D93A7A">Trabajo por zonas</span><span style="background:#16323F">Cierre</span></div>
  </div>
  <div class="regla-pasos" style="--n:5">
    <div style="--c:#16323F"><h3>Hablamos</h3><p>Qué notas y cómo estás de salud.</p></div>
    <div style="--c:#B8295F"><h3>Drenaje</h3><p>Maniobras para activar los ganglios linfáticos. Preparan el cuerpo antes de la madera.</p></div>
    <div style="--c:#16323F"><h3>Aceite</h3><p>Para que la madera deslice.</p></div>
    <div style="--c:#D93A7A"><h3>Trabajo por zonas</h3><p>Cada madera en su zona, con la presión que requiere.</p></div>
    <div style="--c:#16323F"><h3>Cierre</h3><p>Qué te recomiendo hasta la próxima.</p></div>
  </div>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Así se reparte un bono de 10.</h2><p>Un ciclo seguido y, después, mantenimiento. En la valoración te digo cuántas para tu caso.</p></div>
  <div class="calendario" aria-label="Ejemplo: 8 sesiones en 4 semanas, 2 más en las semanas 5 y 7, y mantenimiento cada 15 días">{cal}</div>
  <div class="leyenda"><span>● Ciclo inicial: 1 o 2 por semana</span><span>◉ Hacia la 3.ª o 4.ª se empieza a notar</span><span>○ Mantenimiento: cada 15 días o una vez al mes</span></div>
</div></section>

<section class="seccion" id="precios"><div class="wrap">
  <div class="tit-sec"><h2>Cuánto cuesta.</h2><p>Cuantas más sesiones, menos te cuesta cada una.</p></div>
  <div class="precios-col">
    <div class="recibo">
      <div class="cab-r"><span>Maderoterapia · por sesión</span><img src="{b}img/silueta.svg" alt="" width="16" height="24"></div>
      <div class="linea-r"><b>Valoración y tu plan</b><span class="p">Gratis</span><small>Te miro, te digo qué zonas y cuánto cuesta, y te hago el plan</small></div>
      <div class="linea-r"><b>Sesión suelta</b><span class="p">45–65 €</span><small>Según la zona y el tiempo que necesite</small></div>
      <div class="linea-r"><b>Bono 5 sesiones</b><span class="p">desde 42 €</span><small>3 € menos cada sesión · válido 3 meses</small></div>
      <div class="linea-r"><b>Bono 10 sesiones</b><span class="p">desde 40 €</span><small>5 € menos cada sesión · válido 6 meses</small></div>
      <div class="linea-r"><b>A domicilio</b><span class="p">Pregúntame</span><small>Cambia según la zona de Córdoba</small></div>
    </div>
    <div class="calc-osc">
      <h3>¿Qué te sale mejor?</h3>
      <label for="n-ses" style="display:block;margin-top:1rem">Sesiones que quiero hacer</label>
      <output id="n-val">6</output>
      <input id="n-ses" type="range" min="1" max="20" value="6" style="width:100%;margin:1rem 0">
      <p class="res" id="res" aria-live="polite"></p>
      <p class="suave-osc">Calculado con el precio más bajo y el más alto. El tuyo te lo digo en la valoración.</p>
      <a class="btn" id="calc-wa" href="{wa('Hola Mari Carmen, quiero información de los bonos de maderoterapia')}">Pedírselo a Carmen</a>
    </div>
  </div>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div class="tit-sec"><h2>Para quién no es.</h2><p>Antes de empezar siempre te pregunto por tu salud. Si tienes dudas, consúltalo con tu médico.</p></div>
  <ul class="notas"><li>Si estás embarazada.</li><li>Si tienes cáncer activo o estás en tratamiento.</li><li>Si tienes varices severas o has tenido una trombosis.</li>
    <li>Si tienes alguna enfermedad de la piel en la zona.</li><li>Si tienes problemas de coagulación o tomas anticoagulantes.</li></ul>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div class="tit-sec"><h2>Lo que me preguntáis.</h2></div>
  <div class="faq">
    <details><summary>¿Duele?</summary><p>No debería. Puedes notar presión en las zonas más cargadas. Uso la presión que requiere cada zona: aunque aguantes más, no la subo si no es efectivo. Tiene que sentirse como un trabajo profundo, no como un castigo.</p></details>
    <details><summary>¿Cuánto dura una sesión?</summary><p>Depende de las zonas: por eso el precio va de 45 a 65 €. En la valoración te digo cuánto dura la tuya y cuánto cuesta, antes de empezar.</p></details>
    <details><summary>¿Puedo combinarla con ejercicio?</summary><p>Es lo ideal. La madera trabaja la piel y la retención; el músculo de debajo, que es lo que da forma, lo construye el movimiento. El entrenamiento también lo llevo yo.</p></details>
    <details><summary>¿Tengo que hacer algo antes o después?</summary><p>Antes, bebe agua y ven con la piel limpia, sin cremas. Después, sigue hidratándote y, si puedes, camina un rato.</p></details>
    <details><summary>¿Vienes a casa?</summary><p>Sí, en Córdoba capital. Llevo la camilla y el material; solo necesitas un hueco de unos 2 o 3 metros. A domicilio el precio es otro, porque depende mucho de la zona: pregúntame.</p></details>
  </div>
</div></section>
{pasos()}
{semana(b, 'manos')}'''
    js = '''(function(){
  var r=document.getElementById('n-ses'),v=document.getElementById('n-val'),o=document.getElementById('res'),wa=document.getElementById('calc-wa');if(!r)return;
  function coste(b10,b5,su,P){return b10*10*(P-5)+b5*5*(P-3)+su*P}
  function mejor(n){var best=null;for(var b10=0;b10<=2;b10++)for(var b5=0;b5<=4;b5++){var s=b10*10+b5*5,su=Math.max(0,n-s),e=coste(b10,b5,su,45),t=s+su;
    if(!best||e<best.e||(e===best.e&&t<best.t))best={b10:b10,b5:b5,su:su,e:e,t:t}}best.x=coste(best.b10,best.b5,best.su,65);return best}
  function pinta(){var n=+r.value,b=mejor(n),p=[];if(b.b10)p.push((b.b10>1?b.b10+' × ':'')+'bono 10');if(b.b5)p.push((b.b5>1?b.b5+' × ':'')+'bono 5');
    if(b.su)p.push(b.su+(b.su>1?' sesiones sueltas':' sesión suelta'));var t=p.join(' + ');t=t.charAt(0).toUpperCase()+t.slice(1);v.textContent=n;var sobra=b.t-n;
    o.innerHTML='<b>'+t+'</b><span>Entre '+b.e+' y '+b.x+' €, según la zona: de '+Math.round(b.e/b.t)+' a '+Math.round(b.x/b.t)+' € la sesión.'+(sobra?' Te sobra'+(sobra>1?'n '+sobra:' una')+', y sale más barato que ir justa.':'')+' La valoración, gratis.</span>';
    wa.href='https://wa.me/34646437371?text='+encodeURIComponent('Hola Mari Carmen, quiero hacer '+n+' sesiones de maderoterapia: '+t.toLowerCase()+'. ¿Cuánto me saldría en mi zona?')}
  r.addEventListener('input',pinta);pinta()})();'''
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","name":"Maderoterapia en Córdoba","provider":{"@type":"HealthAndBeautyBusiness","name":"Siluetas de Mujer","telephone":"+34646437371"},'
          '"areaServed":{"@type":"City","name":"Córdoba"},"offers":[{"@type":"AggregateOffer","name":"Sesión de maderoterapia","lowPrice":"45","highPrice":"65","priceCurrency":"EUR"},{"@type":"Offer","name":"Valoración","price":"0","priceCurrency":"EUR"}]}</script>')
    return pagina(b, 'Maderoterapia en Córdoba · precios y bonos · Siluetas de Mujer',
                  'Maderoterapia en Córdoba con rodillo, copa sueca y tabla. Sesión de 45 a 65 € según la zona; con bono, desde 40 € la sesión. Valoración gratis.',
                  cuerpo, 'maderoterapia-cordoba', js, ld)


GENTE = '<i></i>'


def entreno():
    b = '../'
    cuerpo = f'''
<div class="wrap cabeza">
  <div>
    <p class="miga"><a href="{b}">Inicio</a> · Con el movimiento</p>
    <h1>Entrenadora personal para mujeres en Córdoba</h1>
    <p class="lead">Fuerza pensada para el cuerpo de una mujer a partir de los 40, en grupos pequeños, uno a uno o en tu casa.</p>
    <div class="cifras-xl"><div><b>5</b><span>mujeres como máximo</span></div><div><b>2</b><span>días de fuerza a la semana</span></div><div><b>0 €</b><span>la valoración</span></div></div>
    <div class="acciones" style="margin-top:1.8rem"><a class="btn" href="{wa('Hola Mari Carmen, quiero mi valoración gratuita para entrenar')}">Pedir mi valoración gratuita</a><a class="btn linea" href="#formatos">Grupo, 1 a 1 o en casa</a></div>
  </div>
  {foto('grupo', b, carga='eager')}
</div>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>No entrenamos para un espejo. Entrenamos para tu vida.</h2></div>
  <ul class="logros">
    <li>Subir la Cuesta del Bailío <span>sin pararte.</span></li>
    <li>Ir a los Patios en mayo <span>sin que te duelan las rodillas.</span></li>
    <li>Cargar la compra de la Corredera <span>de una vez.</span></li>
    <li>Bailar en la Feria <span>hasta que cierren.</span></li>
    <li>Levantarte del sofá <span>sin apoyar las manos.</span></li>
  </ul>
</div></section>

<section class="seccion" id="formatos"><div class="wrap">
  <div class="tit-sec"><h2>Tres formas de entrenar conmigo.</h2><p>La misma forma de trabajar y la misma app. Cambia cuánta atención tienes y dónde entrenas.</p></div>
  <div class="formatos">
    <div class="formato"><span class="gente" aria-hidden="true">{GENTE * 5}</span><span class="big">Hasta 5</span><h3>Grupo reducido, en la sala</h3><p>Si te motiva entrenar con otras y quieres una rutina fija. Te corrijo a ti, no a una fila.</p></div>
    <div class="formato"><span class="gente" aria-hidden="true"><i class="yo"></i>{GENTE}</span><span class="big">1 a 1</span><h3>Solo tú, en la sala</h3><p>Si empiezas con una lesión o quieres ir a tu ritmo.</p></div>
    <div class="formato"><span class="gente casa" aria-hidden="true"><svg viewBox="0 0 40 34"><path d="M4 16 20 3l16 13M9 13v18h22V13"/><path d="M17 31v-9h6v9"/></svg>{GENTE}</span><span class="big">En casa</span><h3>Voy yo</h3><p>Sola o con una amiga. El material lo llevo yo. En casa el precio es otro, según la zona: pregúntame.</p></div>
  </div>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Una sesión, 50 minutos.</h2><p>Una estructura que se repite, para que sepas a qué vienes. Lo que cambia es la carga, poco a poco.</p></div>
  <div class="regla" style="--cols:8fr 27fr 10fr 5fr">
    <div class="regla-barra" aria-hidden="true"><span style="background:#16323F">Soltar</span><span style="background:#16A39A">Fuerza</span><span style="background:#0A6F69">Equilibrio y juego</span><span style="background:#16323F">Bajar</span></div>
    <div class="regla-escala" aria-hidden="true"><span>0'</span><span>8'</span><span>35'</span><span>45'</span></div>
  </div>
  <div class="regla-pasos" style="--n:4">
    <div style="--c:#16323F"><h3>Soltar</h3><p>Caderas, hombros y respiración.</p></div>
    <div style="--c:#16A39A"><h3>Fuerza</h3><p>Sentadilla a cajón, remo y peso muerto con goma.</p></div>
    <div style="--c:#0A6F69"><h3>Equilibrio y juego</h3><p>Por parejas y con música.</p></div>
    <div style="--c:#16323F"><h3>Bajar</h3><p>Estirar y dos minutos de calma.</p></div>
  </div>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div class="tit-sec"><h2>El primer día no entrenas: te mido.</h2><p>Así, dentro de unas semanas, lo que ha cambiado es un número y no una impresión. Y la valoración es gratis.</p>
    {foto('entreno', b, '4/3')}</div>
  <div class="ficha">
    <div class="cab-r"><span>Valoración · Siluetas de Mujer</span><span>Día 1</span></div>
    <h3>Tu punto de partida</h3>
    <div class="campo"><span>Medidas<small>cintura, cadera, muslo y brazo</small></span><em>cm</em></div>
    <div class="campo"><span>Levantarte de la silla<small>cuántas veces en 30 segundos</small></span><em>veces</em></div>
    <div class="campo"><span>Equilibrio<small>sobre una pierna</small></span><em>seg.</em></div>
    <div class="campo"><span>Movilidad<small>hombros, caderas y espalda</small></span><em>notas</em></div>
    <div class="campo"><span>Tu salud<small>lesiones, suelo pélvico, medicación</small></span><em>notas</em></div>
    <div class="campo"><span>Tu objetivo<small>en tus palabras, tal cual</small></span><em>«…»</em></div>
  </div>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div class="tit-sec"><h2>Y entre clase y clase, tu app.</h2><p>Tus números cada vez que repetimos las pruebas, lo que toca hoy si no vienes, y sesiones cortas de yoga y movilidad para los días de descanso.</p></div>
  <div class="movil" aria-label="Ejemplo de pantalla de la app">
    <div class="top"><span>Siluetas</span><span>Semana 6</span></div>
    <p class="tit-m">Tus medidas</p>
    <div class="dos"><div class="dato-m">Cintura<b>84 cm</b><em>−3</em></div><div class="dato-m">Silla en 30 s<b>14 veces</b><em>+5</em></div></div>
    <svg viewBox="0 0 200 60" aria-hidden="true"><path d="M0 50 L30 46 L60 44 L90 38 L120 34 L150 26 L180 22 L200 16" fill="none" stroke="#16A39A" stroke-width="3" stroke-linecap="round"/></svg>
    <ul><li>Sentadilla a cajón · 3 × 10<b>hecho</b></li><li>Remo con goma · 3 × 12<b>hecho</b></li><li>Movilidad de cadera · 8 min<b>hoy</b></li></ul>
    <p class="nota-m">Pantalla de ejemplo</p>
  </div>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div class="tit-sec"><h2>Lo que me preguntáis.</h2></div>
  <div class="faq">
    <details><summary>¿Tengo que estar en forma para empezar?</summary><p>No. El primer día te mido y ajusto cada ejercicio a lo que puedes hacer hoy.</p></details>
    <details><summary>Tengo artrosis, osteoporosis o dolor de espalda. ¿Puedo?</summary><p>En la mayoría de casos, la fuerza bien adaptada ayuda. Lo hablamos en la valoración y, si hace falta, con tu médico o tu fisio.</p></details>
    <details><summary>¿Me voy a poner «grande»?</summary><p>No. Lo que vas a notar es firmeza, fuerza y que la ropa te cae distinta.</p></details>
    <details><summary>¿Sirve si estoy en la menopausia?</summary><p>Es justo cuando más sirve: la fuerza es lo que mejor frena la pérdida de músculo y hueso. Y cuidamos el suelo pélvico en cada sesión.</p></details>
    <details><summary>¿Qué tengo que llevar?</summary><p>Ropa cómoda, zapatillas y agua. El material lo pongo yo, también en tu casa.</p></details>
  </div>
</div></section>
{pasos()}
{semana(b, 'deporte')}'''
    return pagina(b, 'Entrenadora personal para mujeres en Córdoba · Siluetas de Mujer',
                  'Entrenamiento de fuerza para mujeres a partir de los 40 en Córdoba: grupos de hasta 5, 1 a 1 o en tu casa. Valoración gratis y app con tus medidas.',
                  cuerpo, 'entrenamiento-personal-mujeres-cordoba')


def masajes():
    b = '../'
    s, n = '<span class="s"></span><span class="vh">sí</span>', '<span class="n"></span><span class="vh">no</span>'
    filas = [('Movilidad y flexibilidad', 1, 0, 0), ('Aliviar la tensión muscular', 1, 1, 0), ('Descanso y relajación profunda', 0, 1, 0),
             ('Trabajar una zona concreta', 0, 1, 1), ('Piernas más ligeras', 0, 0, 1), ('Mejorar el aspecto de la piel', 0, 0, 1)]
    tabla = ''.join(f'<tr><td>{f}</td>' + ''.join(f'<td>{s if x else n}</td>' for x in xs) + '</tr>' for f, *xs in filas)
    cuerpo = f'''
<div class="wrap cabeza">
  <div>
    <p class="miga"><a href="{b}">Inicio</a> · Con las manos</p>
    <h1>Masajes en Córdoba para la tensión que se acumula</h1>
    <p class="lead">Dos masajes de 60 minutos, muy distintos entre sí. Uno en camilla y con aceite; el otro en colchoneta y vestida. En la sala o en tu casa (a domicilio, pregúntame el precio).</p>
    <div class="cifras-xl"><div><b>35 €</b><span>descarga · 60 min</span></div><div><b>40 €</b><span>tailandés · 60 min</span></div></div>
    <div class="acciones" style="margin-top:1.8rem"><a class="btn" href="{wa('Hola Mari Carmen, quiero reservar un masaje')}">Reservar un masaje</a><a class="btn linea" href="#elijo">¿Cuál elijo?</a></div>
  </div>
  {foto('descarga', b, carga='eager')}
</div>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Dos masajes, muy distintos.</h2><p>Los dos duran 60 minutos. Cambia cómo se hacen y para qué sirven.</p></div>
  <div class="sino">
    <div class="si"><h3>Masaje de descarga · 35 €</h3><p class="suave">Para la espalda que se carga, los hombros subidos y las piernas que llegan pesadas al final de la semana.</p><ul>
      <li><span><b>En camilla</b><span>y con aceite natural.</span></span></li>
      <li><span><b>Presión a tu medida</b><span>de moderada a profunda.</span></span></li>
      <li><span><b>Donde más tensión hay</b><span>ahí me centro.</span></span></li></ul></div>
    <div class="no" style="--c:var(--turq)"><h3>Masaje tailandés · 40 €</h3><p class="suave">Estiramientos como de yoga que hago yo por ti, y presiones rítmicas con manos, codos y pies.</p><ul>
      <li><span><b>En colchoneta</b><span>en el suelo.</span></span></li>
      <li><span><b>Vestida</b><span>con ropa cómoda y sin aceites.</span></span></li>
      <li><span><b>Para la movilidad</b><span>es el que más se nota.</span></span></li></ul></div>
  </div>
</div></section>

<section class="seccion" id="elijo"><div class="wrap dos-col">
  <div class="tit-sec"><h2>¿Cuál elijo?</h2><p>Según lo que buscas. Si dudas, escríbeme y te oriento.</p></div>
  <table class="matriz"><thead><tr><th>Si buscas…</th><th>Tailandés</th><th>Descarga</th><th>Madero­terapia</th></tr></thead><tbody>{tabla}</tbody></table>
</div></section>

<section class="sobre-foto">{foto('entreno', b, sizes='100vw')}
  <div class="wrap"><div class="tarjeta">
    <h2>Si la tensión vuelve cada semana.</h2>
    <p>El masaje suelta lo que ya está cargado. Para que no vuelva, la espalda necesita fuerza y movilidad. Eso también lo trabajo yo.</p>
    <div class="otras"><a class="enlace" href="{b}espalda-cuello-cargados-cordoba/">Espalda y cuello cargados</a><a class="enlace" href="{b}entrenamiento-personal-mujeres-cordoba/">El entrenamiento</a></div>
  </div></div>
</section>
{pasos()}
{semana(b, 'manos')}'''
    return pagina(b, 'Masajes en Córdoba: descarga y tailandés · Siluetas de Mujer',
                  'Masaje de descarga (35 €) y masaje tailandés (40 €) en Córdoba, 60 minutos, en sala. También a domicilio, con precio según la zona.',
                  cuerpo, 'masajes-cordoba')


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for h in SALIDA.iterdir():  # vaciar sin borrar la carpeta (puede estar servida)
        shutil.rmtree(h) if h.is_dir() else h.unlink()
    (SALIDA / 'css').mkdir()
    css = (FUENTE / 'v3' / 'estilo.css').read_text(encoding='utf-8') + '\n' + (FUENTE / 'v3' / 'modulos.css').read_text(encoding='utf-8')
    (SALIDA / 'css' / 'v3.css').write_text(css, encoding='utf-8')
    shutil.copytree(RAIZ / 'fonts', SALIDA / 'fonts')
    (SALIDA / 'img').mkdir(exist_ok=True)
    for f in ('silueta.svg', 'silueta-arena.svg'):
        shutil.copy(RAIZ / 'img' / f, SALIDA / 'img' / f)
    preparar_fotos()
    pags = {'index.html': portada(), 'maderoterapia-cordoba/index.html': madero(),
            'entrenamiento-personal-mujeres-cordoba/index.html': entreno(), 'masajes-cordoba/index.html': masajes()}
    for slug in AYUDA:
        pags[f'{slug}/index.html'] = ayuda(slug)
    for ruta, txt in pags.items():
        d = SALIDA / ruta
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_text(txt, encoding='utf-8')
        print('ok', ruta)
    (SALIDA / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')


if __name__ == '__main__':
    main()
