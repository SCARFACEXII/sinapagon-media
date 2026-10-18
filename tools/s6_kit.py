from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["kit"]
SP = ["¿Kit de cinco kilowatts o de diez? Mira cuál te toca.",
      "Te toca el de cinco si en el apagón quieres mover nevera, ventiladores, televisor, luces, y alguna cosa de cocina de día.",
      "Te toca el de diez si quieres aire acondicionado de noche, dos neveras o freezer, o una casa grande.",
      "¿Dudas? Pon tus equipos en la calculadora del primer comentario: te dice cuál es el tuyo en un minuto.",
      "¿Cuál crees que te toca? Escríbelo en los comentarios."]
SH = ["¿Kit de 5 kW o de 10 kW? Mira cuál te toca.",
      "El de 5 kW: nevera, ventiladores, TV, luces y algo de cocina de día.",
      "El de 10 kW: aire de noche, 2 neveras o freezer, o casa grande.",
      "¿Dudas? La calculadora del primer comentario te lo dice en 1 minuto.",
      "¿Cuál crees que te toca? Escríbelo en comentarios."]
f402 = foot("402", 0.0, zoom=(1.0, 1.12), dim=110)
def hook(u, dur, t):
    fr = f402(u, dur); d = ImageDraw.Draw(fr)
    pop(fr, u, 0.05, W / 2, 330, lambda dd: (pill(dd, 300, 290, "5 kW", 110, NAVY, CYAN), pill(dd, W - 300, 290, "10 kW", 110, NAVY, YEL)))
    stamp(fr, u, "¿CUÁL TE TOCA?", WHT, W / 2, 620, 100, 0.4, ang=-5); return fr
def card(fr, u, dur, title, col, specs, items):
    fr2 = bg_quiz(0) if fr is None else fr; d = ImageDraw.Draw(fr2)
    d.rounded_rectangle([70, 140, W - 70, 1260], radius=40, fill=(10, 20, 50, 220), outline=col, width=8)
    text_c(d, W / 2, 180, title, 110, col); text_c(d, W / 2, 330, specs, 52, WHT)
    for i, (txt, at) in enumerate(items):
        if u < dur * at: continue
        y = 470 + i * 140; check(d, 170, y + 40, 34, w=12); d.text((230, y), txt, font=F(62), fill=WHT)
    return fr2
def k5(u, dur, t):
    return card(bg_quiz(t), u, dur, "KIT 5 kW", CYAN, "4 paneles · 10 kWh litio", [("Nevera", 0.1), ("Ventiladores", 0.25), ("Televisor", 0.4), ("Luces", 0.5), ("Cocina de día", 0.65)])
def k10(u, dur, t):
    return card(bg_quiz(t), u, dur, "KIT 10 kW", YEL, "12 paneles · 15 kWh litio", [("Aire de noche", 0.15), ("2 neveras o freezer", 0.4), ("Casa grande", 0.65)])
def calc(u, dur, t):
    fr = bg_quiz(t); d = ImageDraw.Draw(fr)
    d.rounded_rectangle([W / 2 - 230, 260, W / 2 + 230, 1080], radius=50, fill=(20, 22, 30), outline=WHT, width=8)
    d.rounded_rectangle([W / 2 - 200, 320, W / 2 + 200, 1020], radius=24, fill=(8, 32, 79))
    text_c(d, W / 2, 360, "CALCULADORA", 46, YEL)
    for i in range(4): d.rounded_rectangle([W / 2 - 170, 460 + i * 110, W / 2 + 170, 540 + i * 110], radius=16, fill=(30, 60, 120))
    if u > dur * 0.4: pill(d, W / 2, 930, "Tu kit: 5 kW ✓", 48, NAVY, GRN)
    if u > dur * 0.6: stamp(fr, u, "1er COMENTARIO", YEL, W / 2, 1220, 70, dur * 0.6, ang=-4)
    return fr
def cta(u, dur, t):
    fr = bg_quiz(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 330, "¿Cuál crees", 100, WHT); text_c(d, W / 2, 450, "que te toca?", 100, YEL)
    pop(fr, u, 0.3, 300, 690, lambda dd: pill(dd, 300, 650, "5 kW", 90, NAVY, CYAN)); pop(fr, u, 0.5, W - 300, 690, lambda dd: pill(dd, W - 300, 650, "10 kW", 90, NAVY, YEL))
    stamp(fr, u, "COMENTA", GRN, W / 2, 950, 110, 0.8, ang=5); return fr
print(run("s6_kit", D, SP, SH, [hook, k5, k10, calc, cta], ()))
