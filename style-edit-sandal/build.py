from cut import out_t
T=out_t
DUR=56.0
# Teks ciri: [src_time, tempoh, teks, sisi, sfx, zoom]  — kecil, putih, ruang kosong atas (tak tutup produk/tangan/baju)
O=[
 (17.25,2.0,"Soft &amp; Flexible","R","ui_blip","punch"),
 (85.05,2.6,"Budget Friendly","L","coin","punch"),
 (88.10,2.4,"Simple &amp; Stylish","R","glass_ting","in"),
 (106.05,2.2,"Lightweight Design","L","ui_notif","out"),
 (109.60,2.6,"Anti-Slip Sole","R","sub_boom","punch"),
 (112.70,3.5,"Waterproof","L","swoosh",None),
 (155.20,3.0,"Everyday Sandals","R","ui_tap","in"),
 (176.00,3.6,"Comfortable Fit","L","riser_shimmer",None),
 (196.80,3.0,"Easy to Clean","R","ui_confirm","punch"),
]
# B-roll fullscreen ~4s: [src_time_mula, tempoh, fail, offset_dalam_broll]
B=[(13.00,4.0,"broll1.mp4",0.3),(112.50,3.9,"broll2.mp4",0.8),(175.85,3.9,"broll2.mp4",8.5)]
HOOK=["Kalau","tak","best,","takkan","grab","3 pasang!"]
VOL={"sub_boom":0.45,"swoosh":0.3,"riser_shimmer":0.35,"coin":0.35,"ui_tap":0.4}
ov=[];au=[];js=[];br=[]
for i,(s0,d,t,side,sfx,z) in enumerate(O):
    s=T(s0); e=s+d
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{d}"><span class="tx">{t}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.4)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,scale:.7,y:14}},{{opacity:1,scale:1,y:0,duration:0.36,ease:"back.out(2.2)"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.09}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in": js.append(f'tl.to("#cam",{{scale:1.06,duration:{d},ease:"sine.inOut"}},{s});')
    elif z=="out": js.append(f'tl.to("#cam",{{scale:1.0,duration:{d},ease:"sine.inOut"}},{s});')
for j,(s0,d,f,off) in enumerate(B):
    s=T(s0)
    br.append(f'<video id="b{j}" class="broll" src="assets/{f}" data-start="{s}" data-duration="{d}" data-media-start="{off}" data-volume="0" muted></video>')
    js.append(f'tl.fromTo("#b{j}",{{opacity:0}},{{opacity:1,duration:0.35,ease:"sine.out"}},{s});')
    js.append(f'tl.fromTo("#b{j}",{{scale:1.0}},{{scale:1.05,duration:{d},ease:"none"}},{s});')
    js.append(f'tl.to("#b{j}",{{opacity:0,duration:0.35,ease:"sine.in"}},{s+d-0.35:.2f});')
hk="".join(f'<span class="k">{w}</span> ' for w in HOOK)
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:3;opacity:0;}}
.word{{position:absolute;top:250px;width:420px;z-index:5;}}
.word.L{{left:150px;text-align:left;}}
.word.R{{right:150px;text-align:right;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;}}
.word.L .tx{{transform-origin:0 100%;}} .word.R .tx{{transform-origin:100% 100%;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#hook{{position:absolute;top:230px;left:120px;right:120px;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:700;
  font-size:40px;line-height:1.35;letter-spacing:-0.04em;text-shadow:0 2px 8px rgba(0,0,0,.5);}}
#hook .k{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  {chr(10).join("  "+x for x in br)}
  <div id="hook" class="clip" data-start="0" data-duration="2.9">{hk}</div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_h" src="sfx/sub_boom.wav" data-start="0.05" data-duration="1.0" data-volume="0.4"></audio>
  <audio id="a_h2" src="sfx/coin.wav" data-start="2.05" data-duration="0.9" data-volume="0.3"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:0.5,ease:"power3.out"}},0.05);
'''+"\n".join(f'tl.fromTo("#hook .k:nth-child({k+1})",{{opacity:0,y:30,scale:1.4}},{{opacity:1,y:0,scale:1,duration:0.28,ease:"back.out(2.5)"}},{[0.05,0.3,0.5,0.95,1.5,2.0][k]});' for k in range(len(HOOK)))+f'''
tl.fromTo("#cam",{{scale:1.09}},{{scale:1.0,duration:0.4,ease:"power3.out"}},2.0);
tl.to("#hook .k",{{opacity:0,y:-12,duration:.22,stagger:.02,ease:"power2.in"}},2.62);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
