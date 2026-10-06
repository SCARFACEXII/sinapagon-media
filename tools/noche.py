from engine3 import *
SP = ["Se va la corriente a las ocho de la noche.", "¿Hasta qué hora te aguanta la batería?",
      "Prendes lo básico: un ventilador, dos bombillos y el celular. Unos ochenta watts.",
      "Con una batería de doce volts y cien amperes de gel, llegas a las dos de la madrugada... y te despiertas sudando.",
      "Con una estación portátil de un kilowatt hora, llegas a las siete de la mañana. Toda la noche.",
      "Pero si le conectas la nevera, se acaba a las tres y media.",
      "Con un sistema de diez kilowatts hora, pasas la noche con nevera, ventilador y televisor... y te sobra.",
      "¿Hasta qué hora te dura la tuya? Escríbelo en los comentarios."]
SH = ["Se va la corriente a las 8 de la noche.", "¿Hasta qué hora te aguanta la batería?",
      "Lo básico: ventilador, 2 bombillos y celular. Unos 80 W.",
      "Batería 12 V 100 Ah de gel: llegas a las 2 am... y te despiertas sudando.",
      "Estación portátil de 1 kWh: llegas a las 7 am. Toda la noche.",
      "Pero si le conectas la nevera, se acaba a las 3:30 am.",
      "Sistema de 10 kWh: nevera, ventilador y TV... y te sobra.",
      "¿Hasta qué hora te dura la tuya? Escríbelo en comentarios."]
def hole(u, dur, t): return bg_noche(t)
def timeline(fr, u, dur, end_h, col, label):
    d = ImageDraw.Draw(fr); x0, x1, y = 110, W - 110, 1180; h0, h1 = 20, 31
    d.rounded_rectangle([x0, y, x1, y + 50], radius=25, fill=(255, 255, 255, 40))
    k = clamp(u / (dur * 0.65)); cur = h0 + (end_h - h0) * ease(k)
    xe = x0 + (x1 - x0) * (cur - h0) / (h1 - h0); d.rounded_rectangle([x0, y, xe, y + 50], radius=25, fill=col)
    for hh, lab in [(20, "8 pm"), (24, "12"), (28, "4 am"), (31, "7 am")]:
        xx = x0 + (x1 - x0) * (hh - h0) / (h1 - h0); d.text((xx - 40, y + 65), lab, font=F(38), fill=GRY)
    clock(d, W / 2, 470, 170, int(cur) % 24, int((cur % 1) * 60))
    text_c(d, W / 2, 680, hora(cur), 92, YEL if cur < end_h - 0.01 or end_h >= 31 else RED, stroke=5, sfill=NAVY)
    d.text((x0, y - 80), label, font=F(52), fill=WHT)
    return cur
def hasta(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); moon(d, W - 200, 230, 80)
    clock(d, W / 2, 620, 220, 20, 0)
    stamp(fr, u, "¿HASTA QUÉ HORA?", YEL, W / 2, 1050, 90, 0.2, ang=-6)
    return fr
def basico(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr)
    if u > 0.2: fan(d, 230, 520, 120, t)
    if u > dur * 0.25: bulb(d, 500, 470, 110); bulb(d, 650, 470, 110)
    if u > dur * 0.45: phone(d, 880, 500, 140)
    if u > dur * 0.6: pop(fr, u, dur * 0.6, W / 2, 920, lambda dd: text_c(dd, W / 2, 850, "≈ 80 W", 160, YEL, stroke=6, sfill=NAVY))
    return fr
def gel(u, dur, t):
    fr = bg_noche(t); cur = timeline(fr, u, dur, 26, (90, 150, 255), "Batería 12 V 100 Ah (gel)"); d = ImageDraw.Draw(fr)
    battery_icon(d, 170, 960, 120, 200, 1 - (cur - 20) / 6, col=(90, 150, 255))
    if cur >= 25.99: thermo(d, W - 170, 930, 220, 0.9); stamp(fr, u, "¡SUDANDO!", RED, W / 2, 920, 80, dur * 0.7, ang=-6)
    return fr
def estacion(u, dur, t):
    fr = bg_noche(t); cur = timeline(fr, u, dur, 31, GRN, "Estación portátil 1 kWh"); d = ImageDraw.Draw(fr)
    station(d, 190, 950, 90)
    if cur >= 30.99: sun(d, W - 190, 930, 60, t); stamp(fr, u, "TODA LA NOCHE", GRN, W / 2, 920, 70, dur * 0.7, ang=-5)
    return fr
def nevera(u, dur, t):
    fr = bg_noche(t); cur = timeline(fr, u, dur, 27.5, RED, "Estación 1 kWh + nevera"); d = ImageDraw.Draw(fr)
    station(d, 170, 950, 80); d.text((290, 905), "+", font=F(90), fill=WHT); fridge(d, 420, 960, 110)
    if cur >= 27.49: stamp(fr, u, "3:30 am", RED, W - 240, 950, 80, dur * 0.7, ang=6)
    return fr
f402 = foot("402", 0.0, zoom=(1.0, 1.12), dim=120)
def sistema(u, dur, t):
    fr = f402(u, dur); d = ImageDraw.Draw(fr)
    pop(fr, u, 0.1, W / 2, 230, lambda dd: pill(dd, W / 2, 190, "SISTEMA 10 kWh", 80, NAVY, YEL))
    for i, (ic, at) in enumerate([("n", 0.25), ("f", 0.4), ("t", 0.55)]):
        if u < dur * at: continue
        cx = 230 + i * 310
        if ic == "n": fridge(d, cx, 560, 130)
        elif ic == "f": fan(d, cx, 520, 100, t)
        else: tv(d, cx, 560, 130)
    if u > dur * 0.7:
        battery_icon(d, W / 2, 970, 170, 280, 0.7, col=GRN); pill(d, W / 2, 1110, "A las 7 am: ¡te sobra!", 60, NAVY, GRN)
    return fr
def cta(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); moon(d, W - 200, 230, 80)
    text_c(d, W / 2, 380, "¿Hasta qué hora", 96, WHT); text_c(d, W / 2, 500, "te dura la tuya?", 96, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 850, 120, 0.4, ang=6)
    if u > 1.2: pop(fr, u, 1.2, W / 2, 1110, lambda dd: pill(dd, W / 2, 1080, "SÍGUEME PARA MÁS", 60, NAVY, YEL))
    return fr
print(run("noche", 39.54938775510204, SP, SH, [hole, hasta, basico, gel, estacion, nevera, sistema, cta], (0,)))
