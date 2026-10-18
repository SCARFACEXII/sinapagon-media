from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["lista"]
SP = ["¿Qué puedes prender con cuatro paneles solares?", "Guárdate este video.",
      "Con cuatro paneles de quinientos cincuenta, de día tienes unos dos kilowatts.",
      "Eso alcanza para la nevera, el freezer, los ventiladores, el televisor, las luces y la lavadora.",
      "Hasta la olla arrocera, si la usas sola.",
      "Lo que no te alcanza: el aire acondicionado todo el día, ni la ducha eléctrica.",
      "Para eso, ocho paneles o más.",
      "¿Qué equipo quieres prender tú? Dímelo en los comentarios."]
SH = ["¿Qué puedes prender con 4 paneles solares?", "Guárdate este video",
      "4 paneles de 550 W: unos 2 kW de día.",
      "Alcanza: nevera, freezer, ventiladores, TV, luces y lavadora.",
      "Hasta la olla arrocera, si la usas sola.",
      "No alcanza: el aire todo el día, ni la ducha eléctrica.",
      "Para eso: 8 paneles o más.",
      "¿Qué equipo quieres prender tú? Dímelo en comentarios."]
def hole(u, dur, t): return bg_plano(t)
def guarda(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    for i in range(4): panel(d, 210 + i * 220, 450, 190, 260)
    stamp(fr, u, "GUÁRDALO", YEL, W / 2, 860, 130, 0.05, ang=-6); return fr
def dos(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr); sun(d, W / 2, 330, 90, t)
    for i in range(4): panel(d, 210 + i * 220, 640, 190, 260)
    if u > dur * 0.4: text_c(d, W / 2, 860, "≈ 2 kW", 170, YEL, stroke=6, sfill=NAVY)
    return fr
ITEMS = [("Nevera", "fridge"), ("Freezer", "fridge"), ("Ventiladores", "fan"), ("TV", "tv"), ("Luces", "bulb"), ("Lavadora", "wash")]
def icon(d, kind, cx, cy, s, t):
    if kind == "fridge": fridge(d, cx, cy, s)
    elif kind == "fan": fan(d, cx, cy - s * 0.2, s * 0.6, t)
    elif kind == "tv": tv(d, cx, cy, s * 0.9)
    elif kind == "bulb": bulb(d, cx, cy, s)
    else:
        d.rounded_rectangle([cx - s * 0.7, cy - s * 0.8, cx + s * 0.7, cy + s * 0.8], radius=14, fill=(230, 235, 245)); d.ellipse([cx - s * 0.45, cy - s * 0.35, cx + s * 0.45, cy + s * 0.55], fill=(60, 120, 200), outline=WHT, width=5)
def alcanza(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    for i, (lab, kind) in enumerate(ITEMS):
        at = dur * (0.05 + i * 0.13)
        if u < at: continue
        cx = 200 + (i % 3) * 340; cy = 420 + (i // 3) * 420
        icon(d, kind, cx, cy, 110, t); check(d, cx + 110, cy - 110, 34, w=12); text_c(d, cx, cy + 140, lab, 50, WHT)
    return fr
def olla(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    from common2 import pot
    pot(d, W / 2, 640, 220); check(d, W / 2 + 260, 480, 60)
    if u > dur * 0.4: stamp(fr, u, "SOLA", YEL, W / 2, 1060, 130, dur * 0.4, ang=-6)
    return fr
def noalcanza(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    ac_unit(d, 300, 520, 360, t); xmark(d, 300, 560, 120); text_c(d, 300, 830, "Aire todo el día", 54, RED)
    if u > dur * 0.45:
        from common2 import shower
        shower(d, W - 280, 600, 200, t); xmark(d, W - 280, 560, 120); text_c(d, W - 280, 830, "Ducha eléctrica", 54, RED)
    return fr
def ocho(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    n = int(clamp(u / (dur * 0.6)) * 8) + 1
    for i in range(min(n, 8)): panel(d, 190 + (i % 4) * 233, 480 + (i // 4) * 320, 200, 280)
    if u > dur * 0.6: stamp(fr, u, "8 O MÁS", GRN, W / 2, 1150, 110, dur * 0.6, ang=-5)
    return fr
def cta(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 360, "¿Qué equipo", 100, WHT); text_c(d, W / 2, 480, "quieres prender?", 100, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 840, 120, 0.4, ang=6); return fr
print(run("s6_lista", D, SP, SH, [hole, guarda, dos, alcanza, olla, noalcanza, ocho, cta], (0,)))
