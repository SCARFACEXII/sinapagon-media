import json, sys
sys.path.insert(0, "/home/claude/w2")
from engine import *

TOTAL = json.load(open("/home/claude/w2/voices.json"))["v2"]["dur"] + 0.6
SPOKEN = ["¿Batería de litio, o de plomo?", "Te lo explico rápido.", "La de plomo es más barata al principio...",
          "pero dura unos quinientos ciclos, y solo puedes usar la mitad de su capacidad.",
          "La de litio cuesta más, pero dura más de tres mil ciclos, y puedes usar casi toda su energía.",
          "O sea: una batería de litio dura lo mismo que seis de plomo.", "Al final, el litio sale más barato.",
          "¿Tú cuál tienes? Dímelo en los comentarios."]
SHOW = ["¿Batería de litio o de plomo?", "Te lo explico rápido.", "La de plomo es más barata al principio...",
        "pero dura unos 500 ciclos y solo usas el 50%.",
        "La de litio cuesta más, pero dura 3.000+ ciclos y usas casi toda su energía.",
        "O sea: 1 de litio dura lo mismo que 6 de plomo.", "Al final, el litio sale más barato.",
        "¿Tú cuál tienes? Dímelo en comentarios."]
T = timings(SPOKEN, TOTAL - 0.6)
track = sub_track(SHOW, T)
S = lambda i: T[i][0]
LEAD = (95, 100, 110)

def vs(u, dur, t):
    fr = bg_frame(t)
    L = new_layer(); d = ImageDraw.Draw(L)
    battery_icon(d, 290, 780, 230, 360, 0.5, col=GRY, body=(40, 44, 52)); text_c(d, 290, 1030, "PLOMO", 76, GRY)
    layer_pop(fr, L, u, 290, 800, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    battery_icon(d, 790, 780, 230, 360, 0.95, col=CYAN); text_c(d, 790, 1030, "LITIO", 76, CYAN)
    layer_pop(fr, L, u, 790, 800, 0.3)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 700, "VS", 150, YEL, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 780, 0.6)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 260, "¿Cuál conviene", 88, WHT); text_c(d, W / 2, 370, "en Cuba?", 88, WHT)
    layer_pop(fr, L, u, W / 2, 360, 0.9)
    return fr

def row(d, y, label, value, vcol):
    d.rounded_rectangle([90, y, W - 90, y + 130], radius=30, fill=(14, 30, 70, 230), outline=(255, 255, 255, 40), width=3)
    d.text((140, y + 30), label, font=F(52, True), fill=WHT)
    f = F(64); tw = d.textlength(value, font=f); d.text((W - 140 - tw, y + 24), value, font=f, fill=vcol)

def plomo(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "PLOMO", 80, WHT, (70, 76, 88))
    battery_icon(d, W / 2, 470, 200, 300, 0.5, col=GRY, body=(40, 44, 52))
    layer_pop(fr, L, u, W / 2, 400, 0)
    t3 = S(3) - S(2)
    for i, (lab, val, col, at) in enumerate([("Precio inicial", "Más barata", GRN, 0.4), ("Vida útil", "≈ 500 ciclos", RED, t3 + 0.3), ("Capacidad usable", "50%", RED, t3 + 2.4)]):
        L = new_layer(); d = ImageDraw.Draw(L); row(d, 720 + i * 160, lab, val, col)
        layer_pop(fr, L, u, W / 2, 785 + i * 160, at)
    return fr

def litio(u, dur, t, fo=[None]):
    if fo[0] is None: fo[0] = Footage("/mnt/user-data/uploads/VID_20260513_125818762.mp4", 0.0, dur, zoom=(1.05, 1.2), focus=(0.5, 0.45))
    fr = fo[0].frame(u); fr.alpha_composite(Image.new("RGBA", (W, H), (0, 10, 30, 90)))
    L = new_layer(); d = ImageDraw.Draw(L); pill(d, W / 2, 150, "LITIO", 80, NAVY, CYAN)
    layer_pop(fr, L, u, W / 2, 190, 0)
    for i, (lab, val, col, at) in enumerate([("Precio inicial", "Más cara", YEL, 0.3), ("Vida útil", "3.000+ ciclos", GRN, dur * 0.35), ("Capacidad usable", "≈ 90%", GRN, dur * 0.7)]):
        L = new_layer(); d = ImageDraw.Draw(L); row(d, 720 + i * 160, lab, val, col)
        layer_pop(fr, L, u, W / 2, 785 + i * 160, at)
    return fr

def equals(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    battery_icon(d, W / 2, 470, 220, 330, 0.95, col=CYAN); text_c(d, W / 2, 680, "1 de LITIO", 70, CYAN)
    layer_pop(fr, L, u, W / 2, 500, 0)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 770, "=", 120, YEL)
    layer_pop(fr, L, u, W / 2, 830, 0.5)
    for k in range(6):
        L = new_layer(); d = ImageDraw.Draw(L)
        cx = 230 + (k % 3) * 310; cy = 1010 + (k // 3) * 0  # single row of 3 x2
        cx = 150 + k * 156; cy = 1000
        battery_icon(d, cx, cy, 110, 170, 0.5, col=GRY, body=(40, 44, 52))
        layer_pop(fr, L, u, cx, cy, 0.8 + k * 0.22, 0.25)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 1120, "6 de PLOMO", 70, GRY)
    layer_pop(fr, L, u, W / 2, 1150, 2.2)
    return fr

def winner(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 330, "A la larga...", 80, WHT)
    layer_pop(fr, L, u, W / 2, 380, 0)
    L = new_layer(); d = ImageDraw.Draw(L)
    battery_icon(d, W / 2, 760, 260, 390, 0.95, col=CYAN)
    bolt(d, W / 2, 760, 90)
    layer_pop(fr, L, u, W / 2, 760, 0.3)
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 1060, "EL LITIO SALE MÁS BARATO", 64, NAVY, GRN)
    layer_pop(fr, L, u, W / 2, 1090, 0.9)
    return fr

def cta(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    chat(d, W / 2, 520, 190); layer_pop(fr, L, u, W / 2, 520, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 800, "¿Tú cuál tienes?", 96, WHT); text_c(d, W / 2, 930, "Dímelo en comentarios", 60, YEL)
    layer_pop(fr, L, u, W / 2, 880, 0.3)
    return fr

scenes = [(0, S(2), vs), (S(2), S(4), plomo), (S(4), S(5), litio), (S(5), S(6), equals), (S(6), S(7), winner), (S(7), TOTAL, cta)]
render("/home/claude/w2/v2.mp4", TOTAL, scenes, track)
