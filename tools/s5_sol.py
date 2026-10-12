from engine3 import *
D = json.load(open("/home/claude/w2/voices5.json"))["sol"]
SP = ["Tu batería amanece al veinte por ciento.", "¿Cuántas horas de sol necesita para llenarse?",
      "Con cuatro paneles de quinientos cincuenta, y sin gastar nada, se llena hacia las cuatro de la tarde.",
      "Pero de día también gastas: nevera, ventiladores, televisor.",
      "Así llega a la noche apenas al setenta por ciento.",
      "Con seis paneles, aunque uses la casa, se llena hacia las tres.",
      "Por eso, si tu batería no se llena, casi siempre faltan paneles, no batería.",
      "¿A qué porcentaje llega la tuya al atardecer? Escríbelo en los comentarios."]
SH = ["Tu batería amanece al 20%.", "¿Cuántas horas de sol necesita para llenarse?",
      "4 paneles de 550 W, sin gastar nada: llena hacia las 4 pm.",
      "Pero de día también gastas: nevera, ventiladores, TV.",
      "Así llega a la noche apenas al 70%.",
      "Con 6 paneles, aunque uses la casa, se llena hacia las 3 pm.",
      "Si tu batería no se llena, casi siempre faltan paneles, no batería.",
      "¿A qué % llega la tuya al atardecer? Escríbelo en comentarios."]
def bg_dia(t):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    for y in range(0, H, 8):
        k = y / H; d.rectangle([0, y, W, y + 8], fill=(int(30 + 60 * k), int(110 + 60 * k), int(200 - 40 * k), 255))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for r in range(500, 0, -50): gd.ellipse([W - 260 - r, 160 - r, W - 260 + r, 160 + r], fill=(255, 220, 120, int(14 * (1 - r / 500) + 4)))
    im.alpha_composite(g); d = ImageDraw.Draw(im)
    for cx, cy, s in [(180 + (t * 15) % 300, 300, 70), (700 - (t * 10) % 300, 220, 55)]:
        for dx, dy, r in [(-0.5, 0.1, 0.45), (0, -0.15, 0.6), (0.55, 0.1, 0.45)]: d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s], fill=(255, 255, 255, 200))
    d.rectangle([0, 1330, W, H], fill=(10, 30, 70, 255))
    return im
def tl(fr, u, dur, end_h, pct0, pct1, col, label, npan):
    d = ImageDraw.Draw(fr); x0, x1, y = 110, W - 110, 1180; h0, h1 = 7, 18
    k = ease(clamp(u / (dur * 0.7))); cur = h0 + (end_h - h0) * k; pct = pct0 + (pct1 - pct0) * k
    d.rounded_rectangle([x0, y, x1, y + 46], radius=23, fill=(255, 255, 255, 60))
    d.rounded_rectangle([x0, y, x0 + (x1 - x0) * (cur - h0) / (h1 - h0), y + 46], radius=23, fill=col)
    for hh, lab in [(7, "7 am"), (12, "12"), (15, "3 pm"), (18, "6 pm")]:
        xx = x0 + (x1 - x0) * (hh - h0) / (h1 - h0); d.text((xx - 38, y + 60), lab, font=F(36), fill=WHT)
    clock(d, 300, 560, 150, int(cur) % 24, int((cur % 1) * 60)); text_c(d, 300, 740, hora(cur), 76, YEL, stroke=5, sfill=NAVY)
    battery_icon(d, W - 280, 600, 200, 360, pct / 100, col=col); text_c(d, W - 280, 560, f"{int(pct)}%", 80, WHT, stroke=6, sfill=NAVY)
    for i in range(npan): panel(d, 140 + i * 120 if npan > 4 else 200 + i * 140, 950, 100 if npan > 4 else 120, 140)
    d.text((x0, y - 66), label, font=F(46), fill=WHT)
def hole(u, dur, t): return bg_dia(t)
def pregunta(u, dur, t):
    fr = bg_dia(t); d = ImageDraw.Draw(fr); battery_icon(d, W / 2, 620, 240, 420, 0.2, col=RED); text_c(d, W / 2, 570, "20%", 100, WHT, stroke=6, sfill=NAVY)
    stamp(fr, u, "¿CUÁNTAS HORAS?", YEL, W / 2, 1000, 100, 0.2, ang=-6); return fr
def cuatro(u, dur, t):
    fr = bg_dia(t); tl(fr, u, dur, 16, 20, 100, GRN, "4 paneles · sin gastar", 4); return fr
def gastos(u, dur, t):
    fr = bg_dia(t); d = ImageDraw.Draw(fr)
    if u > 0.1: fridge(d, 240, 640, 160)
    if u > dur * 0.3: fan(d, W / 2, 600, 110, t)
    if u > dur * 0.55: tv(d, W - 220, 640, 140)
    return fr
def setenta(u, dur, t):
    fr = bg_dia(t); tl(fr, u, dur, 18, 20, 70, RED, "4 paneles · usando la casa", 4); return fr
def seis(u, dur, t):
    fr = bg_dia(t); tl(fr, u, dur, 15, 20, 100, GRN, "6 paneles · usando la casa", 6); return fr
def faltan(u, dur, t):
    fr = bg_dia(t); d = ImageDraw.Draw(fr)
    for i in range(3): panel(d, 300 + i * 240, 640, 200, 280)
    d.text((W / 2 + 340, 560), "+", font=F(160), fill=YEL)
    stamp(fr, u, "FALTAN PANELES", RED, W / 2, 1000, 96, 0.3, ang=-5); return fr
def cta(u, dur, t):
    fr = bg_dia(t); d = ImageDraw.Draw(fr)
    text_c(d, W / 2, 380, "¿A qué % llega", 96, WHT, stroke=6, sfill=NAVY); text_c(d, W / 2, 500, "al atardecer?", 96, YEL, stroke=6, sfill=NAVY)
    stamp(fr, u, "COMENTA", GRN, W / 2, 860, 120, 0.4, ang=6)
    return fr
print(run("s5_sol", D, SP, SH, [hole, pregunta, cuatro, gastos, setenta, seis, faltan, cta], (0,)))
