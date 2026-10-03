from common2 import *
SP = ["¿Batería de gel, o de litio?", "Para tener cinco kilowatts hora útiles, mira la diferencia.",
      "Con gel, necesitas cuatro baterías de doscientos amperes, porque solo puedes usar la mitad de su energía.",
      "Con litio, te basta una sola batería de cuarenta y ocho voltios y cien amperes.",
      "Y además, el litio dura tres o cuatro veces más años.", "Al final, el litio sale más barato.", "¿Tú cuál tienes? Cuéntame en los comentarios."]
SH = ["¿Batería de gel o de litio?", "Para tener 5 kWh útiles, mira la diferencia.",
      "Con gel: 4 baterías de 200 Ah, porque solo usas la mitad de su energía.", "Con litio: 1 sola batería de 48 V y 100 Ah.",
      "Y el litio dura 3 o 4 veces más años.", "Al final, el litio sale más barato.", "¿Tú cuál tienes? Cuéntame en comentarios."]
GEL = (70, 76, 88)
def hook(u, dur, t):
    fr = bg_frame(t)
    for k in range(4):
        L = new_layer(); d = ImageDraw.Draw(L); cx = 120 + (k % 2) * 190; cy = 720 + (k // 2) * 300
        battery_icon(d, cx + 40, cy, 150, 230, 0.5, col=GRY, body=(40, 44, 52)); layer_pop(fr, L, u, cx + 40, cy, 0.1 + k * 0.08, 0.25)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, 255, 1200, "GEL", 70, GRY); layer_pop(fr, L, u, 255, 1220, 0.4)
    L = new_layer(); d = ImageDraw.Draw(L); battery_icon(d, 800, 870, 230, 380, 0.95, col=CYAN); text_c(d, 800, 1200, "LITIO", 70, CYAN)
    layer_pop(fr, L, u, 800, 870, 0.5)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, 555, 800, "VS", 110, YEL, stroke=8, sfill=NAVY); layer_pop(fr, L, u, 555, 860, 0.7)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 240, "¿Gel o litio?", 110, WHT); layer_pop(fr, L, u, W / 2, 300, 0)
    return fr
f1 = foot("403", 8.0, zoom=(1.0, 1.12), dim=110)
def meta(u, dur, t):
    fr = f1(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 230, "Para tener", 76, WHT, stroke=8, sfill=NAVY); pill(d, W / 2, 380, "5 kWh ÚTILES", 100, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 330, 0.05)
    return fr
def gel(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "GEL", 80, WHT, (70, 76, 88)); layer_pop(fr, L, u, W / 2, 190, 0)
    for k in range(4):
        L = new_layer(); d = ImageDraw.Draw(L); cx = 180 + k * 240
        battery_icon(d, cx, 520, 170, 270, 0.5, col=GRY, body=(40, 44, 52)); text_c(d, cx, 690, "200 Ah", 44, GRY)
        layer_pop(fr, L, u, cx, 520, 0.3 + k * 0.3, 0.25)
    if u > dur * 0.5:
        L = new_layer(); d = ImageDraw.Draw(L)
        d.line([(80, 520), (W - 80, 520)], fill=RED, width=6)
        pill(d, W / 2, 820, "Solo usas el 50%", 70, WHT, RED)
        layer_pop(fr, L, u, W / 2, 850, dur * 0.5)
    return fr
f3 = foot("402", 12.0, zoom=(1.0, 1.12), dim=90)
def litio(u, dur, t):
    fr = f3(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 170, "LITIO", 80, NAVY, CYAN)
    text_c(d, W / 2, 310, "1 sola batería", 90, WHT, stroke=8, sfill=NAVY); text_c(d, W / 2, 420, "48 V · 100 Ah", 90, CYAN, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 330, 0.05)
    return fr
def anos(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 200, "¿Cuántos años dura?", 84, WHT); layer_pop(fr, L, u, W / 2, 250, 0)
    d = ImageDraw.Draw(fr); k = ease((u - 0.3) / 1.2) if u > 0.3 else 0; base = 1150; sc = 45
    for i, (lab, v, col, txt) in enumerate([("Gel", 4, GRY, "≈ 4 años"), ("Litio", 15, CYAN, "≈ 15 años")]):
        x = 320 + i * 440; h = v * sc * k
        d.rounded_rectangle([x - 100, base - h, x + 100, base], radius=16, fill=col)
        text_c(d, x, base - h - 90, txt, 60, WHT); text_c(d, x, base + 20, lab, 60, col)
    return fr
f5 = foot("398", 6.6, zoom=(1.05, 1.15), dim=90)
def barato(u, dur, t):
    fr = f5(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 230, "Al final...", 84, WHT, stroke=8, sfill=NAVY); pill(d, W / 2, 380, "EL LITIO SALE MÁS BARATO", 64, NAVY, GRN)
    layer_pop(fr, L, u, W / 2, 330, 0.05)
    return fr
def cta(u, dur, t): return cta_frame(t, u, "¿Tú cuál tienes?", "CUÉNTAME EN COMENTARIOS")
build("g1", SP, SH, [hook, meta, gel, litio, anos, barato, cta], "/home/claude/w2/g1.mp4")
