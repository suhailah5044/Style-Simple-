# Style Misty (Lexend Mega subtitle UI) — Flower Bracelet
# [start, end, text, pos, sfx, zoom]   pos = (align L|R|C, x-from-edge px, top px)
O=[
 [3.4,5.3,"Classy &amp;<br>Timeless Look",("L",150,560),"sub_boom","punch"],
 [8.05,11.45,"Pretty Flower<br>Design 🌸",("R",150,520),"ui_notif","in"],
 [11.55,15.05,"Sparkling<br>Crystal Details",("L",150,1600),"glass_ting","punch"],
 [15.1,18.45,"Premium Gift<br>Box Included",("L",150,1240),"ui_confirm","out"],
 [21.51,24.05,"Elegant<br>Gold Finish",("L",150,560),"riser_shimmer","in"],
 [29.3,32.9,"Easy To Match<br>Any Outfit",("R",120,1520),"ui_blip","out"],
 [43.8,47.2,"Perfect For<br>Daily Wear",("L",150,1320),"ui_tap","in"],
 [47.32,49.4,"Adjustable<br>Length",("R",150,1380),"swoosh","out"],
 [49.45,52.1,"16CM + 5CM<br>Extension",("R",150,1580),"coin","punch"],
 [58.16,64.8,"Sweet Gift<br>For Her 🎁",("R",140,1450),"riser_shimmer","in"],
]
HOOK=("Nampak mahal,","harga murah je!",("R",150,1460))
VOL={"sub_boom":0.5,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
DUR=64.9
def css(p):
    a,x,y=p
    return f"top:{y}px;{'left' if a=='L' else 'right'}:{x}px;"
ov=[];au=[];js=[]
for i,(s,e,t,p,sfx,z) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word {p[0]}" style="{css(p)}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.45)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22}},{{opacity:1,y:0,duration:0.38,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.07,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    else:
        js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
h1,h2,hp=HOOK
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Noto Color Emoji";src:url("assets/NotoColorEmoji.ttf") format("truetype");}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.word{{position:absolute;width:440px;z-index:5;}}
.word.L{{text-align:left;}}
.word.R{{text-align:right;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega","Noto Color Emoji",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#title{{position:absolute;{css(hp)}width:460px;text-align:{'right' if hp[0]=='R' else 'left'};z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:34px;line-height:1.35;letter-spacing:-0.03em;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);}}
#title span{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.5"><span id="t1">{h1}</span><br><span id="t2">{h2}</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_in1" src="sfx/swoosh.wav" data-start="0.05" data-duration="1.0" data-volume="0.4"></audio>
  <audio id="a_in2" src="sfx/coin.wav" data-start="0.6" data-duration="1.0" data-volume="0.35"></audio>\n  <audio id="a_cut1" src="sfx/swoosh.wav" data-start="5.25" data-duration="1.0" data-volume="0.3"></audio>\n  <audio id="a_cut2" src="sfx/swoosh.wav" data-start="26.0" data-duration="1.0" data-volume="0.25"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.45,ease:"expo.out"}},0.1);
tl.fromTo("#t2",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2.6)"}},0.6);
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:1.0,ease:"power3.out"}},0.15);
tl.to("#cam",{{scale:1.06,duration:2.2,ease:"sine.inOut"}},1.2);
tl.to("#title span",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},3.2);
tl.to("#cam",{{scale:1.0,duration:0.6,ease:"sine.inOut"}},3.4);
{chr(10).join(js)}
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:0.5,ease:"power3.out"}},5.35);
tl.fromTo("#cam",{{scale:1.08}},{{scale:1.0,duration:0.5,ease:"power3.out"}},26.1);
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
