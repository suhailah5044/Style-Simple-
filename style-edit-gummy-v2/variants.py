# Generate 4 repurposed videos from the same footage.
# Each variant: a different "cold open" hook clip + a different hook text/layout,
# then the main footage (with some dead parts cut differently per variant).
# Usage: python3 variants.py  -> ../style-edit-gummy-variants/v1..v4/
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "style-edit-gummy-variants")
src = open(os.path.join(HERE, "build.py")).read()
O = eval(src[src.index("O=[") + 2: src.index("VOL=")])
VOL = {"sub_boom": 0.5, "swoosh": 0.3, "riser_shimmer": 0.4, "coin": 0.35, "ui_tap": 0.45}

# hook: (clip_start, clip_end) in the original footage, shown first
# main: list of (start, end) segments of original footage after the hook
V = {
 "v1": dict(
   hook=(55.76, 60.42),
   main=[(3.45, 69.6), (85.0, 113.6)],
   lines=[("Peminat Masam?", 34), ("Ni Wajib Try!", 54)],
   anim="pop", sfx="sub_boom", top=230),
 "v2": dict(
   hook=(96.5, 99.92),
   main=[(3.45, 25.2), (28.5, 69.6), (85.0, 113.6)],
   lines=[("1KG", 72), ("Gummy Halal", 42), ("lebih jimat,", 28), ("lebih berbaloi!", 28)],
   anim="slide", sfx="coin", top=110, align="left"),
 "v3": dict(
   hook=(51.6, 55.76),
   main=[(0.0, 69.6), (85.0, 113.6)],
   lines=[("Amaran!", 32), ("Sekali Makan,", 50), ("Confirm Ketagih", 50)],
   anim="stack", sfx="ui_notif", top=210),
 "v4": dict(
   hook=(20.85, 24.98),
   main=[(3.45, 25.2), (28.5, 69.6), (74.5, 83.2), (85.0, 113.6)],
   lines=[("Anak Suka Sangat!", 50), ("Turkish Gummies masam manis", 28)],
   anim="wipe", sfx="glass_ting", top=230),
}

CSS = '''@font-face{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}
html,body{margin:0;background:#000;}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}
#cam{position:absolute;inset:0;transform-origin:50% 45%;}
#cam video{width:100%;height:100%;object-fit:cover;display:block;}
#flash{position:absolute;inset:0;background:#fff;opacity:0;z-index:4;}
.word{position:absolute;top:240px;width:420px;z-index:5;}
.word.L{left:170px;text-align:left;}
.word.R{right:170px;text-align:right;}
.word .tx{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:800;font-size:34px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);opacity:0;}
.word .bar{display:block;height:4px;width:60px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}
.word.L .bar{transform-origin:0 50%;} .word.R .bar{margin-left:auto;transform-origin:100% 50%;}
#hook{position:absolute;left:60px;right:60px;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:800;
  letter-spacing:-0.03em;line-height:1.2;text-shadow:0 3px 10px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);}
#hook .ln{display:block;opacity:0;}
#hook .hbar{display:block;margin:14px auto 0;transform-origin:50% 50%;height:5px;width:90px;background:#fff;border-radius:3px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}
'''

def remap(t, segs, off):
    """original time -> new time (None if t is cut out)"""
    acc = off
    for a, b in segs:
        if a <= t <= b:
            return acc + (t - a)
        acc += b - a
    return None

def build(name, cfg):
    d = os.path.join(OUT, name)
    os.makedirs(os.path.join(d, "assets"), exist_ok=True)
    for f in ("LexendMega.woff2",):
        shutil.copy(os.path.join(HERE, "assets", f), os.path.join(d, "assets", f))
    if os.path.exists(os.path.join(d, "sfx")):
        shutil.rmtree(os.path.join(d, "sfx"))
    shutil.copytree(os.path.join(HERE, "sfx"), os.path.join(d, "sfx"))

    h0, h1 = cfg["hook"]; H = round(h1 - h0, 3)
    segs = [cfg["hook"]] + cfg["main"]
    DUR = round(sum(b - a for a, b in segs), 2)

    # footage: concat segments with tiny audio fades to avoid clicks
    if "--no-footage" not in sys.argv:
        fc = []
        for i, (a, b) in enumerate(segs):
            fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];"
                      f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03[a{i}];")
        fc.append("".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(HERE, "assets", "footage.mp4"),
                        "-filter_complex", "".join(fc), "-map", "[v]", "-map", "[a]",
                        "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        os.path.join(d, "assets", "footage.mp4")], check=True)

    ov, au, js = [], [], []
    # overlays from main footage, remapped (skip ones cut out or overlapping the hook clip)
    k = 0
    for s, e, t, side, sfx, z, *rest in O:
        ns, ne = remap(s, cfg["main"], H), remap(e, cfg["main"], H)
        if ns is None or ne is None or ne - ns < 0.6:
            continue
        ns, ne = round(ns, 2), round(ne, 2)
        st = f' style="top:{rest[0]}px"' if rest else ""
        ov.append(f'<div id="w{k}" class="clip word {side}"{st} data-start="{ns}" data-duration="{round(ne-ns,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
        au.append(f'<audio id="a{k}" src="sfx/{sfx}.wav" data-start="{max(0,ns-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.45)}"></audio>')
        js.append(f'tl.fromTo("#w{k} .tx",{{opacity:0,y:22}},{{opacity:1,y:0,duration:0.38,ease:"expo.out"}},{ns});')
        js.append(f'tl.fromTo("#w{k} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{ns+0.08:.2f});')
        js.append(f'tl.to("#w{k} .tx,#w{k} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{ne-0.22:.2f});')
        if z == "punch":
            js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{ns});')
        elif z == "in":
            js.append(f'tl.to("#cam",{{scale:1.07,duration:{round(ne-ns,2)},ease:"sine.inOut"}},{ns});')
        else:
            js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(ne-ns,2)},ease:"sine.inOut"}},{ns});')
        k += 1

    # hook text
    lines = "".join(f'<span class="ln" id="h{i}" style="font-size:{sz}px">{tx}</span>' for i, (tx, sz) in enumerate(cfg["lines"]))
    al = cfg.get("align", "center")
    pos = "left:80px;right:auto;text-align:left;" if al == "left" else ""
    hook_html = f'<div id="hook" class="clip" style="top:{cfg["top"]}px;{pos}" data-start="0" data-duration="{H}">{lines}<i class="hbar"{' style="margin-left:0;transform-origin:0 50%"' if al == "left" else ""}></i></div>'
    hj = []
    n = len(cfg["lines"])
    a = cfg["anim"]
    for i in range(n):
        t0 = 0.1 + i * 0.28
        if a == "pop":
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.42,ease:"back.out(2.8)"}},{t0:.2f});')
        elif a == "slide":
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"expo.out"}},{t0:.2f});')
        elif a == "stack":
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,x:{-60 if i%2 else 60}}},{{opacity:1,x:0,duration:.45,ease:"power4.out"}},{t0:.2f});')
        else:  # wipe
            hj.append(f'tl.fromTo("#h{i}",{{opacity:0,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,clipPath:"inset(0 0% 0 0)",duration:.55,ease:"power3.out"}},{t0:.2f});')
    hj.append(f'tl.fromTo("#hook .hbar",{{scaleX:0}},{{scaleX:1,duration:.45,ease:"expo.out"}},{0.1+n*0.28:.2f});')
    if a == "stack":
        hj.append(f'tl.fromTo("#h0",{{rotation:-3}},{{rotation:3,duration:.08,repeat:5,yoyo:true,ease:"none"}},0.4);')
        hj.append('tl.set("#h0",{rotation:0},0.9);')
    hj.append(f'tl.to("#hook .ln,#hook .hbar",{{opacity:0,y:-12,duration:.22,ease:"power2.in"}},{H-0.25:.2f});')
    # hook camera: punch in at start, slow push, then cut to main with flash + whoosh
    hj.append('tl.fromTo("#cam",{scale:1.12},{scale:1.03,duration:.6,ease:"power3.out"},0);')
    hj.append(f'tl.to("#cam",{{scale:1.08,duration:{H-0.7:.2f},ease:"sine.inOut"}},0.6);')
    hj.append(f'tl.set("#cam",{{scale:1.0}},{H});')
    hj.append(f'tl.set("#flash",{{opacity:.55}},{H});')
    hj.append(f'tl.to("#flash",{{opacity:0,duration:.25,ease:"power2.out"}},{H});')
    hook_audio = (f'<audio id="ah" src="sfx/{cfg["sfx"]}.wav" data-start="0.08" data-duration="1.1" data-volume="{VOL.get(cfg["sfx"],0.45)}"></audio>\n'
                  f'  <audio id="ac" src="sfx/swoosh.wav" data-start="{max(0,H-0.15):.2f}" data-duration="1.0" data-volume="0.3"></audio>')

    html = f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
{CSS}</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="flash"></div>
  {hook_html}
  {chr(10).join("  "+x for x in ov)}
  {hook_audio}
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
{chr(10).join(hj)}
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
    open(os.path.join(d, "index.html"), "w").write(html)
    print(name, "dur", DUR, "hook", H, "overlays", k)

if __name__ == "__main__":
    for name in (sys.argv[1:] and [x for x in sys.argv[1:] if not x.startswith("--")]) or V:
        build(name, V[name])
