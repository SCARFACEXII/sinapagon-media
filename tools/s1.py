import json, sys
sys.path.insert(0, "/home/claude/w2")
from engine import *

U = "/root/.claude/uploads/496944e7-2387-59a5-b6d7-4284eb12520e/"
CL = {k: U + v for k, v in {"404": "0731b340-VID-20261001-WA0404.mp4", "403": "65a8fd6a-VID-20261001-WA0403.mp4",
      "399": "b45c053a-VID-20261001-WA0399.mp4", "405": "4debce8f-VID-20261001-WA0405.mp4"}.items()}

TOTAL = json.load(open("/home/claude/w2/voices.json"))["s1"]["dur"] + 0.6
SPOKEN = ["Me preguntaron: gasto ciento cuarenta kilowatts al mes... ¿qué sistema necesito?", "Vamos a calcularlo.",
          "Ciento cuarenta entre treinta días: unos cinco kilowatts hora al día.",
          "Aquí en Cuba, un panel de quinientos cincuenta watts produce unos dos kilowatts hora diarios.",
          "O sea, con cuatro paneles cubres tu consumo, y te sobra para cargar la batería.",
          "Para la noche, una batería de litio de diez kilowatts hora, y un inversor de cinco kilowatts.",
          "Con eso, olvídate del apagón.", "Mira tu recibo de la luz, y escríbeme en los comentarios cuánto gastas tú."]
SHOW = ["Me preguntaron: gasto 140 kWh al mes... ¿qué sistema necesito?", "Vamos a calcularlo.",
        "140 ÷ 30 días = unos 5 kWh al día.",
        "En Cuba, un panel de 550 W produce unos 2 kWh diarios.",
        "Con 4 paneles cubres tu consumo y te sobra para la batería.",
        "Para la noche: batería de litio de 10 kWh e inversor de 5 kW.",
        "Con eso, olvídate del apagón.", "Mira tu recibo y escríbeme cuánto gastas tú."]
T = timings(SPOKEN, TOTAL - 0.6)
track = sub_track(SHOW, T)
S = lambda i: T[i][0]

def foot(key, start, zoom=(1.0, 1.12), focus=(0.5, 0.5), dim=70):
    st = {}
    def get(u, dur):
        if "f" not in st: st["f"] = Footage(CL[key], start, dur, zoom=zoom, focus=focus)
        fr = st["f"].frame(u)
        if dim: fr.alpha_composite(Image.new("RGBA", (W, H), (0, 10, 30, dim)))
        return fr
    return get

def row(d, y, label, value, vcol):
    d.rounded_rectangle([90, y, W - 90, y + 120], radius=30, fill=(10, 26, 64, 225), outline=(255, 255, 255, 50), width=3)
    d.text((140, y + 28), label, font=F(50, True), fill=WHT)
    f = F(62); tw = d.textlength(value, font=f); d.text((W - 140 - tw, y + 22), value, font=f, fill=vcol)

def hook(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 200, "¿Gastas 140 kWh", 90, WHT); text_c(d, W / 2, 310, "al mes?", 90, YEL)
    layer_pop(fr, L, u, W / 2, 260, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    d.rounded_rectangle([W / 2 - 280, 470, W / 2 + 280, 1080], radius=24, fill=(245, 247, 252), outline=WHT, width=4)
    text_c(d, W / 2, 500, "RECIBO DE LUZ", 52, NAVY)
    for k in range(4): d.rounded_rectangle([W / 2 - 220, 600 + k * 50, W / 2 + 120 - k * 40, 622 + k * 50], radius=8, fill=(205, 212, 228))
    d.line([(W / 2 - 230, 830), (W / 2 + 230, 830)], fill=(200, 205, 220), width=3)
    text_c(d, W / 2, 860, "Consumo del mes", 44, (90, 100, 120))
    text_c(d, W / 2, 930, "140 kWh", 110, RED)
    layer_pop(fr, L, u, W / 2, 780, 0.35)
    return fr

f1 = foot("404", 0.0, zoom=(1.0, 1.15), dim=60)
def calc(u, dur, t):
    fr = f1(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 300, "VAMOS A CALCULARLO", 74, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 330, 0.05)
    return fr

def dia(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 330, "140 kWh ÷ 30 días", 92, WHT)
    layer_pop(fr, L, u, W / 2, 380, 0.05)
    d = ImageDraw.Draw(fr)
    if u > dur * 0.4:
        k = ease((u - dur * 0.4) / 0.9)
        text_c(d, W / 2, 560, f"≈ {4.7 * k:.1f} kWh".replace(".", ","), 170, YEL, stroke=6, sfill=NAVY)
        text_c(d, W / 2, 780, "al día", 80, CYAN)
    return fr

f3 = foot("405", 0.0, zoom=(1.0, 1.15), dim=70)
def panel1(u, dur, t):
    fr = f3(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    sun(d, W / 2, 330, 110, t)
    layer_pop(fr, L, u, W / 2, 330, 0)
    L = new_layer(); d = ImageDraw.Draw(L)
    row(d, 520, "1 panel de 550 W", "≈ 2 kWh/día", YEL)
    layer_pop(fr, L, u, W / 2, 580, dur * 0.35)
    return fr

def cuatro(u, dur, t):
    fr = bg_frame(t)
    for k in range(4):
        L = new_layer(); d = ImageDraw.Draw(L)
        cx = 210 + k * 220
        panel(d, cx, 330, 180, 240)
        layer_pop(fr, L, u, cx, 330, 0.1 + k * 0.2, 0.25)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 500, "4 × 2 = 8 kWh/día", 84, YEL)
    layer_pop(fr, L, u, W / 2, 540, 1.0)
    # bars
    d = ImageDraw.Draw(fr)
    if u > dur * 0.45:
        k = ease((u - dur * 0.45) / 0.8); base = 1250; sc = 60
        for i, (lab, v, col) in enumerate([("Consumo", 5, CYAN), ("Producción", 8, GRN)]):
            x = 300 + i * 480; h = v * sc * k
            d.rounded_rectangle([x - 90, base - h, x + 90, base], radius=14, fill=col)
            text_c(d, x, base - h - 80, f"{v} kWh", 56, WHT)
            text_c(d, x, base + 15, lab, 48, GRY)
    return fr

f5 = foot("403", 0.0, zoom=(1.0, 1.12), dim=80)
def noche(u, dur, t):
    fr = f5(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    moon(d, W / 2, 230, 90)
    pill(d, W / 2, 380, "PARA LA NOCHE", 70, NAVY, CYAN)
    layer_pop(fr, L, u, W / 2, 300, 0)
    for i, (lab, val, col, at) in enumerate([("Batería de litio", "10 kWh", GRN, 0.25), ("Inversor", "5 kW", CYAN, 0.6)]):
        L = new_layer(); d = ImageDraw.Draw(L); row(d, 520 + i * 145, lab, val, col)
        layer_pop(fr, L, u, W / 2, 580 + i * 145, dur * at)
    return fr

f6 = foot("399", 12.0, zoom=(1.05, 1.2), focus=(0.5, 0.4), dim=80)
def adios(u, dur, t):
    fr = f6(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 330, "ADIÓS APAGÓN", 96, NAVY, GRN)
    layer_pop(fr, L, u, W / 2, 380, 0.05)
    return fr

def cta(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    chat(d, W / 2, 480, 180); layer_pop(fr, L, u, W / 2, 480, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 760, "¿Cuánto gastas tú?", 92, WHT)
    pill(d, W / 2, 920, "ESCRÍBELO EN COMENTARIOS", 58, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 860, 0.3)
    return fr

fns = [hook, calc, dia, panel1, cuatro, noche, adios, cta]
scenes = [(0 if i == 0 else S(i), S(i + 1) if i < 7 else TOTAL, fn) for i, fn in enumerate(fns)]
render("/home/claude/w2/s1.mp4", TOTAL, scenes, track)
