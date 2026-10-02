from common2 import *
SP = ["¿Cocinar con paneles solares?", "Sí se puede... pero a la hora correcta.", "Una hornilla eléctrica gasta unos mil quinientos watts.",
      "Una hora de noche, se come casi un tercio de una batería de cinco kilowatts hora.",
      "El truco: cocina de día, cuando el sol da directo a los paneles.",
      "Así la energía sale del sol, no de la batería, y la batería queda llena para la noche.",
      "¿Tú cocinas con corriente o con gas? Cuéntame en los comentarios."]
SH = ["¿Cocinar con paneles solares?", "Sí se puede... pero a la hora correcta.", "Una hornilla eléctrica gasta unos 1.500 W.",
      "1 hora de noche se come casi 1/3 de una batería de 5 kWh.", "El truco: cocina de día, con el sol directo en los paneles.",
      "La energía sale del sol, no de la batería, y queda llena para la noche.", "¿Cocinas con corriente o con gas? Cuéntame en comentarios."]
def hook(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 200, "¿Cocinar con", 96, WHT); text_c(d, W / 2, 320, "PANELES SOLARES?", 96, YEL)
    layer_pop(fr, L, u, W / 2, 280, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L); hotplate(d, W / 2, 750, 260, t)
    layer_pop(fr, L, u, W / 2, 750, 0.4)
    return fr
def si(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    d.ellipse([W / 2 - 150, 300, W / 2 + 150, 600], fill=GRN)
    d.line([(W / 2 - 70, 455), (W / 2 - 10, 515), (W / 2 + 85, 390)], fill=WHT, width=32, joint="curve")
    text_c(d, W / 2, 640, "SÍ SE PUEDE", 100, GRN)
    layer_pop(fr, L, u, W / 2, 480, 0)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 820, "pero a la hora correcta", 66, WHT)
    layer_pop(fr, L, u, W / 2, 850, dur * 0.45)
    return fr
def consumo(u, dur, t):
    fr = bg_frame(t); d = ImageDraw.Draw(fr); hotplate(d, W / 2, 450, 230, t)
    L = new_layer(); d = ImageDraw.Draw(L); pill(d, W / 2, 700, "Hornilla eléctrica", 60, WHT, BLUE)
    layer_pop(fr, L, u, W / 2, 730, 0.1)
    d = ImageDraw.Draw(fr)
    if u > dur * 0.45:
        k = ease((u - dur * 0.45) / 0.9)
        text_c(d, W / 2, 850, f"≈ {int(1500 * k):,} W".replace(",", "."), 150, YEL, stroke=6, sfill=NAVY)
    return fr
def noche(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    moon(d, W / 2 - 300, 260, 80); text_c(d, W / 2 + 60, 210, "1 hora de noche", 74, WHT)
    layer_pop(fr, L, u, W / 2, 260, 0)
    d = ImageDraw.Draw(fr)
    lvl = 1 - 0.3 * ease((u - dur * 0.3) / 1.5) if u > dur * 0.3 else 1
    battery_icon(d, W / 2, 720, 260, 420, lvl, col=GRN if lvl > 0.75 else YEL)
    text_c(d, W / 2, 690, f"{int(lvl * 100)}%", 100, WHT, stroke=6, sfill=NAVY)
    text_c(d, W / 2, 970, "Batería de 5 kWh", 56, GRY)
    if u > dur * 0.6:
        L = new_layer(); d = ImageDraw.Draw(L); pill(d, W / 2, 1090, "−1,5 kWh ≈ 30%", 64, WHT, RED)
        layer_pop(fr, L, u, W / 2, 1120, dur * 0.6)
    return fr
f4 = foot("404", 0.0, zoom=(1.0, 1.15), dim=50)
def truco(u, dur, t):
    fr = f4(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 200, "EL TRUCO", 90, NAVY, YEL); text_c(d, W / 2, 360, "Cocina de DÍA", 100, WHT, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 280, 0.05)
    d = ImageDraw.Draw(fr); sun(d, W / 2, 620, 110, t)
    return fr
f5 = foot("402", 0.0, zoom=(1.0, 1.1), dim=80)
def llena(u, dur, t):
    fr = f5(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    sun(d, W / 2 - 230, 300, 80, t); text_c(d, W / 2 + 80, 260, "→ cocina", 70, YEL, stroke=6, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 300, 0)
    L = new_layer(); d = ImageDraw.Draw(L)
    battery_icon(d, W / 2 - 230, 620, 130, 200, 1.0, col=GRN); moon(d, W / 2 - 230 + 0, 470, 0)
    text_c(d, W / 2 + 120, 570, "Batería LLENA", 66, GRN, stroke=6, sfill=NAVY); text_c(d, W / 2 + 120, 660, "para la noche", 60, WHT, stroke=6, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 620, dur * 0.5)
    return fr
def cta(u, dur, t): return cta_frame(t, u, "¿Corriente o gas?", "CUÉNTAME EN COMENTARIOS")
build("c1", SP, SH, [hook, si, consumo, noche, truco, llena, cta], "/home/claude/w2/c1.mp4")
