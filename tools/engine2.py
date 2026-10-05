# Plantilla visual v2: fondos por formato, transición zoom-punch, subtítulos en caja
import json, math, random
from engine import *
import engine as E0

def bg_mito(t):
    im = Image.new("RGBA", (W, H), (16, 17, 24, 255)); d = ImageDraw.Draw(im)
    off = 40 * math.sin(t * 0.8)
    d.polygon([(0, 0), (W * 0.62 + off, 0), (W * 0.38 + off, H), (0, H)], fill=(70, 18, 26, 255))
    d.polygon([(W * 0.62 + off, 0), (W, 0), (W, H), (W * 0.38 + off, H)], fill=(14, 60, 40, 255))
    for k in range(0, H, 6): d.line([(0, k), (W, k)], fill=(0, 0, 0, 40))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([W / 2 - 500, 300, W / 2 + 500, 1300], fill=(255, 255, 255, 18)); im.alpha_composite(g)
    return im
random.seed(7); CONF = [(random.random() * W, random.random() * H, random.choice([(255,196,0),(63,210,255),(255,90,140),(47,224,138)]), random.random() * 6) for _ in range(70)]
def bg_quiz(t):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    for y in range(0, H, 8):
        k = y / H; c = (int(52 + 70 * k), int(18 + 10 * k), int(110 - 20 * k), 255); d.rectangle([0, y, W, y + 8], fill=c)
    for x, y, c, ph in CONF:
        yy = (y + t * 60) % H; r = 7 + 3 * math.sin(t * 3 + ph); d.ellipse([x - r, yy - r, x + r, yy + r], fill=c + (170,))
    return im
def subtitles2(fr, track, t):
    cur = [c for c in track if c[0] <= t < c[1]]
    if not cur: return
    a, b, txt = cur[0]; u = t - a; d = ImageDraw.Draw(fr); f = F(66)
    words = txt.split(); lines = [txt]
    if d.textlength(txt, font=f) > W - 220:
        half = (len(words) + 1) // 2; lines = [" ".join(words[:half]), " ".join(words[half:])]
    hgt = len(lines) * 84 + 40; y0 = 1430; s = 1 + 0.08 * (1 - ease(u / 0.15))
    wmax = max(d.textlength(l, font=f) for l in lines) + 80
    d.rounded_rectangle([W / 2 - wmax / 2 * s, y0, W / 2 + wmax / 2 * s, y0 + hgt], radius=28, fill=(0, 0, 0, 175))
    d.rectangle([W / 2 - wmax / 2 * s, y0, W / 2 - wmax / 2 * s + 10, y0 + hgt], fill=YEL)
    y = y0 + 18
    for ln in lines:
        text_c(d, W / 2, y, ln, 66, YEL if re.search(r"\d", ln) else WHT); y += 84
def render2(out, total, scenes, track, holes=()):
    """holes: list of (a,b) windows that compose will cover with b-roll (subtitles skipped there)."""
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        t = i / FPS
        sc = [s for s in scenes if s[0] <= t < s[1]] or [scenes[-1]]; a, b, fn = sc[0]
        fr = fn(t - a, b - a, t); u = t - a
        if u < 0.22 and a > 0:  # zoom-punch
            z = 1.10 - 0.10 * ease(u / 0.22); cw, ch = W / z, H / z
            fr = fr.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H))
        if not any(h0 <= t < h1 for h0, h1 in holes): subtitles2(fr, track, t)
        chrome(fr, t, total); enc.stdin.write(fr.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait()
def stamp(fr, u, txt, col, cx, cy, size=170, at=0.0, ang=-12):
    if u < at: return
    k = ease((u - at) / 0.25); s = 1.8 - 0.8 * k
    tw = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(txt, font=F(size)); bw = int(tw + 140); bh = int(size * 1.55)
    L = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([20, 20, bw + 20, bh + 20], radius=30, outline=col, width=max(8, size // 12)); text_c(d, (bw + 40) / 2, 20 + bh * 0.13, txt, size, col)
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC); L = L.resize((int(L.width * s), int(L.height * s)))
    a = L.split()[3].point(lambda v: int(v * k)); L.putalpha(a)
    fr.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2)))
