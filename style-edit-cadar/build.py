# Gaya Misty Brooch (versi lembut) untuk Cadar Floral.
# Guna: python3 build.py v1|v2  -> tulis index.html
import sys
V = sys.argv[1] if len(sys.argv) > 1 else "v1"
DUR = 50.73

# Teks hook (tengah, 0-3.4s)
HOOK = {"v1": ("Floral Design,", "So Aesthetic!"),
        "v2": ("Floral Design \U0001F33C", "")}[V]

# [mula, tamat, teks, posisi, sfx]
# posisi = "L|C|R:top_px" — ruang kosong dinding/langsir, tak tutup muka & produk,
# 330-620px dari atas (tak atas sangat), 150px dari tepi (tak tepi sangat). Bertukar-tukar supaya tak bosan.
O = {
 "v1": [
  [3.70, 6.85, "Premium Soft Fabric", "L:470", "soft_chime"],
  [6.95, 10.85, "Sejuk &amp; Lembut!", "L:380", "soft_tap"],
  [14.30, 19.70, "Tak Berbulu!", "L:560", "soft_chime"],
  [19.80, 23.15, "Warna Tak<br>Mudah Luntur", "L:400", "soft_tap"],
  [23.30, 27.85, "Getah 360°<br>Keliling", "R:300", "soft_chime"],
  [30.20, 34.60, "Machine Wash<br>Friendly", "L:430", "soft_tap"],
  [37.60, 41.50, "Fit Kemas,<br>Tak Mudah Tercabut", "L:600", "soft_chime"],
  [41.65, 45.05, "Easy Care,<br>Tahan Lama", "L:470", "soft_tap"],
  [45.15, 50.60, "Bilik Terus<br>Nampak Classy!", "C:410", "soft_sparkle"],
 ],
 "v2": [
  [6.95, 10.85, "Soft &amp; Cooling<br>Fabric", "L:380", "soft_chime"],
  [14.30, 19.70, "360° Elastic Fit", "L:560", "soft_tap"],
  [23.30, 27.85, "No Loose<br>Corners!", "R:300", "soft_chime"],
  [30.20, 34.60, "Easy Wash &amp; Care", "L:430", "soft_tap"],
  [37.60, 41.50, "Long Lasting<br>Colour", "L:600", "soft_chime"],
  [45.15, 50.60, "Sweet Dreams,<br>Comfy Nights ✨", "C:410", "soft_sparkle"],
 ],
}[V]

# Cut scene dalam footage -> motion lembut (4 jenis sahaja, bergilir)
CUTS = [6.90, 9.43, 10.93, 14.23, 23.23, 25.10, 27.93, 30.13, 37.60, 41.57, 45.13]
MOT = {
 "settle": "{scale:1.045,x:0,y:0}",
 "driftL": "{scale:1.04,x:20,y:0}",
 "rise":   "{scale:1.04,x:0,y:18}",
 "driftR": "{scale:1.04,x:-20,y:0}",
}
ORDER = ["settle", "driftL", "rise", "driftR"]
VOL = {"soft_chime": 0.18, "soft_tap": 0.2, "soft_sparkle": 0.16}

ov, au, js = [], [], []
for i, (s, e, tx, pos, sfx) in enumerate(O):
    side, top = pos.split(":")
    ov.append(f'<div id="w{i}" class="clip word {side}" style="top:{top}px" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{tx}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{s:.2f}" data-duration="1.3" data-volume="{VOL[sfx]}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.7,ease:"power2.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0,opacity:1}},{{scaleX:1,duration:0.7,ease:"power2.out"}},{s+0.15:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-6,duration:0.45,ease:"power1.in"}},{e-0.45:.2f});')

text_starts = [o[0] for o in O]
for k, c in enumerate(CUTS):
    m = ORDER[k % 4]
    js.append(f'tl.fromTo("#cam",{MOT[m]},{{scale:1,x:0,y:0,duration:1.2,ease:"power2.out",immediateRender:false}},{c});')
    if not any(abs(c - s) < 0.4 for s in text_starts):
        au.append(f'<audio id="c{k}" src="sfx/air_whoosh.wav" data-start="{max(0,c-0.25):.2f}" data-duration="0.8" data-volume="0.08"></audio>')

h1, h2 = HOOK
html = f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Noto Color Emoji";src:url("assets/NotoColorEmoji.ttf") format("truetype");}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.word{{position:absolute;width:460px;z-index:5;}}
.word.L{{left:150px;text-align:left;}}
.word.R{{right:150px;text-align:right;}}
.word.C{{left:310px;text-align:center;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega","Noto Color Emoji",sans-serif;font-weight:600;font-size:30px;line-height:1.35;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin-top:12px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}} .word.C .bar{{margin:12px auto 0;transform-origin:50% 50%;}}
#title{{position:absolute;top:420px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega","Noto Color Emoji",sans-serif;font-weight:600;font-size:34px;line-height:1.4;letter-spacing:-0.03em;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);}}
#title span{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.5"><span id="t1">{h1}</span><br><span id="t2">{h2}</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_hook" src="sfx/soft_bell.wav" data-start="0.2" data-duration="1.6" data-volume="0.18"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.fromTo("#cam",{{scale:1.06,x:0,y:0}},{{scale:1,x:0,y:0,duration:1.6,ease:"power2.out"}},0);
tl.fromTo("#t1",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.8,ease:"power2.out"}},0.2);
tl.fromTo("#t2",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.8,ease:"power2.out"}},0.55);
tl.to("#title span",{{opacity:0,y:-6,duration:0.45,ease:"power1.in"}},3.0);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html", "w").write(html)
print("built", V, len(O), "overlays")
