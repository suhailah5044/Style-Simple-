# Style Edit v3 — Flat Shoe
# [start, end, text, side, sfx, zoom]
O=[
 [3.42,5.3,"Design Bunga","R","prompt","out"],
 [5.36,6.8,"Simple Je","R","bubble","in"],
 [6.84,8.75,"Sangat Cantik","R","tingting","punch"],
 [8.8,10.15,"Pakai Daily","R","click","out"],
 [10.2,11.25,"Tak Pernah Bosan","R","pluck","in"],
 [11.3,13.15,"Dalam Sangat Lembut","R","prompt","out"],
 [13.2,14.6,"Selesa","R","bubble","in"],
 [14.64,15.5,"Sangat Comfy","R","tingting","punch"],
 [15.56,17.2,"Tapak Dia","L","click","out"],
 [17.24,18.55,"Anti Slip","L","success","punch"],
 [18.6,20.85,"Banyak Pilihan Warna","R","sparkle_up","in"],
 [20.9,22.35,"Macam Kakak Pakai","R","pluck","out"],
 [22.38,23.4,"Checkout Cepat!","R","prompt","punch"],
 [23.44,25.85,"Ramai Dah Beli","R","heartpop","in"],
]
VOL={"tingting":0.35,"sparkle_up":0.35,"success":0.4,"click":0.5,"air":0.3}
DUR=25.9
ov=[];au=[];js=[]
for i,(s,e,t,side,sfx,z) in enumerate(O):
    words="".join(f'<span class="w">{w}</span> ' for w in t.split())
    ov.append(f'<div id="w{i}" class="clip sub {side}" data-start="{s}" data-duration="{round(e-s,2)}"><i class="dot"></i><span class="tx">{words.strip()}</span></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.0" data-volume="{VOL.get(sfx,0.45)}"></audio>')
    # masuk: dot pop, kemudian setiap perkataan blur->jelas (stagger)
    js.append(f'tl.fromTo("#w{i} .dot",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(3)"}},{s});')
    js.append(f'tl.fromTo("#w{i} .w",{{opacity:0,filter:"blur(8px)",x:-6}},{{opacity:1,filter:"blur(0px)",x:0,duration:0.32,stagger:0.06,ease:"power2.out"}},{s+0.05:.2f});')
    # keluar: blur + fade
    js.append(f'tl.to("#w{i} .w,#w{i} .dot",{{opacity:0,filter:"blur(6px)",duration:0.2,ease:"power1.in"}},{e-0.22:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.09}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.07,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    else:
        js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Creato Display";src:url("assets/CreatoDisplay-Medium.otf") format("opentype");font-weight:500;}}
@font-face{{font-family:"Creato Display";src:url("assets/CreatoDisplay-Bold.otf") format("opentype");font-weight:700;}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.sub{{position:absolute;top:300px;width:300px;z-index:5;display:flex;align-items:flex-start;gap:12px;}}
.sub.L{{left:64px;}}
.sub.R{{right:64px;flex-direction:row-reverse;text-align:right;}}
.sub .dot{{flex:none;width:8px;height:8px;margin-top:10px;border-radius:50%;background:#fff;box-shadow:0 0 6px rgba(0,0,0,.35);opacity:0;}}
.sub .tx{{font-family:"Lexend Mega",sans-serif;font-weight:500;font-size:24px;line-height:1.35;letter-spacing:-0.04em;color:#fff;
  text-shadow:0 1px 5px rgba(0,0,0,.7),0 0 2px rgba(0,0,0,.5);}}
.sub .w{{display:inline-block;opacity:0;}}
#title{{position:absolute;top:290px;left:64px;z-index:6;color:#fff;font-family:"Creato Display",sans-serif;
  text-shadow:0 2px 8px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);}}
#title .l1{{display:block;font-weight:500;font-size:40px;line-height:1.1;letter-spacing:.01em;opacity:0;}}
#title .l2{{display:block;font-weight:700;font-size:50px;line-height:1.05;letter-spacing:-.01em;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.35"><span class="l1">Flat shoe</span><span class="l2">paling selesa</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_cork" src="sfx/cork.wav" data-start="0.12" data-duration="1.0" data-volume="0.55"></audio>
  <audio id="a_air" src="sfx/air.wav" data-start="0.5" data-duration="0.5" data-volume="0.25"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#title .l1",{{opacity:0,scale:.5,transformOrigin:"0% 50%"}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.8)"}},0.12);
tl.fromTo("#title .l2",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.45,ease:"expo.out"}},0.5);
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:0.9,ease:"power3.out"}},0.12);
tl.to("#cam",{{scale:1.06,duration:2.2,ease:"sine.inOut"}},1.1);
tl.to("#title .l1,#title .l2",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},3.1);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
