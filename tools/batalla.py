from engine3 import *
SP = ["Gel contra litio. Cuatro rounds... solo una gana.",
      "Round uno: la energía que puedes usar. La de gel, solo la mitad sin dañarla. La de litio, más del noventa por ciento. Punto para el litio.",
      "Round dos: vida útil. Gel, unos quinientos ciclos. Litio, más de cuatro mil. Otro punto para el litio.",
      "Round tres: velocidad de carga. Con pocas horas de sol, el litio se llena mucho más rápido. Tres a cero.",
      "Round cuatro: el precio. Aquí gana el gel: es más barato al comprarlo.",
      "Pero como el litio dura hasta ocho veces más, al final te sale más barato.",
      "Resultado: tres a uno. Gana el litio.", "¿Tú cuál tienes? Dímelo en los comentarios."]
SH = ["Gel contra litio. 4 rounds... solo una gana.",
      "Round 1: energía útil. Gel: solo la mitad. Litio: más del 90%. Punto para litio.",
      "Round 2: vida útil. Gel: unos 500 ciclos. Litio: más de 4000.",
      "Round 3: carga. Con poco sol, el litio se llena mucho más rápido. 3 a 0.",
      "Round 4: precio. Aquí gana el gel: es más barato al comprarlo.",
      "Pero el litio dura hasta 8 veces más: al final sale más barato.",
      "Resultado: 3 a 1. ¡Gana el litio!", "¿Tú cuál tienes? Dímelo en comentarios."]
GELC = (90, 150, 255); LITC = GRN
def board(fr, g, l, rnd=None):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([110, 60, W - 110, 210], radius=30, fill=(0, 0, 0, 200), outline=(255, 255, 255, 80), width=3)
    text_c(d, 300, 85, "GEL", 64, GELC); text_c(d, W - 300, 85, "LITIO", 64, LITC)
    text_c(d, W / 2, 72, f"{g} - {l}", 88, YEL)
    if rnd: pill(d, W / 2, 250, rnd, 54, NAVY, YEL)
def hole(u, dur, t): return bg_ring(t)
def r1(u, dur, t):
    fr = bg_ring(t); board(fr, 0, 1 if u > dur * 0.85 else 0, "ROUND 1 · ENERGÍA ÚTIL"); d = ImageDraw.Draw(fr)
    kg = ease((u - dur * 0.25) / 1.2) if u > dur * 0.25 else 0; kl = ease((u - dur * 0.55) / 1.2) if u > dur * 0.55 else 0
    battery_icon(d, 300, 760, 260, 470, 0.5 * kg, col=GELC); battery_icon(d, W - 300, 760, 260, 470, 0.92 * kl, col=LITC)
    if kg: text_c(d, 300, 1040, "50%", 96, GELC)
    if kl: text_c(d, W - 300, 1040, "90%+", 96, LITC)
    if u > dur * 0.85: stamp(fr, u, "PUNTO", LITC, W - 300, 500, 90, dur * 0.85, ang=-10)
    return fr
def r2(u, dur, t):
    fr = bg_ring(t); board(fr, 0, 2 if u > dur * 0.82 else 1, "ROUND 2 · VIDA ÚTIL"); d = ImageDraw.Draw(fr)
    kg = ease((u - dur * 0.2) / 1.0) if u > dur * 0.2 else 0; kl = ease((u - dur * 0.45) / 1.6) if u > dur * 0.45 else 0
    base = 1250; sc = 0.17
    d.rounded_rectangle([200, base - 500 * sc * kg, 400, base], radius=16, fill=GELC)
    d.rounded_rectangle([W - 400, base - 4000 * sc * kl, W - 200, base], radius=16, fill=LITC)
    if kg: text_c(d, 300, base - 500 * sc * kg - 100, f"{int(500 * kg)}", 80, GELC)
    if kl: text_c(d, W - 300, base - 4000 * sc * kl - 100, f"{int(4000 * kl)}+", 80, LITC)
    text_c(d, W / 2, base + 20, "ciclos de carga", 52, GRY)
    return fr
def r4(u, dur, t):
    fr = bg_ring(t); board(fr, 1 if u > dur * 0.5 else 0, 3, "ROUND 4 · PRECIO"); d = ImageDraw.Draw(fr)
    for cx, col, lab, at in [(300, GELC, "$", 0.2), (W - 300, LITC, "$$$", 0.45)]:
        if u < dur * at: continue
        d.polygon([(cx - 170, 520), (cx + 110, 520), (cx + 190, 680), (cx + 110, 840), (cx - 170, 840)], fill=col)
        d.ellipse([cx + 90, 660, cx + 130, 700], fill=(10, 10, 16)); text_c(d, cx - 30, 600, lab, 120, NAVY)
    if u > dur * 0.5: stamp(fr, u, "GANA GEL", GELC, 300, 1050, 80, dur * 0.5, ang=-8)
    return fr
def r5(u, dur, t):
    fr = bg_ring(t); board(fr, 1, 3); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 300, "Para 10 años de uso:", 66, WHT)
    n = int(clamp(u / (dur * 0.6)) * 8)
    for i in range(n):
        x = 150 + (i % 4) * 130; y = 560 + (i // 4) * 260; battery_icon(d, x, y, 100, 180, 0.6, col=GELC)
    if n: text_c(d, 345, 950, f"{n} de gel", 64, GELC)
    if u > dur * 0.3: battery_icon(d, W - 230, 690, 200, 360, 0.95, col=LITC); text_c(d, W - 230, 950, "1 de litio", 64, LITC)
    return fr
def r6(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 240, "RESULTADO", 80, WHT)
    text_c(d, W / 2, 360, "1 - 3", 200, YEL, stroke=6, sfill=NAVY)
    battery_icon(d, W / 2, 900, 240, 420, 0.95, col=LITC)
    stamp(fr, u, "¡GANA LITIO!", LITC, W / 2, 1230, 110, 0.5, ang=-6)
    return fr
def cta(u, dur, t):
    fr = bg_ring(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 330, "¿Tú cuál", 110, WHT); text_c(d, W / 2, 460, "tienes?", 110, YEL)
    pop(fr, u, 0.3, 300, 760, lambda dd: pill(dd, 300, 720, "GEL", 80, WHT, (40, 80, 200)))
    pop(fr, u, 0.5, W - 300, 760, lambda dd: pill(dd, W - 300, 720, "LITIO", 80, NAVY, LITC))
    stamp(fr, u, "COMENTA", YEL, W / 2, 1010, 110, 0.8, ang=5)
    return fr
print(run("batalla", 52.688979591836734, SP, SH, [hole, r1, r2, hole, r4, r5, r6, cta], (0, 3)))
