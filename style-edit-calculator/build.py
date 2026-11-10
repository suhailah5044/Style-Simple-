# Style Edit — Calculator Solar v2 (animasi masuk berbeza + simbol kira-kira + anak panah). python3 build.py
SUN='<svg viewBox="0 0 24 24" class="ic"><circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="2"/><g stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></g></svg>'
# [mula, tamat, teks, animasi masuk, sfx, vol, zoom]
#  animasi: rise (naik+blur) | prompt (wipe+kursor) | pop (scale bounce) | drop (jatuh+condong) | type (huruf satu-satu)
O=[
 [3.00,5.05,"Comel Sangat","rise","ui_prompt",.33,"out"],
 [5.10,6.05,"Ingatkan Mahal","prompt","ui_select",.35,"none"],
 [6.15,9.35,"Rupanya Murah!","pop","ding_glass",.28,"punch"],
 [11.96,12.95,"Serius!","drop","soft_impact",.4,"punch"],
 [13.10,16.05,"Tekan Best Gila","type","key_triple",.4,"none"],
 [16.15,19.05,"Tak Guna Bateri","rise","ding_soft",.33,"punch"],
 [19.24,21.38,SUN+"Guna Solar Je","prompt","sparkle_lr",.28,"none"],
 [21.45,22.98,"Hidup Kat Sini!","pop","bubble_pop",.4,"punch"],
]
BROLL=[("brollA",13.03,3.10),("brollB",19.10,2.33)]
# anak panah lukis tangan: [id, mula, tamat, path, (x,y,sudut) kepala]
ARROW=[
 ["ar1",19.55,21.38,"M470 300 C 330 380, 300 560, 350 770",(350,770,100)],
 ["ar2",21.70,22.98,"M650 290 C 900 330, 940 560, 745 735",(745,735,137)],
]
# simbol kira-kira terapung (ruang kosong sahaja: bumbung kereta & tepi)
MATH_T=(9.42,12.95)
SYM=[("+",120,215,52),("×",905,170,46),("÷",205,360,40),("−",960,330,54),("%",800,285,38),("=",70,470,40),("×",1000,505,36),("+",285,120,34)]
XSFX=[("hook_shimmer",0.05,1.6,.32),("key_triple",0.62,.5,.45),("ding_soft",0.98,1.0,.25),
      ("whoosh_lr",6.02,.55,.22),("key_tick",9.45,.2,.3),("key_tick",9.75,.2,.25),("key_tick",10.1,.2,.25),
      ("whoosh_rl",12.95,.55,.22),("whoosh_lr",19.02,.55,.22),("ui_select",19.6,.4,.18),("ui_select",21.75,.4,.18)]
DUR=22.98
ov=[];au=[];js=[]
def chars(t):
    if t.startswith("<svg"): return t
    return "".join(f'<span class="ch">{c if c!=" " else "&nbsp;"}</span>' for c in t)
for i,(s,e,t,an,sfx,v,z) in enumerate(O):
    dk=' dk' if any(bs<=s<bs+bd for _,bs,bd in BROLL) else ''
    body=chars(t) if an=="type" else t
    car='<i class="caret"></i>' if an=="prompt" else ''
    ov.append(f'<div id="w{i}" class="clip word{dk}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{body}{car}</span></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.3" data-volume="{v}"></audio>')
    X=f"#w{i} .tx"
    if an=="prompt":
        js.append(f'tl.fromTo("{X}",{{opacity:1,clipPath:"inset(0 100% 0 0)",y:6}},{{clipPath:"inset(0 0% 0 0)",y:0,duration:0.45,ease:"power3.out"}},{s});')
        js.append(f'tl.to("#w{i} .caret",{{opacity:0,duration:0.15}},{s+0.45:.2f});')
    elif an=="pop":
        js.append(f'tl.fromTo("{X}",{{opacity:0,scale:0.55}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(2.6)"}},{s});')
    elif an=="rise":
        js.append(f'tl.fromTo("{X}",{{opacity:0,y:26,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.5,ease:"expo.out"}},{s});')
    elif an=="drop":
        js.append(f'tl.fromTo("{X}",{{opacity:0,y:-30,rotation:-6}},{{opacity:1,y:0,rotation:0,duration:0.45,ease:"bounce.out"}},{s});')
    elif an=="type":
        js.append(f'tl.set("{X}",{{opacity:1}},{s});')
        js.append(f'tl.fromTo("#w{i} .ch",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.22,stagger:0.035,ease:"power2.out"}},{s});')
    js.append(f'tl.to("{X}",{{opacity:0,y:-8,duration:0.18,ease:"power2.in"}},{e-0.2:.2f});')
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
arr=[]
for aid,s,e,p,(hx,hy,ang) in ARROW:
    arr.append(f'<svg id="{aid}" class="clip arrow" data-start="{s}" data-duration="{round(e-s,2)}" viewBox="0 0 1080 1920"><path class="ln" d="{p}" pathLength="1"/>'
               f'<g transform="translate({hx} {hy}) rotate({ang})"><path class="hd" d="M-26 -16 L0 0 L-26 16" pathLength="1"/></g></svg>')
    js.append(f'tl.fromTo("#{aid} .ln",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.inOut"}},{s});')
    js.append(f'tl.fromTo("#{aid} .hd",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.18,ease:"power2.out"}},{s+0.48:.2f});')
    js.append(f'tl.to("#{aid}",{{opacity:0,duration:0.18}},{e-0.2:.2f});')
sym=[]
ms,me=MATH_T
for k,(c,x,y,sz) in enumerate(SYM):
    sym.append(f'<span class="sy" id="sy{k}" style="left:{x}px;top:{y}px;font-size:{sz}px">{c}</span>')
    d=0.07*k
    js.append(f'tl.fromTo("#sy{k}",{{opacity:0,scale:0.3,rotation:-30}},{{opacity:0.75,scale:1,rotation:0,duration:0.45,ease:"back.out(2)"}},{ms+d:.2f});')
    js.append(f'tl.to("#sy{k}",{{y:{-18 if k%2 else -28},rotation:{12 if k%2 else -10},duration:{me-ms-0.6:.2f},ease:"sine.inOut"}},{ms+d+0.45:.2f});')
    js.append(f'tl.to("#sy{k}",{{opacity:0,scale:0.6,duration:0.25,ease:"power2.in"}},{me-0.3+0.02*k:.2f});')
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
  letter-spacing:-0.04em;color:#fff;padding-right:6px;text-shadow:0 2px 8px rgba(0,0,0,.55),0 0 2px rgba(0,0,0,.4);opacity:0;}}
.word .ch{{display:inline-block;}}
.word .caret{{display:inline-block;width:3px;height:30px;background:#fff;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.4);}}
.word.dk .tx{{background:rgba(20,20,24,.42);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);padding:10px 22px 10px 24px;border-radius:999px;text-shadow:none;gap:10px;}}
.word.dk .caret{{height:26px;}}
.ic{{width:28px;height:28px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5));}}
.arrow{{position:absolute;inset:0;width:1080px;height:1920px;z-index:5;overflow:visible;filter:drop-shadow(0 2px 5px rgba(0,0,0,.5));}}
.arrow path{{fill:none;stroke:#fff;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;}}
.sy{{position:absolute;z-index:4;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:300;line-height:1;opacity:0;text-shadow:0 2px 8px rgba(0,0,0,.45);}}
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
  <div id="math" class="clip" data-start="{ms}" data-duration="{round(me-ms,2)}">{"".join(sym)}</div>
  <div id="hook" class="clip" data-start="0" data-duration="3.0"><span id="h1">Calculator Solar</span><span id="h2"><span id="h2t">ada button</span><span id="key">%</span></span></div>
  {chr(10).join("  "+x for x in ov)}
  {chr(10).join("  "+x for x in arr)}
  <audio id="bgm" src="sfx/bgm.wav" data-start="0" data-duration="{DUR}" data-volume="0.09"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#h1",{{opacity:0,y:18,scale:.92}},{{opacity:1,y:0,scale:1,duration:.6,ease:"expo.out"}},0.08);
tl.fromTo("#h2t",{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},0.5);
tl.fromTo("#key",{{opacity:0,scale:.4,rotation:-12}},{{opacity:1,scale:1,rotation:0,duration:.5,ease:"back.out(2.5)"}},0.62);
tl.to("#key",{{y:4,boxShadow:"0 0px 0 rgba(255,255,255,.85),0 2px 6px rgba(0,0,0,.35)",duration:.07,yoyo:true,repeat:1,ease:"power1.inOut"}},0.98);
tl.to("#key",{{y:4,boxShadow:"0 0px 0 rgba(255,255,255,.85),0 2px 6px rgba(0,0,0,.35)",duration:.07,yoyo:true,repeat:1,ease:"power1.inOut"}},1.75);
tl.fromTo("#cam",{{scale:1.08}},{{scale:1.0,duration:1.0,ease:"power3.out"}},0.05);
tl.to("#cam",{{scale:1.05,duration:1.9,ease:"sine.inOut"}},1.05);
tl.to("#hook",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},2.72);
tl.to("#cam",{{scale:1.05,duration:2.5,ease:"sine.inOut"}},9.42);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
