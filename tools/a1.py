from common2 import *
SP = ["Ya tienes paneles, inversor y batería... pero no te alcanza.", "¿Qué le agregas primero?", "Mira tu batería cuando se va el sol.",
      "Si no llega al cien por ciento, te faltan paneles.", "Si llega llena, pero se acaba antes de que amanezca, te falta batería.",
      "Y si todo se apaga cuando prendes la olla o el microondas, el problema es el inversor.",
      "¿Quieres saber qué le falta al tuyo? Usa la calculadora gratis del link en mi perfil... y sígueme para más."]
SH = ["Ya tienes paneles, inversor y batería... pero no te alcanza.", "¿Qué le agregas primero?", "Mira tu batería cuando se va el sol.",
      "Si no llega al 100%, te faltan PANELES.", "Si llega llena pero se acaba antes de amanecer, te falta BATERÍA.",
      "Si todo se apaga al prender la olla o el microondas, es el INVERSOR.", "¿Qué le falta al tuyo? Calculadora gratis en el link de mi perfil."]
f0 = foot("403", 0.0, zoom=(1.0, 1.12), dim=110)
def hook(u, dur, t):
    fr = f0(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 200, "Ya tienes sistema...", 84, WHT, stroke=8, sfill=NAVY); text_c(d, W / 2, 320, "¿y no te alcanza?", 96, YEL, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 280, 0.05)
    return fr
def que(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 250, "¿Qué le agregas", 96, WHT); text_c(d, W / 2, 370, "PRIMERO?", 130, YEL, stroke=6, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 330, 0)
    for k, (lab, col) in enumerate([("Paneles", YEL), ("Batería", GRN), ("Inversor", CYAN)]):
        L = new_layer(); d = ImageDraw.Draw(L); cx = 200 + k * 340
        pill(d, cx, 700, lab, 56, NAVY, col); layer_pop(fr, L, u, cx, 730, 0.3 + k * 0.15, 0.25)
    return fr
f2 = foot("399", 12.0, zoom=(1.05, 1.2), focus=(0.5, 0.4), dim=100)
def mira(u, dur, t):
    fr = f2(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 200, "EL TRUCO", 90, NAVY, YEL); text_c(d, W / 2, 360, "Mira tu batería", 90, WHT, stroke=8, sfill=NAVY); text_c(d, W / 2, 460, "al atardecer", 90, YEL, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 330, 0.05)
    d = ImageDraw.Draw(fr); sun(d, W / 2, 720, 90, t)
    return fr
f3 = foot("404", 1.0, zoom=(1.0, 1.15), dim=90)
def paneles(u, dur, t):
    fr = f3(u, dur); d = ImageDraw.Draw(fr)
    lvl = 0.7 * ease(u / 1.0); battery_icon(d, W / 2, 430, 200, 320, max(lvl, 0.02), col=YEL); text_c(d, W / 2, 400, f"{int(lvl*100)}%", 90, WHT, stroke=6, sfill=NAVY)
    if u > dur * 0.35:
        L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 660, "No llega al 100%", 76, WHT, stroke=8, sfill=NAVY)
        pill(d, W / 2, 800, "TE FALTAN PANELES", 74, NAVY, YEL); layer_pop(fr, L, u, W / 2, 780, dur * 0.35)
    return fr
f4 = foot("407", 0.5, zoom=(1.0, 1.12), dim=100)
def bateria(u, dur, t):
    fr = f4(u, dur); d = ImageDraw.Draw(fr)
    k = ease(u / max(1, dur * 0.6)); lvl = 1 - 0.97 * k
    battery_icon(d, W / 2 - 160, 430, 200, 320, max(lvl, 0.03), col=GRN if lvl > 0.5 else (YEL if lvl > 0.2 else RED)); moon(d, W / 2 + 200, 360, 80)
    text_c(d, W / 2 + 200, 520, "de noche", 54, WHT, stroke=6, sfill=NAVY)
    if u > dur * 0.5:
        L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 680, "Se acaba antes de amanecer", 64, WHT, stroke=8, sfill=NAVY)
        pill(d, W / 2, 820, "TE FALTA BATERÍA", 74, NAVY, GRN); layer_pop(fr, L, u, W / 2, 800, dur * 0.5)
    return fr
f5 = foot("406", 0.0, zoom=(1.0, 1.12), dim=110)
def inversor(u, dur, t):
    fr = f5(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pot(d, W / 2 - 220, 380, 110); microwave(d, W / 2 + 220, 380, 100)
    layer_pop(fr, L, u, W / 2, 380, 0.05)
    d = ImageDraw.Draw(fr)
    if u > dur * 0.3 and int(t * 6) % 2 == 0: warn(d, W / 2, 600, 70)
    if u > dur * 0.45:
        L = new_layer(); d = ImageDraw.Draw(L); text_c(d, W / 2, 720, "Se apaga todo", 76, WHT, stroke=8, sfill=NAVY)
        pill(d, W / 2, 860, "ES EL INVERSOR", 74, NAVY, CYAN); layer_pop(fr, L, u, W / 2, 840, dur * 0.45)
    return fr
def cta(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 330, "¿Qué le falta al tuyo?", 84, WHT); layer_pop(fr, L, u, W / 2, 380, 0)
    L = new_layer(); d = ImageDraw.Draw(L)
    d.rounded_rectangle([140, 480, W - 140, 860], radius=36, fill=(10, 30, 80), outline=YEL, width=5)
    text_c(d, W / 2, 520, "CALCULADORA GRATIS", 52, YEL); text_c(d, W / 2, 610, "Marca", 50, GRY); pill(d, W / 2, 730, "Sí, ya tengo", 56, NAVY, CYAN)
    layer_pop(fr, L, u, W / 2, 670, 0.3)
    L = new_layer(); d = ImageDraw.Draw(L); pill(d, W / 2, 980, "LINK EN MI PERFIL", 60, NAVY, GRN); pill(d, W / 2, 1110, "SÍGUEME PARA MÁS", 54, WHT, BLUE)
    layer_pop(fr, L, u, W / 2, 1040, 0.8)
    return fr
build("a1", SP, SH, [hook, que, mira, paneles, bateria, inversor, cta], "/home/claude/w2/a1.mp4")
