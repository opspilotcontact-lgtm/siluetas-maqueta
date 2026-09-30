# Cambios pedidos por Carmen en sus audios del 30-sep (y el turquesa verdoso, aparte)
import pathlib

def aplicar(fichero, cambios):
    p = pathlib.Path(fichero)
    s = p.read_text(encoding='utf-8')
    for viejo, nuevo in cambios:
        n = s.count(viejo)
        assert n >= 1, f'{fichero}: no encontrado -> {viejo[:70]}'
        s = s.replace(viejo, nuevo)
    p.write_text(s, encoding='utf-8')
    print('ok', fichero, len(cambios))

# ---------- portada
aplicar('fuente/index.plantilla.html', [
    # «el líquido no se va: desaparece la retención» · «sesión de masaje», no «de manos»
    ('En 2 a 5 sesiones de manos muchas mujeres se ven deshinchadas, y es real: se va líquido y se va tensión.',
     'En 2 a 5 sesiones de masaje muchas mujeres se ven deshinchadas, y es real: desaparece la retención y se suelta la tensión.'),
    ('<b>Lo que sí notas es menos líquido retenido</b> y unas piernas más ligeras.',
     '<b>Lo que sí notas es que desaparece la retención</b> y las piernas pesan menos.'),
    ('más una sesión de manos cuando más la necesitas', 'más una sesión de masaje cuando más la necesitas'),
    ('<b>Piernas · 4 sesiones de manos</b>', '<b>Piernas · 4 sesiones de masaje</b>'),
    ('<b>Abdomen · manos + 8 semanas de fuerza</b>', '<b>Abdomen · masaje + 8 semanas de fuerza</b>'),
    ('<span class="m">Manos</span><div class="barra"', '<span class="m">Masaje</span><div class="barra"'),
    ('Aquí las manos llevan algo más de peso al principio.', 'Aquí el masaje lleva algo más de peso al principio.'),
    ('<div class="carril"><b class="m">Manos</b>', '<div class="carril"><b class="m">Masaje</b>'),
    ('Las manos pasan a ser tu cuidado de mantenimiento.', 'El masaje pasa a ser tu cuidado de mantenimiento.'),
    # «no soy graduada, soy certificada» · «masaje y maderoterapia»
    ('Soy Mari Carmen Figueras: graduada en deporte, entrenadora y formadora, y masajista.',
     'Soy Mari Carmen Figueras: entrenadora personal certificada y masajista de masaje y maderoterapia.'),
    ('<span class="pend">titulación exacta a confirmar</span>', '<span class="pend">nombre de los certificados a confirmar</span>'),
    # sin pack bienvenida: solo la valoración es gratis
    ('<div class="precio"><b>60 €</b><span>Pack bienvenida: 2 sesiones de 60 min + valoración + mini plan</span></div>',
     '<div class="precio"><b>Gratis</b><span>La valoración y tu plan. Después, desde 32 € la sesión con bono.</span></div>'),
])

# ---------- maderoterapia
aplicar('fuente/maderoterapia.plantilla.html', [
    ('Pack bienvenida de 2 sesiones por 60 €, sesión suelta 40 €.', 'Valoración y plan gratis; sesión suelta 40 €, bonos de 5 y 10 sesiones.'),
    ('{"@type":"Offer","name":"Pack bienvenida (2 sesiones de 60 min)","price":"60","priceCurrency":"EUR"},',
     '{"@type":"Offer","name":"Valoración inicial y plan","price":"0","priceCurrency":"EUR"},'),
    ('En Siluetas de Mujer, el pack bienvenida de 2 sesiones cuesta 60 €, la sesión suelta 40 €,',
     'En Siluetas de Mujer la valoración y el plan son gratis; la sesión suelta cuesta 40 €,'),
    ('<span><b>60 €</b>la primera vez: 2 sesiones (30 € cada una)</span>',
     '<span><b>Gratis</b>la valoración: te miro y te hago tu plan</span>'),
    ('quiero%20el%20pack%20bienvenida%20de%20maderoterapia"><svg class="ico"><use href="#i-wa"/></svg>Reservar el pack bienvenida</a>\n        <a class="btn suave"',
     'quiero%20mi%20valoraci%C3%B3n%20gratuita%20de%20maderoterapia"><svg class="ico"><use href="#i-wa"/></svg>Pedir mi valoración gratuita</a>\n        <a class="btn suave"'),
    ('cuando lo que pesa es líquido retenido.', 'cuando lo que pesa es la retención.'),
    ('La madera trabaja la piel y el líquido.', 'La madera trabaja la piel y la retención.'),
    ('<div class="linea-r destaca"><b>Pack bienvenida</b><span class="punt"></span><span class="imp">60 €</span><small>2 sesiones + valoración + mini plan · 30 € la sesión · válido 15 días</small></div>',
     '<div class="linea-r destaca"><b>Valoración + tu plan</b><span class="punt"></span><span class="imp">Gratis</span><small>Te miro, hablamos de lo que buscas y te hago el plan en ese momento</small></div>'),
    ('<label class="check"><input type="checkbox" id="primera" checked> Es mi primera vez</label>\n', ''),
    ('<output id="res" for="n-ses primera"><b>Pack bienvenida + 4 sesiones sueltas · 220 €</b><span class="desg">6 sesiones a 36,67 € cada una.</span></output>',
     '<output id="res" for="n-ses"><b>Bono 5 + 1 sesión suelta · 220 €</b><span class="desg">6 sesiones a 36,67 € cada una. La valoración, gratis.</span></output>'),
    ('<h2>Empieza por dos sesiones y decide después.</h2>\n    <p>El pack bienvenida: 2 sesiones de 60 minutos, valoración y un mini plan, por 60 €.</p>\n    <a class="btn" href="https://wa.me/34646437371?text=Hola%20Mari%20Carmen%2C%20quiero%20el%20pack%20bienvenida%20de%20maderoterapia"><svg class="ico"><use href="#i-wa"/></svg>Reservar el pack bienvenida</a>',
     '<h2>Empieza por tu valoración, que es gratis.</h2>\n    <p>Te miro, hablamos de lo que buscas y te hago tu plan en ese momento. Sin compromiso.</p>\n    <a class="btn" href="https://wa.me/34646437371?text=Hola%20Mari%20Carmen%2C%20quiero%20mi%20valoraci%C3%B3n%20gratuita%20de%20maderoterapia"><svg class="ico"><use href="#i-wa"/></svg>Pedir mi valoración gratuita</a>'),
    # calculadora sin pack
    ("var r=document.getElementById('n-ses'),p=document.getElementById('primera'),",
     "var r=document.getElementById('n-ses'),"),
    ('for(var pk=0;pk<=(primera?1:0);pk++)for(var b10=0;b10<=2;b10++)', 'for(var pk=0;pk<=0;pk++)for(var b10=0;b10<=2;b10++)'),
    ("var n=+r.value,b=mejor(n,p.checked),partes=[];", "var n=+r.value,b=mejor(n,false),partes=[];"),
    ("if(b.pk)partes.push('pack bienvenida');\n", ''),
    ("' cada una.'+(sobra?(' Te sobra'+(sobra>1?'n '+sobra:' una')+', y sale más barato que ir justa.'):'')+'</span>';",
     "' cada una.'+(sobra?(' Te sobra'+(sobra>1?'n '+sobra:' una')+', y sale más barato que ir justa.'):'')+' La valoración, gratis.</span>';"),
    ("r.addEventListener('input',pinta);p.addEventListener('change',pinta);pinta();", "r.addEventListener('input',pinta);pinta();"),
])

# ---------- entrenamiento: la valoración gratuita también es la puerta de entrada
aplicar('fuente/entreno.plantilla.html', [
    ('quiero%20probar%20una%20sesi%C3%B3n%20de%20entrenamiento"><svg class="ico"><use href="#i-wa"/></svg>Quiero una sesión de prueba</a>',
     'quiero%20mi%20valoraci%C3%B3n%20gratuita%20para%20entrenar"><svg class="ico"><use href="#i-wa"/></svg>Pedir mi valoración gratuita</a>'),
    ('<small>¿Qué pasa el primer día?</small><b>Te mido y hablamos</b>', '<small>¿Qué pasa el primer día?</small><b>Valoración gratis y tu plan</b>'),
    ('<p class="intro">No empiezas entrenando: empiezas midiendo.', '<p class="intro">No empiezas entrenando: empiezas midiendo, y la valoración es gratis.'),
    ('<h2>Cuando el cuerpo pesa, empiezan las manos</h2>', '<h2>Cuando el cuerpo pesa, empieza el masaje</h2>'),
    ('el entreno hace que lo que consiguen las manos se quede.', 'el entreno hace que lo que consigue el masaje se quede.'),
    ('<h2>Ven a una sesión de prueba y mídete.</h2>\n    <p>Te hago la valoración, entrenas con el grupo y decides después.</p>',
     '<h2>Ven a tu valoración gratuita y mídete.</h2>\n    <p>Te mido, hablamos de lo que buscas y te hago tu plan en ese momento. Después decides.</p>'),
    ('quiero%20probar%20una%20sesi%C3%B3n%20de%20entrenamiento"><svg class="ico"><use href="#i-wa"/></svg>Quiero probar</a>',
     'quiero%20mi%20valoraci%C3%B3n%20gratuita%20para%20entrenar"><svg class="ico"><use href="#i-wa"/></svg>Pedir mi valoración gratuita</a>'),
])

# ---------- artículo de celulitis
aplicar('fuente/celulitis.plantilla.html', [
    ('Menos sensación de volumen cuando hay líquido retenido.', 'Menos sensación de volumen cuando hay retención.'),
    ('<tr class="mia"><td><b>Siluetas de Mujer</b> · pack bienvenida: 2 sesiones de 60 min + valoración + mini plan</td><td>60 €</td></tr>',
     '<tr class="mia"><td><b>Siluetas de Mujer</b> · sesión de 60 min (valoración y plan, gratis)</td><td>40 €</td></tr>'),
])
