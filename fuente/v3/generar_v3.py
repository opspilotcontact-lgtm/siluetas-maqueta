"""Siluetas de Mujer · v3 «el camino».

Genera TODA la web desde una sola plantilla y unos pocos componentes compartidos
(cabecera, pie, el camino, «Tus 3 pasos», la foto), para que el conjunto sea
coherente por construcción y no a mano.

    python fuente/v3/generar.py [salida]      (por defecto: _v3/)

Datos reales: Figueras Wellness (precios), audios de Carmen del 30-sep
(valoración gratis, sin pack, «certificada», «desaparece la retención»).
Fotos: generadas con Gemini el 1-oct, provisionales e «ilustrativas».
"""
import html
import pathlib
import shutil
import sys

from PIL import Image, ImageEnhance

RAIZ = pathlib.Path(__file__).resolve().parents[2]
SALIDA = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / '_v3'
FUENTE = RAIZ / 'fuente'

WA = 'https://wa.me/34646437371?text='
TEL = '646 437 371'
PL, PR = (RAIZ / 'logo' / 'paths.txt').read_text().split('\n')[:2]


def wa(txt):
    from urllib.parse import quote
    return WA + quote(txt)


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
        # mismo tratamiento para toda la serie: algo menos de color y un velo de arena
        im = ImageEnhance.Color(im).enhance(.88)
        im = Image.blend(im, arena.resize(im.size), .06)
        for w in (1200, 640):
            c = im.copy()
            c.thumbnail((w, w))
            c.save(dst / f'{n}-{w}.webp', 'WEBP', quality=72, method=6)


def foto(n, base, ar=None, carga='lazy'):
    estilo = f' style="--ar:{ar}"' if ar else ''
    prio = ' fetchpriority="high"' if carga == 'eager' else ''
    return (f'<figure class="foto"{estilo}><img src="{base}img/fotos/{n}-1200.webp" '
            f'srcset="{base}img/fotos/{n}-640.webp 640w, {base}img/fotos/{n}-1200.webp 1200w" '
            f'sizes="(max-width: 820px) 100vw, 45vw" width="1200" height="805" alt="{FOTOS[n]}" '
            f'loading="{carga}" decoding="async"{prio}><figcaption>Imagen ilustrativa</figcaption></figure>')


# ── Componentes compartidos ─────────────────────────────────────────────────
AYUDAS = [
    ('piernas-cansadas-retencion-cordoba', 'Acabo el día con las piernas pesadas',
     'Pesadez, tobillos marcados, peor con el calor.', 'mv'),
    ('celulitis-cordoba', 'La piel de naranja me quita las ganas de ponerme según qué',
     'Qué puede hacer la maderoterapia, y qué no.', 'mv'),
    ('menopausia-fuerza-cordoba', 'Con la menopausia, mi cuerpo ya no es el mismo',
     'Cintura, energía y fuerza: lo que se puede hacer.', 'vm'),
    ('espalda-cuello-cargados-cordoba', 'Cargo la espalda y el cuello',
     'Primero soltar. Después, que no vuelva.', 'mv'),
    ('empezar-a-entrenar-cordoba', 'Quiero empezar a moverme, pero no estoy en forma',
     'Empezamos desde donde estás hoy.', 'v'),
]
SERVICIOS = [
    ('maderoterapia-cordoba', 'Maderoterapia'),
    ('entrenamiento-personal-mujeres-cordoba', 'Entrenamiento'),
    ('masajes-cordoba', 'Masajes'),
]
RAMA = {'m': '<span class="rama m">Con las manos</span>', 'v': '<span class="rama v">Con el movimiento</span>'}


def cabecera(base, actual=''):
    nav = [(f'{base}#empieza', 'Empieza aquí', '')] + [(f'{base}{u}/', t, u) for u, t in SERVICIOS] + [(f'{base}#donde', 'Dónde', '')]
    cur = ' aria-current="page"'
    enl = ''.join(f'<a href="{h}"{cur if u and u == actual else ""}>{t}</a>' for h, t, u in nav)
    return f'''<a class="salta" href="#contenido">Saltar al contenido</a>
<div class="franja">Propuesta de web para Siluetas de Mujer, en revisión (v3). Las imágenes son ilustrativas, generadas con IA. <a href="{base}v2/">Ver la v2</a></div>
<header class="cab"><div class="wrap">
  <a class="marca" href="{base}" aria-label="Siluetas de Mujer, inicio"><img src="{base}img/silueta.svg" alt="" width="20" height="30"><span><i>Siluetas</i> de Mujer</span></a>
  <nav class="nav" aria-label="Principal">{enl}</nav>
  <a class="btn" href="{wa('Hola Mari Carmen, te escribo desde la web de Siluetas de Mujer')}">WhatsApp</a>
</div></header>'''


def pie(base):
    ay = ''.join(f'<li><a href="{base}{u}/">{t}</a></li>' for u, t, _, _ in AYUDAS)
    se = ''.join(f'<li><a href="{base}{u}/">{t}</a></li>' for u, t in SERVICIOS)
    return f'''<footer class="pie"><div class="wrap">
  <div><a class="marca" href="{base}"><img src="{base}img/silueta-arena.svg" alt="" width="20" height="30"><span><i>Siluetas</i> de Mujer</span></a>
    <p style="margin-top:1rem">Masaje, maderoterapia y entrenamiento para mujeres en Córdoba. Por Mari Carmen Figueras, entrenadora personal certificada y masajista.</p></div>
  <div><h2>Te ayudo con</h2><ul>{ay}</ul></div>
  <div><h2>Servicios</h2><ul>{se}</ul></div>
  <div><h2>Contacto</h2><ul><li><a href="{wa('Hola Mari Carmen')}">WhatsApp {TEL}</a></li><li>Lunes a viernes, de 10:00 a 20:00</li><li>En mi sala o en tu casa, en Córdoba capital</li></ul></div>
  <div class="legal"><span>© 2026 Siluetas de Mujer</span><span>Aviso legal · Privacidad · Cookies</span></div>
</div></footer>'''


PASOS = '''<ol class="camino">
    <li><h3>Me escribes</h3><p>Por WhatsApp, con tus palabras: qué notas y desde cuándo. Te respondo yo.</p></li>
    <li><h3>Valoración gratis</h3><p>Te mido, hablamos de tu salud y de lo que quieres conseguir. Sin prisas.</p></li>
    <li><h3>Tu plan</h3><p>Con las manos, con el movimiento o con las dos cosas. Te digo qué haría, tú decides, y cada pocas semanas lo revisamos juntas.</p></li>
  </ol>'''


def pasos_fin(titulo='Tus 3 pasos para empezar', texto='Sin compromiso. La valoración es gratis y el plan lo decides tú.', msg='Hola Mari Carmen, quiero mi valoración gratuita'):
    """El bloque común: cierra TODAS las páginas con los mismos 3 pasos."""
    return f'''<section class="seccion" id="pasos"><div class="wrap pasos-fin">
  <div class="tit-sec" style="margin:0"><h2>{titulo}</h2><p>{texto}</p>
    <div class="acciones"><a class="btn" href="{wa(msg)}">Pedir mi valoración gratuita</a></div></div>
  {PASOS}
</div></section>'''


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
  var els=d.querySelectorAll('.camino,.sube');
  if(!('IntersectionObserver' in window)){{els.forEach(function(e){{e.classList.add('visto')}});return}}
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('visto');io.unobserve(e.target)}}}})}},{{rootMargin:'0px 0px -12% 0px'}});
  els.forEach(function(e){{io.observe(e)}});
}})();
{extra_js}
</script>
</body>
</html>
'''


# ── Portada ─────────────────────────────────────────────────────────────────
def portada():
    b = ''
    opciones = ''.join(
        f'<li><a href="{u}/"><span class="n">{i}</span><span><b>{t}</b><span class="d">{d}</span>'
        f'<span class="ramas">{"".join(RAMA[r] for r in rr)}</span></span><span class="ir" aria-hidden="true">→</span></a></li>'
        for i, (u, t, d, rr) in enumerate(AYUDAS, 1))
    opciones += (f'<li><a href="{wa("Hola Mari Carmen, no tengo claro por dónde empezar. ¿Me orientas?")}"><span class="n">6</span>'
                 '<span><b>No lo tengo claro: oriéntame tú</b><span class="d">Escríbeme y te digo por dónde empezaría.</span></span>'
                 '<span class="ir" aria-hidden="true">→</span></a></li>')
    cuerpo = f'''
<section class="portada">
  <div class="firma">
    <h1>
      <span class="lado izq">Tu silueta, por fuera<small>con las manos</small></span>
      <span class="sil" aria-hidden="true"><svg viewBox="0 0 100 152"><path fill="#D93A7A" d="{PL}"/><path fill="#16A39A" d="{PR}"/></svg><span class="tapa"></span></span>
      <span class="lado der">y por dentro.<small>con el movimiento</small></span>
    </h1>
  </div>
  <div class="bajo">
    <p class="lead">Soy Mari Carmen Figueras. Masaje, maderoterapia y entrenamiento para mujeres en Córdoba, en mi sala o en tu casa.</p>
    <div class="acciones"><a class="btn" href="#empieza">Empieza por aquí</a><a class="btn linea" href="{wa('Hola Mari Carmen, quiero mi valoración gratuita')}">Pedir valoración gratis</a></div>
    <p class="dato">Lunes a viernes, de 10:00 a 20:00 · Córdoba capital</p>
  </div>
</section>

<section class="seccion" id="empieza"><div class="wrap">
  <div class="tit-sec"><h2>¿Qué te trae por aquí?</h2><p>No hace falta que sepas cómo se llama el tratamiento. Elige lo que más se parece a lo que notas y te cuento qué haría.</p></div>
  <div class="trae">
    <ol class="opciones">{opciones}</ol>
    {foto('grupo', b)}
  </div>
</div></section>

<section class="seccion"><div class="wrap empezamos">
  <div>
    <div class="tit-sec"><h2>Así empezamos: tres pasos, siempre los mismos.</h2><p>Antes de vender nada, te miro. La valoración es gratis y sales con tu plan hecho.</p></div>
    {PASOS}
    <div class="acciones" style="margin-top:2rem"><a class="btn" href="{wa('Hola Mari Carmen, quiero mi valoración gratuita')}">Pedir mi valoración gratuita</a></div>
  </div>
  {foto('maderoterapia', b, '4/5')}
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Dos maneras de cuidarte, una misma persona.</h2><p>Lo que se deshincha con las manos vuelve si el cuerpo no se mueve. Por eso trabajo las dos cosas. Puedes venir solo por una.</p></div>
  <div class="maneras">
    <div class="manera">
      {foto('descarga', b)}
      {RAMA['m']}
      <h3>Por fuera, con las manos</h3>
      <ul class="lista">
        <li><span><b>Maderoterapia</b><br>60 min, piernas, glúteos y abdomen</span><span class="precio">40 €</span></li>
        <li><span><b>Masaje de descarga</b><br>60 min, en camilla</span><span class="precio">35 €</span></li>
        <li><span><b>Masaje tailandés</b><br>60 min, en colchoneta y vestida</span><span class="precio">40 €</span></li>
      </ul>
      <p class="suave" style="margin:0">Bonos de maderoterapia desde 32 € la sesión.</p>
      <div class="otras"><a class="enlace" href="maderoterapia-cordoba/">La maderoterapia</a><a class="enlace" href="masajes-cordoba/">Los masajes</a></div>
    </div>
    <div class="manera">
      {foto('entreno', b, '4/5')}
      {RAMA['v']}
      <h3>Por dentro, con el movimiento</h3>
      <ul class="lista">
        <li><span><b>Grupos de hasta 5 mujeres</b><br>Te corrijo a ti, no a una fila</span></li>
        <li><span><b>Entrenamiento 1 a 1</b><br>En la sala o en tu casa</span></li>
        <li><span><b>Tu app</b><br>Medidas, progreso y entrenos para casa</span></li>
      </ul>
      <div class="otras"><a class="enlace" href="entrenamiento-personal-mujeres-cordoba/">El entrenamiento</a></div>
    </div>
  </div>
</div></section>

<section class="seccion honesta"><div class="wrap">
  <div class="tit-sec"><h2>Lo que vas a oír por ahí, y lo que te digo yo.</h2><p>Sin milagros. Con constancia y alguien que te acompaña.</p></div>
  <div class="frases">
    <div class="frase"><s>«Elimina la celulitis»</s><p>Mejora su aspecto con constancia. <b>Eliminarla, no.</b></p></div>
    <div class="frase"><s>«Quema la grasa localizada»</s><p>La grasa no se funde con un rodillo. <b>Se pierde con movimiento, comida y tiempo.</b></p></div>
    <div class="frase"><s>«Elimina toxinas»</s><p>De eso se encargan tu hígado y tus riñones. <b>Lo que sí notas es que desaparece la retención.</b></p></div>
  </div>
</div></section>

<section class="seccion" id="donde"><div class="wrap donde">
  <div>
    <div class="tit-sec"><h2>En mi sala o en tu casa.</h2><p>En Córdoba capital, de lunes a viernes de 10:00 a 20:00.</p></div>
    <ul class="lista">
      <li><span><b>En la sala</b><br>Un espacio cubierto y tranquilo, con grupos de hasta 5.</span></li>
      <li><span><b>A domicilio</b><br>Llevo la camilla o el material. Solo necesitas un hueco de 2 o 3 metros.</span></li>
    </ul>
    <p class="suave" style="margin-top:1.2rem">¿No sabes si llego a tu barrio? <a href="{wa('Hola Mari Carmen, ¿llegas a mi barrio?')}">Pregúntame</a> y te lo digo.</p>
  </div>
  {foto('cuesta', b)}
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Lo que me preguntáis antes de venir.</h2></div>
  <div class="faq">
    <details><summary>¿La valoración es gratis de verdad?</summary><p>Sí. Te miro, hablamos de lo que buscas y te hago tu plan en ese momento. Después decides.</p></details>
    <details><summary>¿Duele la maderoterapia?</summary><p>No debería doler. Puedes notar presión en las zonas más cargadas, pero la intensidad se adapta a ti y me vas diciendo.</p></details>
    <details><summary>¿Tengo que estar en forma para entrenar?</summary><p>No. Empezamos desde donde estás. En grupos de hasta 5 te puedo corregir a ti.</p></details>
    <details><summary>¿Puedo hacer solo masaje o solo entreno?</summary><p>Claro. Cada cosa funciona sola. Juntas se nota más, y te diré con honestidad cuándo te conviene una u otra.</p></details>
  </div>
</div></section>

<section class="seccion cierre"><div class="wrap">
  <svg viewBox="0 0 100 152" aria-hidden="true"><path fill="#D93A7A" d="{PL}"/><path fill="#16A39A" d="{PR}"/></svg>
  <h2>Cuéntame qué notas. Te respondo yo.</h2>
  <div class="acciones"><a class="btn" href="{wa('Hola Mari Carmen, te escribo desde la web de Siluetas de Mujer')}">Escribir a Carmen</a><a class="btn linea" href="#empieza">Volver a empezar</a></div>
</div></section>'''
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"HealthAndBeautyBusiness","name":"Siluetas de Mujer",'
          '"founder":{"@type":"Person","name":"Mari Carmen Figueras"},"description":"Masaje, maderoterapia y entrenamiento para mujeres en Córdoba, en sala o a domicilio.",'
          '"telephone":"+34646437371","areaServed":{"@type":"City","name":"Córdoba"},"address":{"@type":"PostalAddress","addressLocality":"Córdoba","addressCountry":"ES"},'
          '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"10:00","closes":"20:00"}]}</script>')
    return pagina('', 'Siluetas de Mujer · Masaje, maderoterapia y entrenamiento para mujeres en Córdoba',
                  'Mari Carmen Figueras: masaje, maderoterapia y entrenamiento para mujeres en Córdoba, en su sala o a domicilio. Valoración gratis y un plan hecho para ti.',
                  cuerpo, ld=ld)


# ── Páginas de ayuda: UNA plantilla ─────────────────────────────────────────
AYUDA = {
    'piernas-cansadas-retencion-cordoba': dict(
        titulo='Piernas cansadas e hinchadas al final del día',
        seo='Piernas cansadas y retención de líquidos en Córdoba · Siluetas de Mujer',
        lead='Si los tobillos se marcan con el calcetín y por la tarde las piernas pesan el doble, no estás exagerando. Esto es lo que hacemos, y lo que puedes esperar.',
        foto='piernas',
        notas=['Pesadez que va a más según avanza el día.', 'Tobillos que se marcan con el calcetín.',
               'Peor con el calor de Córdoba y con muchas horas de pie o sentada.', 'Llegas a la noche y las piernas no descansan.'],
        porque='Con muchas horas de pie o sentada, al líquido le cuesta subir. La pantorrilla hace de bomba: si se mueve poco, la pierna se carga. Con el calor se nota todavía más.',
        manos='Maderoterapia y maniobras de drenaje, siempre de abajo arriba. La ligereza se suele notar desde las primeras sesiones: desaparece la retención.',
        mov='Fuerza de piernas y rutinas cortas para que la pantorrilla trabaje y la circulación no dependa solo del masaje.',
        p=62, balanza='Al principio pesan más las manos. Después, el movimiento lo sostiene.',
        tiempos=[('Pronto', 'Ligereza', 'Menos hinchazón en pocas sesiones.'),
                 ('Semanas', 'Piernas que aguantan', 'Llegas a la tarde con menos peso.'),
                 ('Se queda', 'Con movimiento', 'Cuando el movimiento entra en tu semana.')],
        aviso='Si la hinchazón es de una sola pierna, duele, está caliente o aparece de golpe, ve antes a tu médico.',
        servicio=('maderoterapia-cordoba', 'La maderoterapia, con precios')),
    'celulitis-cordoba': dict(
        titulo='Celulitis: lo que la maderoterapia puede hacer, y lo que no',
        seo='Celulitis en Córdoba: qué hace de verdad la maderoterapia · Siluetas de Mujer',
        lead='Mejora el aspecto de la piel y la sensación de volumen, sobre todo si hay retención. No la elimina. Lo que cambia la forma de la zona es el músculo de debajo.',
        foto='maderoterapia',
        notas=['Piel de naranja en muslos y glúteos, más marcada al apretar.', 'Sensación de volumen o de piel poco firme.',
               'Se nota más a partir de los 45, aunque no hayas cambiado nada.'],
        porque='La tiene la gran mayoría de las mujeres adultas. No es una enfermedad ni una señal de dejadez: tiene que ver con cómo se organiza la grasa bajo la piel en el cuerpo de la mujer, con las hormonas y con la circulación.',
        manos='Maderoterapia sobre piernas, glúteos y abdomen, en dirección al drenaje. Piel más suave y uniforme al tacto, y menos volumen cuando hay retención.',
        mov='Un glúteo y una pierna más fuertes cambian la forma de la zona. Sentadillas, puentes y subidas a un escalón, con cargas que suben poco a poco, 2 o 3 días por semana.',
        p=50, balanza='Aquí van a partes iguales.',
        tiempos=[('Pronto', 'Ligereza', 'Menos volumen si hay retención, en las primeras sesiones.'),
                 ('Semanas', 'Piel más uniforme', 'Con constancia en las manos.'),
                 ('8-12 sem.', 'La forma de la zona', 'Con fuerza sostenida.')],
        aviso='No es para ti si estás embarazada, tienes varices importantes, has tenido una trombosis, tomas anticoagulantes o tienes heridas en la zona. Te pregunto siempre por tu salud antes de empezar.',
        servicio=('maderoterapia-cordoba', 'La maderoterapia, con precios')),
    'menopausia-fuerza-cordoba': dict(
        titulo='Menopausia: el cuerpo cambia, y la fuerza es tu mejor aliada',
        seo='Menopausia y entrenamiento de fuerza para mujeres en Córdoba · Siluetas de Mujer',
        lead='La cintura que se ensancha, menos energía, la ropa que cae distinta. No lo estás haciendo peor: el cuerpo cambia. Y se puede hacer mucho.',
        foto='pesa',
        notas=['La barriga y la cintura cambian aunque comas igual.', 'Menos fuerza para cargar o levantarte.',
               'Más cansancio y peor descanso.', 'Hinchazón que va y viene.'],
        porque='Con la bajada de estrógenos se pierden músculo y hueso más deprisa, y la grasa tiende a colocarse más en el abdomen. El músculo no duele cuando se va: por eso cuesta notarlo hasta que falta.',
        manos='Masaje y maderoterapia para la hinchazón y la tensión. Te ayudan a sentirte mejor mientras lo demás se construye.',
        mov='Fuerza de cuerpo entero dos días por semana, cuidando el suelo pélvico en cada sesión. Es lo que mejor frena la pérdida de músculo y de hueso.',
        p=30, balanza='Aquí manda el movimiento. Te lo digo aunque te vendiera más masajes.',
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
        notas=['Cuello y hombros duros.', 'Una espalda que se queja después de un día largo.',
               'Descansas, pero no descansas.', 'La tensión vuelve cada semana.'],
        porque='Muchas horas en la misma postura, cargar peso y el estrés se acumulan en el mismo sitio. El masaje suelta lo que ya está cargado. Para que no vuelva, la espalda necesita fuerza y movilidad.',
        manos='Masaje de descarga en camilla (35 €) o tailandés en colchoneta y vestida (40 €). Suelta la tensión y ayuda a descansar.',
        mov='Movilidad y fuerza de espalda para que la postura aguante sola y la tensión no vuelva a la semana.',
        p=62, balanza='Al principio, manos. Después, el movimiento lo sostiene.',
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
        notas=['Hace años que no haces deporte.', 'Un gimnasio lleno te da corte.',
               'No sabes por dónde empezar ni si te vas a hacer daño.', 'Lo intentaste y lo dejaste.'],
        porque='Casi siempre se deja por empezar demasiado fuerte o sola. Con alguien que te mide el primer día y ajusta cada ejercicio a ti, es mucho más fácil seguir.',
        manos='Si llegas con el cuerpo cargado, una sesión de masaje a tiempo hace que el entreno se lleve mejor.',
        mov='En grupos de hasta 5 mujeres, 1 a 1 o en tu casa. Dos días de fuerza a la semana para empezar, y tus entrenos en la app.',
        p=20, balanza='Aquí el movimiento lleva casi todo el peso.',
        tiempos=[('Día 1', 'Valoración gratis', 'Te mido y ajustamos cada ejercicio a ti.'),
                 ('Semanas', 'Aprendes sin prisa', 'Los movimientos, la carga y tu ritmo.'),
                 ('2-3 meses', 'Fuerza y ganas', 'Subes la Cuesta del Bailío sin pararte.')],
        aviso='Si tienes alguna lesión o tomas medicación, lo hablamos el primer día para adaptar cada ejercicio.',
        servicio=('entrenamiento-personal-mujeres-cordoba', 'El entrenamiento')),
}


def ayuda(slug):
    a = AYUDA[slug]
    b = '../'
    notas = ''.join(f'<li>{n}</li>' for n in a['notas'])
    tiempos = ''.join(f'<li data-t="{t}"><h3>{h}</h3><p>{p}</p></li>' for t, h, p in a['tiempos'])
    otras = ''.join(f'<a class="enlace" href="{b}{u}/">{t}</a>' for u, t, _, _ in AYUDAS if u != slug)
    su, st = a['servicio']
    cuerpo = f'''
<div class="wrap cabeza">
  <div>
    <p class="miga"><a href="{b}">Inicio</a> · <a href="{b}#empieza">Te ayudo con</a></p>
    <h1>{a['titulo']}</h1>
    <p class="lead">{a['lead']}</p>
    <div class="acciones"><a class="btn" href="{wa('Hola Mari Carmen, te escribo por: ' + a['titulo'].lower())}">Cuéntame qué notas</a><a class="btn linea" href="#pasos">Cómo empezamos</a></div>
  </div>
  {foto(a['foto'], b, carga='eager')}
</div>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Lo que notas</h2></div><ul class="notas">{notas}</ul></div>
  <div><div class="tit-sec"><h2>Por qué pasa</h2></div><p class="lead">{a['porque']}</p></div>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Qué hacemos</h2><p>Por fuera y por dentro. Lo que cambia es cuánto pesa cada lado.</p></div>
  <div class="hacemos">
    <div class="hace">{RAMA['m']}<p>{a['manos']}</p></div>
    <div class="hace">{RAMA['v']}<p>{a['mov']}</p></div>
  </div>
  <div class="balanza" role="img" aria-label="Manos {a['p']} %, movimiento {100 - a['p']} %"><div class="barra"><i style="--p:{a['p']}%"></i><i></i></div><p>{a['balanza']} Orientativo: lo ajustamos a ti.</p></div>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Cuándo se nota</h2><p>Lo que se nota pronto y lo que se queda. Cada cuerpo va a su ritmo.</p></div>
    <div class="otras"><a class="enlace" href="{b}{su}/">{st}</a></div></div>
  <ol class="camino tiempos">{tiempos}</ol>
</div>
<div class="wrap"><div class="aviso"><p>{a['aviso']}</p></div></div></section>

{pasos_fin()}

<section class="seccion"><div class="wrap"><div class="tit-sec" style="margin-bottom:.5rem"><h2 style="font-size:1.4rem">Otras cosas en las que te ayudo</h2></div><div class="otras">{otras}</div></div></section>'''
    return pagina(b, a['seo'], a['lead'], cuerpo)


# ── Páginas de servicio (la misma plantilla, con su herramienta) ────────────
def madero():
    b = '../'
    cuerpo = f'''
<div class="wrap cabeza">
  <div>
    <p class="miga"><a href="{b}">Inicio</a> · Con las manos</p>
    <h1>Maderoterapia en Córdoba, explicada sin humo</h1>
    <p class="lead">Una hora de trabajo manual con rodillo, copa y tabla de madera sobre piernas, glúteos y abdomen. Para aliviar la pesadez y mejorar el aspecto de la piel. Si además te mueves, el cambio se queda.</p>
    <div class="cifras"><span><b>Gratis</b>la valoración</span><span><b>40 €</b>sesión de 60 min</span><span><b>32 €</b>con bono de 10</span></div>
    <div class="acciones"><a class="btn" href="{wa('Hola Mari Carmen, quiero mi valoración gratuita de maderoterapia')}">Pedir mi valoración gratuita</a><a class="btn linea" href="#precios">Precios y bonos</a></div>
  </div>
  {foto('maderoterapia', b, carga='eager')}
</div>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Qué es</h2></div>
    <p class="lead">Un masaje corporal con instrumentos de madera. Cada uno tiene su forma y su maniobra, y siempre se trabaja hacia el drenaje.</p>
    <p>Es manual y no invasiva: sin máquinas, sin aparatos y sin productos químicos. Lo que marca la diferencia es saber qué instrumento va en cada zona y con cuánta presión.</p></div>
  <ul class="lista">
    <li><span><b>Rodillo de esferas</b><br>Muslo y glúteo, de abajo arriba.</span></li>
    <li><span><b>Copa sueca</b><br>Efecto parecido a la ventosa sobre la piel de naranja.</span></li>
    <li><span><b>Tabla moldeadora</b><br>Abdomen y costados, en pasadas largas.</span></li>
  </ul>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Lo que vas a notar</h2></div><ul class="notas">
    <li>La piel más suave y con mejor textura, con constancia.</li><li>Sensación de ligereza, sobre todo en las piernas.</li>
    <li>Menos hinchazón: desaparece la retención.</li><li>Una hora para ti, sin prisas y con el móvil lejos.</li></ul></div>
  <div><div class="tit-sec"><h2>Lo que no es</h2></div><ul class="notas">
    <li>No es un milagro de una sesión: los cambios van poco a poco.</li><li>No sustituye a moverte ni a comer bien.</li>
    <li>No es un tratamiento médico.</li><li>No da el mismo resultado a todas.</li></ul></div>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Cuántas sesiones</h2><p>Un ciclo seguido y, después, mantenimiento. En la valoración te digo cuántas para tu caso.</p></div></div>
  <ol class="camino tiempos">
    <li data-t="Sem. 1-4"><h3>Ciclo inicial</h3><p>1 o 2 sesiones por semana.</p></li>
    <li data-t="3.ª-4.ª"><h3>Aquí se empieza a notar</h3><p>Piel más suave y menos hinchazón.</p></li>
    <li data-t="Después"><h3>Mantenimiento</h3><p>Cada 15 días o una vez al mes.</p></li>
  </ol>
</div></section>

<section class="seccion" id="precios"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Cuánto cuesta</h2><p>Cuantas más sesiones, menos te cuesta cada una.</p></div>
    <ul class="lista tarifa">
      <li><span><b>Valoración y tu plan</b><br>Te miro y te hago el plan en el momento</span><span class="precio">Gratis</span></li>
      <li><span><b>Sesión suelta</b><br>60 minutos</span><span class="precio">40 €</span></li>
      <li><span><b>Bono 5 sesiones</b><br>36 € la sesión · válido 3 meses</span><span class="precio">180 €</span></li>
      <li><span><b>Bono 10 sesiones</b><br>32 € la sesión · válido 6 meses</span><span class="precio">320 €</span></li>
    </ul></div>
  <div class="calc">
    <h3>¿Qué te sale mejor?</h3>
    <label for="n-ses">Sesiones que quiero hacer: <output id="n-val">6</output></label>
    <input id="n-ses" type="range" min="1" max="20" value="6">
    <p class="res" id="res" aria-live="polite"></p>
    <a class="btn" id="calc-wa" href="{wa('Hola Mari Carmen, quiero información de los bonos de maderoterapia')}">Pedírselo a Carmen</a>
  </div>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Para quién no es</h2><p>Antes de empezar siempre te pregunto por tu salud.</p></div></div>
  <ul class="notas"><li>Si estás embarazada.</li><li>Si tienes cáncer activo o estás en tratamiento.</li><li>Si tienes varices severas o has tenido una trombosis.</li>
    <li>Si tienes alguna enfermedad de la piel en la zona.</li><li>Si tienes problemas de coagulación o tomas anticoagulantes.</li></ul>
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Lo que me preguntáis</h2></div>
  <div class="faq">
    <details><summary>¿Duele?</summary><p>No debería. Puedes notar presión en las zonas más cargadas, pero la intensidad se adapta a ti. Tiene que sentirse como un trabajo profundo, no como un castigo.</p></details>
    <details><summary>¿Puedo combinarla con ejercicio?</summary><p>Es lo ideal. La madera trabaja la piel y la retención; el músculo de debajo, que es lo que da forma, lo construye el movimiento. El entrenamiento también lo llevo yo.</p></details>
    <details><summary>¿Tengo que hacer algo antes o después?</summary><p>Antes, bebe agua y ven con la piel limpia, sin cremas. Después, sigue hidratándote y, si puedes, camina un rato.</p></details>
    <details><summary>¿Vienes a casa?</summary><p>Sí, en Córdoba capital. Llevo la camilla y el material; solo necesitas un hueco de unos 2 o 3 metros.</p></details>
  </div>
</div></section>
{pasos_fin()}'''
    js = '''(function(){
  var r=document.getElementById('n-ses'),v=document.getElementById('n-val'),o=document.getElementById('res'),wa=document.getElementById('calc-wa');if(!r)return;
  function mejor(n){var best=null;for(var b10=0;b10<=2;b10++)for(var b5=0;b5<=4;b5++){var s=b10*10+b5*5,su=Math.max(0,n-s),e=b10*320+b5*180+su*40,t=s+su;
    if(!best||e<best.e||(e===best.e&&t<best.t))best={b10:b10,b5:b5,su:su,e:e,t:t}}return best}
  function eur(x){return x.toFixed(2).replace('.',',').replace(',00','')+' €'}
  function pinta(){var n=+r.value,b=mejor(n),p=[];if(b.b10)p.push((b.b10>1?b.b10+' × ':'')+'bono 10');if(b.b5)p.push((b.b5>1?b.b5+' × ':'')+'bono 5');
    if(b.su)p.push(b.su+(b.su>1?' sesiones sueltas':' sesión suelta'));var t=p.join(' + ');t=t.charAt(0).toUpperCase()+t.slice(1);v.textContent=n;var sobra=b.t-n;
    o.innerHTML='<b>'+t+' · '+b.e+' €</b><span>'+b.t+' sesiones a '+eur(b.e/b.t)+' cada una.'+(sobra?' Te sobra'+(sobra>1?'n '+sobra:' una')+', y sale más barato que ir justa.':'')+' La valoración, gratis.</span>';
    wa.href='https://wa.me/34646437371?text='+encodeURIComponent('Hola Mari Carmen, quiero hacer '+n+' sesiones de maderoterapia: '+t.toLowerCase()+' ('+b.e+' €).')}
  r.addEventListener('input',pinta);pinta()})();'''
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","name":"Maderoterapia en Córdoba","provider":{"@type":"HealthAndBeautyBusiness","name":"Siluetas de Mujer","telephone":"+34646437371"},'
          '"areaServed":{"@type":"City","name":"Córdoba"},"offers":[{"@type":"Offer","name":"Sesión suelta","price":"40","priceCurrency":"EUR"},{"@type":"Offer","name":"Bono 5 sesiones","price":"180","priceCurrency":"EUR"},{"@type":"Offer","name":"Bono 10 sesiones","price":"320","priceCurrency":"EUR"}]}</script>')
    return pagina(b, 'Maderoterapia en Córdoba · precios y bonos · Siluetas de Mujer',
                  'Maderoterapia en Córdoba: 60 minutos con rodillo, copa y tabla de madera. Sesión 40 €, bono 5 180 €, bono 10 320 €. Valoración gratis.',
                  cuerpo, 'maderoterapia-cordoba', js, ld)


def entreno():
    b = '../'
    cuerpo = f'''
<div class="wrap cabeza">
  <div>
    <p class="miga"><a href="{b}">Inicio</a> · Con el movimiento</p>
    <h1>Entrenadora personal para mujeres en Córdoba</h1>
    <p class="lead">Fuerza pensada para el cuerpo de una mujer a partir de los 40: en grupos de hasta 5, uno a uno o en tu casa. Empiezas con una valoración gratis y sigues tus medidas en la app.</p>
    <div class="cifras"><span><b>5</b>mujeres como máximo por grupo</span><span><b>2</b>días de fuerza a la semana, para empezar</span></div>
    <div class="acciones"><a class="btn" href="{wa('Hola Mari Carmen, quiero mi valoración gratuita para entrenar')}">Pedir mi valoración gratuita</a><a class="btn linea" href="#formatos">Grupo, 1 a 1 o en casa</a></div>
  </div>
  {foto('grupo', b, carga='eager')}
</div>

<section class="seccion" id="formatos"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Grupo, 1 a 1 o en tu casa</h2><p>Las tres con la misma forma de trabajar y con la app. Cambia cuánta atención tienes y dónde entrenas.</p></div></div>
  <ul class="lista">
    <li><span><b>Grupo reducido, en la sala</b><br>Hasta 5 mujeres. Si te motiva entrenar con otras y quieres una rutina fija.</span></li>
    <li><span><b>1 a 1, en la sala</b><br>Solo tú. Si empiezas con una lesión o quieres ir a tu ritmo.</span></li>
    <li><span><b>En tu casa</b><br>Solo tú, o con una amiga. El material lo llevo yo.</span></li>
  </ul>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Cómo es una sesión</h2><p>50 minutos con una estructura que se repite, para que sepas a qué vienes. Lo que cambia es la carga, poco a poco.</p></div>
    {foto('entreno', b, '4/3')}</div>
  <ol class="camino tiempos">
    <li data-t="0-8'"><h3>Soltar</h3><p>Caderas, hombros y respiración.</p></li>
    <li data-t="8-35'"><h3>Fuerza</h3><p>Sentadilla a cajón, remo y peso muerto con goma.</p></li>
    <li data-t="35-45'"><h3>Equilibrio y juego</h3><p>Por parejas y con música.</p></li>
    <li data-t="45-50'"><h3>Bajar</h3><p>Estirar y dos minutos de calma.</p></li>
  </ol>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Qué pasa el primer día</h2><p>No empiezas entrenando: empiezas midiendo. Así, dentro de unas semanas, lo que ha cambiado es un número y no una impresión.</p></div></div>
  <ul class="notas">
    <li><b>Medidas:</b> cintura, cadera, muslo y brazo, siempre en los mismos puntos.</li>
    <li><b>Fuerza de piernas:</b> cuántas veces te levantas de una silla en 30 segundos.</li>
    <li><b>Equilibrio:</b> cuánto aguantas sobre una pierna.</li>
    <li><b>Movilidad:</b> hombros, caderas y espalda.</li>
    <li><b>Tu salud:</b> lesiones, suelo pélvico y medicación.</li>
    <li><b>Tu objetivo:</b> en tus palabras, tal cual.</li>
  </ul>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Tu app, entre clase y clase</h2><p>En la app tienes tus números, lo que toca hoy y algo para los días que no vienes: yoga y movilidad en sesiones cortas.</p></div></div>
  {foto('pesa', b)}
</div></section>

<section class="seccion"><div class="wrap">
  <div class="tit-sec"><h2>Lo que me preguntáis</h2></div>
  <div class="faq">
    <details><summary>¿Tengo que estar en forma para empezar?</summary><p>No. El primer día te mido y ajusto cada ejercicio a lo que puedes hacer hoy.</p></details>
    <details><summary>Tengo artrosis, osteoporosis o dolor de espalda. ¿Puedo?</summary><p>En la mayoría de casos, la fuerza bien adaptada ayuda. Lo hablamos en la valoración y, si hace falta, con tu médico o tu fisio.</p></details>
    <details><summary>¿Me voy a poner «grande»?</summary><p>No. Lo que vas a notar es firmeza, fuerza y que la ropa te cae distinta.</p></details>
    <details><summary>¿Sirve si estoy en la menopausia?</summary><p>Es justo cuando más sirve: la fuerza es lo que mejor frena la pérdida de músculo y hueso. Y cuidamos el suelo pélvico en cada sesión.</p></details>
    <details><summary>¿Qué tengo que llevar?</summary><p>Ropa cómoda, zapatillas y agua. El material lo pongo yo, también en tu casa.</p></details>
  </div>
</div></section>
{pasos_fin()}'''
    return pagina(b, 'Entrenadora personal para mujeres en Córdoba · Siluetas de Mujer',
                  'Entrenamiento de fuerza para mujeres a partir de los 40 en Córdoba: grupos de hasta 5, 1 a 1 o en tu casa. Valoración gratis y app con tus medidas.',
                  cuerpo, 'entrenamiento-personal-mujeres-cordoba')


def masajes():
    b = '../'
    cuerpo = f'''
<div class="wrap cabeza">
  <div>
    <p class="miga"><a href="{b}">Inicio</a> · Con las manos</p>
    <h1>Masajes en Córdoba para la tensión que se acumula</h1>
    <p class="lead">Dos masajes de 60 minutos, muy distintos entre sí: el de descarga, en camilla y con aceite, y el tailandés, en colchoneta y vestida.</p>
    <div class="cifras"><span><b>35 €</b>descarga · 60 min</span><span><b>40 €</b>tailandés · 60 min</span></div>
    <div class="acciones"><a class="btn" href="{wa('Hola Mari Carmen, quiero reservar un masaje')}">Reservar un masaje</a><a class="btn linea" href="#elijo">¿Cuál elijo?</a></div>
  </div>
  {foto('descarga', b, carga='eager')}
</div>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Masaje de descarga</h2><p>Para la espalda que se carga, los hombros subidos y las piernas que llegan pesadas al final de la semana.</p></div>
    <ul class="notas"><li>En camilla y con aceite natural.</li><li>Presión de moderada a profunda, la que toleres.</li><li>Me centro en las zonas con más tensión.</li></ul></div>
  <div><div class="tit-sec"><h2>Masaje tailandés</h2><p>Estiramientos como de yoga que hago yo por ti, y presiones rítmicas con manos, codos y pies.</p></div>
    <ul class="notas"><li>En colchoneta en el suelo.</li><li>Vestida, con ropa cómoda y sin aceites.</li><li>Es el que más se nota en la movilidad.</li></ul></div>
</div></section>

<section class="seccion" id="elijo"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>¿Cuál elijo?</h2><p>Según lo que buscas. Si dudas, escríbeme y te oriento.</p></div></div>
  <ul class="lista">
    <li><span><b>Movilidad y flexibilidad</b></span><span class="precio">Tailandés</span></li>
    <li><span><b>Aliviar la tensión muscular</b></span><span class="precio">Descarga o tailandés</span></li>
    <li><span><b>Descanso y relajación profunda</b></span><span class="precio">Descarga</span></li>
    <li><span><b>Piernas más ligeras</b></span><span class="precio">Maderoterapia</span></li>
    <li><span><b>Mejorar el aspecto de la piel</b></span><span class="precio">Maderoterapia</span></li>
  </ul>
</div></section>

<section class="seccion"><div class="wrap dos-col">
  <div><div class="tit-sec"><h2>Si la tensión vuelve cada semana</h2><p>El masaje suelta lo que ya está cargado. Para que no vuelva a cargarse igual, la espalda necesita fuerza y movilidad. Eso también lo trabajo yo.</p></div>
    <div class="otras"><a class="enlace" href="{b}espalda-cuello-cargados-cordoba/">Espalda y cuello cargados</a><a class="enlace" href="{b}entrenamiento-personal-mujeres-cordoba/">El entrenamiento</a></div></div>
  {foto('entreno', b)}
</div></section>
{pasos_fin()}'''
    return pagina(b, 'Masajes en Córdoba: descarga y tailandés · Siluetas de Mujer',
                  'Masaje de descarga (35 €) y masaje tailandés (40 €) en Córdoba, en sala o a domicilio. 60 minutos.',
                  cuerpo, 'masajes-cordoba')


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for h in SALIDA.iterdir():  # vaciar sin borrar la carpeta (puede estar servida)
        shutil.rmtree(h) if h.is_dir() else h.unlink()
    (SALIDA / 'css').mkdir()
    shutil.copy(FUENTE / 'v3' / 'estilo.css', SALIDA / 'css' / 'v3.css')
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
