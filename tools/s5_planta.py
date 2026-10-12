from engine3 import *
D = json.load(open("/home/claude/w2/voices5.json"))["planta"]
SP = ["Planta de gasolina contra paneles solares. Cinco rounds.",
      "Round uno: el precio de compra. La planta es mucho más barata. Punto para la planta.",
      "Round dos: lo que gastas cada día. Cinco horas de planta son unos cinco litros de gasolina diarios: ciento cincuenta litros al mes. El sol es gratis. Punto para los paneles.",
      "Round tres: el ruido y el humo. La planta no te deja dormir. Los paneles no hacen ruido. Otro punto para los paneles.",
      "Round cuatro: el mantenimiento. La planta pide aceite y bujías a cada rato. Los paneles, casi nada. Van tres a uno para los paneles.",
      "Round cinco: corriente a cualquier hora. Si tienes gasolina, la planta te da corriente de noche sin límite de batería. Punto para la planta.",
      "Resultado: tres a dos. Ganan los paneles, y con la gasolina que ahorras, se pagan solos.",
      "¿Tú qué usas? Dímelo en los comentarios."]
SH = ["Planta de gasolina vs paneles solares. 5 rounds.",
      "Round 1: precio de compra. La planta es mucho más barata. Punto planta.",
      "Round 2: gasto diario. 5 h de planta ≈ 5 litros al día: 150 litros al mes. El sol es gratis.",
      "Round 3: ruido y humo. La planta no te deja dormir. Los paneles no hacen ruido.",
      "Round 4: mantenimiento. La planta pide aceite y bujías. Los paneles, casi nada. 3 a 1.",
      "Round 5: corriente a cualquier hora. Con gasolina, la planta no tiene límite de batería.",
      "Resultado: 3 a 2. Ganan los paneles, y se pagan solos con la gasolina que ahorras.",
      "¿Tú qué usas? Dímelo en comentarios."]
PLC = ORG; PNC = GRN
def board(fr, a, b, rnd=None):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([80, 60, W - 80, 210], radius=30, fill=(0, 0, 0, 200), outline=(255, 255, 255, 80), width=3)
    text_c(d, 260, 90, "PLANTA", 56, PLC); text_c(d, W - 260, 90, "PANELES", 56, PNC); text_c(d, W / 2, 72, f"{a} - {b}", 88, YEL)
    if rnd: pill(d, W / 2, 250, rnd, 50, NAVY, YEL)
def gen(d, cx, cy, s, t):
    sh = 4 * math.sin(t * 40)
    d.rounded_rectangle([cx - s + sh, cy - s * 0.6, cx + s + sh, cy + s * 0.6], radius=20, fill=(220, 110, 30), outline=WHT, width=6)
    d.rounded_rectangle([cx - s * 0.7 + sh, cy - s * 0.35, cx + s * 0.2 + sh, cy + s * 0.35], radius=14, fill=(40, 40, 46))
    d.ellipse([cx + s * 0.35 + sh, cy - s * 0.25, cx + s * 0.75 + sh, cy + s * 0.15], fill=(40, 40, 46))
    for k in range(3):
        x = cx + s + 30 + ((t * 80 + k * 40) % 120); y = cy - s * 0.5 - k * 30; d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=(140, 140, 150, 160))
def hole(u, dur, t): return bg_ring(t)
def r1(u, dur, t):
    fr = bg_ring(t); board(fr, 1 if u > dur * 0.8 else 0, 0, "ROUND 1 · PRECIO DE COMPRA"); d = ImageDraw.Draw(fr)
    gen(d, 280, 620, 150, t); panel(d, W - 280, 620, 220, 300)
    if u > dur * 0.3: text_c(d, 280, 800, "$", 120, PLC); text_c(d, W - 280, 800, "$$$", 120, PNC)
    if u > dur * 0.8: stamp(fr, u, "PUNTO", PLC, 280, 450, 80, dur * 0.8, ang=-8)
    return fr
def r2(u, dur, t):
    fr = bg_ring(t); board(fr, 1, 1 if u > dur * 0.88 else 0, "ROUND 2 · GASTO DIARIO"); d = ImageDraw.Draw(fr)
    n = int(clamp((u - dur * 0.1) / (dur * 0.35)) * 5) if u > dur * 0.1 else 0
    for i in range(n):
        x = 120 + i * 90; d.rounded_rectangle([x, 520, x + 70, 640], radius=10, fill=RED, outline=WHT, width=3); d.rectangle([x + 20, 505, x + 50, 520], fill=WHT)
    if n: text_c(d, 330, 680, f"{n} L/día", 66, RED)
    if u > dur * 0.45: text_c(d, 330, 790, "= 150 L/mes", 72, YEL)
    if u > dur * 0.65: sun(d, W - 250, 620, 90, t); text_c(d, W - 250, 790, "GRATIS", 80, GRN)
    return fr
def r3(u, dur, t):
    fr = bg_ring(t); board(fr, 1, 2 if u > dur * 0.85 else 1, "ROUND 3 · RUIDO Y HUMO"); d = ImageDraw.Draw(fr)
    gen(d, 280, 640, 140, t)
    for k in range(3):
        r = 80 + ((t * 120 + k * 50) % 150); d.arc([280 - r - 140, 640 - r, 280 + r + 140, 640 + r], 300, 60, fill=(255, 255, 255, 120), width=6)
    panel(d, W - 260, 640, 220, 300); text_c(d, W - 260, 820, "Silencio", 60, GRN)
    return fr
def r4(u, dur, t):
    fr = bg_ring(t); board(fr, 1, 3 if u > dur * 0.6 else 2, "ROUND 4 · MANTENIMIENTO"); d = ImageDraw.Draw(fr)
    d.ellipse([200, 560, 330, 720], fill=(200, 160, 40)); d.polygon([(265, 470), (200, 610), (330, 610)], fill=(200, 160, 40)); text_c(d, 240, 760, "Aceite", 54, PLC)
    d.rounded_rectangle([450, 520, 500, 700], radius=10, fill=(200, 200, 210)); d.rectangle([460, 480, 490, 520], fill=(120, 120, 130)); text_c(d, 475, 760, "Bujías", 54, PLC)
    panel(d, W - 260, 620, 220, 300); text_c(d, W - 260, 800, "Casi nada", 58, GRN)
    if u > dur * 0.65: stamp(fr, u, "1 - 3", YEL, W / 2, 1050, 110, dur * 0.65, ang=-5)
    return fr
def r5(u, dur, t):
    fr = bg_ring(t); board(fr, 2 if u > dur * 0.85 else 1, 3, "ROUND 5 · DE NOCHE"); d = ImageDraw.Draw(fr)
    moon(d, W / 2, 420, 90); gen(d, 300, 760, 140, t); text_c(d, 300, 900, "Sin límite", 58, PLC)
    battery_icon(d, W - 280, 760, 140, 230, 0.35, col=PNC); text_c(d, W - 280, 900, "Lo que dé", 58, PNC); text_c(d, W - 280, 960, "la batería", 58, PNC)
    if u > dur * 0.85: stamp(fr, u, "PUNTO", PLC, 300, 580, 80, dur * 0.85, ang=-8)
    return fr
def res(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 230, "RESULTADO", 80, WHT); text_c(d, W / 2, 340, "2 - 3", 200, YEL, stroke=6, sfill=NAVY)
    for i in range(3): panel(d, 300 + i * 240, 800, 200, 280)
    stamp(fr, u, "¡GANAN PANELES!", PNC, W / 2, 1120, 96, 0.4, ang=-6)
    return fr
def cta(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 330, "¿Tú qué usas?", 110, WHT)
    pop(fr, u, 0.3, 300, 640, lambda dd: pill(dd, 300, 600, "PLANTA", 76, WHT, (200, 100, 20)))
    pop(fr, u, 0.5, W - 300, 640, lambda dd: pill(dd, W - 300, 600, "PANELES", 76, NAVY, PNC))
    stamp(fr, u, "COMENTA", YEL, W / 2, 900, 110, 0.8, ang=5)
    return fr
print(run("s5_planta", D, SP, SH, [hole, r1, r2, r3, r4, r5, res, cta], (0,)))
