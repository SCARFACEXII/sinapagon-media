import json, sys
sys.path.insert(0, "/home/claude/w2")
from engine import *
U = "/root/.claude/uploads/496944e7-2387-59a5-b6d7-4284eb12520e/"
CL = {k: U + v for k, v in {"404": "0731b340-VID-20261001-WA0404.mp4", "403": "65a8fd6a-VID-20261001-WA0403.mp4",
      "399": "b45c053a-VID-20261001-WA0399.mp4", "405": "4debce8f-VID-20261001-WA0405.mp4", "402": "3632993f-VID-20261001-WA0402.mp4",
      "406": "45d642d2-VID-20261001-WA0406.mp4", "407": "8f9207e7-VID-20261001-WA0407.mp4", "398": "7e3da322-VID-20261001-WA0398.mp4"}.items()}
def foot(key, start, zoom=(1.0, 1.12), focus=(0.5, 0.5), dim=70):
    st = {}
    def get(u, dur):
        if "f" not in st: st["f"] = Footage(CL[key], start, dur, zoom=zoom, focus=focus)
        fr = st["f"].frame(u)
        if dim: fr.alpha_composite(Image.new("RGBA", (W, H), (0, 10, 30, dim)))
        return fr
    return get
def row(d, y, label, value, vcol):
    d.rounded_rectangle([90, y, W - 90, y + 120], radius=30, fill=(10, 26, 64, 225), outline=(255, 255, 255, 50), width=3)
    d.text((140, y + 28), label, font=F(50, True), fill=WHT)
    f = F(62); tw = d.textlength(value, font=f); d.text((W - 140 - tw, y + 22), value, font=f, fill=vcol)
def hotplate(d, cx, cy, s, t):
    d.rounded_rectangle([cx - s, cy - s * 0.7, cx + s, cy + s * 0.7], radius=30, fill=(30, 32, 38), outline=(120, 125, 135), width=5)
    g = 0.6 + 0.4 * math.sin(t * 5)
    for k, r in enumerate([0.55, 0.4, 0.25]):
        col = (int(255 * g), int(80 + 40 * k), 20)
        d.ellipse([cx - s * r, cy - s * r, cx + s * r, cy + s * r], outline=col, width=12)
def cta_frame(t, u, l1, l2):
    fr = bg_frame(t); L = new_layer(); d = ImageDraw.Draw(L)
    chat(d, W / 2, 480, 180); layer_pop(fr, L, u, W / 2, 480, 0.05)
    L = new_layer(); d = ImageDraw.Draw(L)
    text_c(d, W / 2, 760, l1, 84, WHT)
    pill(d, W / 2, 920, l2, 58, NAVY, YEL)
    layer_pop(fr, L, u, W / 2, 860, 0.3)
    return fr
def build(key, spoken, show, fns, out):
    TOTAL = json.load(open("/home/claude/w2/voices.json"))[key]["dur"] + 0.6
    T = timings(spoken, TOTAL - 0.6); track = sub_track(show, T)
    n = len(fns)
    scenes = [(0 if i == 0 else T[i][0], T[i + 1][0] if i < n - 1 else TOTAL, fn) for i, fn in enumerate(fns)]
    render(out, TOTAL, scenes, track)

def pot(d, cx, cy, s):
    d.rounded_rectangle([cx - s, cy - s * 0.3, cx + s, cy + s * 0.75], radius=int(s * 0.25), fill=(200, 205, 215), outline=WHT, width=4)
    d.rectangle([cx - s * 1.2, cy - s * 0.25, cx - s, cy - s * 0.05], fill=(150, 155, 165)); d.rectangle([cx + s, cy - s * 0.25, cx + s * 1.2, cy - s * 0.05], fill=(150, 155, 165))
    d.rounded_rectangle([cx - s * 1.05, cy - s * 0.5, cx + s * 1.05, cy - s * 0.3], radius=8, fill=(120, 125, 135)); d.ellipse([cx - 14, cy - s * 0.68, cx + 14, cy - s * 0.48], fill=(120, 125, 135))
def microwave(d, cx, cy, s):
    d.rounded_rectangle([cx - s * 1.3, cy - s * 0.75, cx + s * 1.3, cy + s * 0.75], radius=18, fill=(220, 225, 235), outline=WHT, width=4)
    d.rounded_rectangle([cx - s * 1.1, cy - s * 0.55, cx + s * 0.5, cy + s * 0.55], radius=12, fill=(30, 40, 60))
    for k in range(3): d.ellipse([cx + s * 0.75, cy - s * 0.45 + k * s * 0.35, cx + s * 0.95, cy - s * 0.25 + k * s * 0.35], fill=(90, 95, 110))
def shower(d, cx, cy, s, t):
    d.rounded_rectangle([cx - s * 0.7, cy - s * 0.9, cx + s * 0.7, cy - s * 0.5], radius=16, fill=(220, 225, 235), outline=WHT, width=4)
    for k in range(7):
        x = cx - s * 0.55 + k * s * 0.18; y = cy - s * 0.35 + ((t * 300 + k * 37) % (s * 1.2))
        d.line([(x, y), (x, y + 26)], fill=CYAN, width=6)
