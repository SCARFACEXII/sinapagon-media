# Plantilla v3: 5 formatos nuevos (Alerta, Batalla, Plano paso a paso, Noche/cronómetro, Obra/errores)
import sys, json, math, random
sys.path.insert(0, "/home/claude/w2")
from engine2 import *
from common2 import foot, pot, shower, station

ORG = (255, 140, 30); PUR = (170, 90, 255)

# ---------- fondos ----------
def bg_alerta(t):
    im = Image.new("RGBA", (W, H), (14, 8, 10, 255)); d = ImageDraw.Draw(im)
    p = 0.5 + 0.5 * math.sin(t * 6)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for r in range(900, 0, -60):
        a = int(10 + 22 * p * (1 - r / 900))
        gd.ellipse([W / 2 - r, -r * 0.6, W / 2 + r, r * 0.9], fill=(255, 30, 30, a))
    im.alpha_composite(g)
    ang = t * 2.2  # haz giratorio de sirena
    for k in (0, math.pi):
        a = ang + k; x = W / 2 + math.cos(a) * 1600; y = 60 + math.sin(a) * 600
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
        ld.polygon([(W / 2, 60), (x - 260, y), (x + 260, y)], fill=(255, 60, 40, 28)); im.alpha_composite(L)
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 26, W, H], fill=(255, 40, 40, int(120 + 100 * p)))
    return im

def bg_ring(t):
    im = Image.new("RGBA", (W, H), (10, 10, 16, 255)); d = ImageDraw.Draw(im)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    sway = 60 * math.sin(t * 0.7)
    gd.polygon([(W / 2 - 80 + sway, 0), (W / 2 + 80 + sway, 0), (W + 200, H), (-200, H)], fill=(255, 250, 220, 22))
    gd.ellipse([-100, 1150, W + 100, 1700], fill=(255, 250, 220, 30)); im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    for i, col in enumerate([(220, 40, 50), (240, 240, 240), (30, 90, 220)]):
        y = 1180 + i * 70; d.line([(0, y), (W, y + 30)], fill=col, width=10)
    d.rectangle([30, 1150, 60, 1450], fill=(200, 200, 210)); d.rectangle([W - 60, 1150, W - 30, 1450], fill=(200, 200, 210))
    return im

def bg_plano(t):
    im = Image.new("RGBA", (W, H), (12, 52, 128, 255)); d = ImageDraw.Draw(im)
    off = (t * 20) % 60
    for x in range(-60, W + 60, 60): d.line([(x + off, 0), (x + off, H)], fill=(80, 130, 210, 90), width=2)
    for y in range(-60, H + 60, 60): d.line([(0, y + off), (W, y + off)], fill=(80, 130, 210, 90), width=2)
    for x in range(-240, W + 240, 240): d.line([(x + off, 0), (x + off, H)], fill=(140, 180, 240, 120), width=3)
    d.rectangle([24, 24, W - 24, H - 24], outline=(200, 225, 255, 140), width=4)
    return im

random.seed(11); STARS = [(random.random() * W, random.random() * 1100, random.random() * 6, random.choice([2, 3, 4])) for _ in range(110)]
def bg_noche(t):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    for y in range(0, H, 8):
        k = y / H; d.rectangle([0, y, W, y + 8], fill=(int(8 + 30 * k), int(10 + 14 * k), int(40 + 40 * k), 255))
    for x, y, ph, r in STARS:
        a = int(120 + 120 * (0.5 + 0.5 * math.sin(t * 2 + ph))); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
    d.polygon([(0, 1500), (180, 1380), (320, 1440), (520, 1330), (700, 1420), (880, 1350), (W, 1430), (W, H), (0, H)], fill=(6, 8, 20, 255))
    for x, y in [(240, 1450), (600, 1400), (930, 1420)]: d.rectangle([x, y, x + 26, y + 30], fill=(40, 40, 60))  # ventanas apagadas
    return im

def tape(im, y, ang, t):
    L = Image.new("RGBA", (W + 600, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, 0, W + 600, 110], fill=(255, 200, 0, 255))
    off = (t * 80) % 140
    for x in range(-140, W + 740, 140): d.polygon([(x + off, 0), (x + 70 + off, 0), (x + off, 110), (x - 70 + off, 110)], fill=(20, 20, 20, 255))
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC); im.alpha_composite(L, (-300, int(y - L.height / 2)))

def bg_obra(t):
    im = Image.new("RGBA", (W, H), (34, 36, 40, 255)); d = ImageDraw.Draw(im)
    random.seed(3)
    for _ in range(260):
        x, y = random.random() * W, random.random() * H; c = random.randint(40, 60); d.ellipse([x, y, x + 5, y + 5], fill=(c, c, c + 4))
    tape(im, 70, 4, t); tape(im, H - 90, -4, -t)
    return im

# ---------- iconos ----------
def fan(d, cx, cy, s, t):
    for k in range(3):
        a = t * 8 + k * 2.094; x = cx + math.cos(a) * s * 0.5; y = cy + math.sin(a) * s * 0.5
        d.ellipse([x - s * 0.32, y - s * 0.32, x + s * 0.32, y + s * 0.32], fill=(200, 230, 255))
    d.ellipse([cx - s * 0.15, cy - s * 0.15, cx + s * 0.15, cy + s * 0.15], fill=NAVY); d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=WHT, width=8)
    d.rectangle([cx - 10, cy + s, cx + 10, cy + s * 1.6], fill=WHT); d.rounded_rectangle([cx - s * 0.6, cy + s * 1.55, cx + s * 0.6, cy + s * 1.7], radius=8, fill=WHT)
def fridge(d, cx, cy, s, col=(230, 235, 245)):
    d.rounded_rectangle([cx - s * 0.6, cy - s, cx + s * 0.6, cy + s], radius=20, fill=col, outline=WHT, width=5)
    d.line([(cx - s * 0.6, cy - s * 0.25), (cx + s * 0.6, cy - s * 0.25)], fill=(150, 160, 180), width=6); d.rectangle([cx + s * 0.38, cy - s * 0.75, cx + s * 0.46, cy - s * 0.45], fill=(150, 160, 180))
def bulb(d, cx, cy, s, on=True):
    d.ellipse([cx - s * 0.5, cy - s * 0.6, cx + s * 0.5, cy + s * 0.4], fill=YEL if on else (90, 90, 100))
    d.rectangle([cx - s * 0.22, cy + s * 0.35, cx + s * 0.22, cy + s * 0.65], fill=(180, 185, 195))
def phone(d, cx, cy, s):
    d.rounded_rectangle([cx - s * 0.45, cy - s * 0.85, cx + s * 0.45, cy + s * 0.85], radius=24, fill=(30, 32, 40), outline=WHT, width=6)
    d.rounded_rectangle([cx - s * 0.2, cy - s * 0.35, cx + s * 0.2, cy + s * 0.35], radius=6, outline=GRN, width=5)
def tv(d, cx, cy, s):
    d.rounded_rectangle([cx - s, cy - s * 0.6, cx + s, cy + s * 0.5], radius=14, fill=(20, 24, 34), outline=WHT, width=6)
    d.rectangle([cx - 8, cy + s * 0.5, cx + 8, cy + s * 0.75], fill=WHT); d.rounded_rectangle([cx - s * 0.4, cy + s * 0.72, cx + s * 0.4, cy + s * 0.82], radius=6, fill=WHT)
def protector(d, cx, cy, s, t, ok=True):
    d.rounded_rectangle([cx - s * 0.6, cy - s, cx + s * 0.6, cy + s], radius=26, fill=(240, 242, 248), outline=WHT, width=5)
    d.rounded_rectangle([cx - s * 0.42, cy - s * 0.8, cx + s * 0.42, cy - s * 0.3], radius=10, fill=(20, 30, 40))
    text_c(d, cx, cy - s * 0.78, "120V" if ok else "145V", int(s * 0.3), GRN if ok else RED)
    for k, c in enumerate([GRN, YEL, RED]):
        on = (c == GRN and ok) or (c == RED and not ok and int(t * 4) % 2 == 0)
        d.ellipse([cx - s * 0.4 + k * s * 0.3, cy - s * 0.1, cx - s * 0.2 + k * s * 0.3, cy + s * 0.1], fill=c if on else (120, 125, 135))
    for k in (-1, 1): d.rounded_rectangle([cx + k * s * 0.18 - s * 0.06, cy + s * 0.35, cx + k * s * 0.18 + s * 0.06, cy + s * 0.75], radius=6, fill=(60, 60, 70))
def inverter(d, cx, cy, s):
    d.rounded_rectangle([cx - s * 0.7, cy - s, cx + s * 0.7, cy + s], radius=24, fill=(230, 232, 238), outline=WHT, width=5)
    d.rounded_rectangle([cx - s * 0.45, cy - s * 0.7, cx + s * 0.45, cy - s * 0.25], radius=10, fill=(20, 60, 90))
    text_c(d, cx, cy - s * 0.68, "INV", int(s * 0.25), CYAN)
    for k in range(4): d.rectangle([cx - s * 0.5, cy + s * 0.1 + k * s * 0.18, cx + s * 0.5, cy + s * 0.18 + k * s * 0.18], fill=(160, 165, 175))
def breaker(d, cx, cy, s, on=True):
    d.rounded_rectangle([cx - s * 0.35, cy - s, cx + s * 0.35, cy + s], radius=12, fill=(245, 245, 248), outline=(180, 185, 195), width=4)
    d.rounded_rectangle([cx - s * 0.18, cy - s * 0.4, cx + s * 0.18, cy + s * 0.4], radius=8, fill=(40, 40, 50))
    y = cy - s * 0.25 if on else cy + s * 0.05; d.rounded_rectangle([cx - s * 0.14, y, cx + s * 0.14, y + s * 0.2], radius=6, fill=GRN if on else RED)
def clock(d, cx, cy, r, hh, mm):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 246, 250), outline=YEL, width=10)
    for i in range(12):
        a = i * math.pi / 6; d.line([cx + math.sin(a) * r * 0.8, cy - math.cos(a) * r * 0.8, cx + math.sin(a) * r * 0.92, cy - math.cos(a) * r * 0.92], fill=NAVY, width=6)
    ah = (hh % 12 + mm / 60) * math.pi / 6; am = mm * math.pi / 30
    d.line([cx, cy, cx + math.sin(ah) * r * 0.5, cy - math.cos(ah) * r * 0.5], fill=NAVY, width=14)
    d.line([cx, cy, cx + math.sin(am) * r * 0.75, cy - math.cos(am) * r * 0.75], fill=RED, width=8); d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=NAVY)
def hora(h):  # h decimal 20..31 -> "8:00 pm"
    hh = int(h) % 24; mm = int((h - int(h)) * 60); ap = "am" if hh < 12 else "pm"; h12 = hh % 12 or 12
    return f"{h12}:{mm:02d} {ap}"
def number_badge(d, cx, cy, n, col=YEL, fg=NAVY, r=70):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); text_c(d, cx, cy - r * 0.62, str(n), int(r * 1.1), fg)
def xmark(d, cx, cy, s, col=RED, w=22):
    d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=col, width=w); d.line([(cx - s, cy + s), (cx + s, cy - s)], fill=col, width=w)
def check(d, cx, cy, s, col=GRN, w=22):
    d.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.7)], fill=col, width=w, joint="curve")
def pop(fr, u, at, cx, cy, draw):
    L = new_layer(); draw(ImageDraw.Draw(L)); layer_pop(fr, L, u, cx, cy, at)

def run(name, vdur, SP, SH, fns, hole_idx):
    TOTAL = vdur + 0.6
    T = timings(SP, TOTAL - 0.6); track = sub_track(SH, T)
    n = len(fns)
    scenes = [(0 if i == 0 else T[i][0], T[i + 1][0] if i < n - 1 else TOTAL, fn) for i, fn in enumerate(fns)]
    holes = [(scenes[i][0], scenes[i][1]) for i in hole_idx]
    json.dump({"total": TOTAL, "holes": holes, "show": [SH[i] for i in hole_idx]}, open(f"/home/claude/w2/{name}_holes.json", "w"))
    render2(f"/home/claude/w2/{name}.mp4", TOTAL, scenes, track, holes)
    return TOTAL, holes
