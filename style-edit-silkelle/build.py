# [start, end, text, side(L/R/C), top_px, sfx, zoom]  — masa ikut babak dalam cut.py
O=[
 [3.45,6.3,"SILKELLE<br>Creator Exclusive 3.0","R",250,"ui_notif","in"],
 [6.45,9.7,"3D Fit Cup","R",250,"ui_blip","punch"],
 [9.85,12.9,"W-Shaped<br>Upper Support","L",250,"ui_confirm","in"],
 [13.05,16.1,"Push Up &amp;<br>Natural Lift","L",250,"sub_boom","punch"],
 [16.25,19.5,"Wide Anti-Slip<br>Shoulder Strap","L",250,"swoosh","in"],
 [19.65,22.5,"Soft &amp; Breathable<br>Material","R",250,"glass_ting","out"],
 [22.65,25.9,"4 Rows<br>Hook &amp; Eye","R",250,"ui_tap","punch"],
 [26.05,28.9,"Lightweight<br>&amp; Comfy","R",250,"ui_blip","in"],
 [29.05,32.1,"Perfect For<br>Everyday Wear","C",250,"ui_confirm","out"],
 [32.25,35.3,"More Comfort,<br>Better Support","R",250,"sub_boom","punch"],
 [35.45,38.3,"Available Size<br>M – 4XL","C",250,"coin","in"],
 [38.45,41.1,"5 Colours<br>Available","C",250,"ui_notif","out"],
 [41.25,44.6,"Your Everyday<br>Comfort Bra 🤎","C",250,"riser_shimmer","in"],
]
CUTS=[3.4,6.4,9.8,13.0,16.2,19.6,22.6,26.0,29.0,32.2,35.4,38.4,41.2]
VOL={"sub_boom":0.45,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
DUR=44.8
ov=[];au=[];js=[]
for i,(s,e,t,side,top,sfx,z) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word {side}" style="top:{top}px" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.4)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22,scale:.92}},{{opacity:1,y:0,scale:1,duration:0.38,ease:"back.out(2)"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.fromTo("#cam",{{scale:1.0}},{{scale:1.06,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    else:
        js.append(f'tl.fromTo("#cam",{{scale:1.06}},{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
for c in CUTS:  # flash putih lembut tiap potongan
    js.append(f'tl.fromTo("#flash",{{opacity:.35}},{{opacity:0,duration:.25,ease:"power2.out"}},{c});')
    au.append(f'<audio src="sfx/swoosh.wav" data-start="{c-0.12:.2f}" data-duration="0.6" data-volume="0.12"></audio>')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Italianno";src:url("assets/Italianno.woff2") format("woff2");}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0;z-index:4;pointer-events:none;}}
.word{{position:absolute;width:440px;z-index:5;}}
.word.L{{left:120px;text-align:left;}}
.word.R{{right:150px;text-align:right;}}
.word.C{{left:0;right:0;width:auto;text-align:center;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.35;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}} .word.C .bar{{margin:10px auto 0;}}
#title{{position:absolute;top:230px;left:0;right:0;text-align:center;z-index:6;color:#fff;}}
#t1{{display:inline-block;font-family:"Italianno",cursive;font-size:82px;line-height:.95;text-shadow:0 2px 8px rgba(0,0,0,.5);opacity:0;}}
#t2{{display:inline-block;margin-top:6px;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;letter-spacing:-0.03em;text-shadow:0 2px 6px rgba(0,0,0,.5);opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="0.35"></video></div>
  <div id="flash"></div>
  <div id="title" class="clip" data-start="0" data-duration="3.4"><span id="t1">Wireless Bra</span><br><span id="t2">Takda Besi!</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio src="sfx/cork.wav" data-start="0.15" data-duration="1.0" data-volume="0.5"></audio>
  <audio src="sfx/sub_boom.wav" data-start="0.7" data-duration="1.0" data-volume="0.4"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,scale:.6,y:10}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.6)"}},0.15);
tl.fromTo("#t2",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},0.7);
tl.fromTo("#cam",{{scale:1.12}},{{scale:1.02,duration:.5,ease:"power3.out"}},0.7);
tl.to("#cam",{{scale:1.07,duration:2.0,ease:"sine.inOut"}},1.2);
tl.to("#t1,#t2",{{opacity:0,y:-10,duration:.22,ease:"power2.in"}},3.15);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
