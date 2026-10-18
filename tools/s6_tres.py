from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["tres"]
SP = ["Tres cosas que nadie te dice antes de comprar paneles solares.",
      "Uno: lo que decide cuántas horas aguantas es la batería, no los paneles. Y es lo más caro del sistema.",
      "Dos: el inversor tiene que aguantar el arranque de la nevera, el aire y la bomba, no solo lo que gastan.",
      "Tres: no todas las baterías de litio son iguales. Pregunta por el BMS y por la garantía.",
      "La número uno es en la que más gente se equivoca.",
      "¿Cuál no sabías? Dímelo en los comentarios."]
SH = ["3 cosas que nadie te dice antes de comprar paneles.",
      "1: las horas que aguantas las decide la batería, no los paneles. Y es lo más caro.",
      "2: el inversor debe aguantar el arranque de nevera, aire y bomba.",
      "3: no todo el litio es igual. Pregunta por el BMS y la garantía.",
      "La número 1 es en la que más gente se equivoca.",
      "¿Cuál no sabías? Dímelo en comentarios."]
def hole(u, dur, t): return bg_alerta(t)
def head(fr, n): d = ImageDraw.Draw(fr); number_badge(d, W / 2, 230, n, col=RED, fg=WHT, r=90)
def uno(u, dur, t):
    fr = bg_alerta(t); head(fr, 1); d = ImageDraw.Draw(fr)
    panel(d, 280, 640, 220, 300); battery_icon(d, W - 280, 640, 230, 400, 0.8, col=GRN)
    if u > dur * 0.2: xmark(d, 280, 640, 90, w=16); check(d, W - 280, 900, 50)
    if u > dur * 0.6: stamp(fr, u, "LO MÁS CARO", YEL, W / 2, 1120, 96, dur * 0.6, ang=-5)
    return fr
def dos(u, dur, t):
    fr = bg_alerta(t); head(fr, 2); d = ImageDraw.Draw(fr); inverter(d, W / 2, 560, 170)
    for i, lab in enumerate(["Nevera", "Aire", "Bomba"]):
        if u > dur * (0.2 + i * 0.15): pill(d, 220 + i * 320, 860, lab, 56, NAVY, YEL); bolt(d, 220 + i * 320, 980, 40, RED)
    return fr
def tres(u, dur, t):
    fr = bg_alerta(t); head(fr, 3); d = ImageDraw.Draw(fr)
    battery_icon(d, 300, 640, 200, 360, 0.9, col=GRN); battery_icon(d, W - 300, 640, 200, 360, 0.9, col=GRN)
    if u > dur * 0.4:
        d.rounded_rectangle([200, 560, 400, 660], radius=14, fill=(10, 30, 60), outline=CYAN, width=5); text_c(d, 300, 570, "BMS", 56, CYAN)
        pill(d, W / 2, 960, "Garantía por escrito", 60, NAVY, GRN)
    if u > dur * 0.4: text_c(d, W - 300, 610, "?", 140, RED)
    return fr
def masgente(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr); number_badge(d, W / 2, 600, 1, col=YEL, r=200)
    stamp(fr, u, "OJO CON ESTA", RED, W / 2, 1000, 100, 0.2, ang=-5); return fr
def cta(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 360, "¿Cuál no", 110, WHT); text_c(d, W / 2, 490, "sabías?", 110, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 840, 120, 0.4, ang=6); return fr
print(run("s6_tres", D, SP, SH, [hole, uno, dos, tres, masgente, cta], (0,)))
