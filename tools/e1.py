from common2 import *
SP = ["Estos cinco equipos se comen tu batería más rápido que nada.", "Número cinco: la olla reina, unos novecientos watts.",
      "Número cuatro: el microondas, unos mil doscientos.", "Número tres: la hornilla eléctrica, mil quinientos watts.",
      "Número dos: el aire acondicionado... porque se queda encendido toda la noche.", "Y el número uno: la ducha eléctrica, ¡hasta cinco mil watts!",
      "El truco: usa estos equipos de día, cuando hay sol.", "¿Cuál de estos tienes tú? Dímelo en los comentarios."]
SH = ["Estos 5 equipos se comen tu batería más rápido que nada.", "#5: la olla reina, unos 900 W.", "#4: el microondas, unos 1.200 W.",
      "#3: la hornilla eléctrica, 1.500 W.", "#2: el aire acondicionado... encendido toda la noche.", "Y el #1: la ducha eléctrica, ¡hasta 5.000 W!",
      "El truco: úsalos de día, cuando hay sol.", "¿Cuál tienes tú? Dímelo en comentarios."]
f0 = foot("403", 0.0, zoom=(1.0, 1.12), dim=110)
def hook(u, dur, t):
    fr = f0(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 200, "5 EQUIPOS", 150, YEL, stroke=8, sfill=NAVY)
    text_c(d, W / 2, 380, "que se comen", 80, WHT, stroke=8, sfill=NAVY); text_c(d, W / 2, 480, "tu batería", 90, RED, stroke=8, sfill=(60, 0, 0))
    layer_pop(fr, L, u, W / 2, 360, 0.05)
    d = ImageDraw.Draw(fr); lvl = max(0.05, 0.9 - 0.85 * ease(u / dur))
    battery_icon(d, W / 2, 900, 220, 340, lvl, col=GRN if lvl > 0.5 else (YEL if lvl > 0.2 else RED))
    return fr
def rank(key, start, num, name, watts, icon, wv):
    ff = foot(key, start, zoom=(1.0, 1.1), dim=150)
    def fn(u, dur, t):
        fr = ff(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
        text_c(d, W / 2, 110, f"#{num}", 190, YEL if num > 1 else RED, stroke=8, sfill=NAVY)
        layer_pop(fr, L, u, W / 2, 210, 0)
        L = new_layer(); d = ImageDraw.Draw(L)
        d.rounded_rectangle([W / 2 - 300, 380, W / 2 + 300, 760], radius=40, fill=(10, 26, 64, 220), outline=(255, 255, 255, 60), width=3)
        icon(d, W / 2, 570, t)
        layer_pop(fr, L, u, W / 2, 570, 0.15)
        L = new_layer(); d = ImageDraw.Draw(L)
        text_c(d, W / 2, 800, name, 76, WHT, stroke=8, sfill=NAVY)
        layer_pop(fr, L, u, W / 2, 840, 0.35)
        d = ImageDraw.Draw(fr)
        if u > 0.6:
            k = ease((u - 0.6) / 0.8); bw = (W - 240) * min(1, wv / 5000) * k
            d.rounded_rectangle([120, 940, W - 120, 990], radius=25, fill=(255, 255, 255, 30))
            d.rounded_rectangle([120, 940, 120 + max(50, bw), 990], radius=25, fill=RED if wv >= 3000 else YEL)
            text_c(d, W / 2, 1020, watts, 92, YEL if wv < 3000 else RED, stroke=6, sfill=NAVY)
        return fr
    return fn
r5 = rank("402", 0.0, 5, "Olla reina", "≈ 900 W", lambda d, x, y, t: pot(d, x, y, 120), 900)
r4 = rank("399", 3.0, 4, "Microondas", "≈ 1.200 W", lambda d, x, y, t: microwave(d, x, y, 110), 1200)
r3 = rank("406", 0.0, 3, "Hornilla eléctrica", "≈ 1.500 W", lambda d, x, y, t: hotplate(d, x, y, 150, t), 1500)
def ac_ic(d, x, y, t): ac_unit(d, x, y - 30, 440, t); moon(d, x + 200, y - 130, 40)
r2 = rank("407", 0.5, 2, "Aire acondicionado", "toda la noche", ac_ic, 2600)
r1 = rank("404", 1.0, 1, "Ducha eléctrica", "hasta 5.000 W", lambda d, x, y, t: shower(d, x, y + 40, 150, t), 5000)
f6 = foot("405", 0.0, zoom=(1.0, 1.15), dim=60)
def truco(u, dur, t):
    fr = f6(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 200, "EL TRUCO", 90, NAVY, YEL); text_c(d, W / 2, 360, "Úsalos de DÍA", 100, WHT, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 280, 0.05)
    d = ImageDraw.Draw(fr); sun(d, W / 2, 620, 110, t)
    return fr
def cta(u, dur, t): return cta_frame(t, u, "¿Cuál tienes tú?", "DÍMELO EN COMENTARIOS")
build("e1", SP, SH, [hook, r5, r4, r3, r2, r1, truco, cta], "/home/claude/w2/e1.mp4")
