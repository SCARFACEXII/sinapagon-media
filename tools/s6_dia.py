from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["dia"]
SP = ["Apagón de seis de la tarde a cuatro de la mañana. Así se mantiene una casa con paneles.",
      "De día, manda el sol: los paneles mueven la casa y cargan la batería.",
      "Aprovecha para cocinar, lavar y bombear agua.",
      "A las seis se va el sol, y se va la corriente: ahora manda la batería.",
      "Nevera, ventiladores, luces y televisor.",
      "A las cuatro vuelve la corriente, y te sobra batería.",
      "El secreto: lo pesado, siempre de día.",
      "¿Cuántas horas de apagón tienes tú? Escríbelo en los comentarios."]
SH = ["Apagón de 6 pm a 4 am: así se mantiene una casa con paneles.",
      "De día manda el sol: mueve la casa y carga la batería.",
      "Aprovecha: cocina, lava y bombea agua.",
      "6 pm: se va el sol y la corriente. Ahora manda la batería.",
      "Nevera, ventiladores, luces y TV.",
      "4 am: vuelve la corriente, y te sobra batería.",
      "El secreto: lo pesado, siempre de día.",
      "¿Cuántas horas de apagón tienes? Escríbelo en comentarios."]
from common2 import pot
def hole(u, dur, t): return bg_dia(t)
def sol(u, dur, t):
    fr = bg_dia(t); d = ImageDraw.Draw(fr); pill(d, W / 2, 200, "DE DÍA", 70, NAVY, YEL)
    for i in range(4): panel(d, 210 + i * 220, 560, 190, 260)
    lvl = 0.3 + 0.6 * ease(u / dur); battery_icon(d, W / 2, 960, 180, 300, lvl, col=GRN); text_c(d, W / 2, 920, f"{int(lvl * 100)}%", 70, WHT, stroke=5, sfill=NAVY)
    return fr
def pesado(u, dur, t):
    fr = bg_dia(t); d = ImageDraw.Draw(fr)
    if u > 0.1: pot(d, 220, 640, 120); text_c(d, 220, 780, "Cocinar", 54, NAVY)
    if u > dur * 0.3:
        d.rounded_rectangle([W / 2 - 90, 540, W / 2 + 90, 740], radius=16, fill=(230, 235, 245)); d.ellipse([W / 2 - 60, 590, W / 2 + 60, 710], fill=(60, 120, 200)); text_c(d, W / 2, 780, "Lavar", 54, NAVY)
    if u > dur * 0.55:
        d.ellipse([W - 300, 570, W - 160, 710], fill=(70, 130, 220), outline=WHT, width=5); text_c(d, W - 220, 780, "Bombear", 54, NAVY)
    return fr
def seis(u, dur, t):
    k = clamp(u / (dur * 0.5)); fr = bg_dia(t) if k < 0.5 else bg_noche(t); d = ImageDraw.Draw(fr)
    clock(d, W / 2, 560, 180, 18, 0); text_c(d, W / 2, 770, "6:00 pm", 90, YEL, stroke=5, sfill=NAVY)
    if k >= 1: pill(d, W / 2, 960, "Manda la batería", 66, NAVY, GRN)
    return fr
def noche(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); moon(d, W - 200, 230, 80)
    for i, at in enumerate([0.05, 0.25, 0.45, 0.65]):
        if u < dur * at: continue
        cx = 180 + i * 240
        if i == 0: fridge(d, cx, 640, 110)
        elif i == 1: fan(d, cx, 600, 80, t)
        elif i == 2: bulb(d, cx, 620, 100)
        else: tv(d, cx, 640, 100)
    return fr
def cuatro(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); clock(d, 300, 580, 160, 4, 0); text_c(d, 300, 770, "4:00 am", 76, YEL)
    battery_icon(d, W - 280, 620, 220, 400, 0.45, col=GRN); text_c(d, W - 280, 570, "45%", 84, WHT, stroke=6, sfill=NAVY)
    if u > dur * 0.4: stamp(fr, u, "TE SOBRA", GRN, W / 2, 1050, 110, dur * 0.4, ang=-5)
    return fr
def secreto(u, dur, t):
    fr = bg_dia(t); stamp(fr, u, "LO PESADO,", NAVY, W / 2, 560, 120, 0.05, ang=-5); stamp(fr, u, "DE DÍA", (200, 60, 0), W / 2, 820, 140, 0.5, ang=5); return fr
def cta(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 360, "¿Cuántas horas", 100, WHT); text_c(d, W / 2, 480, "de apagón tienes?", 92, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 840, 120, 0.4, ang=6); return fr
print(run("s6_dia", D, SP, SH, [hole, sol, pesado, seis, noche, cuatro, secreto, cta], (0,)))
