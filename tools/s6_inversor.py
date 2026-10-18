from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["inversor"]
SP = ["Inversor de baja frecuencia contra alta frecuencia. ¿Cuál te conviene?",
      "Quédate hasta el final, que aquí se equivoca mucha gente.",
      "El de baja frecuencia lleva por dentro un transformador grande de cobre y hierro. Por eso pesa tanto: uno de seis kilowatts puede pasar de cuarenta kilos.",
      "El de alta frecuencia no lleva ese transformador. Pesa la mitad o menos, y casi todos los híbridos modernos son así.",
      "Round uno, los arranques. El de baja frecuencia aguanta picos de hasta tres veces su potencia por varios segundos. Bombas de pozo, aires viejos, compresores: ahí brilla.",
      "El de alta frecuencia aguanta picos más cortos, por eso hay que ponerlo con margen.",
      "Round dos, el consumo. El de alta frecuencia es más eficiente, y gasta menos batería solo por estar encendido.",
      "Round tres, todo en uno. El híbrido de alta frecuencia trae controlador solar, pantalla y aplicación en el mismo equipo. Al de baja, muchas veces hay que ponerle el controlador aparte.",
      "Round cuatro, la reparación. El de baja frecuencia se repara más fácil. En el de alta, si se quema la placa, muchas veces toca cambiarla completa.",
      "Resultado: empate, dos a dos.",
      "Para una casa normal, con nevera, ventiladores y aire inverter, el híbrido de alta frecuencia va perfecto.",
      "Si mueves motores grandes, el de baja frecuencia aguanta mejor el golpe.",
      "¿Cuál tienes tú, baja o alta? Dímelo en los comentarios."]
SH = ["Inversor de baja frecuencia vs alta frecuencia. ¿Cuál te conviene?",
      "Quédate hasta el final: aquí se equivoca mucha gente.",
      "Baja frecuencia: transformador grande de cobre y hierro. Uno de 6 kW puede pasar de 40 kg.",
      "Alta frecuencia: sin ese transformador. Pesa la mitad o menos. Así son casi todos los híbridos.",
      "Round 1: arranques. El de baja aguanta picos de hasta 3 veces su potencia por varios segundos. Bombas, aires viejos, compresores.",
      "El de alta aguanta picos más cortos: ponlo con margen.",
      "Round 2: consumo. El de alta es más eficiente y gasta menos batería solo por estar encendido.",
      "Round 3: todo en uno. El híbrido trae controlador solar, pantalla y app. Al de baja, muchas veces, hay que ponerle el controlador aparte.",
      "Round 4: reparación. El de baja se repara más fácil. En el de alta, si se quema la placa, toca cambiarla.",
      "Resultado: empate, 2 a 2.",
      "Casa normal (nevera, ventiladores, aire inverter): el híbrido de alta va perfecto.",
      "Motores grandes: el de baja aguanta mejor el golpe.",
      "¿Cuál tienes tú, baja o alta? Dímelo en comentarios."]
BAJ = (240, 150, 50); ALT = CYAN
LX, RX = 290, W - 290

def lf(d, cx, cy, s, cut=False):
    # inversor de baja frecuencia: caja ancha y pesada
    d.rounded_rectangle([cx - s, cy - s * 0.95, cx + s, cy + s * 0.95], radius=26, fill=(70, 76, 88), outline=WHT, width=5)
    d.rounded_rectangle([cx - s * 0.6, cy - s * 0.75, cx + s * 0.6, cy - s * 0.4], radius=10, fill=(20, 60, 90))
    text_c(d, cx, cy - s * 0.72, "LF", int(s * 0.24), BAJ)
    if cut:
        # transformador: núcleo de hierro + bobinas de cobre
        d.rectangle([cx - s * 0.62, cy - s * 0.25, cx + s * 0.62, cy + s * 0.78], fill=(40, 44, 52), outline=(150, 150, 160), width=4)
        d.rectangle([cx - s * 0.5, cy - s * 0.15, cx + s * 0.5, cy + s * 0.68], fill=(120, 124, 132))
        d.rectangle([cx - s * 0.18, cy - s * 0.15, cx + s * 0.18, cy + s * 0.68], fill=(90, 94, 100))
        for k in range(7):
            y = cy - s * 0.1 + k * s * 0.11
            d.rounded_rectangle([cx - s * 0.36, y, cx + s * 0.36, y + s * 0.08], radius=6, fill=(205, 120, 50))
    else:
        for k in range(4): d.rectangle([cx - s * 0.7, cy - s * 0.1 + k * s * 0.2, cx + s * 0.7, cy - s * 0.02 + k * s * 0.2], fill=(120, 126, 136))

def hf(d, cx, cy, s): inverter(d, cx, cy, s)

def board(fr, a, b, rnd=None):
    d = ImageDraw.Draw(fr); d.rounded_rectangle([80, 60, W - 80, 210], radius=30, fill=(0, 0, 0, 200), outline=(255, 255, 255, 80), width=3)
    text_c(d, 240, 90, "BAJA", 60, BAJ); text_c(d, W - 240, 90, "ALTA", 60, ALT); text_c(d, W / 2, 72, f"{a} - {b}", 88, YEL)
    if rnd: pill(d, W / 2, 250, rnd, 50, NAVY, YEL)

def pair(d, cy=620):
    lf(d, LX, cy, 170); hf(d, RX, cy, 150)

def wrench(d, cx, cy, s, col=(200, 205, 215)):
    d.line([(cx - s, cy + s), (cx + s * 0.5, cy - s * 0.5)], fill=col, width=int(s * 0.32))
    d.ellipse([cx + s * 0.2, cy - s * 1.0, cx + s * 1.0, cy - s * 0.2], fill=col)
    d.ellipse([cx + s * 0.5, cy - s * 0.9, cx + s * 0.95, cy - s * 0.45], fill=(30, 30, 40))

def pump(d, cx, cy, s):
    d.ellipse([cx - s, cy - s * 0.7, cx + s * 0.4, cy + s * 0.7], fill=(70, 130, 220), outline=WHT, width=5)
    d.rectangle([cx + s * 0.3, cy - s * 0.3, cx + s * 1.1, cy + s * 0.3], fill=(150, 160, 175), outline=WHT, width=4)
    d.rectangle([cx - s * 0.5, cy + s * 0.6, cx + s * 0.2, cy + s * 0.9], fill=(90, 95, 105))

def hole(u, dur, t): return bg_ring(t)

def quedate(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); pair(d, 560)
    pill(d, LX, 830, "BAJA FREC.", 56, NAVY, BAJ); pill(d, RX, 830, "ALTA FREC.", 56, NAVY, ALT)
    text_c(d, W / 2, 530, "VS", 84, YEL, stroke=5, sfill=NAVY)
    if u > dur * 0.3: stamp(fr, u, "HASTA EL FINAL", RED, W / 2, 1100, 92, dur * 0.3, ang=-5)
    return fr

def baja(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); pill(d, W / 2, 140, "BAJA FRECUENCIA", 64, NAVY, BAJ)
    lf(d, W / 2, 620, 280, cut=u > dur * 0.2)
    if u > dur * 0.2: pill(d, W / 2, 960, "Transformador de cobre y hierro", 50, WHT, (40, 40, 50))
    if u > dur * 0.6: stamp(fr, u, "+40 kg", RED, W / 2, 1160, 130, dur * 0.6, ang=-6)
    return fr

def alta(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); pill(d, W / 2, 140, "ALTA FRECUENCIA", 64, NAVY, ALT)
    lf(d, LX, 620, 190); hf(d, RX, 650, 150)
    if u > dur * 0.25: text_c(d, LX, 830, "Con transformador", 44, BAJ); text_c(d, RX, 800, "Sin transformador", 44, ALT)
    if u > dur * 0.35: text_c(d, RX, 880, "½ del peso", 70, GRN)
    if u > dur * 0.6: pill(d, W / 2, 1060, "Así son casi todos los híbridos", 52, NAVY, ALT)
    return fr

def r1(u, dur, t):
    fr = bg_ring(t); board(fr, 1 if u > dur * 0.85 else 0, 0, "ROUND 1 · ARRANQUES"); d = ImageDraw.Draw(fr); pair(d)
    if u > dur * 0.2:
        for k in range(3): bolt(d, LX - 100 + k * 100, 380, 46, YEL)
        text_c(d, LX, 860, "×3 por segundos", 60, GRN)
    if u > dur * 0.55:
        pump(d, 230, 1060, 70); ac_unit(d, W / 2, 1040, 220, t)
        d.ellipse([W - 300, 990, W - 160, 1130], fill=(160, 170, 185), outline=WHT, width=5); text_c(d, W - 230, 1140, "Compresor", 40, WHT)
    return fr

def r1b(u, dur, t):
    fr = bg_ring(t); board(fr, 1, 0, "ROUND 1 · ARRANQUES"); d = ImageDraw.Draw(fr); pair(d)
    bolt(d, RX, 380, 46, YEL); text_c(d, RX, 860, "Picos cortos", 60, YEL)
    if u > dur * 0.4: stamp(fr, u, "PONLO CON MARGEN", YEL, W / 2, 1080, 84, dur * 0.4, ang=-5)
    return fr

def r2(u, dur, t):
    fr = bg_ring(t); board(fr, 1, 1 if u > dur * 0.8 else 0, "ROUND 2 · CONSUMO"); d = ImageDraw.Draw(fr)
    k = ease(u / dur)
    battery_icon(d, LX, 640, 220, 400, 1 - 0.35 * k, col=YEL); battery_icon(d, RX, 640, 220, 400, 1 - 0.15 * k, col=GRN)
    text_c(d, LX, 880, "Gasta más", 60, BAJ); text_c(d, RX, 880, "Gasta menos", 60, GRN)
    if u > dur * 0.4: pill(d, W / 2, 1060, "solo por estar encendido", 56, NAVY, YEL)
    return fr

def r3(u, dur, t):
    fr = bg_ring(t); board(fr, 1, 2 if u > dur * 0.85 else 1, "ROUND 3 · TODO EN UNO"); d = ImageDraw.Draw(fr); pair(d, 560)
    for i, (lab, at) in enumerate([("Controlador solar", 0.15), ("Pantalla", 0.3), ("App", 0.42)]):
        if u > dur * at: pill(d, RX, 800 + i * 110, lab, 46, NAVY, ALT)
    if u > dur * 0.6: pill(d, LX, 800, "+ controlador", 46, NAVY, BAJ); text_c(d, LX, 870, "aparte", 46, BAJ)
    return fr

def r4(u, dur, t):
    fr = bg_ring(t); board(fr, 2 if u > dur * 0.85 else 1, 2, "ROUND 4 · REPARACIÓN"); d = ImageDraw.Draw(fr); pair(d, 560)
    if u > dur * 0.2: wrench(d, LX, 900, 60); text_c(d, LX, 1010, "Se repara", 60, GRN)
    if u > dur * 0.55:
        d.rounded_rectangle([RX - 110, 840, RX + 110, 960], radius=10, fill=(20, 110, 60), outline=WHT, width=4)
        for k in range(5): d.rectangle([RX - 90 + k * 40, 860, RX - 70 + k * 40, 880], fill=(30, 30, 30))
        xmark(d, RX, 900, 70); text_c(d, RX, 1010, "Cambiar placa", 56, RED)
    return fr

def res(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 220, "RESULTADO", 80, WHT); text_c(d, W / 2, 330, "2 - 2", 200, YEL, stroke=6, sfill=NAVY)
    pair(d, 780); stamp(fr, u, "EMPATE", YEL, W / 2, 1130, 120, 0.3, ang=-6); return fr

def casa(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); pill(d, W / 2, 160, "CASA NORMAL", 64, NAVY, WHT)
    fridge(d, 230, 470, 110); fan(d, W / 2, 440, 80, t); ac_unit(d, W - 230, 430, 260, t)
    hf(d, W / 2, 800, 150)
    if u > dur * 0.4: pill(d, W / 2, 1050, "Híbrido de alta frecuencia ✓", 56, NAVY, GRN)
    return fr

def motores(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); pill(d, W / 2, 160, "MOTORES GRANDES", 64, NAVY, WHT)
    pump(d, 300, 460, 110); ac_unit(d, W - 280, 440, 300, t)
    lf(d, W / 2, 800, 170)
    if u > dur * 0.3: pill(d, W / 2, 1050, "Baja frecuencia ✓", 60, NAVY, BAJ)
    return fr

def cta(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 330, "¿Cuál tienes tú?", 100, WHT)
    pop(fr, u, 0.3, 300, 640, lambda dd: pill(dd, 300, 600, "BAJA", 84, NAVY, BAJ))
    pop(fr, u, 0.5, W - 300, 640, lambda dd: pill(dd, W - 300, 600, "ALTA", 84, NAVY, ALT))
    stamp(fr, u, "COMENTA", YEL, W / 2, 900, 110, 0.8, ang=5); return fr

print(run("s6_inversor", D, SP, SH, [hole, quedate, baja, alta, r1, r1b, r2, r3, r4, res, casa, motores, cta], (0,)))
