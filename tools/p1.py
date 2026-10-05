from common2 import *
SP = ["¿Cuánto te dura una batería pequeña en el apagón?",
      "Una batería de doce voltios y cien amperes: unas ocho horas con un ventilador, el router y las luces. Pero con la nevera, no llegas a la mañana.",
      "Una estación portátil de dos kilowatts hora: la nevera, un ventilador y las luces, toda la noche.",
      "Y un kit de diez kilowatts hora: nevera, freezer, televisor y ventiladores, sin preocuparte.",
      "¿Cuál te sirve a ti? Depende de lo que quieras mantener encendido.",
      "Calcula el tuyo gratis con el link en mi perfil... y sígueme para más."]
SH = ["¿Cuánto te dura una batería pequeña en el apagón?",
      "12 V 100 Ah: unas 8 horas con ventilador, router y luces. Con la nevera, no llegas a la mañana.",
      "Estación portátil de 2 kWh: nevera, ventilador y luces toda la noche.",
      "Kit de 10 kWh: nevera, freezer, TV y ventiladores, sin preocuparte.",
      "¿Cuál te sirve? Depende de lo que quieras encender.", "Calcula el tuyo gratis: link en mi perfil."]
def hook(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 190, "¿Cuánto te dura", 96, WHT); text_c(d, W / 2, 310, "una batería pequeña?", 84, YEL)
    layer_pop(fr, L, u, W / 2, 260, 0.05)
    for k, (s, lab) in enumerate([(0.6, "12 V"), (0.8, "2 kWh"), (1.0, "10 kWh")]):
        L = new_layer(); d = ImageDraw.Draw(L); cx = 230 + k * 310; h = 220 * s + 120
        battery_icon(d, cx, 820 - h / 2 + 120, 120 + 60 * s, h, 0.8, col=[YEL, CYAN, GRN][k]); text_c(d, cx, 980, lab, 56, WHT)
        layer_pop(fr, L, u, cx, 800, 0.3 + k * 0.2, 0.25)
    return fr
def b12(u, dur, t):
    fr = bg_frame(t); d0 = ImageDraw.Draw(fr); battery_icon(d0, W / 2, 1060, 160, 240, 0.35, col=YEL)
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 140, "BATERÍA 12 V · 100 Ah", 64, NAVY, YEL); text_c(d, W / 2, 260, "≈ 8 horas", 110, WHT, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 210, 0)
    checks(fr, u, [("Ventilador", True), ("Router", True), ("Luces", True), ("Nevera toda la noche", False)], 470, dur * 0.2, dur * 0.17)
    return fr
def est(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 140, "ESTACIÓN PORTÁTIL · 2 kWh", 60, NAVY, CYAN); station(d, W / 2, 400, 180)
    layer_pop(fr, L, u, W / 2, 330, 0)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 600, "Toda la noche", 90, YEL); layer_pop(fr, L, u, W / 2, 640, dur * 0.6)
    checks(fr, u, [("Nevera", True), ("Ventilador", True), ("Luces", True)], 790, dur * 0.25, dur * 0.12)
    return fr
f3 = foot("403", 0.0, zoom=(1.0, 1.12), dim=120)
def kit(u, dur, t):
    fr = f3(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 140, "KIT 10 kWh", 70, NAVY, GRN); text_c(d, W / 2, 260, "Sin preocuparte", 90, WHT, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 210, 0)
    checks(fr, u, [("Nevera", True), ("Freezer", True), ("Televisor", True), ("Ventiladores", True)], 470, dur * 0.15, dur * 0.14)
    return fr
def cual(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 300, "¿Cuál te sirve?", 110, WHT); text_c(d, W / 2, 460, "Depende de lo que", 66, GRY); text_c(d, W / 2, 540, "quieras encender", 66, YEL)
    layer_pop(fr, L, u, W / 2, 420, 0)
    return fr
def cta(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    chat(d, W / 2, 420, 160); layer_pop(fr, L, u, W / 2, 420, 0)
    L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 660, "Calcula el tuyo gratis", 80, WHT)
    pill(d, W / 2, 820, "LINK EN MI PERFIL", 64, NAVY, GRN); pill(d, W / 2, 960, "SÍGUEME PARA MÁS", 54, WHT, BLUE)
    layer_pop(fr, L, u, W / 2, 860, 0.3)
    return fr
build("p1", SP, SH, [hook, b12, est, kit, cual, cta], "/home/claude/w2/p1.mp4")
