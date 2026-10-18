from engine3 import *
D = json.load(open("/home/claude/w2/voices6.json"))["internet"]
SP = ["Este sistema circula por internet: inversor de tres kilowatts, seis paneles y dos baterías de doce volts.",
      "Dice que mueve aire, nevera y lavadora. ¿Funciona?", "¡Mito!",
      "Esas dos baterías de gel dan casi cinco kilowatts hora, pero solo puedes usar la mitad sin dañarlas.",
      "Con eso, el aire te dura dos o tres horas, y ya.",
      "Y un inversor de tres kilowatts se dispara si arrancan el aire y la nevera a la vez.",
      "Para lo que promete, necesitas cinco kilowatts, y diez de litio.",
      "¿Has visto otro sistema así de milagroso? Mándamelo en los comentarios."]
SH = ["Circula por internet: inversor 3 kW, 6 paneles y 2 baterías de 12 V.",
      "Dice que mueve aire, nevera y lavadora. ¿Funciona?", "¡MITO!",
      "2 baterías de gel ≈ 4,8 kWh, pero solo usas la mitad.",
      "Con eso, el aire dura 2 o 3 horas, y ya.",
      "Un inversor de 3 kW se dispara si arrancan aire y nevera juntos.",
      "Para lo que promete: 5 kW y 10 kWh de litio.",
      "¿Viste otro sistema milagroso? Mándamelo en comentarios."]
def hole(u, dur, t): return bg_mito(t)
def promete(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    inverter(d, W / 2, 380, 130); text_c(d, W / 2, 530, "3 kW", 70, YEL)
    for i, at in enumerate([0.1, 0.3, 0.5]):
        if u < dur * at: continue
        cx = 230 + i * 310
        if i == 0: ac_unit(d, cx, 800, 240, t)
        elif i == 1: fridge(d, cx, 820, 110)
        else:
            d.rounded_rectangle([cx - 90, 720, cx + 90, 920], radius=14, fill=(230, 235, 245)); d.ellipse([cx - 60, 770, cx + 60, 890], fill=(60, 120, 200))
        d.line([(W / 2, 600), (cx, 690)], fill=YEL, width=6)
    if u > dur * 0.7: text_c(d, W / 2, 1050, "¿Funciona?", 110, WHT)
    return fr
def mito(u, dur, t):
    fr = bg_mito(t); stamp(fr, u, "MITO", RED, W / 2, 620, 220, 0.05); return fr
def bat(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr)
    for i in range(2): battery_icon(d, 360 + i * 360, 620, 220, 380, 0.5 if u > dur * 0.5 else 1.0, col=YEL if u > dur * 0.5 else GRN)
    text_c(d, W / 2, 900, "≈ 4,8 kWh", 100, WHT)
    if u > dur * 0.5: text_c(d, W / 2, 1030, "usables: la mitad", 76, RED)
    return fr
def horas(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); ac_unit(d, W / 2, 380, 480, t)
    clock(d, W / 2, 800, 170, 23 + int(ease(u / (dur * 0.7)) * 2.5), 0)
    if u > dur * 0.5: stamp(fr, u, "2-3 HORAS", RED, W / 2, 1100, 100, dur * 0.5, ang=-5)
    return fr
def dispara(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); sh = 10 * math.sin(t * 40) if u > dur * 0.4 else 0
    inverter(d, W / 2 + sh, 600, 200)
    if u > dur * 0.4:
        for k in range(3): bolt(d, 260 + k * 280, 330 + 30 * (k % 2), 80, YEL)
        stamp(fr, u, "¡SE DISPARA!", RED, W / 2, 1040, 100, dur * 0.4, ang=6)
    return fr
def necesita(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 260, "Lo que de verdad necesitas", 64, WHT)
    pop(fr, u, 0.2, W / 2, 520, lambda dd: pill(dd, W / 2, 480, "Inversor 5 kW", 84, NAVY, CYAN))
    pop(fr, u, dur * 0.4, W / 2, 720, lambda dd: pill(dd, W / 2, 680, "10 kWh de litio", 84, NAVY, GRN))
    return fr
def cta(u, dur, t):
    fr = bg_mito(t); d = ImageDraw.Draw(fr); text_c(d, W / 2, 330, "¿Viste otro sistema", 92, WHT); text_c(d, W / 2, 450, "milagroso?", 100, YEL)
    stamp(fr, u, "MÁNDAMELO", GRN, W / 2, 820, 110, 0.4, ang=6); return fr
print(run("s6_internet", D, SP, SH, [hole, promete, mito, bat, horas, dispara, necesita, cta], (0,)))
