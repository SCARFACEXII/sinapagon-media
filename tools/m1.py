import json, sys
sys.path.insert(0, "/home/claude/w2")
from engine import *

U = "/root/.claude/uploads/496944e7-2387-59a5-b6d7-4284eb12520e/"
CL = {k: U + v for k, v in {"404": "0731b340-VID-20261001-WA0404.mp4", "402": "3632993f-VID-20261001-WA0402.mp4",
      "399": "b45c053a-VID-20261001-WA0399.mp4", "406": "45d642d2-VID-20261001-WA0406.mp4", "403": "65a8fd6a-VID-20261001-WA0403.mp4",
      "405": "4debce8f-VID-20261001-WA0405.mp4", "407": "8f9207e7-VID-20261001-WA0407.mp4"}.items()}

TOTAL = json.load(open("/home/claude/w2/voices.json"))["m1"]["dur"] + 0.6
SPOKEN = ["Así quedan instalaciones solares reales, aquí en Cuba.",
          "Este es el kit más pedido: inversor de cinco kilowatts, cuatro paneles solares, y diez kilowatts hora de batería de litio.",
          "Con eso mueves nevera, freezer, televisor, ventiladores y luces...", "y pasas la noche sin apagón.",
          "¿Y si quieres poner aire acondicionado?",
          "Entonces vas al grande: inversor de diez kilowatts, doce paneles, y quince kilowatts hora de batería.",
          "Ese aguanta la casa completa, aire incluido.", "¿Cuál de los dos necesitas tú? Escríbeme en los comentarios."]
SHOW = ["Así quedan instalaciones solares reales en Cuba.",
        "El kit más pedido: inversor de 5 kW, 4 paneles y 10 kWh de batería de litio.",
        "Con eso mueves nevera, freezer, TV, ventiladores y luces...", "y pasas la noche sin apagón.",
        "¿Y si quieres poner aire acondicionado?",
        "Vas al grande: inversor de 10 kW, 12 paneles y 15 kWh de batería.",
        "Ese aguanta la casa completa, aire incluido.", "¿Cuál de los dos necesitas tú? Escríbeme en comentarios."]
T = timings(SPOKEN, TOTAL - 0.6)
track = sub_track(SHOW, T)
S = lambda i: T[i][0]

def foot(key, start, zoom=(1.0, 1.12), focus=(0.5, 0.5), dim=60):
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

f0 = foot("404", 0.0, zoom=(1.0, 1.15), dim=30)
def hook(u, dur, t):
    fr = f0(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 200, "MONTAJES REALES", 76, NAVY, YEL)
    text_c(d, W / 2, 330, "Así quedan en Cuba", 78, WHT, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 260, 0.05)
    return fr

f1 = foot("402", 0.0, zoom=(1.0, 1.1), dim=70)
def kit5(u, dur, t):
    fr = f1(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 170, "KIT MÁS PEDIDO", 72, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 200, 0)
    for i, (lab, val, col, at) in enumerate([("Inversor", "5 kW", CYAN, 0.30), ("Paneles solares", "4", YEL, 0.52), ("Batería de litio", "10 kWh", GRN, 0.72)]):
        L = new_layer(); d = ImageDraw.Draw(L); row(d, 330 + i * 145, lab, val, col)
        layer_pop(fr, L, u, W / 2, 390 + i * 145, dur * at)
    return fr

f2 = foot("399", 12.0, zoom=(1.05, 1.2), focus=(0.5, 0.4), dim=80)
def equipos(u, dur, t):
    fr = f2(u, dur)
    items = ["Nevera", "Freezer", "Televisor", "Ventiladores", "Luces"]
    for i, it in enumerate(items):
        L = new_layer(); d = ImageDraw.Draw(L)
        y = 260 + i * 130
        pill(d, W / 2, y, "✓  " + it, 64, NAVY, GRN)
        layer_pop(fr, L, u, W / 2, y + 30, 0.15 + i * dur * 0.16, 0.25)
    return fr

f3 = foot("406", 0.0, zoom=(1.0, 1.12), dim=110)
def noche(u, dur, t):
    fr = f3(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    moon(d, W / 2, 380, 120)
    pill(d, W / 2, 600, "TODA LA NOCHE", 80, NAVY, CYAN)
    layer_pop(fr, L, u, W / 2, 480, 0.05)
    return fr

f4 = foot("403", 0.0, zoom=(1.0, 1.12), dim=110)
def aire(u, dur, t):
    fr = f4(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    ac_unit(d, W / 2, 360, 520, t)
    text_c(d, W / 2, 600, "¿Y con AIRE?", 110, YEL, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 470, 0.05)
    return fr

f5 = foot("405", 0.0, zoom=(1.0, 1.15), dim=70)
def kit10(u, dur, t):
    fr = f5(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 170, "KIT GRANDE", 72, WHT, BLUE)
    layer_pop(fr, L, u, W / 2, 200, 0)
    for i, (lab, val, col, at) in enumerate([("Inversor", "10 kW", CYAN, 0.25), ("Paneles solares", "12", YEL, 0.45), ("Batería de litio", "15 kWh", GRN, 0.66)]):
        L = new_layer(); d = ImageDraw.Draw(L); row(d, 330 + i * 145, lab, val, col)
        layer_pop(fr, L, u, W / 2, 390 + i * 145, dur * at)
    return fr

f6 = foot("407", 0.5, zoom=(1.0, 1.12), dim=70)
def completa(u, dur, t):
    fr = f6(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 230, "CASA COMPLETA", 84, NAVY, GRN)
    pill(d, W / 2, 380, "+ AIRE ACONDICIONADO", 60, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 300, 0.1)
    return fr

def card(d, x0, title, lines, col):
    d.rounded_rectangle([x0, 560, x0 + 430, 1060], radius=36, fill=(10, 26, 64, 235), outline=col, width=6)
    cx = x0 + 215
    text_c(d, cx, 600, title, 66, col)
    for i, ln in enumerate(lines): text_c(d, cx, 730 + i * 100, ln, 52, WHT)

def cta(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 250, "¿Cuál necesitas tú?", 92, WHT)
    layer_pop(fr, L, u, W / 2, 300, 0)
    L = new_layer(); d = ImageDraw.Draw(L); card(d, 90, "KIT 5 kW", ["4 paneles", "10 kWh", "Sin aire"], CYAN)
    layer_pop(fr, L, u, 305, 800, 0.3)
    L = new_layer(); d = ImageDraw.Draw(L); card(d, 560, "KIT 10 kW", ["12 paneles", "15 kWh", "Con aire"], YEL)
    layer_pop(fr, L, u, 775, 800, 0.55)
    L = new_layer(); d = ImageDraw.Draw(L); pill(d, W / 2, 1180, "ESCRÍBEME EN COMENTARIOS", 56, NAVY, GRN)
    layer_pop(fr, L, u, W / 2, 1210, 1.0)
    return fr

fns = [hook, kit5, equipos, noche, aire, kit10, completa, cta]
scenes = [(S(i), S(i + 1) if i < 7 else TOTAL, fn) for i, fn in enumerate(fns)]
scenes[0] = (0, S(1), hook)
render("/home/claude/w2/m1.mp4", TOTAL, scenes, track)
