# Kemeja Cotton Umi — V1 (gaya tulisan "perfume": Lexend Mega 24px + sub 15px + bar kecil, hook pill kaca)
# Tenang & smooth: cut sikit, tiada zoom punch, animasi lembut satu-satu. Warna footage asal, tiada filter, tiada muzik.
import json, os, subprocess, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "src/raw.mov"
# segmen sumber (saat) — hook dulu, kemudian cerita berturutan (cut hanya bila buang ayat ulang / jeda panjang)
# Satu footage -> 5 video, setiap satu intro/hook lain. Guna: VARIANT=V2 python3 build.py <src.mov>
VARS = {
 "V1": ([(30.36, 32.30), (0.00, 24.15), (25.88, 28.55), (32.80, 34.70), (36.90, 46.36), (47.85, 51.15), (54.45, 58.58), (63.70, 65.50)],
        [["Didi", "Besar?"], ["Pun", "Muat!"]]),
 "V2": ([(42.40, 46.36), (0.00, 24.15), (25.88, 28.55), (32.80, 34.70), (36.90, 42.30), (47.85, 51.15), (54.45, 58.58), (63.70, 65.50)],
        [["Hitam", "Never"], ["Fails!"]]),
 "V3": ([(36.30, 38.10), (0.00, 24.15), (25.88, 28.55), (28.90, 32.30), (32.80, 34.70), (38.10, 46.36), (54.45, 58.58), (63.70, 65.50)],
        [["Cotton", "Tapi"], ["Tak", "Panas?"]]),
 "V4": ([(54.45, 58.58), (0.00, 24.15), (25.88, 28.55), (32.80, 34.70), (36.90, 46.36), (47.85, 51.15), (63.70, 65.50)],
        [["Kerja,", "OT,"], ["Holiday?"]]),
 "V5": ([(0.00, 24.15), (25.88, 28.55), (28.90, 32.30), (32.80, 34.70), (36.90, 46.36), (47.85, 51.15), (54.45, 58.58), (63.70, 65.50)],
        [["Siapa", "Tak", "Suka"], ["Kemeja", "Ni?"]]),
}
VN = os.environ.get("VARIANT", "V1"); SEG, HOOK = VARS[VN]
# overlay: [src mula, src tamat, TAJUK, sub]
OS = [
 [4.85, 8.30, "BAGGY GIRL ERA", "Kemeja Cotton Umi"],
 [10.96, 13.90, "COMFY FIT CHECK", "Loose, selesa & cantik"],
 [14.66, 16.30, "COTTON TOP 🤎", "Material cotton, tak panas"],
 [16.70, 20.30, "LOOSE BUT STILL CUTE", "Depan & belakang labuh"],
 [20.68, 24.10, "EASY OOTD", "Jeans atau skirt pun okay"],
 [25.92, 28.50, "HALF BUTTON DETAIL", "Butang separuh, berkolar"],
 [39.84, 42.20, "SIMPLE BUT CLASSY", "Lawa, cantik, selesa"],
 [43.10, 46.30, "BLACK TOP NEVER FAILS", "Senang nak match"],
 [47.88, 50.90, "ONE SIZE FIT", "Besar, kecil memang ngam"],
 [54.48, 58.50, "DAILY OUTFIT APPROVED", "Kerja • OT • Holiday"],
]
CUTS = []; t = 0
for s, e in SEG: CUTS.append((s, e, t)); t += e - s
DUR = round(t, 2)
def T(src):
    for s, e, o in CUTS:
        if s - 0.05 <= src <= e + 0.05: return round(o + max(0, src - s), 2)
    return None
O = []
for a, b, tx, sb in OS:
    s0, s1 = T(a), T(b)
    if s0 is None or s1 is None or s0 < 2.3: continue   # overlay dalam hook -> skip (hook pill dah cakap)
    O.append([s0, s1, tx, sb])
O.sort()

if not os.path.exists(f"assets/footage_{VN}.mp4") or "--recut" in sys.argv:
    f = []
    for i, (a, b) in enumerate(SEG):
        d = b - a
        f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=0.015,afade=t=out:st={d-0.02:.3f}:d=0.02[a{i}]")
    n = len(SEG)
    fc = ";".join(f) + ";" + "".join(f"[v{i}][a{i}]" for i in range(n)) + \
         f"concat=n={n}:v=1:a=1[cv][ca];[cv]scale=1080:1920:flags=lanczos,setsar=1[ov]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[ov]", "-map", "[ca]",
                    "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", f"assets/footage_{VN}.mp4"], check=True)

ov = []; au = []; js = []
for i, (s, e, tx, sb) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word" data-start="{s}" data-duration="{round(e-s,2)}">'
              f'<div class="tx">{tx}</div><div class="sb">{sb}</div><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/pop.wav" data-start="{max(0,s-0.02):.2f}" data-duration="0.6" data-volume="0.22"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .sb",{{opacity:0,y:6}},{{opacity:.92,y:0,duration:0.5,ease:"power2.out"}},{s+0.12:.2f});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{s+0.2:.2f});')
    js.append(f'tl.to("#w{i}",{{opacity:0,duration:0.3,ease:"power1.in"}},{e-0.3:.2f});')

hook_html = "".join('<div class="hl">' + "".join(f'<span class="hw">{w}</span>' for w in L) + "</div>" for L in HOOK)
html = f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
@font-face{{font-family:"Noto Color Emoji";src:url("assets/NotoColorEmoji.ttf") format("truetype");}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
/* gaya perfume: kiri atas (ruang dinding kosong atas kepala), dalam safe zone TikTok/Reels */
.word{{position:absolute;top:255px;left:100px;width:620px;z-index:5;}}
.word .tx{{font-family:"Lexend Mega","Noto Color Emoji",sans-serif;font-weight:600;font-size:24px;line-height:1.3;letter-spacing:-0.04em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5);opacity:0;}}
.word .sb{{font-family:"Lexend Mega",sans-serif;font-weight:400;font-size:15px;line-height:1.3;letter-spacing:-0.03em;color:#fff;margin-top:6px;
  text-shadow:0 2px 6px rgba(0,0,0,.5);opacity:0;}}
.word .bar{{display:block;height:3px;width:46px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.4);transform:scaleX(0);transform-origin:0 50%;}}
/* hook pill kaca kanan atas (macam perfume / luggage) */
#hook{{position:absolute;top:255px;right:150px;z-index:6;padding:14px 28px 16px;border-radius:34px;text-align:right;
  background:rgba(10,14,24,.34);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1.5px solid rgba(255,255,255,.35);
  transform-origin:100% 0;opacity:0;}}
#hook .hl{{font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:26px;line-height:1.35;letter-spacing:-0.05em;color:#fff;white-space:nowrap;}}
#hook .hw{{display:inline-block;margin-left:10px;opacity:0;text-shadow:0 2px 6px rgba(0,0,0,.35);}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage_{VN}.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="hook" class="clip" data-start="0" data-duration="2.1">{hook_html}</div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_hook" src="sfx/hook.wav" data-start="0.25" data-duration="1.2" data-volume="0.4"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1.05}},0);
tl.to("#cam",{{scale:1.0,duration:1.9,ease:"sine.out"}},0);
tl.fromTo("#hook",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.8)"}},0.3);
tl.fromTo("#hook .hw",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.35,ease:"expo.out",stagger:0.12}},0.42);
tl.to("#hook",{{opacity:0,y:-10,duration:0.22,ease:"power2.in"}},1.82);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html", "w").write(html)
print("DUR", DUR)
for o in O: print(f"{o[0]:6.2f}-{o[1]:6.2f} {o[2]}")
