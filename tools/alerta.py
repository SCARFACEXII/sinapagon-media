from engine3 import *
SP = ["Volvió la corriente... y se te quemó la nevera.", "¿Por qué pasa?",
      "Cuando la corriente regresa, llega con subidas y bajadas de voltaje: picos que pueden pasar de ciento cuarenta volts.",
      "La nevera es la que más sufre: si arranca de golpe, el compresor se fuerza.",
      "La solución: un protector de voltaje con retardo. Espera unos minutos, y solo deja pasar la corriente cuando está estable.",
      "Y si tienes inversor híbrido, ponle uno también a la entrada de la red: en modo red, el inversor deja pasar la corriente directo a tu casa.",
      "Un protector cuesta mucho menos que una nevera nueva.",
      "¿Se te ha quemado algo cuando vino la corriente? Cuéntamelo en los comentarios."]
SH = ["Volvió la corriente... y se te quemó la nevera.", "¿Por qué pasa?",
      "Al regresar, la corriente llega con picos de más de 140 V.",
      "La nevera es la que más sufre: el compresor se fuerza.",
      "Solución: protector de voltaje con retardo. Espera y deja pasar solo corriente estable.",
      "¿Inversor híbrido? Ponle uno también a la entrada de la red.",
      "Un protector cuesta mucho menos que una nevera nueva.",
      "¿Se te ha quemado algo? Cuéntamelo en comentarios."]
def hole(u, dur, t): return bg_alerta(t)
def porque(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    warn(d, W / 2, 420, 170)
    stamp(fr, u, "ALERTA", RED, W / 2, 800, 190, 0.05, ang=-8)
    if u > 0.5: pop(fr, u, 0.5, W / 2, 1100, lambda dd: text_c(dd, W / 2, 1060, "¿Por qué pasa?", 96, WHT))
    return fr
def picos(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 150, "Voltaje cuando regresa", 70, WHT)
    x0, x1, y0 = 90, W - 90, 760; sc = 3.2
    d.rectangle([x0, 330, x1, 1150], outline=(255, 255, 255, 60), width=3)
    for v, col in [(110, GRN), (130, GRN), (140, RED)]:
        y = y0 - (v - 120) * sc * 3; d.line([(x0, y), (x1, y)], fill=col + (120,), width=3); d.text((x0 + 10, y - 50), f"{v} V", font=F(40), fill=col)
    k = clamp(u / (dur * 0.7)); pts = []
    for i in range(int(200 * k)):
        x = x0 + (x1 - x0) * i / 200; tt = i / 200
        v = 120 + 6 * math.sin(i * 0.9) + (28 * math.exp(-((tt - 0.22) ** 2) / 0.0008)) - (22 * math.exp(-((tt - 0.45) ** 2) / 0.0006)) + (30 * math.exp(-((tt - 0.7) ** 2) / 0.0005))
        pts.append((x, y0 - (v - 120) * sc * 3))
    if len(pts) > 1: d.line(pts, fill=YEL, width=9, joint="curve")
    if u > dur * 0.55: stamp(fr, u, "+140 V", RED, W / 2, 1300, 110, dur * 0.55, ang=6)
    return fr
def nevera(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    sh = 14 * math.sin(t * 40) if u > 0.8 else 0
    fridge(d, W / 2 + sh, 640, 300, col=(255, 200, 200) if u > 0.8 else (230, 235, 245))
    if u > 0.8:
        for k in range(3): bolt(d, W / 2 - 300 + k * 300, 270 + 40 * (k % 2), 70, YEL)
        pop(fr, u, 1.0, W / 2, 1120, lambda dd: pill(dd, W / 2, 1080, "COMPRESOR FORZADO", 66, WHT, RED))
    return fr
def solucion(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    pop(fr, u, 0.05, W / 2, 190, lambda dd: pill(dd, W / 2, 150, "LA SOLUCIÓN", 76, NAVY, GRN))
    ok = u > dur * 0.6; d = ImageDraw.Draw(fr)
    protector(d, W / 2, 640, 300, t, ok)
    if u > dur * 0.3 and not ok:
        left = max(0, 180 - int((u - dur * 0.3) / (dur * 0.3) * 180))
        text_c(d, W / 2, 1000, f"Espera {left // 60}:{left % 60:02d}", 84, YEL)
    if ok:
        check(d, W / 2, 1060, 70); text_c(d, W / 2, 1150, "Corriente estable", 70, GRN)
    return fr
def diagrama(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 140, "¿Inversor híbrido?", 84, YEL)
    nodes = [("RED", 330), ("PROTECTOR", 620), ("INVERSOR", 910), ("TU CASA", 1200)]
    for i, (lab, y) in enumerate(nodes):
        at = 0.3 + i * dur * 0.15
        if u < at: continue
        if i == 0: bolt(d, W / 2, y, 90)
        elif i == 1: protector(d, W / 2, y, 110, t, True)
        elif i == 2: inverter(d, W / 2, y, 110)
        else:
            d.polygon([(W / 2, y - 120), (W / 2 - 140, y - 20), (W / 2 + 140, y - 20)], fill=WHT); d.rectangle([W / 2 - 110, y - 20, W / 2 + 110, y + 100], fill=WHT)
        d.text((W / 2 + 170, y - 40), lab, font=F(56), fill=WHT)
        if i > 0: d.line([(W / 2, nodes[i - 1][1] + 130), (W / 2, y - 140)], fill=YEL, width=10)
    return fr
def cta(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 300, "¿Se te ha quemado", 92, WHT); text_c(d, W / 2, 420, "algo al volver", 92, WHT); text_c(d, W / 2, 540, "la corriente?", 92, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 880, 120, 0.4, ang=6)
    if u > 1.2: pop(fr, u, 1.2, W / 2, 1130, lambda dd: pill(dd, W / 2, 1100, "SÍGUEME PARA MÁS", 60, NAVY, YEL))
    return fr
print(run("alerta", 42.76244897959184, SP, SH, [hole, porque, picos, nevera, solucion, diagrama, hole, cta], (0, 6)))
