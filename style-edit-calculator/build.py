# Style Edit — Calculator Solar (overlay UI prompt, putih kecil). python3 build.py
CART='<svg viewBox="0 0 24 24" class="ic"><path d="M3 4h2.2l2.1 10.2a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.3" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9.5" cy="19.5" r="1.5" fill="#fff"/><circle cx="17" cy="19.5" r="1.5" fill="#fff"/></svg>'
SUN='<svg viewBox="0 0 24 24" class="ic"><circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="2"/><g stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></g></svg>'
# [mula, tamat, teks, sfx, vol, zoom]  (zoom: in/out/punch/none — hanya untuk kamera utama)
O=[
 [3.00,5.05,"Comel Sangat","ui_prompt",.35,"out"],
 [5.10,6.05,"Ingatkan Mahal","ui_select",.35,"none"],
 [6.15,9.35,"Rupanya Murah!","ding_glass",.28,"punch"],
 [9.42,11.90,CART+"Check Bakul Kuning","ui_prompt",.3,"in"],
 [11.96,12.95,"Serius!","soft_impact",.4,"punch"],
 [13.10,16.05,"Tekan Best Gila","key_triple",.4,"none"],
 [16.15,19.05,"Tak Guna Bateri","ding_soft",.33,"punch"],
 [19.24,21.38,SUN+"Guna Solar Je","sparkle_lr",.28,"none"],
 [21.45,22.98,"Hidup Kat Sini!","bubble_pop",.4,"punch"],
]
BROLL=[("brollA",13.03,3.10),("brollB",19.10,2.33)]
XSFX=[("hook_shimmer",0.05,1.6,.32),("key_triple",0.62,.5,.45),("ding_soft",0.98,1.0,.25),
      ("whoosh_lr",6.02,.55,.22),("whoosh_rl",12.95,.55,.22),("whoosh_lr",19.02,.55,.22)]
DUR=22.98
ov=[];au=[];js=[]
for i,(s,e,t,sfx,v,z) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word{' dk' if any(bs<=s<bs+bd for _,bs,bd in BROLL) else ''}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}<i class="caret"></i></span></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.3" data-volume="{v}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{clipPath:"inset(0 100% 0 0)",opacity:1,y:6}},{{clipPath:"inset(0 0% 0 0)",y:0,duration:0.42,ease:"power3.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .caret",{{opacity:1}},{{opacity:0,duration:0.15}},{s+0.42:.2f});')
    js.append(f'tl.to("#w{i} .tx",{{opacity:0,y:-6,duration:0.18,ease:"power2.in"}},{e-0.2:.2f});')
    if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.09}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in": js.append(f'tl.to("#cam",{{scale:1.06,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    elif z=="out": js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
for j,(n,s,d,v) in enumerate(XSFX):
    au.append(f'<audio id="x{j}" src="sfx/{n}.wav" data-start="{s}" data-duration="{d}" data-volume="{v}"></audio>')
br=[]
for n,s,d in BROLL:
    br.append(f'<video id="{n}" class="clip broll" src="assets/{n}.mp4" data-start="{s}" data-duration="{d}" data-has-audio="false"></video>')
    js.append(f'tl.fromTo("#{n}",{{scale:1.06}},{{scale:1.0,duration:0.5,ease:"power3.out"}},{s});')
    js.append(f'tl.to("#{n}",{{scale:1.03,duration:{d-0.5:.2f},ease:"sine.inOut"}},{s+0.5:.2f});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
@font-face{{font-family:"Jakarta";src:url("assets/PlusJakartaSans.woff2") format("woff2");font-weight:200 800;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%;}}
video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;inset:0;z-index:3;}}
.word{{position:absolute;top:212px;left:0;right:0;text-align:center;z-index:5;}}
.word .tx{{position:relative;display:inline-flex;align-items:center;gap:12px;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:27px;line-height:1.3;
  letter-spacing:-0.04em;color:#fff;padding-right:6px;text-shadow:0 2px 8px rgba(0,0,0,.55),0 0 2px rgba(0,0,0,.4);clip-path:inset(0 100% 0 0);}}
.word .caret{{display:inline-block;width:3px;height:30px;background:#fff;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.4);}}
.word.dk .tx{{background:rgba(20,20,24,.42);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);padding:10px 22px 10px 24px;border-radius:999px;text-shadow:none;}}
.word.dk .caret{{height:26px;}}
.ic{{width:28px;height:28px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5));}}
#hook{{position:absolute;top:172px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Jakarta",sans-serif;text-shadow:0 2px 10px rgba(0,0,0,.5);}}
#h1{{display:block;font-weight:700;font-size:44px;letter-spacing:-0.02em;line-height:1.1;}}
#h2{{display:inline-flex;align-items:center;gap:14px;margin-top:12px;font-weight:500;font-size:28px;letter-spacing:0.01em;}}
#key{{display:inline-grid;place-items:center;width:50px;height:50px;border:2.5px solid #fff;border-radius:14px;font-weight:700;font-size:26px;
  box-shadow:0 4px 0 rgba(255,255,255,.85),0 6px 12px rgba(0,0,0,.35);}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  {chr(10).join("  "+x for x in br)}
  <div id="hook" class="clip" data-start="0" data-duration="3.0"><span id="h1">Calculator Solar</span><span id="h2"><span id="h2t">ada button</span><span id="key">%</span></span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="bgm" src="sfx/bgm.wav" data-start="0" data-duration="{DUR}" data-volume="0.09"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#h1",{{opacity:0,y:18,scale:.92}},{{opacity:1,y:0,scale:1,duration:.6,ease:"expo.out"}},0.08);
tl.fromTo("#h2t",{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},0.5);
tl.fromTo("#key",{{opacity:0,scale:.4,rotate:-12}},{{opacity:1,scale:1,rotate:0,duration:.5,ease:"back.out(2.5)"}},0.62);
tl.to("#key",{{y:4,boxShadow:"0 0px 0 rgba(255,255,255,.85),0 2px 6px rgba(0,0,0,.35)",duration:.07,yoyo:true,repeat:1,ease:"power1.inOut"}},0.98);
tl.to("#key",{{y:4,boxShadow:"0 0px 0 rgba(255,255,255,.85),0 2px 6px rgba(0,0,0,.35)",duration:.07,yoyo:true,repeat:1,ease:"power1.inOut"}},1.75);
tl.fromTo("#cam",{{scale:1.08}},{{scale:1.0,duration:1.0,ease:"power3.out"}},0.05);
tl.to("#cam",{{scale:1.05,duration:1.9,ease:"sine.inOut"}},1.05);
tl.to("#hook",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},2.72);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
