# 4 more repurposed videos (V5-V8) with aesthetic fonts, auto-placed subtitles that
# move to empty space (avoid face + product), and a different loud hook sound each.
# Usage: python3 aesthetic.py [v5 v6 ...] [--no-footage]
#   -> ../style-edit-gummy-aesthetic/v5..v8/
import os, sys, math, shutil, subprocess, json
import numpy as np, cv2
from variants import O, HERE

OUT = os.path.join(HERE, "..", "style-edit-gummy-aesthetic")
FONTS = os.path.join(HERE, "assets", "fonts")
SAFE_R = 140      # TikTok right-side buttons
SAFE_B = 420      # TikTok caption / bottom UI
SAFE_T = 150      # TikTok top tabs

# ---------- per-video config ----------
V = {
 "v5": dict(  # Playfair Display italic, blur-in, white + hairline
   hook=[(41.6, 44.3)],
   main=[(0.0, 25.2), (28.5, 41.5), (44.3, 69.6), (85.0, 113.6)],
   style="playfair", hook_sfx="hk_drop", tr_sfx="tr_swish", trans="flash",
   lines=[("reaction jujur", "PlayfairI", 400, 34), ("Ya Allah,", "PlayfairI", 700, 92),
          ("sedapnya!", "PlayfairI", 700, 92), ("Turkish Gummies · masam manis", "Playfair", 500, 28)]),
 "v6": dict(  # Cormorant Garamond italic, cream, word-by-word
   hook=[(28.5, 33.1)],
   main=[(3.45, 28.4), (33.1, 69.6), (85.0, 113.6)],
   style="cormorant", hook_sfx="hk_braam", tr_sfx="tr_chime", trans="blur",
   lines=[("Bentuk Gigi", "CormorantI", 700, 104), ("pun ada?!", "CormorantI", 600, 80),
          ("✦  TURKISH GUMMIES  ✦", "Cormorant", 600, 28)]),
 "v7": dict(  # Fraunces in soft dark glass pill
   hook=[(63.05, 68.8)],
   main=[(0.0, 25.2), (28.5, 63.0), (85.0, 113.6)],
   style="fraunces", hook_sfx="hk_scratch", tr_sfx="tr_tape", trans="whip",
   lines=[("Bekal Wajib", "Fraunces", 650, 78), ("Masa Travel", "FrauncesI", 600, 78),
          ("1KG · puas makan ramai-ramai", "Fraunces", 500, 30)]),
 "v8": dict(  # Josefin Sans uppercase tracking-in + Parisienne script accent
   hook=[(105.3, 107.1), (110.8, 111.65)],
   main=[(3.45, 69.6), (77.0, 83.2), (85.0, 105.2), (107.1, 110.8), (111.9, 113.6)],
   style="josefin", hook_sfx="hk_flash", tr_sfx="tr_zap", trans="warm",
   lines=[("jujur,", "Parisienne", 400, 110), ("SANGAT RECOMMEND", "Josefin", 700, 54),
          ("BERBALOI SETIAP SEN", "Josefin", 500, 24)]),
}

FONT_FILES = {"Playfair": "Playfair.woff2", "PlayfairI": "PlayfairItalic.woff2",
              "Cormorant": "Cormorant.woff2", "CormorantI": "CormorantItalic.woff2",
              "Fraunces": "Fraunces.woff2", "FrauncesI": "FrauncesItalic.woff2",
              "Parisienne": "Parisienne.woff2", "Josefin": "JosefinSans.woff2"}

# subtitle look per style: font key, weight, size, char-width factor (for box estimate), box width
SUB = {
 "playfair": dict(font="PlayfairI", w=600, fs=46, cw=0.47, W=470),
 "cormorant": dict(font="CormorantI", w=600, fs=56, cw=0.40, W=470),
 "fraunces": dict(font="Fraunces", w=600, fs=36, cw=0.62, W=480),
 "josefin": dict(font="Josefin", w=600, fs=30, cw=0.88, W=470),
}
# manual placements (verified on snapshots) for the tight close-up shots
PIN = {"Ambil Yang Mix": ("L", 80, 190, 260)}
SFXVOL = {"sub_boom": 0.5, "swoosh": 0.3, "riser_shimmer": 0.4, "coin": 0.35, "ui_tap": 0.45}

def css(style):
    ff = "\n".join(f'@font-face{{font-family:"{k}";src:url("assets/{v}") format("woff2");font-weight:100 900;}}'
                   for k, v in FONT_FILES.items())
    s = SUB[style]
    base = f'''{ff}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
#fx{{position:absolute;inset:0;opacity:0;z-index:4;pointer-events:none;}}
.sub{{position:absolute;z-index:5;}}
.sub .tx{{display:inline-block;font-family:"{s['font']}",serif;font-weight:{s['w']};font-size:{s['fs']}px;line-height:1.18;color:#fff;
  text-shadow:0 2px 14px rgba(0,0,0,.6),0 0 3px rgba(0,0,0,.45);opacity:0;text-wrap:balance;}}
.sub .tx.nw{{white-space:nowrap;}}
.sub.L{{text-align:left;}} .sub.C{{text-align:center;}} .sub.R{{text-align:right;}}
#hook{{position:absolute;left:70px;right:{SAFE_R}px;text-align:center;z-index:6;color:#fff;
  text-shadow:0 3px 18px rgba(0,0,0,.6),0 0 3px rgba(0,0,0,.45);}}
#hook .ln{{display:block;opacity:0;line-height:1.1;}}
#hook .ln.sm{{margin-top:16px;}}
'''
    extra = {
     "playfair": '''.sub .tx{letter-spacing:-0.01em;}
.sub .ul{display:block;height:2px;width:70px;background:#fff;margin-top:12px;transform:scaleX(0);box-shadow:0 1px 4px rgba(0,0,0,.3);}
.sub.L .ul{transform-origin:0 50%;} .sub.R .ul{margin-left:auto;transform-origin:100% 50%;} .sub.C .ul{margin:12px auto 0;}
''',
     "cormorant": '''.sub .tx{color:#FFF4E2;}
.sub .tx .w{display:inline-block;opacity:0;}
.sub .sp{display:block;font-family:"Cormorant";font-size:26px;color:#FFF4E2;opacity:0;margin-bottom:2px;letter-spacing:.3em;}
''',
     "fraunces": '''.sub .tx{background:rgba(28,22,22,.38);padding:14px 26px 16px;border-radius:28px;color:#fff;text-shadow:none;
  box-shadow:0 6px 24px rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.22);}
#hook .ln:nth-child(3){background:rgba(28,22,22,.38);display:inline-block;padding:10px 24px;border-radius:28px;margin-top:18px;text-shadow:none;}
''',
     "josefin": '''.sub .tx{text-transform:uppercase;letter-spacing:.12em;}
.sub .ln2{display:block;height:1px;width:100%;background:rgba(255,255,255,.85);margin-top:10px;transform:scaleX(0);}
.sub.L .ln2{transform-origin:0 50%;} .sub.R .ln2{transform-origin:100% 50%;}
#hook .ln:nth-child(2){letter-spacing:.08em;} #hook .ln:nth-child(3){letter-spacing:.32em;}
#hook .ln:nth-child(2){margin-top:8px;}
''',
    }[style]
    return base + extra

# ---------- footage ----------
def build_footage(segs, out):
    fc = []
    for i, (a, b) in enumerate(segs):
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];"
                  f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03[a{i}];")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(HERE, "assets", "footage.mp4"),
                    "-filter_complex", "".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "15",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out], check=True)

def remap_range(s, e, segs, off):
    acc = off
    for a, b in segs:
        if a <= s < b:
            ne = min(e, b)
            return acc + (s - a), acc + (ne - a)
        acc += b - a
    return None

# ---------- auto placement ----------
CASC = [cv2.CascadeClassifier(cv2.data.haarcascades + f) for f in
        ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml")]
SC = 4  # analysis downscale

class Scene:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.last_face = None; self.last_t = -99
    def masks(self, t):
        self.cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = self.cap.read()
        if not ok: return None
        sm = cv2.resize(fr, (1080 // SC, 1920 // SC))
        g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        faces = [r for c in CASC for r in c.detectMultiScale(g, 1.08, 4, minSize=(20, 20))]
        head = np.zeros(g.shape, np.uint8)
        if len(faces):
            f = max(faces, key=lambda r: r[2] * r[3]); self.last_face = f; self.last_t = t
        elif abs(t - self.last_t) < 6:
            f = self.last_face
        else:
            f = None
        if f is not None:
            x, y, w, h = f
            mx, mt = (.12, .25) if w * SC > 450 else (.35, .45)   # big close-up face: tighter margin
            cv2.rectangle(head, (int(x - mx * w), int(y - mt * h)), (int(x + (1 + mx) * w), int(y + 1.5 * h)), 1, -1)
        else:  # unknown: assume a head somewhere centre-top
            cv2.rectangle(head, (60, 60), (210, 240), 1, -1)
        hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
        raw = ((hsv[..., 1] > 150) & (hsv[..., 2] > 150)).astype(np.uint8)
        raw = cv2.morphologyEx(raw, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        prod = cv2.dilate(raw, np.ones((9, 9), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(prod)
        pm = np.zeros_like(prod)
        for i in range(1, n):  # expand significant gummy blobs to cover the container
            x, y, w, h, a = st[i]
            if raw[lab == i].sum() > 120:
                cv2.rectangle(pm, (int(x - .3 * w), int(y - .4 * h)), (int(x + 1.3 * w), int(y + 1.25 * h)), 1, -1)
        edges = cv2.Canny(g, 60, 140) / 255.0
        return head, pm, edges

def best_box(scene, times, W, H, prev=None, hook=False, alts=()):
    ms = [m for m in (scene.masks(t) for t in times) if m is not None]
    head = np.maximum.reduce([m[0] for m in ms]); prod = np.maximum.reduce([m[1] for m in ms])
    edges = np.mean([m[2] for m in ms], 0)
    opts = [(W, H)] + list(alts)
    best = None; allc = []
    for W, H in opts:
      narrow = 8 if W != opts[0][0] else 0   # small cost for the narrower (more wrapped) box
      if hook:
          cols = [("C", (1080 - W) // 2)]
      else:  # fine horizontal steps; alignment follows which side the box sits on
          xs = list(range(80, 1080 - SAFE_R - W + 1, 40)) + [1080 - SAFE_R - W]
          cols = []
          for x in xs:
              cx = x + W / 2
              cols.append(("L" if cx < 430 else "R" if cx > 610 else "C", x))
      for col, x in cols:
        for y in range(SAFE_T + 20, 1920 - SAFE_B - H, 40):
            a, b, c, d = y // SC, (y + H) // SC, x // SC, (x + W) // SC
            area = max(1, (b - a) * (d - c))
            sh = head[a:b, c:d].sum() / area; sp = prod[a:b, c:d].sum() / area
            se = edges[a:b, c:d].mean()
            s = 1000 * sh + 900 * sp + 40 * se + 60 * (y / 1920) + narrow
            if prev and abs(x - prev[2]) < 60 and abs(y - prev[1]) < 60: s += 9          # move around when there is room
            if prev and col == prev[0]: s += 3
            cand = (s, col, x, y, sh, sp, W); allc.append(cand)
            if best is None or s < best[0]: best = cand
    if not hook and best[5] > 0.05:   # still on the product: accept a little hijab-edge overlap instead
        clean = [c for c in allc if c[5] < 0.02 and c[4] < 0.65]
        if clean: best = min(clean, key=lambda c: (c[4], c[0]))
    return best

# ---------- html ----------
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

def build(name, cfg):
    d = os.path.join(OUT, name)
    os.makedirs(os.path.join(d, "assets"), exist_ok=True)
    for v in FONT_FILES.values(): shutil.copy(os.path.join(FONTS, v), os.path.join(d, "assets", v))
    if os.path.exists(os.path.join(d, "sfx")): shutil.rmtree(os.path.join(d, "sfx"))
    shutil.copytree(os.path.join(HERE, "sfx"), os.path.join(d, "sfx"))
    segs = cfg["hook"] + cfg["main"]
    H = round(sum(b - a for a, b in cfg["hook"]), 3)
    DUR = round(sum(b - a for a, b in segs), 2)
    foot = os.path.join(d, "assets", "footage.mp4")
    if "--no-footage" not in sys.argv or not os.path.exists(foot): build_footage(segs, foot)
    scene = Scene(foot)
    st, S = cfg["style"], SUB[cfg["style"]]

    # hook placement
    hl = cfg["lines"]
    hh = int(sum(sz * 1.05 for _, _, _, sz in hl) + 30)
    hb = best_box(scene, [0.3, H / 2, max(0.3, H - 0.3)], 900, hh, hook=True)
    hook_top = hb[3]
    spans = "".join(f'<span class="ln{" sm" if sz < 40 else ""}" id="h{i}" style="font-family:\'{f}\';font-weight:{w};font-size:{sz}px">{esc(tx)}</span>'
                    for i, (tx, f, w, sz) in enumerate(hl))
    hook_html = f'<div id="hook" class="clip" style="top:{hook_top}px" data-start="0" data-duration="{H}">{spans}</div>'

    hj = [f'tl.set("#cam",{{scale:1}},0);']
    for i in range(len(hl)):
        t0 = 0.06 + i * 0.22
        if st == "playfair":
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,y:30,filter:"blur(14px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.55,ease:"power3.out"}},{t0:.2f});')
        elif st == "cormorant":
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,scale:1.25,letterSpacing:"0.12em"}},{{opacity:1,scale:1,letterSpacing:"0em",duration:.7,ease:"expo.out"}},{t0:.2f});')
        elif st == "fraunces":
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,y:-50,rotation:{-4 if i%2 else 4}}},{{opacity:1,y:0,rotation:0,duration:.5,ease:"back.out(2.2)"}},{t0:.2f});')
        else:
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,clipPath:"inset(0 100% 0 0)",x:-20}},{{opacity:1,clipPath:"inset(0 0% 0 0)",x:0,duration:.6,ease:"power4.out"}},{t0:.2f});')
    hj.append(f'tl.to("#hook",{{y:-14,duration:{max(.5,H-0.6):.2f},ease:"sine.inOut"}},0.5);')
    hj.append(f'tl.to("#hook .ln",{{opacity:0,duration:.22,ease:"power2.in"}},{H-0.24:.2f});')
    # hook camera: hard punch on the hit, slow push
    hj.append('tl.fromTo("#cam",{scale:1.16},{scale:1.04,duration:.5,ease:"power4.out"},0);')
    hj.append(f'tl.to("#cam",{{scale:1.09,duration:{max(.3,H-0.6):.2f},ease:"sine.inOut"}},0.5);')
    hj.append(f'tl.set("#cam",{{scale:1.0}},{H});')
    tr = cfg["trans"]
    if tr == "flash":
        hj += [f'tl.set("#fx",{{background:"#fff",opacity:.7}},{H});', f'tl.to("#fx",{{opacity:0,duration:.3,ease:"power2.out"}},{H});']
    elif tr == "warm":
        hj += [f'tl.set("#fx",{{background:"#ffe6c2",opacity:.75}},{H});', f'tl.to("#fx",{{opacity:0,duration:.45,ease:"power2.out"}},{H});']
    elif tr == "blur":
        hj += [f'tl.fromTo("#cam",{{filter:"blur(18px)"}},{{filter:"blur(0px)",duration:.45,ease:"power2.out",immediateRender:false}},{H});']
    else:  # whip
        hj += [f'tl.fromTo("#cam",{{scale:1.3,rotation:-3}},{{scale:1,rotation:0,duration:.4,ease:"expo.out",immediateRender:false}},{H});']

    ov, au, js = [], [], []
    k = 0; prev = None; placements = []
    for s, e, t, side, sfx, z, *rest in O:
        r = remap_range(s, e, cfg["main"], H)
        if r is None or r[1] - r[0] < 0.6: continue
        ns, ne = round(r[0], 2), round(r[1], 2)
        if ns < H + 0.35: ns = round(H + 0.35, 2)
        if ne - ns < 0.6: continue
        plain = t.replace('<span style="white-space:nowrap">', "").replace("</span>", "")
        def hgt(Wd):
            lines = max(1, math.ceil(len(plain) * S["fs"] * S["cw"] / Wd))
            return int(lines * S["fs"] * 1.2 + (70 if st == "fraunces" else 34))
        if st == "fraunces" and len(plain) <= 22:   # pill: keep on one line, box = pill size
            pw = min(S["W"], int(len(plain) * S["fs"] * S["cw"] + 64))
            b = best_box(scene, [ns + 0.1, (ns + ne) / 2, ne - 0.1], pw, int(S["fs"] * 1.2 + 70), prev)
        else:
            b = best_box(scene, [ns + 0.1, (ns + ne) / 2, ne - 0.1], S["W"], hgt(S["W"]), prev, alts=[(340, hgt(340)), (260, hgt(260))])
        if plain in PIN:   # checked by eye: auto spot was too close to the product
            col, x, y, BW = PIN[plain]; b = (0, col, x, y, 0.0, 0.0, BW)
        _, col, x, y, sh, sp, BW = b; prev = (col, y, x)
        pad = 52 if st == "fraunces" else 0
        nw = " nw" if (len(plain) * S["fs"] * S["cw"] + pad <= BW or (st == "fraunces" and len(plain) <= 22)) else ""
        placements.append(dict(t=ns, text=plain, col=col, x=x, y=y, head=round(float(sh), 3), prod=round(float(sp), 3)))
        if st == "cormorant":
            inner = "".join(f'<span class="w">{esc(wd)}</span> ' for wd in plain.split())
            body = f'<i class="sp">✦</i><span class="tx{nw}">{inner}</span>'
        elif st == "playfair":
            body = f'<span class="tx{nw}">{esc(plain)}</span><i class="ul"></i>'
        elif st == "josefin":
            body = f'<span class="tx{nw}">{esc(plain)}</span><i class="ln2"></i>'
        else:
            body = f'<span class="tx{nw}">{esc(plain)}</span>'
        ov.append(f'<div id="w{k}" class="clip sub {col}" style="left:{x}px;top:{y}px;width:{BW}px" data-start="{ns}" data-duration="{round(ne-ns,2)}">{body}</div>')
        au.append(f'<audio id="a{k}" src="sfx/{sfx}.wav" data-start="{max(0,ns-0.02):.2f}" data-duration="1.1" data-volume="{SFXVOL.get(sfx,0.45)}"></audio>')
        w = f"#w{k}"
        if st == "playfair":
            js += [f'tl.fromTo("{w} .tx",{{opacity:0,y:16,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"power3.out"}},{ns});',
                   f'tl.fromTo("{w} .ul",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"expo.out"}},{ns+0.12:.2f});',
                   f'tl.to("{w} .tx,{w} .ul",{{opacity:0,y:-8,filter:"blur(6px)",duration:.22,ease:"power2.in"}},{ne-0.24:.2f});']
        elif st == "cormorant":
            js += [f'tl.set("{w} .tx",{{opacity:1}},{ns});',
                   f'tl.fromTo("{w} .sp",{{opacity:0,rotation:-90,scale:.4}},{{opacity:1,rotation:0,scale:1,duration:.4,ease:"back.out(2)"}},{ns});',
                   f'tl.fromTo("{w} .w",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.35,stagger:.07,ease:"power2.out"}},{ns+0.05:.2f});',
                   f'tl.to("{w} .tx,{w} .sp",{{opacity:0,duration:.22,ease:"power2.in"}},{ne-0.24:.2f});']
        elif st == "fraunces":
            js += [f'tl.fromTo("{w} .tx",{{opacity:0,scale:.82,y:10}},{{opacity:1,scale:1,y:0,duration:.42,ease:"back.out(1.8)"}},{ns});',
                   f'tl.to("{w} .tx",{{opacity:0,scale:.94,duration:.2,ease:"power2.in"}},{ne-0.22:.2f});']
        else:
            js += [f'tl.fromTo("{w} .tx",{{opacity:0,letterSpacing:"0.45em"}},{{opacity:1,letterSpacing:"0.12em",duration:.6,ease:"power3.out"}},{ns});',
                   f'tl.fromTo("{w} .ln2",{{scaleX:0}},{{scaleX:1,duration:.55,ease:"expo.out"}},{ns+0.1:.2f});',
                   f'tl.to("{w} .tx,{w} .ln2",{{opacity:0,duration:.2,ease:"power2.in"}},{ne-0.22:.2f});']
        js.append(f'tl.fromTo("{w}",{{y:0}},{{y:-10,duration:{round(ne-ns,2)},ease:"sine.inOut"}},{ns});')  # gentle float
        if z == "punch":
            js.append(f'tl.fromTo("#cam",{{scale:1.09}},{{scale:1.02,duration:.45,ease:"power3.out",immediateRender:false}},{ns});')
        elif z == "in":
            js.append(f'tl.to("#cam",{{scale:1.06,duration:{round(ne-ns,2)},ease:"sine.inOut"}},{ns});')
        else:
            js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(ne-ns,2)},ease:"sine.inOut"}},{ns});')
        k += 1

    audio = [f'<audio id="ah" src="sfx/{cfg["hook_sfx"]}.wav" data-start="0" data-duration="2.0" data-volume="0.9"></audio>',
             f'<audio id="at" src="sfx/{cfg["tr_sfx"]}.wav" data-start="{max(0,H-0.12):.2f}" data-duration="0.8" data-volume="0.55"></audio>'] + au
    html = f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
{css(st)}</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="fx"></div>
  {hook_html}
{chr(10).join("  " + x for x in ov)}
{chr(10).join("  " + x for x in audio)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
{chr(10).join(hj)}
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
    open(os.path.join(d, "index.html"), "w").write(html)
    json.dump(dict(hook_top=hook_top, hook_score=[round(float(v), 3) for v in (hb[4], hb[5])], subs=placements),
              open(os.path.join(d, "placements.json"), "w"), ensure_ascii=False, indent=1)
    bad = [p for p in placements if p["head"] > 0.02 or p["prod"] > 0.02]
    print(name, "dur", DUR, "hook", H, "hook_top", hook_top, "subs", k, "cols",
          {c: sum(p["col"] == c for p in placements) for c in "LCR"}, "overlap_warn", len(bad))

if __name__ == "__main__":
    names = [x for x in sys.argv[1:] if not x.startswith("--")] or list(V)
    for n in names: build(n, V[n])
