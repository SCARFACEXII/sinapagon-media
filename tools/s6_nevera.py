from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["nevera"]
SP = ["Nevera vieja contra nevera inverter. ¿Cuál se come tu batería?",
      "Round uno: consumo al día. La vieja, unos dos kilowatts hora. La inverter, menos de uno. Punto para la inverter.",
      "Round dos: el arranque. La vieja arranca de golpe y pide hasta seis veces su potencia. La inverter arranca suave. Dos a cero.",
      "Round tres: el precio. La vieja ya la tienes: no te cuesta nada. Punto para la vieja.",
      "Resultado: dos a uno. Si vas a poner paneles, la inverter te ahorra casi la mitad de batería.",
      "¿Tu nevera es vieja o inverter? Dímelo en los comentarios."]
SH = ["Nevera vieja vs nevera inverter. ¿Cuál se come tu batería?",
      "Round 1: consumo. Vieja ≈ 2 kWh/día. Inverter: menos de 1.",
      "Round 2: arranque. La vieja pide hasta 6 veces su potencia. La inverter, suave.",
      "Round 3: precio. La vieja ya la tienes: no te cuesta nada.",
      "Resultado: 2 a 1. La inverter te ahorra casi la mitad de batería.",
      "¿Tu nevera es vieja o inverter? Dímelo en comentarios."]
OLD = (200, 200, 190); NEWC = GRN
def board(fr, a, b, rnd=None):
    d = ImageDraw.Draw(fr); d.rounded_rectangle([80, 60, W - 80, 210], radius=30, fill=(0, 0, 0, 200), outline=(255, 255, 255, 80), width=3)
    text_c(d, 250, 90, "VIEJA", 58, (230, 200, 120)); text_c(d, W - 250, 90, "INVERTER", 58, NEWC); text_c(d, W / 2, 72, f"{a} - {b}", 88, YEL)
    if rnd: pill(d, W / 2, 250, rnd, 52, NAVY, YEL)
def two(d):
    fridge(d, 280, 640, 200, col=(225, 215, 190)); fridge(d, W - 280, 640, 200)
def hole(u, dur, t): return bg_ring(t)
def r1(u, dur, t):
    fr = bg_ring(t); board(fr, 0, 1 if u > dur * 0.85 else 0, "ROUND 1 · CONSUMO"); d = ImageDraw.Draw(fr); two(d)
    if u > dur * 0.25: text_c(d, 280, 880, "≈ 2 kWh", 80, RED)
    if u > dur * 0.5: text_c(d, W - 280, 880, "< 1 kWh", 80, GRN)
    return fr
def r2(u, dur, t):
    fr = bg_ring(t); board(fr, 0, 2 if u > dur * 0.85 else 1, "ROUND 2 · ARRANQUE"); d = ImageDraw.Draw(fr); two(d)
    if u > dur * 0.2:
        for k in range(3): bolt(d, 180 + k * 100, 360, 50, RED)
        text_c(d, 280, 880, "×6 de golpe", 66, RED)
    if u > dur * 0.6: text_c(d, W - 280, 880, "Suave", 80, GRN)
    return fr
def r3(u, dur, t):
    fr = bg_ring(t); board(fr, 1 if u > dur * 0.7 else 0, 2, "ROUND 3 · PRECIO"); d = ImageDraw.Draw(fr); two(d)
    if u > dur * 0.3: text_c(d, 280, 880, "$0", 110, (230, 200, 120)); text_c(d, W - 280, 880, "$$$", 110, GRN)
    if u > dur * 0.7: stamp(fr, u, "PUNTO", (230, 200, 120), 280, 1060, 80, dur * 0.7, ang=-8)
    return fr
def res(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 230, "GANA LA INVERTER", 80, WHT); text_c(d, W / 2, 340, "2 - 1", 200, GRN, stroke=6, sfill=NAVY)
    fridge(d, W / 2, 800, 190); stamp(fr, u, "-50% BATERÍA", GRN, W / 2, 1150, 96, 0.5, ang=-6); return fr
def cta(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 330, "¿Tu nevera es...", 100, WHT)
    pop(fr, u, 0.3, 300, 640, lambda dd: pill(dd, 300, 600, "VIEJA", 80, NAVY, (230, 200, 120)))
    pop(fr, u, 0.5, W - 300, 640, lambda dd: pill(dd, W - 300, 600, "INVERTER", 76, NAVY, GRN))
    stamp(fr, u, "COMENTA", YEL, W / 2, 900, 110, 0.8, ang=5); return fr
print(run("s6_nevera", D, SP, SH, [hole, r1, r2, r3, res, cta], (0,)))
