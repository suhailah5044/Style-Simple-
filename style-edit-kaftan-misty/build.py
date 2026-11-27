# Style Edit — "Misty" (Kaftan / Baju Tidur Zebra)
# [start, end, text, side, top_px, motion, sfx]
#   side: L / R (jarak dari tepi = EDGE px) ; motion: mist / slide / bloom / spread (4 jenis sahaja)
EDGE = 110
O = [
 [3.0, 5.7, "Loose &amp; Relaxed<br>Cutting", "L", 430, "mist",   "mist_whoosh"],
 [5.8, 8.7, "Motif Memang Onz!",          "L", 400, "slide",  "bubble_pop"],
 [8.8, 11.4,"Comfy Vibes Only!",          "L", 540, "bloom",  "soft_chime"],
 [11.6,14.5,"Comfy Untuk Tidur!",         "L", 440, "mist",   "mist_whoosh"],
 [17.2,20.1,"Cantik &amp; Stylish!",      "L", 440, "spread", "sparkle"],
 [26.5,30.3,"Short Sleeve Design",        "L", 390, "slide",  "bubble_pop"],
 [30.4,33.4,"Long Dress Style",           "L", 450, "mist",   "mist_whoosh"],
 [39.1,42.6,"Perfect For<br>Homewear!",      "L", 560, "bloom",  "soft_chime"],
 [42.7,46.0,"Zebra Wave<br>Pattern 🖤",  "L", 350, "spread", "sparkle"],
 [46.1,50.1,"Selesa Untuk<br>Daily Wear",    "R", 520, "slide",  "bubble_pop"],
 [53.5,56.3,"Banyak Design<br>Pilihan",      "R", 470, "mist",   "mist_whoosh"],
 [56.4,58.2,"Floral Pattern 🌸",          "R", 560, "bloom",  "soft_chime"],
 [58.3,61.5,"Leopard Print 🤎",           "L", 500, "slide",  "bubble_pop"],
 [61.6,66.5,"Simple But Stylish!",        "R", 360, "spread", "sparkle"],
 [68.2,72.6,"Size S, M &amp; L",          "R", 430, "mist",   "soft_chime"],
]
VOL = {"mist_whoosh":0.22, "bubble_pop":0.28, "soft_chime":0.18, "sparkle":0.16, "airy_swell":0.22}
DUR = 81.9

IN = {
 "mist":   ('{opacity:0,y:18,filter:"blur(14px)"}', '{opacity:1,y:0,filter:"blur(0px)",duration:0.7,ease:"power2.out"}'),
 "slide":  ('{opacity:0,x:"__DX__",filter:"blur(6px)"}', '{opacity:1,x:0,filter:"blur(0px)",duration:0.65,ease:"power3.out"}'),
 "bloom":  ('{opacity:0,scale:0.88,filter:"blur(10px)"}', '{opacity:1,scale:1,filter:"blur(0px)",duration:0.7,ease:"back.out(1.4)"}'),
 "spread": ('{opacity:0,letterSpacing:"0.18em",filter:"blur(8px)"}', '{opacity:1,letterSpacing:"0.01em",filter:"blur(0px)",duration:0.8,ease:"power2.out"}'),
}

ov, au, js = [], [], []
zoom_in = True
for i, (s, e, t, side, top, mo, sfx) in enumerate(O):
    pos = f"left:{EDGE}px" if side == "L" else f"right:{EDGE}px"
    ov.append(f'<div id="w{i}" class="clip card-wrap {side}" style="top:{top}px;{pos}" data-start="{s}" data-duration="{round(e-s,2)}">'
              f'<div class="card"><i class="gem"></i><span class="tx">{t}</span></div></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.05):.2f}" data-duration="1.2" data-volume="{VOL[sfx]}"></audio>')
    a, b = IN[mo]
    dx = "-40" if side == "L" else "40"
    js.append(f'tl.fromTo("#w{i} .card",{a.replace(chr(34)+"__DX__"+chr(34), dx)},{b},{s});')
    js.append(f'tl.fromTo("#w{i} .gem",{{opacity:0,scale:0,rotate:-45}},{{opacity:1,scale:1,rotate:0,duration:0.5,ease:"back.out(2)"}},{s+0.3:.2f});')
    # gerak halus semasa teks dipapar (mengapung perlahan)
    js.append(f'tl.to("#w{i} .card",{{y:"-=6",duration:{round(e-s-0.9,2)},ease:"sine.inOut"}},{s+0.7:.2f});')
    js.append(f'tl.to("#w{i} .card",{{opacity:0,filter:"blur(10px)",y:"-=8",duration:0.3,ease:"power1.in"}},{e-0.32:.2f});')
    # kamera: zum lembut silih ganti setiap tukar babak
    target = 1.045 if zoom_in else 1.0
    js.append(f'tl.to("#cam",{{scale:{target},duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    zoom_in = not zoom_in

html = f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Cormorant";src:url("assets/Cormorant-600i.woff2") format("woff2");font-style:italic;font-weight:600;}}
@font-face{{font-family:"Montserrat";src:url("assets/Montserrat-500.woff2") format("woff2");font-weight:500;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 42%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.card-wrap{{position:absolute;z-index:5;}}
.card-wrap.R .tx{{text-align:right;}}
.card{{position:relative;display:inline-block;padding:16px 26px 17px;border-radius:24px;opacity:0;
  background:linear-gradient(135deg,rgba(255,255,255,.26),rgba(120,90,130,.22) 60%,rgba(70,45,80,.30));
  border:1.5px solid rgba(255,255,255,.55);
  backdrop-filter:blur(14px) saturate(1.15);-webkit-backdrop-filter:blur(14px) saturate(1.15);
  box-shadow:0 10px 30px rgba(40,20,50,.18), inset 0 1px 0 rgba(255,255,255,.5);}}
.card .tx{{font-family:"Montserrat","Noto Color Emoji",sans-serif;font-weight:500;font-size:36px;line-height:1.22;white-space:nowrap;letter-spacing:.01em;color:#fff;
  text-shadow:0 1px 3px rgba(40,20,50,.55),0 0 12px rgba(40,20,50,.35);text-align:left;display:inline-block;}}
.gem{{position:absolute;top:-11px;width:22px;height:22px;
  background:radial-gradient(circle at 35% 35%,#fff 0 30%,#ffe9f6 55%,rgba(255,255,255,0) 72%);
  clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%);
  filter:drop-shadow(0 0 6px rgba(255,255,255,.9));}}
.card-wrap.L .gem{{left:-9px;}} .card-wrap.R .gem{{right:-9px;}}
#hook{{position:absolute;top:500px;right:{EDGE}px;width:400px;text-align:right;z-index:6;}}
#hook .h{{display:block;font-family:"Cormorant",serif;font-style:italic;font-weight:600;font-size:76px;line-height:.98;color:#fff;
  text-shadow:0 0 18px rgba(255,255,255,.55),0 3px 14px rgba(60,30,70,.45);opacity:0;}}
#hook .h2{{font-size:62px;}}
#hook .rule{{display:block;margin:14px 0 0 auto;width:120px;height:2px;background:linear-gradient(90deg,rgba(255,255,255,0),#fff);transform:scaleX(0);transform-origin:100% 50%;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="hook" class="clip" data-start="0" data-duration="2.95"><span class="h h1">Floral Design,</span><span class="h h2">So Aesthetic!</span><i class="rule"></i></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_hook" src="sfx/airy_swell.wav" data-start="0.0" data-duration="1.4" data-volume="{VOL["airy_swell"]}"></audio>
  <audio id="a_hook2" src="sfx/sparkle.wav" data-start="0.75" data-duration="1.2" data-volume="0.14"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1.06}},0);
tl.to("#cam",{{scale:1.0,duration:2.9,ease:"sine.out"}},0);
tl.fromTo("#hook .h1",{{opacity:0,y:20,filter:"blur(14px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.8,ease:"power2.out"}},0.15);
tl.fromTo("#hook .h2",{{opacity:0,y:20,filter:"blur(14px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.8,ease:"power2.out"}},0.5);
tl.fromTo("#hook .rule",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power3.out"}},0.9);
tl.to("#hook .h,#hook .rule",{{opacity:0,filter:"blur(10px)",y:-8,duration:0.3,ease:"power1.in"}},2.6);
{chr(10).join(js)}
tl.to("#cam",{{scale:1.0,duration:2.5,ease:"sine.inOut"}},72.6);
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html", "w").write(html)
print("ok", len(O), "overlays")
