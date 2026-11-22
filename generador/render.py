"""Reel 'recepcionista IA' para empresas de reformas — estética blanco/naranja con flujos por pasos."""
import json, math, os, subprocess, sys
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("WORK", os.getcwd())  # carpeta con timing.json
H_ = json.load(open(os.environ["HISTORIA"]))  # historia del día
W, H, FPS = 1080, 1920, 30
AGENCIA = H_.get("marca", "norte.local")

OR = (226, 84, 52); OR_L = (250, 222, 212); OR_XL = (253, 240, 235)
INK = (22, 22, 26); GREY = (142, 140, 146); LGREY = (214, 210, 210); WHITE = (255, 255, 255)
GREEN = (46, 190, 98)
FD = "/usr/share/fonts/opentype/inter/"
@lru_cache(None)
def F(name, size): return ImageFont.truetype(FD + name, size)
BLK = lambda s: F("InterDisplay-Black.otf", s)
XB = lambda s: F("Inter-ExtraBold.otf", s)
BD = lambda s: F("Inter-Bold.otf", s)
SB = lambda s: F("Inter-SemiBold.otf", s)
MD = lambda s: F("Inter-Medium.otf", s)

TM = json.load(open(os.path.join(WORK, "timing.json")))
LINES = TM["lines"]; TOTAL = TM["total"]
def first(scene): return next((l["start"] for l in LINES if l["scene"] == scene), 1e9)  # escena ausente = nunca
def line_t(i): return LINES[i]["start"]
def sl(scene, i):
    ls = [l for l in LINES if l["scene"] == scene]
    return ls[min(i, len(ls) - 1)]["start"]
C = H_["cliente"]; HM = H_["hora_mensaje"]
def hm_sec(hm): h, m = hm.split(":"); return int(h) * 3600 + int(m) * 60

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def eback(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def pr(t, a, d): return clamp((t - a) / d)

# ---------- tiles ----------
def shadowed(img, blur=16, dy=10, alpha=55, color=(150, 70, 50)):
    pad = blur * 2 + abs(dy)
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, color + (0,))
    a = Image.new("L", out.size, 0)
    a.paste(img.getchannel("A").point(lambda v: v * alpha // 255), (pad, pad + dy))
    a = a.filter(ImageFilter.GaussianBlur(blur))
    sh.putalpha(a)
    out.alpha_composite(sh)
    out.alpha_composite(img, (pad, pad))
    return out

def paste(dst, tile, cx, cy, scale=1.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01: return
    t = tile
    if abs(scale - 1) > 0.005:
        t = t.resize((max(1, int(t.width * scale)), max(1, int(t.height * scale))), Image.BICUBIC)
    if alpha < 0.995:
        t = t.copy(); t.putalpha(t.getchannel("A").point(lambda v: int(v * alpha)))
    dst.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))

def pop(dst, tile, cx, cy, t, t0, d=0.45, base_alpha=1.0):
    p = pr(t, t0, d)
    if p <= 0: return
    paste(dst, tile, cx, cy + (1 - eo(p)) * 18, 0.86 + 0.14 * eback(p), base_alpha * eo(min(1, p * 1.6)))

def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([int(v) for v in box], radius=r, fill=fill, outline=outline, width=width)

def check(d, cx, cy, s, color=WHITE, w=5):
    d.line([(cx - s * 0.45, cy + s * 0.02), (cx - s * 0.12, cy + s * 0.32), (cx + s * 0.48, cy - s * 0.3)], fill=color, width=w, joint="curve")

def text_w(txt, font): b = font.getbbox(txt); return b[2] - b[0]

def wrap(txt, font, maxw):
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# ---------- icons (drawn in a 64x64 box at scale k) ----------
def icon(d, kind, x, y, k=1.0):
    S = lambda v: v * k
    if kind == "chat":
        rr(d, (x, y, x + S(64), y + S(64)), int(S(18)), fill=GREEN)
        d.ellipse((x + S(14), y + S(14), x + S(50), y + S(46)), outline=WHITE, width=int(S(5)))
        d.polygon([(x + S(17), y + S(38)), (x + S(13), y + S(52)), (x + S(27), y + S(45))], fill=WHITE)
    elif kind == "wave":
        hs = [14, 26, 40, 22, 34, 18, 10]
        for i, h_ in enumerate(hs):
            cx = x + S(8 + i * 8)
            d.line([(cx, y + S(32 - h_ / 2)), (cx, y + S(32 + h_ / 2))], fill=OR, width=int(S(5)))
    elif kind == "spark":
        cx, cy = x + S(32), y + S(32)
        for a in range(4):
            ang = a * math.pi / 2
            pts = [(cx + math.cos(ang) * S(30), cy + math.sin(ang) * S(30)),
                   (cx + math.cos(ang + math.pi / 4) * S(8), cy + math.sin(ang + math.pi / 4) * S(8)),
                   (cx, cy),
                   (cx + math.cos(ang - math.pi / 4) * S(8), cy + math.sin(ang - math.pi / 4) * S(8))]
            d.polygon(pts, fill=OR)
        d.ellipse((cx + S(14), cy - S(30), cx + S(26), cy - S(18)), fill=OR)
    elif kind == "folder":
        d.polygon([(x + S(6), y + S(14)), (x + S(26), y + S(14)), (x + S(32), y + S(22)), (x + S(58), y + S(22)),
                   (x + S(58), y + S(52)), (x + S(6), y + S(52))], fill=(238, 150, 120))
        rr(d, (x + S(6), y + S(26), x + S(58), y + S(54)), int(S(6)), fill=OR)
    elif kind == "cal":
        rr(d, (x + S(6), y + S(10), x + S(58), y + S(58)), int(S(9)), fill=WHITE, outline=(60, 120, 230), width=int(S(4)))
        d.rectangle((x + S(8), y + S(12), x + S(56), y + S(24)), fill=(60, 120, 230))
        for i in range(3):
            for j in range(2):
                d.rectangle((x + S(16 + i * 13), y + S(32 + j * 11), x + S(22 + i * 13), y + S(38 + j * 11)), fill=(60, 120, 230))
    elif kind == "alarm":
        d.ellipse((x + S(10), y + S(12), x + S(54), y + S(56)), fill=WHITE, outline=OR, width=int(S(5)))
        d.line([(x + S(32), y + S(34)), (x + S(32), y + S(22))], fill=INK, width=int(S(4)))
        d.line([(x + S(32), y + S(34)), (x + S(42), y + S(38))], fill=INK, width=int(S(4)))
        d.ellipse((x + S(4), y + S(6), x + S(18), y + S(20)), fill=OR); d.ellipse((x + S(46), y + S(6), x + S(60), y + S(20)), fill=OR)
    elif kind == "bell":
        d.pieslice((x + S(12), y + S(8), x + S(52), y + S(56)), 180, 360, fill=(240, 170, 40))
        d.rectangle((x + S(12), y + S(32), x + S(52), y + S(46)), fill=(240, 170, 40))
        d.rectangle((x + S(6), y + S(44), x + S(58), y + S(50)), fill=(220, 140, 20))
        d.ellipse((x + S(26), y + S(48), x + S(38), y + S(60)), fill=(220, 140, 20))
    elif kind == "card":
        rr(d, (x + S(4), y + S(12), x + S(60), y + S(52)), int(S(8)), fill=(245, 205, 150))
        d.ellipse((x + S(12), y + S(20), x + S(28), y + S(36)), fill=OR)
        d.rectangle((x + S(34), y + S(22), x + S(52), y + S(26)), fill=WHITE)
        d.rectangle((x + S(34), y + S(32), x + S(48), y + S(36)), fill=WHITE)
        d.pieslice((x + S(10), y + S(36), x + S(30), y + S(56)), 180, 360, fill=OR)
    elif kind == "camera":
        rr(d, (x + S(4), y + S(18), x + S(60), y + S(54)), int(S(8)), fill=(70, 72, 80))
        d.rectangle((x + S(22), y + S(12), x + S(42), y + S(20)), fill=(70, 72, 80))
        d.ellipse((x + S(20), y + S(24), x + S(44), y + S(48)), fill=WHITE)
        d.ellipse((x + S(26), y + S(30), x + S(38), y + S(42)), fill=(70, 72, 80))
    elif kind == "robot":
        d.line([(x + S(32), y + S(4)), (x + S(32), y + S(14))], fill=INK, width=int(S(4)))
        d.ellipse((x + S(27), y + S(0), x + S(37), y + S(10)), fill=OR)
        rr(d, (x + S(8), y + S(14), x + S(56), y + S(52)), int(S(14)), fill=(60, 64, 76))
        rr(d, (x + S(14), y + S(22), x + S(50), y + S(42)), int(S(9)), fill=(150, 225, 240))
        d.ellipse((x + S(21), y + S(27), x + S(29), y + S(37)), fill=INK); d.ellipse((x + S(35), y + S(27), x + S(43), y + S(37)), fill=INK)
    elif kind == "moon":
        d.ellipse((x + S(8), y + S(8), x + S(56), y + S(56)), fill=(245, 190, 60))
        d.ellipse((x + S(22), y + S(0), x + S(66), y + S(46)), fill=WHITE)
    elif kind == "sun":
        cx, cy = x + S(32), y + S(32)
        for a in range(8):
            ang = a * math.pi / 4
            d.line([(cx + math.cos(ang) * S(18), cy + math.sin(ang) * S(18)), (cx + math.cos(ang) * S(28), cy + math.sin(ang) * S(28))], fill=(245, 170, 40), width=int(S(5)))
        d.ellipse((cx - S(13), cy - S(13), cx + S(13), cy + S(13)), fill=(245, 170, 40))
    elif kind == "lock":
        rr(d, (x + S(12), y + S(28), x + S(52), y + S(58)), int(S(6)), fill=OR)
        d.arc((x + S(18), y + S(8), x + S(46), y + S(40)), 180, 360, fill=OR, width=int(S(6)))
        d.line([(x + S(19), y + S(24)), (x + S(19), y + S(30))], fill=OR, width=int(S(6)))
        d.line([(x + S(45), y + S(24)), (x + S(45), y + S(30))], fill=OR, width=int(S(6)))

# ---------- components ----------
@lru_cache(None)
def node(kind, label, sub):
    s = 132
    im = Image.new("RGBA", (300, 250), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0 = (300 - s) // 2
    rr(d, (x0, 8, x0 + s, 8 + s), 32, fill=OR)                      # canto 3D
    rr(d, (x0, 0, x0 + s, s - 2), 32, fill=WHITE, outline=(243, 205, 195), width=3)
    icon(d, kind, x0 + 30, 30, 1.13)
    f1, f2 = BD(30), MD(21)
    d.text((150, s + 34), label, font=f1, fill=INK, anchor="mm")
    if sub: d.text((150, s + 68), sub, font=f2, fill=GREY, anchor="mm")
    return shadowed(im)
NODE_DY = 78  # desplazamiento: centro del tile -> centro del cuadrado

@lru_cache(None)
def badge():
    im = Image.new("RGBA", (52, 52), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 50, 50), fill=OR, outline=WHITE, width=4); check(d, 26, 27, 22, WHITE, 5)
    return im

def node_at(dst, kind, label, sub, cx, cy, t, t0, tcheck=None):
    """cx,cy = centro del cuadrado del nodo."""
    tile = node(kind, label, sub)
    pop(dst, tile, cx, cy + NODE_DY - 22, t, t0)
    if tcheck is not None and t >= tcheck:
        p = pr(t, tcheck, 0.35)
        paste(dst, badge(), cx + 62, cy - 62, 0.5 + 0.5 * eback(p), eo(p * 2))

@lru_cache(None)
def card(w, h, key, *args):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), 30, fill=WHITE, outline=(240, 226, 222), width=2)
    CARDS[key](im, d, w, h, *args)
    return shadowed(im, blur=20, dy=14, alpha=45)

def ticks(d, x, y, col=(110, 160, 220)):
    for o in (0, 9):
        d.line([(x + o, y + 6), (x + o + 5, y + 11), (x + o + 15, y)], fill=col, width=3)

def bubble(d, x, y, w, txt, mine=False, time=None, font=None):
    font = font or MD(31)
    lines = wrap(txt, font, w - 52)
    h = 34 + len(lines) * 42 + (26 if time else 0)
    rr(d, (x, y, x + w, y + h), 24, fill=OR_XL if mine else (241, 241, 243))
    for i, l in enumerate(lines):
        d.text((x + 26, y + 22 + i * 42), l, font=font, fill=INK)
    if time:
        tw = text_w(time, MD(20))
        d.text((x + w - 30 - tw - (26 if mine else 0), y + h - 34), time, font=MD(20), fill=GREY)
        if mine: ticks(d, x + w - 46, y + h - 30)
    return h

def head(d, x, y, name, status, letter="M", col=(236, 120, 150)):
    d.ellipse((x, y, x + 64, y + 64), fill=col)
    d.text((x + 32, y + 32), letter, font=BD(30), fill=WHITE, anchor="mm")
    d.text((x + 82, y + 4), name, font=BD(32), fill=INK)
    d.text((x + 82, y + 40), status, font=MD(22), fill=GREY)

CARDS = {}
def c_chat(im, d, w, h, state):
    head(d, 34, 30, C["nombre"], "en línea", C["nombre"][0], tuple(C.get("color", (236, 120, 150))))
    d.line([(0, 116), (w, 116)], fill=(240, 236, 234), width=2)
    y = 140
    if state >= 1:
        rr(d, (34, y, w - 34, y + 54), 16, fill=OR_XL)
        icon(d, "lock", 48, y + 12, 0.48)
        d.text((88, y + 27), H_["estado_cerrado"], font=SB(25), fill=OR, anchor="lm")
        y += 78
    bubble(d, 34, y, w - 140, H_["mensaje"], time=HM)
CARDS["chat"] = c_chat

def c_notif(im, d, w, h, titulo, detalle, nota, hora, grande):
    k = 1.0 if grande else 0.78
    s_ = int(76 * k)
    d.ellipse((26, 26, 26 + s_, 26 + s_), fill=OR)
    icon(d, "moon", 26 + s_ * 0.16, 26 + s_ * 0.16, s_ / 64 * 0.68)
    x = 26 + s_ + 22
    d.text((x, 24), "Agenda · " + hora, font=MD(int(22 * k + 2)), fill=GREY)
    d.text((x, 24 + 34 * k), titulo, font=XB(int(38 * k)), fill=INK)
    if detalle: d.text((x, 24 + 86 * k), detalle, font=SB(int(28 * k)), fill=OR)
    if nota: d.text((x, 24 + 128 * k), nota, font=MD(int(24 * k)), fill=GREY)
    d.ellipse((w - 72, 30, w - 28, 74), fill=GREEN); check(d, w - 50, 53, 20, WHITE, 5)
CARDS["notif"] = c_notif

def c_quote(im, d, w, h):
    d.text((30, 26), "Mensaje de " + C["nombre"].split()[0] + "  →  texto", font=SB(22), fill=GREY)
    for i, l in enumerate(wrap("«" + H_["mensaje"] + "»", MD(30), w - 60)):
        d.text((30, 66 + i * 40), l, font=MD(30), fill=INK)
CARDS["quote"] = c_quote

def c_recep(im, d, w, h):
    rr(d, (0, 0, w - 1, h - 1), 30, outline=OR, width=4)
    rr(d, (26, 24, 110, 108), 22, fill=OR_XL); icon(d, "robot", 36, 34, 1.0)
    d.text((132, 34), "Recepcionista IA", font=XB(40), fill=INK)
    d.text((132, 82), "Agente de IA · 24 h", font=MD(24), fill=GREY)
    d.ellipse((w - 76, h / 2 - 24, w - 28, h / 2 + 24), fill=OR); check(d, w - 52, h / 2 + 1, 22, WHITE, 5)
CARDS["recep"] = c_recep

def c_agenda(im, d, w, h):
    d.text((30, 24), "Agenda · mañana", font=SB(24), fill=GREY)
    rows = [(a, "Libre" if b else "Ocupado", b) for a, b in H_["agenda"]]
    for i, (hh, st, free) in enumerate(rows):
        y = 62 + i * 62
        rr(d, (22, y, w - 22, y + 52), 14, fill=OR_XL if free else (246, 246, 247))
        d.text((44, y + 26), hh, font=BD(30), fill=INK if free else GREY, anchor="lm")
        d.ellipse((170, y + 20, 182, y + 32), fill=OR if free else LGREY)
        d.text((196, y + 26), st, font=SB(27), fill=OR if free else GREY, anchor="lm")
CARDS["agenda"] = c_agenda

def c_reply(im, d, w, h, sel):
    hb = bubble(d, 24, 24, w - 48, H_["respuesta"], mine=True, time=HM, font=MD(29))
    for i, hh in enumerate(H_["huecos"][:2]):
        y = 24 + hb + 18 + i * 76
        on = sel and i == 0
        rr(d, (24, y, w - 24, y + 62), 16, fill=OR if on else WHITE, outline=OR, width=3)
        d.text((w / 2, y + 31), hh, font=BD(30), fill=WHITE if on else OR, anchor="mm")
CARDS["reply"] = c_reply

def c_side(im, d, w, h, title, sub):
    rr(d, (18, 22, 58, 62), 10, fill=OR_XL); check(d, 38, 43, 20, OR, 4)
    d.text((74, 22), title, font=BD(26), fill=INK)
    d.text((74, 56), sub, font=MD(20), fill=GREY)
CARDS["side"] = c_side

def c_summary(im, d, w, h, n):
    rr(d, (26, 24, 82, 80), 16, fill=OR_XL); icon(d, "robot", 32, 30, 0.7)
    d.text((100, 26), "Recepcionista IA", font=BD(28), fill=INK)
    d.text((100, 60), "para " + H_["empresa"], font=MD(21), fill=GREY)
    for i, l in enumerate(wrap(H_["resumen_intro"], MD(28), w - 60)):
        d.text((30, 112 + i * 38), l, font=MD(28), fill=INK)
    rows = [tuple(r) for r in H_["resumen"]]
    for i in range(n):
        hh, nm, tag, urg = rows[i]
        y = 200 + i * 70
        rr(d, (22, y, w - 22, y + 58), 14, fill=(248, 247, 247))
        d.text((44, y + 29), hh, font=BD(28), fill=INK, anchor="lm")
        d.text((150, y + 29), nm, font=MD(28), fill=INK, anchor="lm")
        tw = text_w(tag, SB(21)) + 30
        rr(d, (w - 40 - tw, y + 13, w - 40, y + 45), 16, fill=OR_L if urg else (236, 236, 240))
        d.text((w - 40 - tw / 2, y + 29), tag, font=SB(21), fill=OR if urg else GREY, anchor="mm")
    d.text((w - 30, h - 34), "08:00", font=MD(20), fill=GREY, anchor="ra")
CARDS["summary"] = c_summary

def c_remind(im, d, w, h, conf):
    hb = bubble(d, 24, 24, w - 48, H_["recordatorio"], mine=True, time=H_["huecos"][0], font=MD(29))
    y = 24 + hb + 18
    rr(d, (24, y, w - 24, y + 62), 16, fill=OR if conf else WHITE, outline=OR, width=3)
    d.text((w / 2, y + 31), "Confirmar ✓" if False else "Confirmar", font=BD(30), fill=WHITE if conf else OR, anchor="mm")
CARDS["remind"] = c_remind

def c_reject(im, d, w, h):
    bubble(d, 24, 24, w - 48, H_["rechazo"], time=H_["hora_rechazo"])
CARDS["reject"] = c_reject

def c_steps(im, d, w, h, active):
    names = [("PASO 1", "Escucha"), ("PASO 2", "Entiende"), ("PASO 3", "Responde"), ("PASO 4", "Avisa")]
    bw = (w - 60 - 3 * 14) / 4
    for i, (a, b) in enumerate(names):
        x = 30 + i * (bw + 14)
        on = i < active
        rr(d, (x, 26, x + bw, h - 26), 18, fill=OR_XL if on else (247, 246, 246), outline=OR if on else (232, 228, 228), width=3)
        d.text((x + bw / 2, h / 2 - 18), a, font=BD(20), fill=OR if on else GREY, anchor="mm")
        d.text((x + bw / 2, h / 2 + 16), b, font=BD(26), fill=INK if on else GREY, anchor="mm")
CARDS["steps"] = c_steps

# ---------- connectors ----------
def bez(p0, p3, vertical=False, n=60):
    (x0, y0), (x3, y3) = p0, p3
    if vertical: c1, c2 = (x0, y0 + (y3 - y0) * 0.55), (x3, y3 - (y3 - y0) * 0.55)
    else: c1, c2 = (x0 + (x3 - x0) * 0.5, y0), (x3 - (x3 - x0) * 0.5, y3)
    pts = []
    for i in range(n + 1):
        u = i / n
        x = (1 - u) ** 3 * x0 + 3 * (1 - u) ** 2 * u * c1[0] + 3 * (1 - u) * u * u * c2[0] + u ** 3 * x3
        y = (1 - u) ** 3 * y0 + 3 * (1 - u) ** 2 * u * c1[1] + 3 * (1 - u) * u * u * c2[1] + u ** 3 * y3
        pts.append((x, y))
    return pts

def link(d, p0, p1, prog, t_show=1.0, vertical=False):
    if t_show <= 0: return
    pts = bez(p0, p1, vertical)
    d.line(pts, fill=(230, 222, 220), width=5, joint="curve")
    if prog > 0:
        k = max(2, int(len(pts) * prog))
        d.line(pts[:k], fill=OR, width=6, joint="curve")
        x, y = pts[k - 1]; d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=OR)

# ---------- background ----------
def make_bg():
    bg = Image.new("RGBA", (W, H), WHITE)
    px = bg.load()
    for y in range(H):
        g = y / H
        c = (int(252 - 3 * g), int(249 - 8 * g), int(247 - 8 * g))
        for x in range(W): px[x, y] = c + (255,)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse((-200, 700, W + 200, 1500), fill=(250, 214, 200, 110))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    bg.alpha_composite(glow)
    d = ImageDraw.Draw(bg)
    for y in range(600, 1420, 34):
        for x in range(20, W, 34):
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(232, 210, 204))
    return bg
BG = make_bg()

# ---------- title & pills ----------
TITLE = [(l, bool(a)) for l, a in H_["titulo"]]
@lru_cache(None)
def title_tile(size):
    f = BLK(size); lh = int(size * 1.02)
    im = Image.new("RGBA", (W, lh * 3 + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, acc) in enumerate(TITLE):
        d.text((W / 2, 20 + lh * i + lh / 2), l, font=f, fill=OR if acc else INK, anchor="mm")
    return im

def pill(content, h=60):
    """content: list of (kind, value)"""
    parts, wsum = [], 22
    for kind, v in content:
        if kind == "tag": w_ = text_w(v, XB(22)) + 24
        elif kind == "txt": w_ = text_w(v, BD(28))
        elif kind == "icon": w_ = 34
        parts.append((kind, v, w_)); wsum += w_ + 12
    wsum += 10
    im = Image.new("RGBA", (wsum, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, wsum - 1, h - 1), h // 2, fill=WHITE, outline=(238, 228, 226), width=2)
    x = 22
    for kind, v, w_ in parts:
        if kind == "tag":
            rr(d, (x, 13, x + w_, h - 13), 8, fill=OR); d.text((x + w_ / 2, h / 2), v, font=XB(22), fill=WHITE, anchor="mm")
        elif kind == "txt": d.text((x, h / 2), v, font=BD(28), fill=INK, anchor="lm")
        elif kind == "icon": icon(d, v, x, h / 2 - 15, 0.48)
        x += w_ + 12
    return shadowed(im, blur=10, dy=5, alpha=35)

def fmt_clock(sec):
    sec = int(sec) % 86400
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"

# ---------- captions ----------
def build_chunks():
    chunks = []
    for li, l in enumerate(LINES):
        words = l["text"].split()
        tot = sum(len(w_) + 1 for w_ in words)
        t, wt = l["start"], []
        dur = l["end"] - l["start"]
        for w_ in words:
            dd = dur * (len(w_) + 1) / tot; wt.append((w_, t, t + dd)); t += dd
        cur = []
        for item in wt:
            if cur and (len(cur) >= 3 or len(" ".join(x[0] for x in cur + [item])) > 20):
                chunks.append(cur); cur = []
            cur.append(item)
        if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        s = c[0][1]; e = c[-1][2]
        nxt = chunks[i + 1][0][1] if i + 1 < len(chunks) else e + 1.2
        out.append((s, min(nxt, e + 0.7), c))
    return out
CHUNKS = build_chunks()

def draw_caption(img, t):
    for s, e, c in CHUNKS:
        if s <= t < e: break
    else: return
    f = XB(52)
    words = [w_ for w_, _, _ in c]
    widths = [text_w(w_, f) for w_ in words]
    sp = 16; tw = sum(widths) + sp * (len(words) - 1)
    bw, bh = tw + 56, 92
    im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, bw - 1, bh - 1), 16, fill=WHITE)
    x = 28
    for (w_, ws, we), ww in zip(c, widths):
        col = OR if ws <= t < we + 0.05 or (t >= we and w_.isupper() and len(w_) > 2) else INK
        d.text((x, bh / 2 + 2), w_, font=f, fill=col, anchor="lm"); x += ww + sp
    tile = shadowed(im, blur=12, dy=6, alpha=40)
    p = pr(t, s, 0.18)
    paste(img, tile, W / 2, 1440, 0.9 + 0.1 * eback(p), 1.0)

# ---------- scenes ----------
PY = 600  # origen vertical del panel
SC = ["g0", "s1", "s2", "s3", "p1", "p2", "p2b", "p3", "p3b", "p4", "p4b", "fin", "cta"]
SC = [x for x in SC if x == "s1" or any(l["scene"] == x for l in LINES)]  # escenas opcionales
STARTS = {s: (0.0 if i == 0 else first(s) - 0.35) for i, s in enumerate(SC)}  # la primera escena empieza en 0
ORDER = sorted(SC, key=lambda s: STARTS[s])
def scene_range(s):
    i = ORDER.index(s)
    return STARTS[s], (STARTS[ORDER[i + 1]] if i + 1 < len(ORDER) else TOTAL)

# Escenas que comparten lienzo (no hay transición entre ellas)
GROUP = {"g0": "Z", "s1": "A", "s2": "A", "s3": "B", "p1": "C", "p2": "D", "p2b": "D", "p3": "E", "p3b": "E", "p4": "F", "p4b": "G", "fin": "H", "cta": "I"}

def sc_Z(L, t):
    """Gancho 'resultado primero': la cita ya está agendada antes de contar la historia."""
    g = H_.get("gancho", {})
    p = pr(t, 0.05, 0.5)
    shake = math.sin(t * 38) * 10 * (1 - p) if t < 0.6 else 0
    tile = card(860, 250, "notif", g.get("titulo", "Nueva cita agendada"), g.get("detalle", ""), g.get("nota", ""), g.get("hora", H_["hora_mensaje"]), True)
    paste(L, tile, W / 2 + shake, 120 + (1 - eo(p)) * -160 + 80, 0.9 + 0.1 * eback(p), eo(min(1, p * 2)))
    for i, ex in enumerate(g.get("extras", [])[:2]):
        t0 = 0.55 + 0.4 * i
        tt = card(760, 200, "notif", ex[0], ex[1], "", ex[2], False)
        pop(L, tt, W / 2, 430 + i * 190, t, t0)

def sc_A(L, t):
    t2 = first("s2")
    state = 1 if t >= t2 + 0.2 else 0
    a = 1.0
    t4 = sl("s2", 1)
    if t > t4 + 0.4: a = 1 - 0.55 * eo(pr(t, t4 + 0.4, 0.8))
    pop(L, card(760, 330 if state == 0 else 408, "chat", state), 470, 290 if state == 0 else 330, t, 0.5, base_alpha=a)
    if t > t4 + 1.6:
        pop(L, card(700, 150, "reject"), 500, 650, t, t4 + 1.6)

def sc_B(L, t):
    t0 = first("s3")
    pop(L, card(760, 140, "recep"), 500, 200, t, t0 + 0.4)
    pop(L, card(900, 170, "steps", 0), 520, 420, t, t0 + 1.1)

def sc_C(L, t):
    t0 = first("p1")
    d = ImageDraw.Draw(L)
    a, b = (230, 160), (760, 160)
    link(d, (a[0] + 70, a[1]), (b[0] - 70, b[1]), eio(pr(t, t0 + 0.8, 1.0)))
    node_at(L, "chat", "Mensaje nuevo", "WhatsApp · web", *a, t, t0 + 0.1, t0 + 0.6)
    node_at(L, "wave", "Lee o transcribe", "texto y audios", *b, t, t0 + 1.4, t0 + 2.2)
    pop(L, card(760, 230, "quote"), 500, 520, t, t0 + 2.3)

def sc_D(L, t):
    t0 = first("p2"); tb = first("p2b")
    d = ImageDraw.Draw(L)
    cx = 500
    kids = [(220, "spark", "Cerebro IA", "entiende"), (500, "folder", "Memoria", "historial"), (780, "cal", "Agenda", "calendario")]
    for i, (x, *_r) in enumerate(kids):
        link(d, (cx + (x - cx) * 0.3, 190), (x, 330), eio(pr(t, t0 + 0.7 + 0.25 * i, 0.6)), vertical=True)
    pop(L, card(760, 140, "recep"), cx, 130, t, t0)
    for i, (x, k, l, s) in enumerate(kids):
        tc = (t0 + 1.5) if i < 2 else (tb + 0.3)
        node_at(L, k, l, s, x, 330 + 50, t, t0 + 0.9 + 0.25 * i, tc)
    # etiqueta urgente
    tu = t0 + 1.9
    if t >= tu:
        pop(L, pill([("icon", "lock"), ("txt", "Urgente: fuga de agua")]) if False else urgent_tag(), cx + 190, 40, t, tu)
    if t >= tb:
        pop(L, card(520, 270, "agenda"), 560, 668, t, tb + 0.15)

@lru_cache(None)
def urgent_tag():
    f = BD(24); txt = H_["etiqueta"]; w_ = text_w(txt, f) + 70
    im = Image.new("RGBA", (w_, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w_ - 1, 47), 24, fill=WHITE, outline=OR, width=3)
    d.rectangle((20, 16, 30, 32), fill=OR)
    d.text((44, 24), txt, font=f, fill=OR, anchor="lm")
    return shadowed(im, blur=8, dy=4, alpha=35)

def sc_E(L, t):
    t0 = first("p3"); tb = first("p3b"); tc = sl("p3b", 1)
    d = ImageDraw.Draw(L)
    src = (230, 110)
    outs = [(760, y_, *a) for y_, a in zip((60, 320, 580), H_["acciones"])]
    tl = [tc + 0.3, tc + 1.4, tc + 2.6]
    for i, (x, y, *_r) in enumerate(outs):
        link(d, (src[0] + 72, src[1]), (x - 72, y), eio(pr(t, tl[i] - 0.6, 0.6)), t_show=pr(t, t0 + 0.6, 0.3))
    node_at(L, "chat", "Responde", "WhatsApp", *src, t, t0, t0 + 0.5)
    sel = t >= tb + 0.5
    _lines = len(wrap(H_["respuesta"], MD(29), 460 - 48 - 52))
    _h = 24 + (34 + _lines * 42 + 26) + 18 + 2 * 76 + 10
    pop(L, card(460, _h, "reply", sel), src[0] + 20, 280 + _h / 2, t, t0 + 0.4)
    for i, (x, y, k, l, s, ct, cs) in enumerate(outs):
        node_at(L, k, l, ct if t >= tl[i] + 0.15 else s, x, y, t, t0 + 0.8 + 0.15 * i, tl[i])

def sc_F(L, t):
    t0 = first("p4")
    d = ImageDraw.Draw(L)
    a, b = (230, 110), (760, 110)
    link(d, (a[0] + 72, a[1]), (b[0] - 72, b[1]), eio(pr(t, t0 + 0.6, 0.7)))
    node_at(L, "alarm", "Cada mañana", "08:00", *a, t, t0, t0 + 0.5)
    node_at(L, "chat", "Resumen", "al dueño", *b, t, t0 + 1.0, t0 + 1.5)
    t2 = sl("p4", 1)
    n = 0 if t < t2 - 0.2 else 1 if t < t2 + 0.5 else 2 if t < t2 + 1.0 else 3
    pop(L, card(800, 420, "summary", n), 500, 560, t, t0 + 1.5)

def sc_G(L, t):
    t0 = first("p4b")
    d = ImageDraw.Draw(L)
    a = (500, 110)
    node_at(L, "bell", "Recordatorios", "24 h antes", *a, t, t0, t0 + 0.5)
    link(d, (a[0], a[1] + 150), (a[0], 330), eio(pr(t, t0 + 0.4, 0.5)), vertical=True)
    conf = t >= t0 + 2.3
    pop(L, card(620, 300, "remind", conf), 500, 500, t, t0 + 0.8)

def sc_H(L, t):
    t0 = first("fin")
    k = clamp((t - t0 + 0.2) / 0.9)
    pop(L, card(760, 140, "recep"), 500, 200, t, t0 - 0.3)
    pop(L, card(900, 170, "steps", min(4, int(k * 4.99))), 520, 420, t, t0 - 0.2)

def sc_I(L, t):
    t0 = first("cta")
    pass  # se dibuja en draw_cta (usa todo el lienzo)

SCN = {"Z": sc_Z, "A": sc_A, "B": sc_B, "C": sc_C, "D": sc_D, "E": sc_E, "F": sc_F, "G": sc_G, "H": sc_H, "I": sc_I}
GSTART = {}
for s in ORDER:
    g = GROUP[s]; GSTART.setdefault(g, STARTS[s])
GORDER = sorted(GSTART, key=lambda g: GSTART[g])

def group_at(t):
    cur = GORDER[0]
    for g in GORDER:
        if t >= GSTART[g]: cur = g
    return cur

PANEL_H = 820
TR = 0.35
def draw_panel(img, t):
    g = group_at(t)
    i = GORDER.index(g)
    gs = GSTART[g]
    layers = []
    if t - gs < TR and i > 0:
        p = eio((t - gs) / TR)
        layers.append((GORDER[i - 1], -220 * p, 1 - p))
        layers.append((g, 220 * (1 - p), p))
    else:
        layers.append((g, 0, 1))
    for gg, ox, a in layers:
        if gg == "I": continue
        L = Image.new("RGBA", (W, PANEL_H), (0, 0, 0, 0))
        SCN[gg](L, t)
        paste(img, L, W / 2 + ox, PY + PANEL_H / 2, 1.0, a)

@lru_cache(None)
def comment_box(txt):
    w_, h = 820, 92
    im = Image.new("RGBA", (w_, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w_ - 1, h - 1), 46, fill=WHITE, outline=OR if txt else (232, 228, 228), width=4 if txt else 2)
    d.ellipse((26, 26, 66, 66), fill=(250, 210, 90))
    if txt: d.text((88, h / 2), txt, font=BD(34), fill=INK, anchor="lm")
    else: d.text((88, h / 2), "Añade un comentario…", font=MD(30), fill=GREY, anchor="lm")
    d.text((w_ - 36, h / 2), "Publicar", font=BD(28), fill=(60, 140, 240), anchor="rm")
    return shadowed(im, blur=14, dy=6, alpha=40)

@lru_cache(None)
def cta_title():
    f = XB(62)
    a, b, c = "¿Quieres esta ", "recepcionista", "?"
    im = Image.new("RGBA", (W, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tw = text_w(a + b + c, f); x = (W - tw) / 2
    d.text((x, 50), a, font=f, fill=INK, anchor="lm"); x += text_w(a, f) + 14
    d.text((x, 50), b, font=f, fill=OR, anchor="lm"); x += text_w(b, f) + 4
    d.text((x, 50), c, font=f, fill=INK, anchor="lm")
    return im

@lru_cache(None)
def brand():
    im = Image.new("RGBA", (W, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = BLK(54); tw = text_w(AGENCIA, f)
    x = (W - tw - 70) / 2
    d.ellipse((x, 52, x + 50, 102), fill=OR); icon(d, "moon", x + 9, 61, 0.5)
    d.text((x + 70, 77), AGENCIA, font=f, fill=INK, anchor="lm")
    d.text((W / 2, 135), "Recepcionistas con IA para negocios locales", font=MD(28), fill=GREY, anchor="mm")
    return im

def draw_cta(img, t):
    t0 = STARTS["cta"]
    if t < t0: return
    tl = first("cta")
    pop(img, cta_title(), W / 2, 690, t, t0 + 0.1)
    word = H_["cta_palabra"]
    kt = tl + 1.9
    n = 0 if t < kt else min(len(word), int((t - kt) / 0.07) + 1)
    pop(img, comment_box(word[:n]), W / 2, 830, t, t0 + 0.3)
    if t >= kt + 0.9:
        pop(img, sub_note(), W / 2, 930, t, kt + 0.9)
    tb_ = min(tl + 3.6, LINES[-1]["end"] + 0.2)
    if t >= tb_:
        pop(img, brand(), W / 2, 1140, t, tb_)

@lru_cache(None)
def sub_note():
    im = Image.new("RGBA", (W, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((W / 2, 30), "y te enseñamos una demo con tu negocio", font=SB(30), fill=GREY, anchor="mm")
    return im

# ---------- header ----------
_T0 = hm_sec(HM); _IC = "moon" if (_T0 >= 20 * 3600 or _T0 < 7 * 3600) else "sun"
CLOCK = {"s1": (_T0, _IC), "s3": (_T0 + 3, _IC), "p1": (_T0 + 4, _IC),
         "p2": (_T0 + 9, _IC), "p2b": (_T0 + 14, _IC), "p3": (_T0 + 19, _IC),
         "p3b": (_T0 + 26, _IC), "p4": (8 * 3600, "sun"), "p4b": (8 * 3600 + 30, "sun")}
PASO = {"p1": ("PASO 1", "Escucha"), "p2": ("PASO 2", "Entiende"), "p2b": ("PASO 2", "Entiende"),
        "p3": ("PASO 3", "Responde"), "p3b": ("PASO 3", "Responde"), "p4": ("PASO 4", "Avisa"), "p4b": ("PASO 4", "Avisa")}

def scene_at(t):
    cur = ORDER[0]
    for s in ORDER:
        if t >= STARTS[s]: cur = s
    return cur

def clock_value(t):
    s = scene_at(t)
    if s == "s2":
        # avance rápido de la noche: 22:00 -> 07:58
        a = sl("s2", 1); e = a + 1.6
        base = _T0 + 6 + (t - STARTS["s2"])
        if t < a: return base, _IC
        p = eio(pr(t, a, e - a))
        target = hm_sec(H_["hora_rechazo"]) + (86400 if hm_sec(H_["hora_rechazo"]) < _T0 else 0)
        return base + p * (target - _T0 - 6), (_IC if p < 0.8 else "sun")
    v, ic = CLOCK.get(s, (None, None))
    if v is None: return None, None
    return v + (t - STARTS[s]), ic

def draw_header(img, t):
    # título: grande al principio, luego pequeño
    p = eio(pr(t, 1.7, 0.6))
    size_big, size_small = 84, 62
    if t >= STARTS["cta"]:
        a = 1 - eo(pr(t, STARTS["cta"], 0.4))
    else: a = 1
    if a <= 0: return
    if p <= 0: paste(img, title_tile(size_big), W / 2, 420, 1, a)
    elif p >= 1: paste(img, title_tile(size_small), W / 2, 335, 1, a)
    else:
        tile = title_tile(size_big); sc = (size_big + (size_small - size_big) * p) / size_big
        paste(img, tile, W / 2, 420 + (335 - 420) * p, sc, a)
    if p < 1: return
    pa = eo(pr(t, 2.3, 0.4)) * a
    s = scene_at(t)
    items = []
    if s in PASO: items.append(pill([("tag", PASO[s][0]), ("txt", PASO[s][1])]))
    if s == "fin":
        items = [pill([("icon", "alarm"), ("txt", H_.get("pie", "Todo en menos de 1 minuto"))])]
    else:
        v, ic = clock_value(t)
        if v is not None: items.append(pill([("icon", ic), ("txt", fmt_clock(v))]))
    if not items: return
    gap = 16; tw = sum(i.width - 40 for i in items) + gap * (len(items) - 1)
    x = W / 2 - tw / 2
    for it in items:
        paste(img, it, x + (it.width - 40) / 2, 515, 1, pa); x += it.width - 40 + gap

def frame(t):
    img = BG.copy()
    draw_panel(img, t)
    draw_cta(img, t)
    draw_header(img, t)
    draw_caption(img, t)
    return img.convert("RGB")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "preview":
        ts = [float(x) for x in sys.argv[2].split(",")]
        for t in ts: frame(t).save(os.path.join(WORK, f"prev_{t:05.1f}.jpg"), quality=85)
    else:
        a, b = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (0, TOTAL)
        out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(WORK, "video.mp4")
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                              "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        n0, n1 = int(a * FPS), int(b * FPS)
        for n in range(n0, n1):
            p.stdin.write(frame(n / FPS).tobytes())
        p.stdin.close(); p.wait()
