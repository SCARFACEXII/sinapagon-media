import sys, json
sys.path.insert(0, "/home/claude/w2")
from engine2 import *
from common2 import foot, panel as _p
TOTAL = 38.84408163265306 + 0.6
SP = ["¿Los paneles solares no funcionan cuando está nublado?", "¡Mito!",
      "Con nubes, los paneles siguen produciendo... pero menos: entre un diez y un treinta por ciento.",
      "Por eso, después de varios días nublados, la batería no se llena.",
      "Y aquí viene lo curioso: la lluvia les viene bien, porque los limpia.",
      "Lo que sí les baja el rendimiento es el calor extremo: los paneles trabajan mejor con sol... y fresco.",
      "Consejo: si en tu zona nubla mucho, ponle uno o dos paneles de más.",
      "¿Qué otro mito quieres que desmienta? Escríbelo en los comentarios... y sígueme para más."]
SH = ["¿Los paneles no funcionan cuando está nublado?", "¡MITO!", "Con nubes siguen produciendo, pero menos: entre 10 y 30%.",
      "Por eso, tras varios días nublados, la batería no se llena.", "Lo curioso: la lluvia les viene bien, porque los limpia.",
      "Lo que sí les baja el rendimiento es el calor extremo.", "Consejo: si nubla mucho en tu zona, ponle 1 o 2 paneles de más.",
      "¿Qué otro mito desmiento? Escríbelo y sígueme para más."]
T = timings(SP, TOTAL - 0.6); track = sub_track(SH, T); S = lambda i: T[i][0]
def cloud(d, cx, cy, s, col=(200, 205, 215)):
    for dx, dy, r in [(-0.5, 0.1, 0.45), (0, -0.15, 0.6), (0.55, 0.1, 0.45)]: d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s], fill=col)
    d.rounded_rectangle([cx - 0.95 * s, cy, cx + 0.95 * s, cy + 0.5 * s], radius=int(0.25 * s), fill=col)
def hole(u, dur, t): return bg_mito(t)
def mito(u, dur, t):
    fr = bg_mito(t); stamp(fr, u, "MITO", RED, W / 2, 620, 220, 0.05)
    return fr
def prod(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 170, "Lo que producen", 80, WHT)
    k = ease((u - 0.3) / 1.2) if u > 0.3 else 0; base = 1150
    sun(d, 320, 420, 90, t); cloud(d, 760, 420, 110)
    d.rounded_rectangle([220, base - 460 * k, 420, base], radius=20, fill=YEL); text_c(d, 320, base - 460 * k - 90, f"{int(100*k)}%", 76, YEL)
    v = 0.3 * k if u > dur * 0.4 else 0.1 * k
    d.rounded_rectangle([660, base - 460 * v, 860, base], radius=20, fill=CYAN); text_c(d, 760, base - 460 * v - 90, "10–30%" if u > dur * 0.4 else f"{int(100*v)}%", 70, CYAN)
    text_c(d, 320, base + 20, "Sol", 56, GRY); text_c(d, 760, base + 20, "Nublado", 56, GRY)
    return fr
def dias(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    for k, dd in enumerate(["Lun", "Mar", "Mié"]):
        cx = 230 + k * 310; cloud(d, cx, 300, 80); text_c(d, cx, 400, dd, 52, GRY)
    lvl = 0.6 + 0.04 * math.sin(t * 2)
    battery_icon(d, W / 2, 800, 220, 360, lvl, col=YEL); text_c(d, W / 2, 770, "60%", 96, WHT, stroke=6, sfill=NAVY)
    if u > dur * 0.4: text_c(d, W / 2, 1040, "No se llena", 84, RED)
    return fr
def calor(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    lvl = ease(u / 2.0); thermo(d, W / 2 - 230, 600, 420, lvl); text_c(d, W / 2 - 230, 330, f"{int(30 + 35*lvl)}°C", 72, RED if lvl > 0.5 else WHT)
    _p(d, W / 2 + 220, 560, 260, 360)
    if u > dur * 0.35: text_c(d, W / 2 + 220, 790, f"−{int(15*lvl)}%", 96, RED)
    if u > dur * 0.65:
        L = new_layer(); dd = ImageDraw.Draw(L); pill(dd, W / 2, 1050, "MEJOR: SOL + FRESCO", 64, NAVY, GRN); layer_pop(fr, L, u, W / 2, 1080, dur * 0.65)
    return fr
def cta(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 330, "¿Qué otro", 100, WHT); text_c(d, W / 2, 450, "MITO desmiento?", 100, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 800, 120, 0.4, ang=8)
    if u > 1.2:
        L = new_layer(); dd = ImageDraw.Draw(L); pill(dd, W / 2, 1100, "SÍGUEME PARA MÁS", 60, NAVY, YEL); layer_pop(fr, L, u, W / 2, 1130, 1.2)
    return fr
fns = [hole, mito, prod, dias, hole, calor, hole, cta]
scenes = [(0 if i == 0 else S(i), S(i + 1) if i < 7 else TOTAL, fn) for i, fn in enumerate(fns)]
holes = [(scenes[i][0], scenes[i][1]) for i in (0, 4, 6)]
json.dump({"total": TOTAL, "holes": holes, "show": [SH[i] for i in (0, 4, 6)]}, open("/home/claude/w2/mito_holes.json", "w"))
render2("/home/claude/w2/mito.mp4", TOTAL, scenes, track, holes)
