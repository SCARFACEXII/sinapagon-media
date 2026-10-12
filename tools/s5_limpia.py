from engine3 import *
D = json.load(open("/home/claude/w2/voices5.json"))["limpia"]
SP = ["Panel sucio, panel que produce menos: hasta un veinte por ciento menos.", "Así se limpian sin dañarlos.",
      "Uno: la hora. Temprano en la mañana, o al atardecer. Nunca a mediodía: el agua fría sobre el vidrio caliente lo puede rajar.",
      "Dos: solo agua y una esponja o un paño suave. Nada de cepillos duros, ni detergente fuerte, ni hidrolavadora.",
      "Tres: nunca te pares encima del panel. Las celdas se parten por dentro, aunque no se vea.",
      "¿Cada cuánto? Cada mes, o cuando veas polvo, hojas o excremento de pájaros.",
      "¿Cuándo fue la última vez que limpiaste los tuyos? Cuéntamelo en los comentarios."]
SH = ["Panel sucio = hasta 20% menos de producción.", "Así se limpian sin dañarlos.",
      "1: temprano o al atardecer. Nunca a mediodía: el agua fría raja el vidrio caliente.",
      "2: solo agua y esponja o paño suave. Nada de cepillo duro, detergente fuerte ni hidrolavadora.",
      "3: nunca te pares encima: las celdas se parten por dentro.",
      "¿Cada cuánto? Cada mes, o cuando veas polvo, hojas o excremento de pájaros.",
      "¿Cuándo limpiaste los tuyos? Cuéntamelo en comentarios."]
def hole(u, dur, t): return bg_obra(t)
def head(fr, n, title):
    d = ImageDraw.Draw(fr); pill(d, W / 2, 210, f"PASO {n}", 76, NAVY, YEL); text_c(d, W / 2, 330, title, 76, WHT)
def sin(u, dur, t):
    fr = bg_obra(t); d = ImageDraw.Draw(fr); panel(d, W / 2, 560, 420, 560)
    for k in range(18): x = W / 2 - 180 + (k * 53) % 360; y = 330 + (k * 97) % 480; d.ellipse([x, y, x + 22, y + 16], fill=(150, 120, 80))
    stamp(fr, u, "SIN DAÑARLOS", GRN, W / 2, 1020, 110, 0.1, ang=-6); return fr
def hora_(u, dur, t):
    fr = bg_obra(t); head(fr, 1, "La hora"); d = ImageDraw.Draw(fr)
    clock(d, 270, 640, 130, 7, 0); text_c(d, 270, 800, "7 am ✓", 60, GRN)
    clock(d, W - 270, 640, 130, 18, 0); text_c(d, W - 270, 800, "6 pm ✓", 60, GRN)
    if u > dur * 0.45:
        clock(d, W / 2, 1000, 110, 12, 0); xmark(d, W / 2, 1000, 120); text_c(d, W / 2 + 230, 970, "12", 70, RED)
    return fr
def como(u, dur, t):
    fr = bg_obra(t); head(fr, 2, "Con qué"); d = ImageDraw.Draw(fr)
    for i, (txt, ok, at) in enumerate([("Agua", 1, 0.05), ("Esponja / paño suave", 1, 0.15), ("Cepillo duro", 0, 0.45), ("Detergente fuerte", 0, 0.6), ("Hidrolavadora", 0, 0.75)]):
        if u > dur * at: pop(fr, u, dur * at, W / 2, 560 + i * 130, lambda dd, y=530 + i * 130, s=txt, o=ok: pill(dd, W / 2, y, ("✓  " if o else "NO · ") + s, 58, NAVY if o else WHT, GRN if o else RED))
    return fr
def pisar(u, dur, t):
    fr = bg_obra(t); head(fr, 3, "Nunca lo pises"); d = ImageDraw.Draw(fr)
    panel(d, W / 2, 700, 420, 560)
    if u > dur * 0.3:
        for p in [[(400, 520), (470, 640), (430, 720), (520, 860)], [(640, 560), (580, 700), (660, 800)]]: d.line(p, fill=RED, width=8)
    if u > dur * 0.5: stamp(fr, u, "SE PARTEN", RED, W / 2, 1100, 100, dur * 0.5, ang=6)
    return fr
f404 = foot("404", 0.0, zoom=(1.0, 1.12), dim=60)
def cada(u, dur, t):
    fr = f404(u, dur); stamp(fr, u, "CADA MES", YEL, W / 2, 520, 120, 0.1, ang=-6)
    pop(fr, u, 0.6, W / 2, 790, lambda dd: pill(dd, W / 2, 760, "o si ves polvo, hojas o pájaros", 54, NAVY, GRN))
    return fr
def cta(u, dur, t):
    fr = bg_obra(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 330, "¿Cuándo limpiaste", 94, WHT); text_c(d, W / 2, 450, "los tuyos?", 94, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 800, 120, 0.4, ang=-5)
    if u > 1.2: pop(fr, u, 1.2, W / 2, 1100, lambda dd: pill(dd, W / 2, 1070, "SÍGUEME PARA MÁS", 60, NAVY, YEL))
    return fr
print(run("s5_limpia", D, SP, SH, [hole, sin, hora_, como, pisar, cada, cta], (0,)))
