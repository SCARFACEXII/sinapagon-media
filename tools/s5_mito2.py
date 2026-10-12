from engine3 import *
D = json.load(open("/home/claude/w2/voices5.json"))["mito2"]
SP = ["¿Hay que descargar la batería de litio completa antes de cargarla?", "¡Mito!",
      "Eso era con las baterías viejas de níquel, que tenían efecto memoria.",
      "La de litio no tiene memoria: la puedes cargar cuando quieras, aunque esté al ochenta por ciento.",
      "Al contrario: descargarla hasta cero, seguido, le acorta la vida.",
      "Lo ideal es usarla entre el veinte y el noventa por ciento.",
      "Y no te preocupes por cargarla todos los días: el BMS la protege.",
      "¿Qué otro mito quieres que desmienta? Escríbelo en los comentarios."]
SH = ["¿Hay que descargar el litio completo antes de cargarlo?", "¡MITO!",
      "Eso era con las viejas de níquel, que tenían efecto memoria.",
      "El litio no tiene memoria: cárgalo cuando quieras, aunque esté al 80%.",
      "Al contrario: descargarla a 0% seguido le acorta la vida.",
      "Lo ideal: usarla entre 20% y 90%.",
      "Cargarla todos los días no la daña: el BMS la protege.",
      "¿Qué otro mito desmiento? Escríbelo en comentarios."]
def hole(u, dur, t): return bg_mito(t)
def mito(u, dur, t):
    fr = bg_mito(t); stamp(fr, u, "MITO", RED, W / 2, 620, 220, 0.05); return fr
def niquel(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    for k in range(3):
        cx = 260 + k * 280; d.rounded_rectangle([cx - 70, 420, cx + 70, 760], radius=24, fill=(60, 140, 90), outline=WHT, width=6)
        d.rectangle([cx - 25, 395, cx + 25, 420], fill=WHT); text_c(d, cx, 540, "Ni", 80, WHT)
    if u > dur * 0.35: stamp(fr, u, "ANTES", YEL, W / 2, 960, 110, dur * 0.35, ang=-6)
    return fr
def cuando(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    lvl = 0.8 + 0.2 * clamp((u - dur * 0.3) / (dur * 0.6))
    battery_icon(d, W / 2, 680, 280, 480, lvl, col=GRN); text_c(d, W / 2, 620, f"{int(lvl * 100)}%", 110, WHT, stroke=6, sfill=NAVY)
    bolt(d, W / 2 + 200, 470, 70)
    if u > dur * 0.5: pop(fr, u, dur * 0.5, W / 2, 1060, lambda dd: pill(dd, W / 2, 1020, "Cárgala cuando quieras ✓", 66, NAVY, GRN))
    return fr
def cero(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    lvl = 0.6 * (1 - clamp(u / (dur * 0.6)))
    battery_icon(d, W / 2, 680, 280, 480, lvl, col=RED, cracked=u > dur * 0.6); text_c(d, W / 2, 620, f"{int(lvl * 100)}%", 110, WHT, stroke=6, sfill=NAVY)
    if u > dur * 0.6: stamp(fr, u, "MENOS VIDA", RED, W / 2, 1050, 100, dur * 0.6, ang=6)
    return fr
def rango(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    x0, x1, y = 130, W - 130, 640; k = ease(u / 1.0)
    d.rounded_rectangle([x0, y, x1, y + 90], radius=45, fill=(255, 255, 255, 40))
    a = x0 + (x1 - x0) * 0.2; b = x0 + (x1 - x0) * (0.2 + 0.7 * k)
    d.rounded_rectangle([a, y, b, y + 90], radius=45, fill=GRN)
    for p, lab in [(0.2, "20%"), (0.9, "90%")]:
        xx = x0 + (x1 - x0) * p; d.text((xx - 40, y + 110), lab, font=F(48), fill=YEL if p in (0.2, 0.9) else GRY)
    text_c(d, W / 2, 420, "Zona ideal", 100, GRN)
    return fr
def bms(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    battery_icon(d, W / 2, 660, 280, 480, 0.9, col=GRN)
    d.rounded_rectangle([W / 2 - 110, 560, W / 2 + 110, 680], radius=18, fill=(10, 30, 60), outline=CYAN, width=6); text_c(d, W / 2, 570, "BMS", 72, CYAN)
    if u > dur * 0.4: stamp(fr, u, "PROTEGIDA", GRN, W / 2, 1060, 100, dur * 0.4, ang=-5)
    return fr
def cta(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 330, "¿Qué otro", 100, WHT); text_c(d, W / 2, 450, "MITO desmiento?", 100, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 800, 120, 0.4, ang=8)
    if u > 1.2: pop(fr, u, 1.2, W / 2, 1130, lambda dd: pill(dd, W / 2, 1100, "SÍGUEME PARA MÁS", 60, NAVY, YEL))
    return fr
print(run("s5_mito2", D, SP, SH, [hole, mito, niquel, cuando, cero, rango, bms, cta], (0,)))
