import sys, json
sys.path.insert(0, "/home/claude/w2")
from engine2 import *
from common2 import pot, shower, hotplate
TOTAL = 41.24734693877551 + 0.6
SP = ["¿Cuál gasta más? Adivina antes de que te lo diga.", "Ronda uno: un ventilador toda la noche... o la olla reina una hora.",
      "... ¡La olla! Gasta más que el ventilador en toda la noche.", "Ronda dos: la bomba de agua una hora... o la nevera todo el día.",
      "... ¡La nevera! Tres veces más.", "Y la última: cargar tu celular todo un año... o una hora de ducha eléctrica.",
      "... ¡La ducha! Una sola hora gasta más que un año entero cargando el teléfono.", "¿Cuántas acertaste? Dímelo en los comentarios... y sígueme para más."]
SH = ["¿Cuál gasta más? Adivina antes que yo.", "Ronda 1: ventilador toda la noche... o olla reina 1 hora.", "¡La olla! Más que el ventilador toda la noche.",
      "Ronda 2: bomba de agua 1 hora... o nevera todo el día.", "¡La nevera! 3 veces más.", "La última: cargar el celular 1 año... o 1 hora de ducha eléctrica.",
      "¡La ducha! 1 hora gasta más que 1 año cargando el teléfono.", "¿Cuántas acertaste? Dímelo y sígueme para más."]
T = timings(SP, TOTAL - 0.6); track = sub_track(SH, T); S = lambda i: T[i][0]
def fan(d, cx, cy, s, t):
    for k in range(3):
        a = t * 8 + k * 2.094; x = cx + math.cos(a) * s * 0.5; y = cy + math.sin(a) * s * 0.5
        d.ellipse([x - s * 0.32, y - s * 0.32, x + s * 0.32, y + s * 0.32], fill=(200, 230, 255))
    d.ellipse([cx - s * 0.15, cy - s * 0.15, cx + s * 0.15, cy + s * 0.15], fill=NAVY); d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=WHT, width=8)
    d.rectangle([cx - 10, cy + s, cx + 10, cy + s * 1.6], fill=WHT); d.rounded_rectangle([cx - s * 0.6, cy + s * 1.55, cx + s * 0.6, cy + s * 1.7], radius=8, fill=WHT)
def fridge(d, cx, cy, s):
    d.rounded_rectangle([cx - s * 0.6, cy - s, cx + s * 0.6, cy + s], radius=20, fill=(230, 235, 245), outline=WHT, width=5)
    d.line([(cx - s * 0.6, cy - s * 0.25), (cx + s * 0.6, cy - s * 0.25)], fill=(150, 160, 180), width=6); d.rectangle([cx + s * 0.38, cy - s * 0.75, cx + s * 0.46, cy - s * 0.45], fill=(150, 160, 180))
def pump(d, cx, cy, s):
    d.ellipse([cx - s * 0.7, cy - s * 0.5, cx + s * 0.3, cy + s * 0.5], fill=(70, 130, 220), outline=WHT, width=5)
    d.rectangle([cx + s * 0.2, cy - s * 0.2, cx + s * 1.0, cy + s * 0.05], fill=(150, 160, 180)); d.rectangle([cx - s * 0.35, cy - s * 0.9, cx - s * 0.05, cy - s * 0.45], fill=(150, 160, 180))
    for k in range(3): d.ellipse([cx + s * 1.05, cy - s * 0.1 + k * 30, cx + s * 1.2, cy + s * 0.05 + k * 30], fill=CYAN)
def phone(d, cx, cy, s, t):
    d.rounded_rectangle([cx - s * 0.45, cy - s * 0.85, cx + s * 0.45, cy + s * 0.85], radius=24, fill=(30, 32, 40), outline=WHT, width=6)
    lvl = (t * 0.4) % 1; d.rounded_rectangle([cx - s * 0.2, cy - s * 0.35, cx + s * 0.2, cy + s * 0.35], radius=6, outline=GRN, width=5)
    d.rectangle([cx - s * 0.15, cy + s * 0.3 - s * 0.6 * lvl, cx + s * 0.15, cy + s * 0.3], fill=GRN)
def title(u, dur, t):
    fr = bg_quiz(t); d = ImageDraw.Draw(fr)
    stamp(fr, u, "¿CUÁL GASTA MÁS?", YEL, W / 2, 520, 92, 0.05, ang=-6)
    L = new_layer(); dd = ImageDraw.Draw(L); text_c(dd, W / 2, 820, "Adivina antes que yo", 72, WHT); layer_pop(fr, L, u, W / 2, 860, 0.6)
    return fr
def vs(rnd, lname, lsub, licon, rname, rsub, ricon):
    def fn(u, dur, t):
        fr = bg_quiz(t); d = ImageDraw.Draw(fr)
        pill(d, W / 2, 130, rnd, 64, NAVY, YEL)
        for side, (nm, sb, ic) in enumerate([(lname, lsub, licon), (rname, rsub, ricon)]):
            L = new_layer(); dd = ImageDraw.Draw(L); cx = 280 + side * 520
            dd.rounded_rectangle([cx - 230, 300, cx + 230, 1000], radius=40, fill=(0, 0, 0, 90), outline=WHT, width=4)
            ic(dd, cx, 540, t); text_c(dd, cx, 760, nm, 60, WHT); text_c(dd, cx, 850, sb, 46, YEL)
            layer_pop(fr, L, u, cx, 650, 0.1 + side * dur * 0.45, 0.3)
        d = ImageDraw.Draw(fr)
        if u > dur * 0.5: text_c(d, W / 2, 580, "VS", 120, WHT, stroke=8, sfill=(80, 20, 120))
        if u > dur - 1.0:
            n = max(1, 3 - int((u - (dur - 1.0)) * 3)); text_c(d, W / 2, 1100, str(n), 160, YEL, stroke=8, sfill=(80, 20, 120))
        return fr
    return fn
def reveal(lname, lval, rname, rval, win):
    def fn(u, dur, t):
        fr = bg_quiz(t); d = ImageDraw.Draw(fr); k = ease((u - 0.2) / 1.0) if u > 0.2 else 0
        mx = max(lval, rval); base = 1150
        for side, (nm, v) in enumerate([(lname, lval), (rname, rval)]):
            cx = 300 + side * 480; h = 560 * v / mx * k; col = GRN if side == win else (120, 110, 160)
            d.rounded_rectangle([cx - 120, base - h, cx + 120, base], radius=20, fill=col)
            text_c(d, cx, base - h - 90, f"{v:.1f} kWh".replace(".", ","), 66, WHT); text_c(d, cx, base + 20, nm, 56, GRY)
        if u > 1.1: stamp(fr, u, "¡GANA!", GRN, 300 + win * 480, 300, 80, 1.1, ang=-8)
        return fr
    return fn
def hole(u, dur, t): return bg_quiz(t)
def cta(u, dur, t):
    fr = bg_quiz(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 380, "¿Cuántas", 110, WHT); text_c(d, W / 2, 510, "acertaste?", 110, YEL)
    for k in range(3):
        L = new_layer(); dd = ImageDraw.Draw(L); cx = 280 + k * 260; dd.ellipse([cx - 90, 700, cx + 90, 880], fill=(0, 0, 0, 90), outline=WHT, width=5); text_c(dd, cx, 735, f"{k+1}/3", 70, YEL)
        layer_pop(fr, L, u, cx, 790, 0.3 + k * 0.2, 0.25)
    if u > 1.2:
        L = new_layer(); dd = ImageDraw.Draw(L); pill(dd, W / 2, 1060, "DÍMELO EN COMENTARIOS", 56, NAVY, GRN); pill(dd, W / 2, 1180, "SÍGUEME PARA MÁS", 54, NAVY, YEL); layer_pop(fr, L, u, W / 2, 1120, 1.2)
    return fr
fns = [title,
       vs("RONDA 1", "Ventilador", "toda la noche", lambda d, x, y, t: fan(d, x, y - 40, 110, t), "Olla reina", "1 hora", lambda d, x, y, t: pot(d, x, y, 120)),
       reveal("Ventilador", 0.6, "Olla", 0.9, 1),
       vs("RONDA 2", "Bomba de agua", "1 hora", lambda d, x, y, t: pump(d, x - 30, y, 120), "Nevera", "todo el día", lambda d, x, y, t: fridge(d, x, y, 150)),
       reveal("Bomba", 0.4, "Nevera", 1.2, 1),
       vs("ÚLTIMA RONDA", "Cargar celular", "1 año entero", lambda d, x, y, t: phone(d, x, y, 150, t), "Ducha eléctrica", "1 hora", lambda d, x, y, t: shower(d, x, y + 30, 140, t)),
       hole, cta]
scenes = [(0 if i == 0 else S(i), S(i + 1) if i < 7 else TOTAL, fn) for i, fn in enumerate(fns)]
holes = [(scenes[6][0], scenes[6][1])]
json.dump({"total": TOTAL, "holes": holes, "show": [SH[6]]}, open("/home/claude/w2/quiz_holes.json", "w"))
render2("/home/claude/w2/quiz.mp4", TOTAL, scenes, track, holes)
