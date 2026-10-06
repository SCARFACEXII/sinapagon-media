from engine3 import *
SP = ["¿Quieres poner el aire acondicionado con paneles solares?", "Hazlo en tres pasos.",
      "Paso uno: que sea inverter. Un split inverter de una tonelada gasta unos novecientos watts, y arranca suave, sin pico.",
      "Paso dos: calcula los paneles. Ocho horas de aire de día son unos siete kilowatts hora: con paneles de quinientos cincuenta, son unos cuatro paneles solo para él.",
      "Paso tres: de noche, la batería. Otras ocho horas de aire de noche piden otros siete kilowatts hora, así que necesitas una batería de quince en adelante.",
      "El truco: enfría el cuarto de día con el sol, y de noche ponlo en veintiséis grados con temporizador.",
      "Así gastas mucho menos batería.",
      "¿Tienes aire en casa? Dime cuántas toneladas es, y te digo cuántos paneles necesita."]
SH = ["¿Aire acondicionado con paneles solares?", "Hazlo en 3 pasos.",
      "Paso 1: que sea inverter. 1 tonelada ≈ 900 W, y arranca suave, sin pico.",
      "Paso 2: 8 horas de día ≈ 7 kWh. Con paneles de 550 W: unos 4 paneles solo para él.",
      "Paso 3: de noche, batería. 8 horas más ≈ 7 kWh: batería de 15 kWh en adelante.",
      "El truco: enfría el cuarto de día con el sol, y de noche a 26 °C con temporizador.",
      "Así gastas mucho menos batería.",
      "¿Tienes aire? Dime cuántas toneladas y te digo cuántos paneles."]
def hole(u, dur, t): return bg_plano(t)
def step_head(fr, u, n, title):
    d = ImageDraw.Draw(fr); number_badge(d, 170, 200, n); d.text((270, 150), title, font=F(70), fill=WHT)
    d.line([(90, 300), (W - 90, 300)], fill=(200, 225, 255), width=3)
def tres(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    ac_unit(d, W / 2, 380, 600, t)
    stamp(fr, u, "3 PASOS", YEL, W / 2, 820, 170, 0.05, ang=-5)
    return fr
def paso1(u, dur, t):
    fr = bg_plano(t); step_head(fr, u, 1, "Que sea INVERTER"); d = ImageDraw.Draw(fr)
    x0, x1, base = 120, W - 120, 1050; k = clamp(u / (dur * 0.6))
    d.line([(x0, base), (x1, base)], fill=WHT, width=4); d.line([(x0, base), (x0, 450)], fill=WHT, width=4)
    d.text((x0 + 10, 440), "Watts al arrancar", font=F(40), fill=GRY)
    old = []; new = []
    for i in range(int(120 * k)):
        x = x0 + (x1 - x0) * i / 120; tt = i / 120
        o = 0.45 + 0.85 * math.exp(-((tt - 0.12) ** 2) / 0.0012) if tt > 0.05 else 0
        n = 0.45 * ease((tt - 0.05) / 0.4) if tt > 0.05 else 0
        old.append((x, base - o * 420)); new.append((x, base - n * 420))
    if len(old) > 1: d.line(old, fill=RED, width=8); d.line(new, fill=GRN, width=10)
    if k > 0.3:
        d.text((x0 + 230, 540), "Normal: pico fuerte", font=F(46), fill=RED); d.text((x0 + 230, 1080), "Inverter: suave", font=F(46), fill=GRN)
    if u > dur * 0.6: pop(fr, u, dur * 0.6, W / 2, 1260, lambda dd: pill(dd, W / 2, 1220, "1 tonelada ≈ 900 W", 64, NAVY, YEL))
    return fr
def paso2(u, dur, t):
    fr = bg_plano(t); step_head(fr, u, 2, "Calcula los paneles"); d = ImageDraw.Draw(fr)
    sun(d, 200, 470, 70, t)
    if u > dur * 0.1: d.text((330, 420), "0,9 kW × 8 h", font=F(78), fill=WHT)
    if u > dur * 0.3: text_c(d, W / 2, 580, "≈ 7 kWh", 130, YEL, stroke=5, sfill=NAVY)
    n = int(clamp((u - dur * 0.55) / (dur * 0.3)) * 4) if u > dur * 0.55 else 0
    for i in range(n): panel(d, 190 + i * 233, 950, 200, 270)
    if n == 4: pop(fr, u, dur * 0.85, W / 2, 1200, lambda dd: pill(dd, W / 2, 1160, "4 PANELES de 550 W", 64, NAVY, GRN))
    return fr
def paso3(u, dur, t):
    fr = bg_plano(t); step_head(fr, u, 3, "De noche: batería"); d = ImageDraw.Draw(fr)
    moon(d, 210, 470, 80)
    if u > dur * 0.15: d.text((340, 420), "+ 8 h ≈ 7 kWh", font=F(78), fill=WHT)
    lvl = ease((u - dur * 0.45) / 1.4) if u > dur * 0.45 else 0
    battery_icon(d, W / 2, 900, 280, 470, lvl, col=GRN)
    if u > dur * 0.6: text_c(d, W / 2, 1170, "15 kWh o más", 92, YEL)
    return fr
def menos(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    d.rounded_rectangle([W / 2 - 260, 300, W / 2 + 260, 700], radius=40, fill=(240, 244, 250), outline=WHT, width=6)
    text_c(d, W / 2, 360, "26°C", 190, NAVY)
    clock(d, W / 2, 940, 150, 23, int(u * 20) % 60)
    if u > 0.4: stamp(fr, u, "MENOS BATERÍA", GRN, W / 2, 1220, 80, 0.4, ang=-5)
    return fr
def cta(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr)
    ac_unit(d, W / 2, 330, 520, t)
    text_c(d, W / 2, 640, "¿Cuántas toneladas", 88, WHT); text_c(d, W / 2, 750, "es tu aire?", 88, YEL)
    pop(fr, u, 0.5, W / 2, 960, lambda dd: pill(dd, W / 2, 920, "Te digo cuántos paneles", 60, NAVY, YEL))
    stamp(fr, u, "COMENTA", GRN, W / 2, 1190, 110, 0.9, ang=6)
    return fr
print(run("plano", 55.06612244897959, SP, SH, [hole, tres, paso1, paso2, paso3, hole, menos, cta], (0, 5)))
