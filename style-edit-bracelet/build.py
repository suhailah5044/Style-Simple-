# Bracelet Titanium — HyperFrames build (python3 build.py -> index.html)
# Overlay kata kunci: [mula, tamat, "Teks", sfx, zoom(in|out|punch|-)]
O=[
 [6.50,7.50,"Titanium","ui_prompt","in"],
 [12.90,15.00,"Tahan Berbulan","click","out"],
 [15.15,16.05,"Tak Berkarat","ding","punch"],
 [16.15,17.90,"Tak Luntur","ui_prompt","in"],
 [18.60,19.40,"Memang Love","tingting","out"],
 [20.55,22.20,"Koleksi Lavis","pop","in"],
 [23.60,24.70,"Ada Bangle","click","out"],
 [29.70,30.95,"Sesuai Pakai Daily","ui_prompt","in"],
 [37.90,39.15,"Tangan Besar / Kecil","pop","out"],
 [40.10,41.60,"Ada Adjuster","ding","punch"],
 [44.50,46.40,"Stand By Raya","ui_prompt","in"],
 [48.80,49.90,"Tahan Lama","ding","punch"],
 [52.30,53.70,"Still Elok","click","out"],
 [58.90,60.80,"Grab Sebelum Sold Out","soft_impact","punch"],
]
# B-roll: [mula, tamat, fail, mula-dalam-klip, gaya(slice|card)]
B=[
 [8.60,11.70,"b1947",0.3,"slice"],
 [33.80,35.85,"b1948",0.4,"card"],
 [41.55,44.25,"b1947",3.2,"slice"],
]
VOL={"ui_prompt":.4,"click":.45,"ding":.3,"tingting":.28,"pop":.4,"sparkle":.25,"soft_impact":.5}
DUR=63.1
el=[];au=[];js=[]
for i,(s,e,t,sfx,z) in enumerate(O):
    el.append(f'<div id="w{i}" class="clip w" data-start="{s}" data-duration="{e-s:.2f}"><div class="box"><i class="k tl"></i><i class="k tr"></i><i class="k bl"></i><i class="k br"></i><span class="tx">{t}</span></div></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-.03):.2f}" data-duration="1.2" data-volume="{VOL[sfx]}"></audio>')
    js+= [f'tl.fromTo("#w{i} .tx",{{opacity:0,filter:"blur(8px)",scale:1.18}},{{opacity:1,filter:"blur(0px)",scale:1,duration:.42,ease:"expo.out"}},{s});',
          f'tl.fromTo("#w{i} .k",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.32,ease:"back.out(2)",stagger:.03}},{s+.04:.2f});',
          f'tl.to("#w{i} .k",{{opacity:0,duration:.25}},{s+.75:.2f});',
          f'tl.to("#w{i} .tx",{{opacity:0,filter:"blur(6px)",duration:.2,ease:"power2.in"}},{e-.22:.2f});']
    if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:.45,ease:"power3.out"}},{s});')
    elif z=="in": js.append(f'tl.to("#cam",{{scale:1.07,duration:{e-s:.2f},ease:"sine.inOut"}},{s});')
    elif z=="out": js.append(f'tl.to("#cam",{{scale:1.0,duration:{e-s:.2f},ease:"sine.inOut"}},{s});')
for j,(s,e,f,ms,sty) in enumerate(B):
    d=f'data-start="{s}" data-duration="{e-s:.2f}" data-playback-start="{ms}" muted data-volume="0"'
    if sty=="slice":
        inner="".join(f'<div class="sl s{k}"><video id="v{j}{k}" src="assets/{f}.mp4" {d} data-has-audio="false"></video></div>' for k in range(3))
        el.append(f'<div id="b{j}" class="broll"><div class="push">{inner}</div></div>')
        for k in range(3):
            js.append(f'tl.fromTo("#b{j} .s{k}",{{xPercent:{(-1)**k*100}}},{{xPercent:0,duration:.34,ease:"expo.out"}},{s+k*.05:.2f});')
        au.append(f'<audio id="fb{j}" src="sfx/frame_break.wav" data-start="{s-.02:.2f}" data-duration=".6" data-volume=".35"></audio>')
    else:
        el.append(f'<div id="b{j}" class="broll"><div class="push"><div class="card"><video id="v{j}" src="assets/{f}.mp4" {d} data-has-audio="false"></video></div></div></div>')
        js+= [f'tl.fromTo("#b{j} .card",{{scale:.55,rotation:-5,opacity:0}},{{scale:.84,rotation:0,opacity:1,duration:.38,ease:"back.out(1.6)"}},{s});',
              f'tl.to("#b{j} .card",{{scale:1,borderRadius:0,outlineColor:"rgba(255,255,255,0)",duration:.32,ease:"power3.inOut"}},{s+.7:.2f});']
        au.append(f'<audio id="fp{j}" src="sfx/pop.wav" data-start="{s:.2f}" data-duration=".3" data-volume=".35"></audio>')
        au.append(f'<audio id="fi{j}" src="sfx/soft_impact.wav" data-start="{s+.7:.2f}" data-duration=".7" data-volume=".4"></audio>')
    js+= [f'tl.set("#b{j}",{{opacity:1}},{s});',f'tl.fromTo("#b{j} .push",{{scale:1.0}},{{scale:1.08,duration:{e-s:.2f},ease:"none"}},{s});',
          f'tl.to("#b{j}",{{opacity:0,duration:.16}},{e-.16:.2f});']
    au.append(f'<audio id="wo{j}" src="sfx/whoosh.wav" data-start="{e-.3:.2f}" data-duration=".6" data-volume=".28"></audio>')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Cormorant";src:url("assets/CormorantItalic.woff2") format("woff2");font-style:italic;font-weight:500;}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%;}}
video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;inset:0;z-index:3;opacity:0;}}
.broll .push{{position:absolute;inset:0;}}
.sl{{position:absolute;inset:0;}}
.s0{{clip-path:inset(0 0 66.6% 0);}} .s1{{clip-path:inset(33.3% 0 33.3% 0);}} .s2{{clip-path:inset(66.6% 0 0 0);}}
.card{{position:absolute;inset:0;border-radius:28px;overflow:hidden;outline:6px solid #fff;outline-offset:-6px;box-shadow:0 20px 60px rgba(0,0,0,.45);}}
.w{{position:absolute;top:262px;left:0;right:0;text-align:center;z-index:6;}}
.w .box{{position:relative;display:inline-block;padding:16px 26px;}}
.w .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:500;font-size:26px;line-height:1.2;letter-spacing:-0.02em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;white-space:nowrap;}}
.k{{position:absolute;width:11px;height:11px;border:0 solid #fff;opacity:0;filter:drop-shadow(0 1px 2px rgba(0,0,0,.4));}}
.tl{{left:0;top:0;border-left-width:2px;border-top-width:2px;}} .tr{{right:0;top:0;border-right-width:2px;border-top-width:2px;}}
.bl{{left:0;bottom:0;border-left-width:2px;border-bottom-width:2px;}} .br{{right:0;bottom:0;border-right-width:2px;border-bottom-width:2px;}}
#title{{position:absolute;top:215px;left:0;right:0;text-align:center;z-index:7;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.45);}}
#t1{{display:inline-block;font-family:"Cormorant",serif;font-style:italic;font-weight:500;font-size:64px;line-height:1;opacity:0;}}
#t2{{display:block;font-family:"Lexend Mega",sans-serif;font-weight:400;font-size:17px;letter-spacing:.42em;margin-top:12px;opacity:0;}}
#line{{display:block;width:120px;height:1.5px;background:#fff;margin:14px auto 0;transform:scaleX(0);}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/aroll_cut.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.3"><span id="t1">Bracelet</span><span id="t2">TITANIUM</span><i id="line"></i></div>
  {chr(10).join("  "+x for x in el)}
  <audio id="bgm" src="sfx/bgm.wav" data-start="0" data-duration="{DUR}" data-volume="0.09"></audio>
  <audio id="a_in" src="sfx/intro_pan.wav" data-start="0.05" data-duration="1.6" data-volume="0.45"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,y:18,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.7,ease:"expo.out"}},0.1);
tl.fromTo("#t2",{{opacity:0,scaleX:1.35}},{{opacity:1,scaleX:1,duration:.8,ease:"expo.out"}},0.45);
tl.fromTo("#line",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"expo.out"}},0.6);
tl.fromTo("#cam",{{scale:1.12}},{{scale:1.0,duration:1.2,ease:"power3.out"}},0);
tl.to("#cam",{{scale:1.05,duration:2.0,ease:"sine.inOut"}},1.2);
tl.to("#title span,#line",{{opacity:0,y:-10,filter:"blur(6px)",duration:.3,ease:"power2.in"}},3.0);
tl.to("#cam",{{scale:1.0,duration:1.5,ease:"sine.inOut"}},3.3);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
