from engine3 import *
SP = ["Tres errores de instalación solar que te salen caros.",
      "Error uno: cables finos. Entre la batería y el inversor pasa mucha corriente: si el cable es fino, se calienta y se derrite. Usa el calibre que pide el manual.",
      "Error dos: sin protección. Cada parte necesita su breaker o su fusible: los paneles, la batería y la salida a la casa.",
      "Error tres: paneles en la sombra. Una sola sombra, de un árbol o de un tanque, baja la producción de toda la fila.",
      "Y un bonus: no pongas el inversor al sol ni encerrado. Necesita aire para enfriarse.",
      "Una instalación bien hecha dura años.", "Una mal hecha, te cuesta el equipo.",
      "¿Tienes dudas con tu instalación? Pregúntame en los comentarios."]
SH = ["3 errores de instalación solar que te salen caros.",
      "Error 1: cables finos. Batería a inversor: mucha corriente. Cable fino = se calienta y se derrite. Usa el calibre del manual.",
      "Error 2: sin protección. Breaker o fusible en paneles, batería y salida a la casa.",
      "Error 3: sombra. Una sola sombra baja la producción de toda la fila.",
      "Bonus: el inversor ni al sol ni encerrado. Necesita aire.",
      "Una instalación bien hecha dura años.", "Una mal hecha, te cuesta el equipo.",
      "¿Dudas con tu instalación? Pregúntame en comentarios."]
def hole(u, dur, t): return bg_obra(t)
def head(fr, n, title, col=RED):
    d = ImageDraw.Draw(fr); pill(d, W / 2, 210, f"ERROR #{n}" if n else "BONUS", 76, WHT if n else NAVY, col)
    text_c(d, W / 2, 330, title, 76, WHT)
def cables(u, dur, t):
    fr = bg_obra(t); head(fr, 1, "Cables finos"); d = ImageDraw.Draw(fr)
    battery_icon(d, 210, 720, 200, 330, 0.8, col=GRN); inverter(d, W - 210, 720, 170)
    good = u > dur * 0.75
    if not good:
        heat = clamp((u - dur * 0.15) / (dur * 0.4)); col = (int(255), int(220 - 180 * heat), int(80 - 60 * heat))
        d.line([(320, 720), (W - 330, 720)], fill=col, width=10)
        if heat > 0.6:
            for k in range(3):
                x = 420 + k * 120; y = 680 - ((t * 120 + k * 40) % 120); d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=(150, 150, 160, 140))
            stamp(fr, u, "SE DERRITE", RED, W / 2, 1050, 90, dur * 0.4, ang=-6)
    else:
        d.line([(320, 720), (W - 330, 720)], fill=(200, 40, 40), width=46)
        check(d, W / 2, 1000, 70); text_c(d, W / 2, 1100, "Calibre del manual", 70, GRN)
    return fr
def proteccion(u, dur, t):
    fr = bg_obra(t); head(fr, 2, "Sin protección"); d = ImageDraw.Draw(fr)
    for i, lab in enumerate(["Paneles", "Batería", "Casa"]):
        at = dur * (0.35 + i * 0.15)
        if u < at: continue
        cx = 210 + i * 330; breaker(d, cx, 720, 180, on=True); text_c(d, cx, 930, lab, 60, YEL)
    return fr
def sombra(u, dur, t):
    fr = bg_obra(t); head(fr, 3, "Paneles en la sombra"); d = ImageDraw.Draw(fr)
    sh = u > dur * 0.35
    for i in range(4): panel(d, 180 + i * 240, 700, 210, 290)
    if sh:
        L = new_layer(); ld = ImageDraw.Draw(L); ld.ellipse([60, 520, 320, 900], fill=(0, 0, 0, 170)); fr.alpha_composite(L); d = ImageDraw.Draw(fr)
        d.rectangle([20, 560, 50, 900], fill=(90, 60, 30)); d.ellipse([-90, 440, 120, 620], fill=(40, 120, 50))
    k = 1 - 0.6 * ease((u - dur * 0.45) / 1.0) if u > dur * 0.45 else 1
    d.rounded_rectangle([140, 1000, 140 + 800 * k, 1080], radius=20, fill=GRN if k > 0.9 else RED)
    text_c(d, W / 2, 1100, f"Producción: {int(100 * k)}%", 66, WHT)
    return fr
def bonus(u, dur, t):
    fr = bg_obra(t); head(fr, 0, "Dónde va el inversor", YEL); d = ImageDraw.Draw(fr)
    inverter(d, 230, 620, 110); sun(d, 230, 450, 40, t); xmark(d, 230, 620, 90)
    if u > dur * 0.25:
        d.rectangle([W / 2 - 120, 500, W / 2 + 120, 760], outline=(160, 120, 70), width=14); inverter(d, W / 2, 630, 80); xmark(d, W / 2, 630, 90)
    if u > dur * 0.55:
        inverter(d, W - 230, 620, 110)
        for k in range(3):
            x = W - 230 + 150 + ((t * 120 + k * 50) % 120); d.line([(x, 560 + k * 50), (x + 40, 560 + k * 50)], fill=CYAN, width=8)
        check(d, W - 230, 860, 60)
    if u > dur * 0.55: text_c(d, W / 2, 1000, "Sombra + aire", 90, GRN)
    return fr
f404 = foot("404", 0.0, zoom=(1.0, 1.1), dim=60)
def bien(u, dur, t):
    fr = f404(u, dur); stamp(fr, u, "BIEN HECHA", GRN, W / 2, 520, 120, 0.1, ang=-6)
    pop(fr, u, 0.5, W / 2, 790, lambda dd: pill(dd, W / 2, 760, "DURA AÑOS", 70, NAVY, YEL))
    return fr
def mal(u, dur, t):
    fr = bg_obra(t); d = ImageDraw.Draw(fr)
    sh = 10 * math.sin(t * 50)
    battery_icon(d, 300 + sh, 720, 220, 380, 0.2, col=RED, cracked=True); inverter(d, W - 300 - sh, 720, 150)
    for k in range(4):
        x = W - 300 + (k - 1.5) * 60; y = 500 - ((t * 140 + k * 50) % 200); d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(130, 130, 140, 150))
    stamp(fr, u, "MAL HECHA", RED, W / 2, 1080, 110, 0.1, ang=6)
    return fr
def cta(u, dur, t):
    fr = bg_obra(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 360, "¿Dudas con tu", 100, WHT); text_c(d, W / 2, 480, "instalación?", 100, YEL)
    stamp(fr, u, "PREGÚNTAME", GRN, W / 2, 820, 110, 0.4, ang=-5)
    if u > 1.2: pop(fr, u, 1.2, W / 2, 1110, lambda dd: pill(dd, W / 2, 1080, "SÍGUEME PARA MÁS", 60, NAVY, YEL))
    return fr
print(run("obra", 47.56897959183674, SP, SH, [hole, cables, proteccion, sombra, bonus, bien, mal, cta], (0,)))
