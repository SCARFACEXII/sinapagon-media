import json, sys
sys.path.insert(0, "/home/claude/w2")
from engine import *

TOTAL = json.load(open("/home/claude/w2/voices.json"))["v1"]["dur"] + 0.6
SPOKEN = ["Tres errores que matan tu batería de litio...", "y casi todo el mundo los comete.",
          "Error número uno: configurar mal el inversor.", "Si le dejas los voltajes de una batería de plomo, la sobrecargas todos los días.",
          "Error número dos: descargarla hasta cero.", "Déjale siempre un diez o veinte por ciento de reserva.",
          "Error número tres: ponerla al sol, o en un lugar caliente.", "El calor le acorta la vida más que cualquier otra cosa.",
          "¿Cometías alguno? Cuéntamelo en los comentarios...", "y sígueme para más."]
SHOW = ["3 errores que matan tu batería de litio...", "y casi todos los cometen.",
        "Error #1: configurar mal el inversor.", "Con voltajes de plomo, la sobrecargas todos los días.",
        "Error #2: descargarla hasta 0%.", "Déjale siempre 10 o 20% de reserva.",
        "Error #3: ponerla al sol o en un lugar caliente.", "El calor le acorta la vida más que nada.",
        "¿Cometías alguno? Cuéntamelo en comentarios...", "y sígueme para más."]
T = timings(SPOKEN, TOTAL - 0.6)
track = sub_track(SHOW, T)
S = lambda i: T[i][0]

def hook(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 330, "3 ERRORES", 150, RED, stroke=6, sfill=(60, 0, 0))
    layer_pop(fr, L, u, W / 2, 430, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 590, "que matan tu", 80, WHT); text_c(d, W / 2, 690, "BATERÍA DE LITIO", 92, YEL)
    layer_pop(fr, L, u, W / 2, 700, 0.5)
    L = new_layer(); d = ImageDraw.Draw(L)
    sh = 10 * math.sin(t * 40) if u > 1.2 else 0
    battery_icon(d, W / 2 + sh, 1050, 260, 380, 0.15, col=RED, cracked=u > 1.2)
    layer_pop(fr, L, u, W / 2, 1050, 0.8)
    return fr

def err1(u, dur, t, fo=[None]):
    if fo[0] is None: fo[0] = Footage("/mnt/user-data/uploads/VID_20260513_125818762.mp4", 11.6, dur, zoom=(1.0, 1.18), focus=(0.5, 0.35))
    fr = fo[0].frame(u)
    dim = Image.new("RGBA", (W, H), (0, 10, 30, 70)); fr.alpha_composite(dim)
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "ERROR #1", 70, WHT, RED)
    text_c(d, W / 2, 300, "Configurar mal", 84, WHT, stroke=8); text_c(d, W / 2, 400, "el inversor", 84, WHT, stroke=8)
    layer_pop(fr, L, u, W / 2, 300, 0.0)
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 560, "Voltajes de PLOMO = sobrecarga", 50, WHT, (150, 20, 20))
    layer_pop(fr, L, u, W / 2, 580, S(3) - S(2))
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 680, "Usa los voltajes de LITIO", 50, NAVY, GRN)
    layer_pop(fr, L, u, W / 2, 700, S(3) - S(2) + 2.2)
    return fr

def err2(u, dur, t):
    fr = bg_frame(t); d0 = ImageDraw.Draw(fr)
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "ERROR #2", 70, WHT, RED)
    text_c(d, W / 2, 300, "Descargarla hasta 0%", 80, WHT)
    layer_pop(fr, L, u, W / 2, 300, 0)
    t5 = S(5) - S(4)
    if u < t5:
        lvl = 1 - ease((u - 0.4) / max(0.5, t5 - 0.8))
        col = GRN if lvl > 0.5 else (YEL if lvl > 0.2 else RED)
    else:
        lvl = 0.2 * ease((u - t5) / 0.8); col = GRN
    d = ImageDraw.Draw(fr)
    battery_icon(d, W / 2, 820, 300, 520, lvl, col=col)
    text_c(d, W / 2, 790, f"{int(round(lvl * 100))}%", 110, WHT, stroke=6, sfill=NAVY)
    if u >= t5:
        L = new_layer(); d = ImageDraw.Draw(L)
        d.line([W / 2 - 230, 820 + 260 - 0.2 * 400 - 40, W / 2 + 230, 820 + 260 - 0.2 * 400 - 40], fill=YEL, width=8)
        pill(d, W / 2, 1150, "Deja 10–20% de reserva", 58, NAVY, GRN)
        layer_pop(fr, L, u, W / 2, 1170, t5 + 0.3)
    return fr

def err3(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 150, "ERROR #3", 70, WHT, RED)
    text_c(d, W / 2, 300, "Sol y calor", 90, WHT)
    layer_pop(fr, L, u, W / 2, 300, 0)
    d = ImageDraw.Draw(fr)
    sun(d, W / 2 - 200, 700, 120, t)
    lvl = ease(u / 3.0)
    thermo(d, W / 2 + 230, 760, 380, lvl)
    text_c(d, W / 2 + 230, 470, f"{int(25 + 25 * lvl)}°C", 70, RED if lvl > 0.5 else WHT)
    t7 = S(7) - S(6)
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 1150, "El calor le acorta la vida", 56, WHT, (150, 20, 20))
    layer_pop(fr, L, u, W / 2, 1170, t7)
    return fr

def cta(u, dur, t):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    chat(d, W / 2, 520, 190)
    layer_pop(fr, L, u, W / 2, 520, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 800, "¿Cometías alguno?", 90, WHT)
    text_c(d, W / 2, 920, "Cuéntamelo en comentarios", 58, YEL)
    layer_pop(fr, L, u, W / 2, 880, 0.35)
    L = new_layer(); d = ImageDraw.Draw(L)
    pill(d, W / 2, 1110, "SÍGUEME PARA MÁS", 60, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 1130, S(9) - S(8))
    return fr

scenes = [(0, S(2), hook), (S(2), S(4), err1), (S(4), S(6), err2), (S(6), S(8), err3), (S(8), TOTAL, cta)]
render("/home/claude/w2/v1.mp4", TOTAL, scenes, track)
