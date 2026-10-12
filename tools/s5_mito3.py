from engine3 import *
D = json.load(open("/home/claude/w2/voices5.json"))["mito3"]
SP = ["¿Un inversor más grande gasta más batería?", "¡Realidad... a medias!",
      "Todo inversor gasta algo solo por estar encendido, aunque no tengas nada conectado.",
      "Uno de cinco kilowatts gasta unos cincuenta watts. Uno de diez, cerca de cien.",
      "En una noche de doce horas, eso es más de un kilowatt hora.",
      "Pero si tu casa necesita un inversor grande, ponlo: uno chico se dispara, o se daña.",
      "El truco: no lo dejes prendido sin necesidad, y si tiene modo ahorro, actívalo.",
      "¿Sabías que tu inversor consume solo? Dímelo en los comentarios."]
SH = ["¿Un inversor más grande gasta más batería?", "¡REALIDAD... A MEDIAS!",
      "Todo inversor gasta algo solo por estar encendido, aunque no conectes nada.",
      "5 kW ≈ 50 W en vacío. 10 kW ≈ 100 W.",
      "En una noche de 12 horas: más de 1 kWh.",
      "Pero si tu casa necesita uno grande, ponlo: uno chico se dispara o se daña.",
      "El truco: no lo dejes prendido sin necesidad, y activa el modo ahorro.",
      "¿Sabías que tu inversor consume solo? Dímelo en comentarios."]
def hole(u, dur, t): return bg_mito(t)
def medias(u, dur, t):
    fr = bg_mito(t); stamp(fr, u, "REALIDAD", GRN, W / 2, 560, 170, 0.05, ang=-8)
    stamp(fr, u, "A MEDIAS", YEL, W / 2, 820, 140, 0.5, ang=6); return fr
def vacio(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); inverter(d, W / 2, 620, 240)
    k = 0.5 + 0.5 * math.sin(t * 6)
    d.rounded_rectangle([W / 2 - 230, 950, W / 2 + 230, 1050], radius=24, fill=(0, 0, 0, 180)); text_c(d, W / 2, 960, "Nada conectado", 60, WHT)
    bolt(d, W / 2 + 290, 480, 60, col=(255, int(160 + 90 * k), 0)); return fr
def barras(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); base = 1100
    for i, (lab, v, col, at) in enumerate([("5 kW", 50, CYAN, 0.1), ("10 kW", 100, YEL, 0.5)]):
        k = ease((u - dur * at) / 0.8) if u > dur * at else 0; x = 330 + i * 420
        d.rounded_rectangle([x - 100, base - v * 5 * k, x + 100, base], radius=16, fill=col)
        if k: text_c(d, x, base - v * 5 * k - 100, f"{int(v * k)} W", 76, WHT)
        text_c(d, x, base + 20, lab, 60, GRY)
    return fr
def noche(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); moon(d, W / 2, 330, 100)
    text_c(d, W / 2, 520, "100 W × 12 h", 96, WHT)
    if u > dur * 0.35: text_c(d, W / 2, 680, "= 1,2 kWh", 150, YEL, stroke=6, sfill=NAVY)
    if u > dur * 0.6: battery_icon(d, W / 2, 1020, 140, 220, 0.75, col=YEL)
    return fr
def chico(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    inverter(d, 300, 640, 120); xmark(d, 300, 640, 130); text_c(d, 300, 840, "Chico", 64, RED)
    inverter(d, W - 300, 620, 200); check(d, W - 300, 900, 60); text_c(d, W - 300, 980, "El justo", 64, GRN)
    if u > dur * 0.4: bolt(d, 300, 450, 70, col=RED)
    return fr
def truco(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); pill(d, W / 2, 260, "EL TRUCO", 80, NAVY, YEL)
    on = u > dur * 0.45
    d.rounded_rectangle([W / 2 - 220, 560, W / 2 + 220, 760], radius=100, fill=GRN if on else (90, 90, 100))
    cx = W / 2 + (120 if on else -120); d.ellipse([cx - 85, 575, cx + 85, 745], fill=WHT)
    text_c(d, W / 2, 820, "Modo ahorro", 84, GRN if on else WHT)
    return fr
def cta(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 330, "¿Sabías que tu", 96, WHT); text_c(d, W / 2, 450, "inversor consume solo?", 84, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 800, 120, 0.4, ang=8)
    if u > 1.2: pop(fr, u, 1.2, W / 2, 1130, lambda dd: pill(dd, W / 2, 1100, "SÍGUEME PARA MÁS", 60, NAVY, YEL))
    return fr
print(run("s5_mito3", D, SP, SH, [hole, medias, vacio, barras, noche, chico, truco, cta], (0,)))
