from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["aire"]
SP = ["¿Aire acondicionado toda la noche con paneles? Mira lo que le pasa a tu batería.",
      "Diez de la noche: batería al cien por ciento.",
      "Prendes un split inverter de una tonelada, a veintiséis grados. Gasta unos quinientos watts de promedio.",
      "A las seis de la mañana, junto con la nevera y un ventilador, llega al cincuenta por ciento.",
      "O sea: con una batería de diez kilowatts hora, pasas la noche fresco, y te sobra la mitad.",
      "El truco son los veintiséis grados: a dieciocho, gasta casi el doble.",
      "¿A cuántos grados pones el tuyo? Dímelo en los comentarios."]
SH = ["¿Aire toda la noche con paneles? Mira tu batería.", "10 pm: batería al 100%.",
      "Split inverter de 1 tonelada a 26 °C: ≈ 500 W de promedio.",
      "6 am, con nevera y ventilador: batería al 50%.",
      "Con 10 kWh pasas la noche fresco y te sobra la mitad.",
      "El truco: 26 °C. A 18 °C gasta casi el doble.",
      "¿A cuántos grados pones el tuyo? Dímelo en comentarios."]
def hole(u, dur, t): return bg_noche(t)
def diez(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); clock(d, 300, 600, 170, 22, 0); text_c(d, 300, 800, "10:00 pm", 76, YEL)
    battery_icon(d, W - 280, 620, 220, 400, 1.0, col=GRN); text_c(d, W - 280, 570, "100%", 84, WHT, stroke=6, sfill=NAVY); return fr
def split(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); ac_unit(d, W / 2, 420, 600, t)
    d.rounded_rectangle([W / 2 - 200, 700, W / 2 + 200, 900], radius=30, fill=(240, 244, 250)); text_c(d, W / 2, 720, "26°C", 140, NAVY)
    if u > dur * 0.5: pop(fr, u, dur * 0.5, W / 2, 1090, lambda dd: pill(dd, W / 2, 1050, "≈ 500 W promedio", 70, NAVY, YEL))
    return fr
def noche(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); k = ease(clamp(u / (dur * 0.75)))
    cur = 22 + 8 * k; clock(d, 300, 560, 160, int(cur) % 24, int((cur % 1) * 60)); text_c(d, 300, 750, hora(cur), 72, YEL)
    lvl = 1 - 0.5 * k; battery_icon(d, W - 280, 600, 220, 400, lvl, col=GRN if lvl > 0.6 else YEL)
    text_c(d, W - 280, 550, f"{int(lvl * 100)}%", 84, WHT, stroke=6, sfill=NAVY)
    ac_unit(d, 200, 1000, 220, t); fridge(d, W / 2, 1010, 80); fan(d, W - 220, 990, 60, t)
    return fr
def sobra(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); sun(d, W - 200, 260, 60, t)
    battery_icon(d, W / 2, 640, 260, 460, 0.5, col=YEL); text_c(d, W / 2, 580, "50%", 110, WHT, stroke=6, sfill=NAVY)
    stamp(fr, u, "TE SOBRA LA MITAD", GRN, W / 2, 1050, 84, 0.3, ang=-5); return fr
def truco(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); pill(d, W / 2, 230, "EL TRUCO", 80, NAVY, YEL); base = 1100
    for i, (lab, v, col, at) in enumerate([("26°C", 500, GRN, 0.1), ("18°C", 950, RED, 0.45)]):
        k = ease((u - dur * at) / 0.8) if u > dur * at else 0; x = 330 + i * 420
        d.rounded_rectangle([x - 110, base - v * 0.6 * k, x + 110, base], radius=16, fill=col)
        if k: text_c(d, x, base - v * 0.6 * k - 100, f"{int(v * k)} W", 72, WHT)
        text_c(d, x, base + 20, lab, 70, WHT)
    return fr
def cta(u, dur, t):
    fr = bg_noche(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 360, "¿A cuántos grados", 96, WHT); text_c(d, W / 2, 480, "pones el tuyo?", 96, YEL)
    stamp(fr, u, "COMENTA", GRN, W / 2, 840, 120, 0.4, ang=6); return fr
print(run("s6_aire", D, SP, SH, [hole, diez, split, noche, sobra, truco, cta], (0,)))
