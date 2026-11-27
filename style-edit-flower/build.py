# Style Misty (Lexend Mega subtitle UI) — Flower Bracelet
# [start, end, text, pos, sfx, zoom]   pos = (align L|R|C, x-from-edge px, top px)
O=[
 [4.0,7.4,"Pretty Flower<br>Design 🌸",("R",150,520),"ui_notif","in"],
 [7.5,11.0,"Sparkling<br>Crystal Details",("L",150,1600),"glass_ting","punch"],
 [11.05,14.4,"Premium Gift<br>Box Included",("L",150,1240),"ui_confirm","out"],
 [17.46,20.0,"Elegant<br>Gold Finish",("L",150,560),"riser_shimmer","in"],
 [23.2,27.6,"Classy &amp;<br>Timeless Look",("R",150,1500),"sub_boom","punch"],
 [30.8,34.4,"Easy To Match<br>Any Outfit",("R",150,1520),"ui_blip","out"],
 [45.3,48.7,"Perfect For<br>Daily Wear",("L",150,1320),"ui_tap","in"],
 [48.82,50.9,"Adjustable<br>Length",("R",150,1380),"swoosh","out"],
 [50.95,53.6,"16CM + 5CM<br>Extension",("R",150,1580),"coin","punch"],
 [59.66,66.3,"Sweet Gift<br>For Her 🎁",("R",140,1450),"riser_shimmer","in"],
]
HOOK=("Flower design,","so classy!",("R",130,340))
VOL={"sub_boom":0.5,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
DUR=66.4
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
  <audio id="a_cork" src="sfx/cork.wav" data-start="0.15" data-duration="1.0" data-volume="0.55"></audio>
  <audio id="a_t2" src="sfx/glass_ting.wav" data-start="0.6" data-duration="0.9" data-volume="0.3"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,scale:.6,y:10}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.6)"}},0.15);
tl.fromTo("#t2",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},0.6);
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:1.0,ease:"power3.out"}},0.15);
tl.to("#cam",{{scale:1.06,duration:2.2,ease:"sine.inOut"}},1.2);
tl.to("#title span",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},3.2);
tl.to("#cam",{{scale:1.0,duration:0.6,ease:"sine.inOut"}},3.4);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
