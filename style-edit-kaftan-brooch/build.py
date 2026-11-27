# Gaya Misty Brooch (sebijik edit Cadar) untuk Kaftan Zebra — video ke-2.
# Hook audio: harp_rise (lain dari video pertama yang guna airy_swell + sparkle).
DUR = 81.9
HOOK = ("Floral Design,", "So Aesthetic!")

# [mula, tamat, teks, "L|C|R:top_px", sfx]
# Ruang kosong (langsir/dinding), tak tutup muka & produk, 360-560px dari atas, 150px dari tepi.
O = [
 [3.00, 5.70, "Loose &amp; Relaxed<br>Cutting", "L:430", "soft_chime"],
 [5.80, 8.70, "Motif Memang<br>Onz!", "L:330", "soft_tap"],
 [8.80, 11.40, "Comfy Vibes<br>Only!", "L:540", "soft_chime"],
 [11.60, 14.50, "Comfy Untuk<br>Tidur!", "L:440", "soft_tap"],
 [17.20, 20.10, "Cantik &amp;<br>Stylish!", "L:440", "soft_chime"],
 [26.50, 30.30, "Short Sleeve<br>Design", "L:390", "soft_tap"],
 [30.50, 33.40, "Long Dress<br>Style", "L:450", "soft_chime"],
 [39.10, 42.60, "Perfect For<br>Homewear!", "L:560", "soft_tap"],
 [42.70, 46.00, "Zebra Wave<br>Pattern 🖤", "L:340", "soft_sparkle"],
 [46.10, 50.10, "Selesa Untuk<br>Daily Wear", "R:520", "soft_chime"],
 [53.50, 56.30, "Banyak Design<br>Pilihan", "R:470", "soft_tap"],
 [56.40, 58.20, "Floral Pattern 🌸", "R:560", "soft_sparkle"],
 [58.30, 61.50, "Leopard Print 🤎", "L:500", "soft_sparkle"],
 [61.60, 66.50, "Simple But<br>Stylish!", "R:360", "soft_chime"],
 [68.30, 72.60, "Size S, M &amp; L", "R:430", "soft_tap"],
]

# Cut scene dalam footage (ffmpeg scene detect) -> motion lembut, 4 jenis bergilir
CUTS = [2.93, 16.70, 30.47, 34.97, 63.70, 68.27]
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

# motion pada setiap cut scene + bila teks bertukar (tanpa cut berdekatan)
text_starts = [o[0] for o in O]
moments = sorted(set(CUTS + [s for s in text_starts if not any(abs(s - c) < 1.3 for c in CUTS)]))
for k, c in enumerate(moments):
    m = ORDER[k % 4]
    js.append(f'tl.fromTo("#cam",{MOT[m]},{{scale:1,x:0,y:0,duration:1.2,ease:"power2.out",immediateRender:false}},{c});')
    if c in CUTS and not any(abs(c - s) < 0.4 for s in text_starts):
        au.append(f'<audio id="c{k}" src="sfx/air_whoosh.wav" data-start="{max(0,c-0.25):.2f}" data-duration="0.8" data-volume="0.08"></audio>')

h1, h2 = HOOK
html = f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
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
#title .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin:12px auto 0;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="2.95"><span id="t1">{h1}</span><br><span id="t2">{h2}</span><i class="bar"></i></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_hook" src="sfx/harp_rise.wav" data-start="0.15" data-duration="2.0" data-volume="0.2"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.fromTo("#cam",{{scale:1.06,x:0,y:0}},{{scale:1,x:0,y:0,duration:1.6,ease:"power2.out"}},0);
tl.fromTo("#t1",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.8,ease:"power2.out"}},0.2);
tl.fromTo("#t2",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.8,ease:"power2.out"}},0.55);
tl.fromTo("#title .bar",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.out"}},0.8);
tl.to("#title span,#title .bar",{{opacity:0,y:-6,duration:0.45,ease:"power1.in"}},2.45);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html", "w").write(html)
print("built", len(O), "overlays,", len(moments), "motions")
