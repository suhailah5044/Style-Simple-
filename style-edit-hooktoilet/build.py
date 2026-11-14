# Hook Toilet — style v2 (Lexend Mega putih kecil) + kinetic hook + b-roll full screen
# Masa = masa output (selepas buang ayat ulang src 23.5–26.67s)
# [start, end, tajuk, subline, side(C/L/R), sfx, zoom]
O=[
 [7.45,9.65,"Budget-Friendly","Bawah RM3, lagi murah dari teh ais","C","coin","punch"],
 [10.0,12.0,"Stainless Steel","Silver clean, vibe minimalist","C","glass_ting","in"],
 [12.55,16.0,"Grip Dia Ketat","Batang mop tak melurut jatuh","C","ui_tap","none"],
 [18.95,21.6,"Pilihan 2–5 Hook","Ikut berapa batang nak sangkut","C","ui_blip","in"],
 [21.8,23.45,"No Drill, No Drama","Lekat je, dinding tak rosak","C","sub_boom","punch"],
 [23.6,26.5,"Hygiene Level Up","Berus tak kena lantai, cepat kering","C","ui_confirm","none"],
 [29.4,33.0,"Gam Super Kuat","Confirm tak tercabut","C","sub_boom","none"],
 [34.5,38.4,"Tekan Beg Kuning","Hook stainless toilet","L","riser_shimmer","in"],
]
# b-roll full screen: [start, dur, file]
B=[[12.3,4.0,"broll1"],[29.15,4.0,"broll2"]]
# hook kinetic: [masa, perkataan, baris, besar?]
K=[[0.0,"Bila",1,0],[0.32,"dah",1,0],[0.48,"sangkut,",1,0],[0.9,"barulah",2,0],[1.2,"cantik!",2,1]]
VOL={"sub_boom":0.5,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
DUR=41.4
ov=[];au=[];js=[];br=[]
for i,(s,e,t,sub,side,sfx,z) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><span class="sb">{sub}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.45)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22,scale:.85}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2.2)"}},{s});')
    js.append(f'tl.fromTo("#w{i} .sb",{{opacity:0,y:12}},{{opacity:.92,y:0,duration:0.38,ease:"expo.out"}},{s+0.12:.2f});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .sb,#w{i} .bar",{{opacity:0,y:-10,duration:0.22,ease:"power2.in"}},{e-0.24:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.06,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
        nxt=O[i+1][0] if i+1<len(O) else 99
        if nxt-e>0.7: js.append(f'tl.to("#cam",{{scale:1.0,duration:0.6,ease:"sine.inOut"}},{e:.2f});')
for j,(s,d,f) in enumerate(B):
    br.append(f'<video id="b{j}" class="clip broll" src="assets/{f}.mp4" data-start="{s}" data-duration="{d}" data-has-audio="false" muted></video>')
    au.append(f'<audio id="ab{j}" src="sfx/swoosh.wav" data-start="{s-0.05:.2f}" data-duration="1.0" data-volume="0.25"></audio>')
    js.append(f'tl.fromTo("#b{j}",{{opacity:0}},{{opacity:1,duration:0.35,ease:"sine.out"}},{s});')
    js.append(f'tl.fromTo("#b{j}",{{scale:1.08}},{{scale:1.0,duration:{d},ease:"sine.out"}},{s});')
    js.append(f'tl.to("#b{j}",{{opacity:0,duration:0.35,ease:"sine.in"}},{s+d-0.35:.2f});')
kin=[];
for k,(s,w,ln,big) in enumerate(K):
    kin.append(f'<span id="k{k}" class="kw{" big" if big else ""}">{w}</span>'+("<br>" if k==2 else " "))
    js.append(f'tl.fromTo("#k{k}",{{opacity:0,y:28,scale:{1.6 if big else .5}}},{{opacity:1,y:0,scale:1,duration:{0.45 if big else 0.3},ease:"back.out(2.6)"}},{s});')
    if big: js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.02,duration:0.5,ease:"power3.out"}},{s});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:3;opacity:0;}}
.word{{position:absolute;top:250px;z-index:5;}}
.word.C{{left:140px;right:140px;text-align:center;}}
.word.L{{left:120px;width:430px;text-align:left;}}
.word.R{{right:160px;width:430px;text-align:right;}}
.word span{{display:block;font-family:"Lexend Mega",sans-serif;color:#fff;letter-spacing:-0.03em;opacity:0;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);}}
.word .tx{{font-weight:600;font-size:30px;line-height:1.3;}}
.word .sb{{font-weight:400;font-size:19px;line-height:1.4;margin-top:6px;letter-spacing:-0.04em;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.C .bar{{margin:10px auto 0;}} .word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#hook{{position:absolute;top:250px;left:0;right:0;text-align:center;z-index:6;font-family:"Lexend Mega",sans-serif;font-weight:600;color:#fff;
  font-size:32px;line-height:1.35;letter-spacing:-0.03em;text-shadow:0 2px 8px rgba(0,0,0,.5);}}
#hook .kw{{display:inline-block;opacity:0;}}
#hook .big{{font-size:52px;font-weight:800;letter-spacing:-0.04em;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  {chr(10).join("  "+x for x in br)}
  <div id="hook" class="clip" data-start="0" data-duration="3.1">{"".join(kin)}</div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_k" src="sfx/ui_tap.wav" data-start="0.0" data-duration="0.8" data-volume="0.35"></audio>
  <audio id="a_k2" src="sfx/glass_ting.wav" data-start="1.18" data-duration="0.9" data-volume="0.35"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
{chr(10).join(js)}
tl.to("#cam",{{scale:1.0,duration:1.0,ease:"sine.inOut"}},1.8);
tl.to("#hook .kw",{{opacity:0,y:-12,duration:.25,stagger:.03,ease:"power2.in"}},2.8);
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
