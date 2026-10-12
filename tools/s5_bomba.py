from engine3 import *
D = json.load(open("/home/claude/w2/voices5.json"))["bomba"]
SP = ["¿Se puede poner la bomba de agua con paneles solares?", "Sí, en tres pasos.",
      "Paso uno: mira la potencia de tu bomba. Una de medio caballo gasta unos cuatrocientos watts, pero al arrancar pide hasta tres veces más.",
      "Paso dos: el inversor. Para ese arranque necesitas un inversor de por lo menos tres kilowatts. Con un kit de cinco, vas sobrado.",
      "Paso tres: la hora. Llena el tanque de día, con el sol.",
      "Una hora de bomba son unos cuatrocientos watts hora, menos de lo que produce un solo panel en una mañana.",
      "Así no tocas la batería, y de noche tienes agua.",
      "¿De cuántos caballos es tu bomba? Dímelo en los comentarios."]
SH = ["¿La bomba de agua con paneles solares?", "Sí, en 3 pasos.",
      "Paso 1: bomba de ½ HP ≈ 400 W, pero al arrancar pide hasta 3 veces más.",
      "Paso 2: inversor de 3 kW como mínimo. Con un kit de 5 kW, vas sobrado.",
      "Paso 3: llena el tanque de día, con el sol.",
      "1 hora de bomba ≈ 400 Wh: menos de lo que da 1 panel en una mañana.",
      "Así no tocas la batería, y de noche tienes agua.",
      "¿De cuántos caballos es tu bomba? Dímelo en comentarios."]
def hole(u, dur, t): return bg_plano(t)
def head(fr, n, title):
    d = ImageDraw.Draw(fr); number_badge(d, 170, 200, n); d.text((270, 150), title, font=F(70), fill=WHT)
    d.line([(90, 300), (W - 90, 300)], fill=(200, 225, 255), width=3)
def pumpic(d, cx, cy, s, t):
    d.ellipse([cx - s * 0.7, cy - s * 0.5, cx + s * 0.3, cy + s * 0.5], fill=(70, 130, 220), outline=WHT, width=6)
    d.rectangle([cx + s * 0.2, cy - s * 0.2, cx + s * 1.1, cy + s * 0.05], fill=(150, 160, 180)); d.rectangle([cx - s * 0.35, cy - s * 0.95, cx - s * 0.05, cy - s * 0.45], fill=(150, 160, 180))
    for k in range(4):
        y = cy - s * 0.1 + ((t * 200 + k * 40) % 160); d.ellipse([cx + s * 1.1, y, cx + s * 1.25, y + 26], fill=CYAN)
def tres(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr); pumpic(d, W / 2 - 80, 430, 240, t)
    stamp(fr, u, "3 PASOS", YEL, W / 2, 860, 170, 0.05, ang=-5)
    return fr
def paso1(u, dur, t):
    fr = bg_plano(t); head(fr, 1, "Su potencia"); d = ImageDraw.Draw(fr)
    x0, x1, base = 120, W - 120, 1050; k = clamp(u / (dur * 0.65)); pts = []
    for i in range(int(120 * k)):
        tt = i / 120; v = (0.33 + 0.67 * math.exp(-((tt - 0.12) ** 2) / 0.0015)) if tt > 0.06 else 0
        pts.append((x0 + (x1 - x0) * tt, base - v * 480))
    d.line([(x0, base), (x1, base)], fill=WHT, width=4)
    if len(pts) > 1: d.line(pts, fill=YEL, width=10)
    if k > 0.25: d.text((x0 + 200, 520), "Arranque ≈ 1.200 W", font=F(54), fill=RED)
    if k > 0.6: d.text((x0 + 300, 1080), "Trabajando ≈ 400 W", font=F(54), fill=GRN)
    return fr
def paso2(u, dur, t):
    fr = bg_plano(t); head(fr, 2, "El inversor"); d = ImageDraw.Draw(fr)
    inverter(d, 300, 700, 210)
    if u > dur * 0.2: text_c(d, 740, 520, "Mínimo", 64, WHT); text_c(d, 740, 610, "3 kW", 150, YEL, stroke=5, sfill=NAVY)
    if u > dur * 0.6: pop(fr, u, dur * 0.6, W / 2, 1150, lambda dd: pill(dd, W / 2, 1110, "Kit 5 kW: vas sobrado ✓", 64, NAVY, GRN))
    return fr
def unahora(u, dur, t):
    fr = bg_plano(t); head(fr, 3, "Hazlo de día"); d = ImageDraw.Draw(fr)
    sun(d, 220, 520, 90, t); pumpic(d, 260, 900, 150, t)
    if u > dur * 0.15: text_c(d, 720, 430, "1 h de bomba", 62, WHT); text_c(d, 720, 520, "≈ 0,4 kWh", 110, YEL, stroke=5, sfill=NAVY)
    if u > dur * 0.5:
        panel(d, 720, 860, 230, 310); text_c(d, 720, 1040, "1 panel / mañana", 54, WHT); text_c(d, 720, 1110, "≈ 1 kWh", 80, GRN)
    return fr
def noche(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr); moon(d, W / 2, 330, 110)
    battery_icon(d, 330, 800, 220, 380, 1.0, col=GRN); text_c(d, 330, 1030, "Batería intacta", 56, GRN)
    for k in range(5):
        y = 640 + ((t * 220 + k * 70) % 330); d.line([(W - 330, y), (W - 330, y + 40)], fill=CYAN, width=14)
    d.rounded_rectangle([W - 430, 560, W - 230, 640], radius=16, fill=(200, 205, 215)); text_c(d, W - 330, 1030, "Agua de noche", 56, CYAN)
    return fr
def cta(u, dur, t):
    fr = bg_plano(t); d = ImageDraw.Draw(fr); pumpic(d, W / 2 - 60, 360, 200, t)
    text_c(d, W / 2, 640, "¿De cuántos caballos", 84, WHT); text_c(d, W / 2, 750, "es tu bomba?", 84, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 1050, 110, 0.5, ang=6)
    return fr
print(run("s5_bomba", D, SP, SH, [hole, tres, paso1, paso2, hole, unahora, noche, cta], (0, 4)))
