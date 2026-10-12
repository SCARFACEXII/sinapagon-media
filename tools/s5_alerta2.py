from engine3 import *
D = json.load(open("/home/claude/w2/voices5.json"))["alerta2"]
SP = ["Si tu batería de litio hace esto... ¡ojo!", "Cuatro señales de que se está dañando.",
      "Uno: se descarga mucho más rápido que antes, aunque gastes lo mismo.",
      "Dos: se calienta al cargar o al descargar. Una batería sana se mantiene tibia.",
      "Tres: se apaga de golpe con equipos que antes aguantaba. Es el BMS cortando para protegerla.",
      "Cuatro: está hinchada, o huele raro. Esa, desconéctala ya, y no la cargues más.",
      "Casi siempre la causa es la misma: descargas a cero seguidas, calor, o el inversor mal configurado.",
      "¿Tu batería tiene alguna de estas señales? Cuéntamelo en los comentarios."]
SH = ["Si tu batería de litio hace esto... ¡ojo!", "4 señales de que se está dañando.",
      "1: se descarga mucho más rápido, aunque gastes lo mismo.",
      "2: se calienta al cargar o descargar. Una sana se mantiene tibia.",
      "3: se apaga de golpe con equipos que antes aguantaba: es el BMS protegiéndola.",
      "4: hinchada o huele raro. Desconéctala ya y no la cargues más.",
      "Causas: descargas a 0% seguidas, calor o inversor mal configurado.",
      "¿Tu batería tiene alguna señal? Cuéntamelo en comentarios."]
def hole(u, dur, t): return bg_alerta(t)
def head(fr, n):
    d = ImageDraw.Draw(fr); pill(d, W / 2, 170, f"SEÑAL #{n}", 76, WHT, RED)
def cuatro(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr); warn(d, W / 2, 420, 170)
    stamp(fr, u, "4 SEÑALES", RED, W / 2, 820, 150, 0.05, ang=-8); return fr
def s1(u, dur, t):
    fr = bg_alerta(t); head(fr, 1); d = ImageDraw.Draw(fr)
    k = clamp(u / (dur * 0.7))
    battery_icon(d, 300, 680, 220, 400, 1 - 0.4 * k, col=GRN); text_c(d, 300, 920, "Antes", 60, GRN)
    battery_icon(d, W - 300, 680, 220, 400, max(0.05, 1 - 0.95 * k), col=RED); text_c(d, W - 300, 920, "Ahora", 60, RED)
    return fr
def s2(u, dur, t):
    fr = bg_alerta(t); head(fr, 2); d = ImageDraw.Draw(fr)
    lvl = ease(u / (dur * 0.6)); battery_icon(d, 330, 700, 220, 400, 0.7, col=YEL)
    for k in range(3):
        x = 260 + k * 70; y = 460 - ((t * 120 + k * 30) % 80); d.arc([x - 20, y - 30, x + 20, y + 30], 200, 340, fill=RED, width=8)
    thermo(d, W - 300, 700, 440, lvl); text_c(d, W - 300, 380, f"{int(30 + 25 * lvl)}°C", 80, RED if lvl > 0.5 else WHT)
    return fr
def s3(u, dur, t):
    fr = bg_alerta(t); head(fr, 3); d = ImageDraw.Draw(fr)
    off = u > dur * 0.35
    bulb(d, 300, 640, 220, on=not off); battery_icon(d, W - 300, 680, 220, 400, 0.5, col=YEL)
    d.rounded_rectangle([W - 400, 600, W - 200, 700], radius=16, fill=(10, 30, 60), outline=CYAN, width=5); text_c(d, W - 300, 608, "BMS", 60, CYAN)
    if off: stamp(fr, u, "¡CORTE!", RED, W / 2, 1020, 100, dur * 0.35, ang=-6)
    return fr
def s4(u, dur, t):
    fr = bg_alerta(t); head(fr, 4); d = ImageDraw.Draw(fr)
    b = ease(u / 1.5) * 50
    d.rounded_rectangle([W / 2 - 170, 420, W / 2 + 170, 900], radius=40, fill=(30, 50, 90), outline=WHT, width=8)
    d.ellipse([W / 2 - 170 - b, 480, W / 2 - 170 + b, 840], fill=(30, 50, 90), outline=RED, width=6); d.ellipse([W / 2 + 170 - b, 480, W / 2 + 170 + b, 840], fill=(30, 50, 90), outline=RED, width=6)
    if u > dur * 0.45: stamp(fr, u, "DESCONÉCTALA", RED, W / 2, 1090, 90, dur * 0.45, ang=-5)
    return fr
def causas(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 230, "¿Por qué pasa?", 90, YEL)
    for i, (txt, at) in enumerate([("Descargas a 0% seguidas", 0.15), ("Calor", 0.45), ("Inversor mal configurado", 0.7)]):
        if u > dur * at: pop(fr, u, dur * at, W / 2, 480 + i * 170, lambda dd, y=470 + i * 170, s=txt: pill(dd, W / 2, y, s, 62, WHT, (150, 30, 30)))
    return fr
def cta(u, dur, t):
    fr = bg_alerta(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 320, "¿Tu batería tiene", 92, WHT); text_c(d, W / 2, 440, "alguna señal?", 92, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 800, 120, 0.4, ang=6)
    if u > 1.2: pop(fr, u, 1.2, W / 2, 1100, lambda dd: pill(dd, W / 2, 1070, "SÍGUEME PARA MÁS", 60, NAVY, YEL))
    return fr
print(run("s5_alerta2", D, SP, SH, [hole, cuatro, s1, s2, s3, s4, causas, cta], (0,)))
