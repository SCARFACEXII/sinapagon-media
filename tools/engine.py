import math, subprocess, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BLK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
BLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
NAVY = (8, 32, 79); BLUE = (22, 104, 227); CYAN = (0, 229, 255); YEL = (255, 196, 0)
RED = (255, 77, 77); GRN = (46, 224, 122); WHT = (255, 255, 255); GRY = (150, 160, 175)
_fc = {}
def F(size, bold=False):
    k = (size, bold)
    if k not in _fc: _fc[k] = ImageFont.truetype(BLD if bold else BLK, size)
    return _fc[k]

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):  # overshoot pop
    x = clamp(x); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------------- timing ----------------
def timings(sentences, total):
    """sentences: list of spoken strings. Returns [(start,end)] matched to total duration."""
    def pause(s):
        s = s.strip()
        if s.endswith("..."): return 0.6
        if s[-1] in ".?!": return 0.45
        if s[-1] == ":": return 0.25
        return 0.15
    pauses = [pause(s) for s in sentences]; pauses[-1] = 0
    intra = [s.count(",") * 0.12 for s in sentences]
    chars = [len(s) for s in sentences]
    rate = (total - sum(pauses) - sum(intra)) / sum(chars)
    out = []; t = 0.05
    for c, p, i in zip(chars, pauses, intra):
        d = c * rate + i
        out.append((t, t + d)); t += d + p
    return out

def chunks(text, maxw=4):
    words = text.split(); out = []; cur = []
    for w in words:
        cur.append(w)
        if len(cur) >= maxw or re.search(r"[.,:?!…]$", w):
            out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

def sub_track(display_sentences, times):
    track = []
    for txt, (a, b) in zip(display_sentences, times):
        cs = chunks(txt); tot = sum(len(c) for c in cs); t = a
        for c in cs:
            d = (b - a) * len(c) / tot; track.append((t, t + d, c)); t += d
    return track

# ---------------- drawing helpers ----------------
def bg_frame(t, hue=0):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(0, H, 4):
        k = y / H
        r = int(6 + 10 * (1 - k)); g = int(16 + 30 * (1 - k)); b = int(40 + 50 * (1 - k))
        d.rectangle([0, y, W, y + 4], fill=(r, g, b))
    im = im.convert("RGBA"); gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
    for i in range(3):
        cx = W / 2 + 380 * math.sin(t * 0.35 + i * 2.1); cy = H / 2 + 600 * math.cos(t * 0.27 + i * 1.7)
        col = [BLUE, CYAN, YEL][i]
        gd.ellipse([cx - 330, cy - 330, cx + 330, cy + 330], fill=col + (38,))
    gl = gl.filter(ImageFilter.GaussianBlur(120))
    im = Image.alpha_composite(im, gl)
    gd = ImageDraw.Draw(im)
    for x in range(0, W, 90): gd.line([x, 0, x, H], fill=(255, 255, 255, 10))
    for y in range(0, H, 90): gd.line([0, y, W, y], fill=(255, 255, 255, 10))
    return im

def text_c(d, cx, y, txt, size, fill, bold=False, stroke=0, sfill=(0, 0, 0)):
    f = F(size, bold); bb = d.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], y - bb[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return bb[3] - bb[1]

def pill(d, cx, y, txt, size, fg, bg, padx=34, pady=20):
    f = F(size); bb = d.textbbox((0, 0), txt, font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.rounded_rectangle([cx - tw / 2 - padx, y - pady, cx + tw / 2 + padx, y + th + pady], radius=(th + 2 * pady) // 2, fill=bg)
    d.text((cx - tw / 2 - bb[0], y - bb[1]), txt, font=f, fill=fg)
    return th + 2 * pady

def layer_pop(base, layer, u, cx, cy, delay=0, dur=0.35):
    """composite layer (RGBA same size as canvas) scaled with pop around (cx,cy)"""
    s = back((u - delay) / dur) if u > delay else 0
    if s <= 0.01: return
    a = clamp((u - delay) / (dur * 0.6))
    if abs(s - 1) > 0.005:
        w, h = layer.size; nw, nh = max(1, int(w * s)), max(1, int(h * s))
        l2 = layer.resize((nw, nh)); pos = (int(cx - cx * s), int(cy - cy * s))
        tmp = Image.new("RGBA", base.size, (0, 0, 0, 0)); tmp.paste(l2, pos, l2); layer = tmp
    if a < 1:
        r, g, b, al = layer.split(); al = al.point(lambda p: int(p * a)); layer = Image.merge("RGBA", (r, g, b, al))
    base.alpha_composite(layer)

def new_layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

# icons
def battery_icon(d, cx, cy, w, h, level, col=GRN, body=(20, 40, 80), outline=WHT, cracked=False):
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([cx - w * 0.18, y0 - h * 0.07, cx + w * 0.18, y0 + 4], radius=8, fill=outline)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(w * 0.14), fill=body, outline=outline, width=max(6, int(w * 0.05)))
    pad = w * 0.12; ih = h - 2 * pad; fh = ih * clamp(level)
    if fh > 2:
        d.rounded_rectangle([x0 + pad, y0 + pad + ih - fh, x0 + w - pad, y0 + h - pad], radius=int(w * 0.07), fill=col)
    if cracked:
        pts = [(cx - w * 0.1, y0 + h * 0.1), (cx + w * 0.08, y0 + h * 0.35), (cx - w * 0.06, y0 + h * 0.5), (cx + w * 0.1, y0 + h * 0.8)]
        d.line(pts, fill=RED, width=10, joint="curve")

def bolt(d, cx, cy, s, col=YEL):
    p = [(0.1, -1), (-0.55, 0.12), (-0.02, 0.12), (-0.2, 1), (0.55, -0.2), (0.02, -0.2), (0.25, -1)]
    d.polygon([(cx + x * s, cy + y * s) for x, y in p], fill=col, outline=NAVY)

def warn(d, cx, cy, s):
    d.polygon([(cx, cy - s), (cx - s * 1.1, cy + s * 0.9), (cx + s * 1.1, cy + s * 0.9)], fill=RED)
    d.rounded_rectangle([cx - s * 0.1, cy - s * 0.45, cx + s * 0.1, cy + s * 0.35], radius=6, fill=WHT)
    d.ellipse([cx - s * 0.11, cy + s * 0.5, cx + s * 0.11, cy + s * 0.72], fill=WHT)

def sun(d, cx, cy, r, t):
    for i in range(12):
        a = i * math.pi / 6 + t * 0.6
        d.line([cx + math.cos(a) * r * 1.25, cy + math.sin(a) * r * 1.25, cx + math.cos(a) * r * 1.7, cy + math.sin(a) * r * 1.7], fill=YEL, width=int(r * 0.16))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YEL)

def moon(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 240, 255))
    d.ellipse([cx - r * 0.45, cy - r * 1.1, cx + r * 1.45, cy + r * 0.8], fill=(14, 30, 70))

def thermo(d, cx, cy, h, level):
    w = h * 0.22
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(w / 2), fill=WHT)
    d.ellipse([cx - w, cy + h / 2 - w * 0.6, cx + w, cy + h / 2 + w * 1.4], fill=WHT)
    col = (int(255), int(200 - 150 * level), int(60 - 40 * level))
    d.ellipse([cx - w * 0.75, cy + h / 2 - w * 0.35, cx + w * 0.75, cy + h / 2 + w * 1.15], fill=col)
    fh = (h - w) * clamp(level)
    d.rounded_rectangle([cx - w * 0.25, cy + h / 2 - fh, cx + w * 0.25, cy + h / 2 + 10], radius=int(w * 0.25), fill=col)

def panel(d, cx, cy, w, h):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=10, fill=(20, 60, 140), outline=WHT, width=6)
    for i in range(1, 4): d.line([cx - w / 2 + w * i / 4, cy - h / 2, cx - w / 2 + w * i / 4, cy + h / 2], fill=(120, 170, 255), width=3)
    for j in range(1, 6): d.line([cx - w / 2, cy - h / 2 + h * j / 6, cx + w / 2, cy - h / 2 + h * j / 6], fill=(120, 170, 255), width=3)

def ac_unit(d, cx, cy, w, t):
    h = w * 0.34
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(h * 0.3), fill=(240, 244, 250), outline=(180, 190, 205), width=5)
    d.rounded_rectangle([cx - w * 0.42, cy + h * 0.15, cx + w * 0.42, cy + h * 0.3], radius=8, fill=(190, 200, 215))
    d.ellipse([cx + w * 0.36, cy - h * 0.3, cx + w * 0.42, cy - h * 0.18], fill=GRN)
    for i in range(4):
        off = (t * 120 + i * 60) % 240
        yy = cy + h / 2 + 30 + off
        a = int(200 * (1 - off / 240))
        d.arc([cx - w * 0.35 + i * 40, yy - 20, cx - w * 0.05 + i * 40, yy + 20], 200, 340, fill=CYAN + (a,), width=8)
        d.arc([cx + w * 0.05 - i * 40, yy - 20, cx + w * 0.35 - i * 40, yy + 20], 200, 340, fill=CYAN + (a,), width=8)

def chat(d, cx, cy, s):
    d.rounded_rectangle([cx - s, cy - s * 0.7, cx + s, cy + s * 0.55], radius=int(s * 0.35), fill=WHT)
    d.polygon([(cx - s * 0.4, cy + s * 0.5), (cx - s * 0.75, cy + s * 0.95), (cx - s * 0.05, cy + s * 0.5)], fill=WHT)
    for i in (-1, 0, 1): d.ellipse([cx + i * s * 0.45 - s * 0.12, cy - s * 0.2, cx + i * s * 0.45 + s * 0.12, cy + s * 0.04], fill=BLUE)

# footage reader
class Footage:
    def __init__(self, path, start, dur, zoom=(1.0, 1.15), focus=(0.5, 0.5)):
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(start), "-i", path, "-t", str(dur + 0.5),
                                      "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=contrast=1.06:saturation=1.15",
                                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.last = None; self.zoom = zoom; self.focus = focus; self.dur = dur
    def frame(self, u):
        raw = self.proc.stdout.read(W * H * 3)
        if len(raw) == W * H * 3: self.last = Image.frombytes("RGB", (W, H), raw)
        im = self.last
        z = self.zoom[0] + (self.zoom[1] - self.zoom[0]) * clamp(u / self.dur)
        cw, ch = W / z, H / z; fx, fy = self.focus
        x0 = (W - cw) * fx; y0 = (H - ch) * fy
        return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H)).convert("RGBA")

# overlays common
def subtitles(fr, track, t):
    cur = [c for c in track if c[0] <= t < c[1]]
    if not cur: return
    a, b, txt = cur[0]; u = t - a
    d = ImageDraw.Draw(fr); s = 1 + 0.12 * (1 - ease(u / 0.12))
    size = int(74 * s)
    words = txt.split(); lines = [txt]
    f = F(size)
    if d.textlength(txt, font=f) > W - 140:
        half = (len(words) + 1) // 2; lines = [" ".join(words[:half]), " ".join(words[half:])]
    y = 1400
    for ln in lines:
        col = YEL if re.search(r"\d", ln) else WHT
        text_c(d, W / 2, y, ln, size, col, stroke=9, sfill=(0, 0, 0))
        y += int(size * 1.25)

def chrome(fr, t, total):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, 12], fill=(255, 255, 255, 40))
    d.rectangle([0, 0, W * clamp(t / total), 12], fill=YEL)
    f = F(40); txt = "SIN APAGÓN"; tw = d.textlength(txt, font=f)
    d.rounded_rectangle([W - tw - 100, H - 128, W - 24, H - 58], radius=35, fill=NAVY + (220,))
    bolt(d, W - tw - 70, H - 93, 20)
    d.text((W - tw - 44, H - 122), txt, font=f, fill=YEL)

def render(out, total, scenes, track):
    """scenes: list of (start, end, fn) where fn(t_local, dur, t_global) -> RGBA frame"""
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    n = int(total * FPS)
    for i in range(n):
        t = i / FPS
        sc = [s for s in scenes if s[0] <= t < s[1]] or [scenes[-1]]
        a, b, fn = sc[0]
        fr = fn(t - a, b - a, t)
        # quick white flash transition at scene start
        if t - a < 0.12 and a > 0:
            fl = Image.new("RGBA", (W, H), (255, 255, 255, int(120 * (1 - (t - a) / 0.12)))); fr.alpha_composite(fl)
        subtitles(fr, track, t)
        chrome(fr, t, total)
        enc.stdin.write(fr.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait()
