# Karpet Luar Anti Slip — HyperFrames 9:16. Footage asal (HDR->SDR tonemap sahaja), tiada filter warna.
# Footage karpet sahaja (tiada orang). Scene: [id, mula, durasi, zoom]  zoom: in | out | punch | none
SC=[
 ["s1",0.0,3.0,"out"],      # IMG_1978 hook
 ["s2",3.0,2.0,"in"],       # IMG_1971
 ["s3",5.0,2.6,"mock"],     # IMG_1983 dalam phone mockup
 ["s4",7.6,2.4,"punch"],    # IMG_1982 close-up bulu (digital zoom)
 ["s5",10.0,1.6,"out"],     # IMG_1979
 ["s6",11.6,1.7,"in"],      # IMG_1976 pijak
 ["s7",13.3,1.4,"out"],     # IMG_1980 (14.7-15.0 frame break keluar)
 ["s8",14.7,1.8,"punch"],   # IMG_1972 bawah TPE
 ["s9",16.5,2.2,"in"],      # IMG_1974 corak
 ["s10",18.7,1.6,"out"],    # IMG_1973
 ["s11",20.3,1.6,"in"],     # IMG_1981
 ["s13",21.9,2.3,"in"],     # IMG_1970 akhir
]
DUR=24.2
FB=14.7;FBD=0.3;FBSRC="s7";FBMS=1.4
# Overlay: [mula, tamat, baris1, baris2, posisi(L|R|C), top(px), sfx]
O=[
 [3.1,4.9,"Outdoor Mat","Upgrade!","R dk",230,"bell_ding"],
 [5.6,7.45,"Biggest Size","80 × 120 cm","C",150,"ting2"],
 [7.75,9.85,"400 GSM","Coarse Fiber","R",230,"ui_prompt"],
 [11.7,13.2,"Scrape Off","Dirt & Sand","L dk",230,"ui_prompt"],
 [13.4,14.65,"Water","Resistant","R",240,"bell_ding"],
 [14.9,16.4,"TPE Anti-Slip","Base","R",230,"ui_prompt"],
 [16.65,18.6,"Minimalist","Embossed Design","L",230,"ui_prompt"],
 [22.1,24.05,"Perfect for","Home Entrance","C dk",215,"ting2"],
]
# SFX transisi: [masa, sfx, volume]
T=[
 [0.05,"soft_impact",0.4],[0.35,"bubble_pop",0.3],
 [2.92,"air_whoosh",0.28],
 [4.9,"air_whoosh",0.25],[5.15,"ui_click",0.35],[5.45,"soft_impact",0.35],
 [7.5,"air_whoosh",0.28],[7.62,"soft_impact",0.3],
 [9.95,"ui_click",0.3],
 [11.55,"air_whoosh",0.22],
 [14.68,"frame_break",0.4],
 [16.45,"ui_click",0.3],
 [18.62,"air_whoosh",0.22],[20.25,"ui_click",0.28],
 [21.82,"air_whoosh",0.25],[21.95,"bubble_pop",0.25],
]
VOL={"bell_ding":0.22,"ting2":0.25,"ui_prompt":0.38}
vid=[];ov=[];au=[];js=[]
for i,(sid,s,d,z) in enumerate(SC):
    zi=10+i
    js.append(f'tl.set("#{sid}",{{visibility:"visible"}},{s});tl.set("#{sid}",{{visibility:"hidden"}},{s+d});')
    if z=="mock":
        vid.append(f'''<div id="{sid}" class="scene mock" style="z-index:{zi};visibility:hidden">
    <div class="bg"><i class="spot"></i><i class="grid"></i></div>
    <div class="phone" id="phone"><div class="scr"><video id="v_{sid}" src="assets/clips/{sid}.mp4" data-start="{s}" data-duration="{d}" muted playsinline></video></div><i class="isl"></i></div>
  </div>''')
        js.append(f'tl.fromTo("#phone",{{scale:1.5,borderRadius:0}},{{scale:1,borderRadius:84,duration:.65,ease:"power3.inOut"}},{s});')
        js.append(f'tl.fromTo("#{sid} .bg",{{opacity:0}},{{opacity:1,duration:.4}},{s+0.15});')
        js.append(f'tl.to("#phone",{{y:-14,duration:{d-0.7},ease:"sine.inOut"}},{s+0.65});')
        continue
    vid.append(f'<div id="{sid}" class="scene" style="z-index:{zi};visibility:hidden"><div class="cam"><video id="v_{sid}" src="assets/clips/{sid}.mp4" data-start="{s}" data-duration="{d}" muted playsinline></video></div></div>')
    c=f"#{sid} .cam"
    if z=="punch": js.append(f'tl.fromTo("{c}",{{scale:1.14}},{{scale:1.04,duration:.5,ease:"power3.out"}},{s});tl.to("{c}",{{scale:1.1,duration:{d-0.5},ease:"sine.inOut"}},{s+0.5});')
    elif z=="in": js.append(f'tl.fromTo("{c}",{{scale:1.0}},{{scale:1.07,duration:{d},ease:"sine.inOut"}},{s});')
    elif z=="out": js.append(f'tl.fromTo("{c}",{{scale:1.08}},{{scale:1.0,duration:{d},ease:"sine.out"}},{s});')
# frame break: 3 jalur s6 pecah keluar, s7 di bawah
for k,(top,bot,dx) in enumerate([(0,34,-1),(33,67,1),(66,100,-1)]):
    vid.append(f'<div id="fb{k}" class="scene" style="z-index:40;visibility:hidden;clip-path:polygon(0 {top}%,100% {top+2*dx}%,100% {bot+2*dx}%,0 {bot}%)"><div class="cam"><video id="v_fb{k}" src="assets/clips/{FBSRC}.mp4" data-start="{FB}" data-duration="{FBD+0.01*k:.2f}" data-media-start="{FBMS}" muted playsinline></video></div></div>')
    js.append(f'tl.set("#fb{k}",{{visibility:"visible"}},{FB});tl.set("#fb{k}",{{visibility:"hidden"}},{FB+FBD});')
    js.append(f'tl.fromTo("#fb{k}",{{x:0,rotation:0}},{{x:{dx*1150},rotation:{dx*4},duration:{FBD},ease:"power3.in"}},{FB+0.02*k});')
js.append(f'tl.fromTo("#flash",{{opacity:0}},{{opacity:.55,duration:.05,yoyo:true,repeat:1}},{FB});')
for i,(s,e,a,b,pos,top,sfx) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word {pos}" data-start="{s}" data-duration="{round(e-s,2)}" style="top:{top}px">{'<b class="gl"></b>' if "dk" in pos else ""}<div class="l1"><span>{a}</span></div><div class="l2"><span>{b}</span></div><i class="bar"></i></div>')
    au.append(f'<audio id="ao{i}" src="sfx/{sfx}.wav" data-start="{s:.2f}" data-duration="1.2" data-volume="{VOL.get(sfx,0.3)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .l1 span",{{yPercent:110}},{{yPercent:0,duration:.5,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .l2 span",{{yPercent:110}},{{yPercent:0,duration:.5,ease:"expo.out"}},{s+0.12:.2f});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"expo.out"}},{s+0.18:.2f});')
    js.append(f'tl.to("#w{i} .l1 span,#w{i} .l2 span",{{yPercent:-110,duration:.25,ease:"power2.in",stagger:.04}},{e-0.3:.2f});')
    if "dk" in pos: js.append(f'tl.fromTo("#w{i} .gl",{{opacity:0}},{{opacity:1,duration:.35}},{s});tl.to("#w{i} .gl",{{opacity:0,duration:.3}},{e-0.3:.2f});')
    js.append(f'tl.to("#w{i} .bar",{{scaleX:0,duration:.22,ease:"power2.in"}},{e-0.26:.2f});')
for j,(s,sfx,v) in enumerate(T):
    au.append(f'<audio id="at{j}" src="sfx/{sfx}.wav" data-start="{s:.2f}" data-duration="1.0" data-volume="{v}"></audio>')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
.scene{{position:absolute;inset:0;overflow:hidden;}}
.cam{{position:absolute;inset:0;transform-origin:50% 50%;}}
.cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
/* phone mockup + latar pro */
.mock .bg{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 38%,#2b2f36 0%,#15171b 55%,#0b0c0e 100%);}}
.mock .spot{{position:absolute;left:140px;top:300px;width:800px;height:1300px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.10),rgba(255,255,255,0));}}
.mock .grid{{position:absolute;inset:0;opacity:.18;background-image:radial-gradient(rgba(255,255,255,.55) 1.2px,transparent 1.4px);background-size:36px 36px;
  -webkit-mask-image:radial-gradient(70% 60% at 50% 55%,transparent 30%,#000 100%);mask-image:radial-gradient(70% 60% at 50% 55%,transparent 30%,#000 100%);}}
.phone{{position:absolute;left:50%;top:50%;width:700px;height:1290px;margin:-570px 0 0 -350px;border-radius:84px;background:#0d0e10;
  box-shadow:0 0 0 3px #3a3d43,0 0 0 9px #1a1b1e,0 40px 90px rgba(0,0,0,.6);transform-origin:50% 50%;overflow:hidden;}}
.phone .scr{{position:absolute;inset:14px;border-radius:70px;overflow:hidden;background:#000;}}
.phone video{{width:100%;height:100%;object-fit:cover;display:block;}}
.phone .isl{{position:absolute;top:34px;left:50%;width:150px;height:42px;margin-left:-75px;border-radius:21px;background:#000;}}
/* overlay teks: putih, kecil, ruang kosong */
.word{{position:absolute;z-index:60;width:520px;font-family:"Lexend Mega",sans-serif;color:#fff;
  text-shadow:0 0 14px rgba(0,0,0,.45),0 2px 8px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.4);}}
.word.L{{left:150px;text-align:left;}} .word.R{{right:150px;text-align:right;}} .word.C{{left:50%;margin-left:-260px;text-align:center;}}
.word .l1,.word .l2{{overflow:hidden;line-height:1.25;padding:2px 0;}}
.word span{{display:inline-block;}}
.word .l1{{font-weight:600;font-size:30px;letter-spacing:-0.03em;}}
.word .l2{{font-weight:400;font-size:24px;letter-spacing:-0.01em;opacity:.95;margin-top:2px;}}
.word .bar{{display:block;height:2px;width:48px;background:#fff;margin-top:12px;box-shadow:0 1px 4px rgba(0,0,0,.35);}}
.word.dk,#hook{{text-shadow:0 0 18px rgba(0,0,0,.55),0 2px 8px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.4);}}
.gl{{display:block;position:absolute;opacity:0;left:-60px;right:-60px;top:-50px;bottom:-50px;z-index:-1;
  background:radial-gradient(closest-side,rgba(0,0,0,.30),rgba(0,0,0,0));}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}} .word.C .bar{{margin:12px auto 0;}}
/* hook 0-3s (cover story) */
#hook{{position:absolute;top:205px;left:0;right:0;z-index:60;text-align:center;font-family:"Lexend Mega",sans-serif;color:#fff;
  text-shadow:0 2px 10px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.35);}}
#hook .k{{font-size:17px;font-weight:400;letter-spacing:.32em;opacity:.9;}}
#hook .h{{font-size:40px;font-weight:600;letter-spacing:-0.035em;line-height:1.2;margin-top:0;overflow:hidden;}}
#hook .h span{{display:inline-block;}}
#hook .bar{{display:block;height:2px;width:56px;background:#fff;margin:14px auto 0;}}
#flash{{position:absolute;inset:0;background:#fff;z-index:50;opacity:0;pointer-events:none;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  {chr(10).join("  "+x for x in vid)}
  <div id="flash"></div>
  <div id="hook" class="clip" data-start="0" data-duration="2.95"><b class="gl" id="hgl" style="left:50%;right:auto;width:620px;margin-left:-310px;top:-40px;bottom:-40px"></b><div class="h"><span id="h1">Karpet Luar</span></div><div class="h" style="margin-top:0"><span id="h2">Anti Slip</span></div><i class="bar" id="hb"></i></div>
  {chr(10).join("  "+x for x in ov)}
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set(".word span",{{yPercent:110}},0);tl.set(".word .bar",{{scaleX:0}},0);
tl.fromTo("#hgl",{{opacity:0}},{{opacity:1,duration:.4}},0.15);

tl.fromTo("#h1",{{yPercent:110}},{{yPercent:0,duration:.55,ease:"expo.out"}},0.3);
tl.fromTo("#h2",{{yPercent:110}},{{yPercent:0,duration:.55,ease:"expo.out"}},0.45);
tl.fromTo("#hb",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"expo.out"}},0.6);
tl.to("#hook",{{opacity:0,y:-12,duration:.25,ease:"power2.in"}},2.65);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok",len(html))
