import json, sys
sys.path.insert(0, "/home/claude/w2")
from engine import *

TOTAL = json.load(open("/home/claude/w2/voices.json"))["v3"]["dur"] + 0.6
SPOKEN = ["¿Se puede poner el aire acondicionado con paneles solares?", "Sí... pero con cuidado.",
          "Un split de doce mil BTU, inverter, consume unos novecientos watts.", "Ocho horas de noche, son unos siete kilowatts hora.",
          "Para eso necesitas unos seis paneles de quinientos cincuenta watts, un inversor de cinco kilowatts, y una batería grande: de diez kilowatts hora o más.",
          "Si solo lo quieres usar de día, con el sol, sale mucho más barato.", "¿Quieres que te calcule el tuyo? Escríbeme."]
SHOW = ["¿Se puede poner el aire acondicionado con paneles solares?", "Sí... pero con cuidado.",
        "Un split de 12.000 BTU inverter consume unos 900 W.", "8 horas de noche = unos 7 kWh.",
        "Necesitas unos 6 paneles de 550 W, un inversor de 5 kW y una batería de 10 kWh o más.",
        "Si solo lo usas de día, con el sol, sale mucho más barato.", "¿Te calculo el tuyo? Escríbeme."]
T = timings(SPOKEN, TOTAL - 0.6)
track = sub_track(SHOW, T)
S = lambda i: T[i][0]

def countup(d, cx, y, val, u, at, dur_c, fmt, size, col):
    k = ease((u - at) / dur_c) if u > at else 0
    text_c(d, cx, y, fmt(val * k), size, col, stroke=6, sfill=NAVY)

def hook(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 230, "¿Aire acondicionado", 84, WHT); text_c(d, W / 2, 340, "con PANELES SOLARES?", 84, YEL)
    layer_pop(fr, L, u, W / 2, 330, 0)
    d = ImageDraw.Draw(fr)
    if u > 0.4: ac_unit(d, W / 2, 640, 620, t)
    L = new_layer(); d = ImageDraw.Draw(L)
    for k in range(3): panel(d, 250 + k * 290, 1050, 240, 170)
    layer_pop(fr, L, u, W / 2, 1050, 1.0)
    return fr

def yes(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    d.ellipse([W / 2 - 170, 380, W / 2 + 170, 720], fill=GRN)
    d.line([(W / 2 - 80, 555), (W / 2 - 15, 620), (W / 2 + 95, 480)], fill=WHT, width=36, joint="curve")
    text_c(d, W / 2, 770, "SÍ SE PUEDE", 110, GRN)
    layer_pop(fr, L, u, W / 2, 600, 0)
    L = new_layer(); d = ImageDraw.Draw(L)
    warn(d, W / 2 - 250, 1010, 60); d.text((W / 2 - 160, 975), "pero con cuidado", font=F(70), fill=WHT)
    layer_pop(fr, L, u, W / 2, 1010, max(0.6, dur * 0.45))
    return fr

def consumo(u, dur, t):
    fr = bg_frame(t); d = ImageDraw.Draw(fr)
    ac_unit(d, W / 2, 380, 560, t)
    L = new_layer(); d = ImageDraw.Draw(L); pill(d, W / 2, 660, "Split 12.000 BTU inverter", 58, WHT, BLUE)
    layer_pop(fr, L, u, W / 2, 690, 0.2)
    d = ImageDraw.Draw(fr)
    if u > dur * 0.55:
        text_c(d, W / 2, 850, "consume", 60, GRY)
        countup(d, W / 2, 940, 900, u, dur * 0.55, 1.0, lambda v: f"≈ {int(v)} W", 150, YEL)
    return fr

def noche(u, dur, t):
    fr = bg_frame(t); d = ImageDraw.Draw(fr)
    moon(d, W / 2, 420, 140)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 640, "8 h × 900 W", 100, WHT)
    layer_pop(fr, L, u, W / 2, 690, 0.2)
    d = ImageDraw.Draw(fr)
    if u > dur * 0.45:
        countup(d, W / 2, 850, 7, u, dur * 0.45, 0.9, lambda v: f"≈ {v:.0f} kWh", 160, CYAN)
    return fr

def necesitas(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 170, "Lo que necesitas", 84, WHT); layer_pop(fr, L, u, W / 2, 210, 0)
    L = new_layer(); d = ImageDraw.Draw(L)
    for k in range(6): panel(d, 150 + k * 156, 440, 130, 180)
    text_c(d, W / 2, 570, "6 paneles de 550 W", 70, YEL)
    layer_pop(fr, L, u, W / 2, 500, dur * 0.08)
    L = new_layer(); d = ImageDraw.Draw(L)
    d.rounded_rectangle([W / 2 - 110, 700, W / 2 + 110, 900], radius=26, fill=(240, 244, 250), outline=WHT, width=5)
    d.ellipse([W / 2 - 50, 740, W / 2 + 50, 840], fill=NAVY); bolt(d, W / 2, 790, 38)
    text_c(d, W / 2, 930, "Inversor de 5 kW", 70, CYAN)
    layer_pop(fr, L, u, W / 2, 820, dur * 0.42)
    L = new_layer(); d = ImageDraw.Draw(L)
    battery_icon(d, W / 2, 1110, 150, 200, 0.95, col=GRN)
    text_c(d, W / 2, 1240, "Batería de 10 kWh o más", 66, GRN)
    layer_pop(fr, L, u, W / 2, 1150, dur * 0.66)
    return fr

def dia(u, dur, t):
    fr = bg_frame(t); d = ImageDraw.Draw(fr)
    sun(d, W / 2, 480, 150, t)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 780, "Solo de día", 96, WHT)
    pill(d, W / 2, 930, "MUCHO MÁS BARATO", 72, NAVY, GRN)
    layer_pop(fr, L, u, W / 2, 900, 0.3)
    return fr

def cta(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    chat(d, W / 2, 520, 190); layer_pop(fr, L, u, W / 2, 520, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 800, "¿Te calculo el tuyo?", 92, WHT)
    pill(d, W / 2, 960, "ESCRÍBEME POR WHATSAPP", 60, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 900, 0.3)
    return fr

scenes = [(0, S(1), hook), (S(1), S(2), yes), (S(2), S(3), consumo), (S(3), S(4), noche), (S(4), S(5), necesitas), (S(5), S(6), dia), (S(6), TOTAL, cta)]
render("/home/claude/w2/v3.mp4", TOTAL, scenes, track)
