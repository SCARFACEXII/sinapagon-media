from common2 import *
SP = ["¿Tu batería se acaba antes de que amanezca?", "Casi siempre es por una de tres cosas.",
      "Uno: tienes equipos que gastan mucho de noche, como el aire o la olla.", "Dos: tus paneles no alcanzan para llenarla de día.",
      "Tres: la batería es muy pequeña para tus horas de apagón.", "El truco para saberlo: mira a qué porcentaje llega cuando se va el sol.",
      "Si no llega al cien por ciento, el problema son los paneles, no la batería.", "¿A ti a qué hora se te acaba? Dímelo en los comentarios."]
SH = ["¿Tu batería se acaba antes de que amanezca?", "Casi siempre es por una de 3 cosas.",
      "#1: equipos que gastan mucho de noche, como el aire o la olla.", "#2: tus paneles no alcanzan para llenarla de día.",
      "#3: la batería es pequeña para tus horas de apagón.", "El truco: mira a qué % llega cuando se va el sol.",
      "Si no llega al 100%, el problema son los paneles, no la batería.", "¿A qué hora se te acaba? Dímelo en comentarios."]
def hook(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 190, "¿Tu batería", 96, WHT); text_c(d, W / 2, 300, "NO LLEGA", 120, RED, stroke=6, sfill=(60, 0, 0)); text_c(d, W / 2, 430, "a la mañana?", 90, WHT)
    layer_pop(fr, L, u, W / 2, 330, 0.05)
    d = ImageDraw.Draw(fr); moon(d, W / 2 + 280, 700, 80)
    lvl = max(0.03, 0.8 - 0.8 * ease(u / max(1, dur - 0.3)))
    col = GRN if lvl > 0.5 else (YEL if lvl > 0.2 else RED)
    battery_icon(d, W / 2 - 60, 900, 260, 420, lvl, col=col)
    text_c(d, W / 2 - 60, 870, f"{int(lvl * 100)}%", 100, WHT, stroke=6, sfill=NAVY)
    return fr
f1 = foot("406", 0.0, dim=90)
def tres(u, dur, t):
    fr = f1(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 300, "3 CAUSAS", 110, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 360, 0.05)
    return fr
def c1(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "CAUSA #1", 70, WHT, RED); text_c(d, W / 2, 290, "Equipos grandes de noche", 70, WHT)
    layer_pop(fr, L, u, W / 2, 230, 0)
    d = ImageDraw.Draw(fr); moon(d, W / 2 + 330, 500, 70)
    L = new_layer(); d = ImageDraw.Draw(L); ac_unit(d, W / 2 - 200, 650, 420, t); text_c(d, W / 2 - 200, 820, "Aire", 60, CYAN)
    layer_pop(fr, L, u, W / 2 - 200, 700, dur * 0.4)
    L = new_layer(); d = ImageDraw.Draw(L); hotplate(d, W / 2 + 230, 690, 150, t); text_c(d, W / 2 + 230, 820, "Olla", 60, YEL)
    layer_pop(fr, L, u, W / 2 + 230, 700, dur * 0.7)
    return fr
f3 = foot("404", 0.5, zoom=(1.0, 1.15), dim=70)
def c2(u, dur, t):
    fr = f3(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "CAUSA #2", 70, WHT, RED); text_c(d, W / 2, 290, "Pocos paneles", 90, WHT, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 230, 0)
    return fr
def c3(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "CAUSA #3", 70, WHT, RED); text_c(d, W / 2, 290, "Batería muy pequeña", 80, WHT)
    layer_pop(fr, L, u, W / 2, 230, 0)
    d = ImageDraw.Draw(fr)
    battery_icon(d, W / 2 - 220, 720, 140, 220, 0.3, col=RED); moon(d, W / 2 + 200, 620, 80)
    if u > dur * 0.4:
        text_c(d, W / 2 + 200, 760, "12 h", 110, YEL); text_c(d, W / 2 + 200, 890, "de apagón", 54, GRY)
    return fr
f5 = foot("399", 12.0, zoom=(1.05, 1.2), focus=(0.5, 0.4), dim=90)
def truco(u, dur, t):
    fr = f5(u, dur); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 200, "EL TRUCO", 90, NAVY, YEL)
    text_c(d, W / 2, 360, "¿A qué % llega", 84, WHT, stroke=8, sfill=NAVY); text_c(d, W / 2, 460, "al atardecer?", 84, YEL, stroke=8, sfill=NAVY)
    layer_pop(fr, L, u, W / 2, 330, 0.05)
    return fr
def diag(u, dur, t):
    fr = bg_frame(t); d = ImageDraw.Draw(fr)
    lvl = 0.7 * ease(u / 1.2)
    battery_icon(d, W / 2, 520, 240, 380, max(lvl, 0.02), col=YEL)
    text_c(d, W / 2, 490, f"{int(lvl * 100)}%", 100, WHT, stroke=6, sfill=NAVY)
    if u > dur * 0.4:
        L = new_layer(); d = ImageDraw.Draw(L)
        text_c(d, W / 2, 780, "No llega al 100%", 80, WHT)
        pill(d, W / 2, 920, "FALTAN PANELES", 80, WHT, RED)
        layer_pop(fr, L, u, W / 2, 880, dur * 0.4)
    return fr
def cta(u, dur, t): return cta_frame(t, u, "¿A qué hora se te acaba?", "DÍMELO EN COMENTARIOS")
build("b1", SP, SH, [hook, tres, c1, c2, c3, truco, diag, cta], "/home/claude/w2/b1.mp4")
