# CCTV — style v2 (Lexend Mega subtitle + garis) + kad gambar overlay
# Teks: [start, end, text, sfx, zoom]
O=[
 [4.0,8.85,"Security Rumah Lagi Senang!","ui_blip","in"],
 [11.96,15.1,"Boleh Monitor Dari Phone!","ui_tap","out"],
 [15.2,20.4,"Real-Time Phone Monitoring","ui_notif","in"],
 [20.8,24.4,"4MP HD Camera 📸","sub_boom","punch"],
 [24.5,27.85,"Clear 1080P Video","glass_ting","out"],
 [32.44,34.9,"Two-Way Audio","ui_blip","in"],
 [34.98,36.8,"Boleh Dengar &amp; Bercakap!","ui_confirm","out"],
 [36.9,38.1,"Motion Detection Alert","ui_notif","none"],
 [38.15,39.35,"AI Human Detection","ui_tap","none"],
 [39.42,41.25,"Auto Tracking Movement","ui_blip","none"],
 [41.32,42.95,"Instant Notification Alert","ui_notif","none"],
 [43.0,45.05,"Supports Cloud Storage","ui_confirm","in"],
 [51.06,54.86,"360° Remote Rotation","swoosh","out"],
 [60.0,64.4,"Night Vision Support 🌙","riser_shimmer","in"],
 [68.24,70.46,"CCTV Ni Banyak Function!","sub_boom","punch"],
]
# Gambar: [start, end, file]
IMG=[
 [27.88,32.4,"IMG_4062","left:50px;margin-left:0;top:560px;width:470px;"],
 [36.9,39.35,"IMG_4060",""],
 [39.42,42.95,"IMG_4061",""],
 [70.52,76.5,"IMG_4057",""],
]
VOL={"sub_boom":0.5,"swoosh":0.35,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
DUR=82.0
ov=[];au=[];js=[]
for i,(s,e,t,sfx,z) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.45)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22}},{{opacity:1,y:0,duration:0.38,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.07,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    elif z=="out":
        js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
for j,(s,e,f,pos) in enumerate(IMG):
    ov.append(f'<div id="g{j}" class="clip card" style="{pos}" data-start="{s}" data-duration="{round(e-s,2)}"><img src="img/{f}.jpg"></div>')
    au.append(f'<audio id="ag{j}" src="sfx/swoosh.wav" data-start="{max(0,s-0.05):.2f}" data-duration="1.0" data-volume="0.35"></audio>')
    js.append(f'tl.fromTo("#g{j}",{{opacity:0,scale:.6,y:40}},{{opacity:1,scale:1,y:0,duration:0.42,ease:"back.out(1.8)"}},{s});')
    js.append(f'tl.fromTo("#g{j} img",{{scale:1}},{{scale:1.06,duration:{round(e-s,2)},ease:"none"}},{s});')
    js.append(f'tl.to("#g{j}",{{opacity:0,scale:.9,duration:0.25,ease:"power2.in"}},{e-0.27:.2f});')
    js.append(f'tl.to("#cam",{{scale:1.04,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Italianno";src:url("assets/Italianno.woff2") format("woff2");}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
@font-face{{font-family:"Noto Color Emoji";src:url("assets/NotoColorEmoji.ttf") format("truetype");}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.word{{position:absolute;top:230px;left:140px;right:140px;text-align:center;z-index:6;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega","Noto Color Emoji",sans-serif;font-weight:600;font-size:32px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;margin:10px auto 0;background:#fff;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.card{{position:absolute;top:350px;left:50%;width:560px;margin-left:-280px;z-index:5;opacity:0;background:#fff;padding:10px;border-radius:28px;box-shadow:0 18px 40px rgba(0,0,0,.35);overflow:hidden;box-sizing:border-box;}}

.card img{{display:block;width:100%;border-radius:20px;}}
#title{{position:absolute;top:230px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Italianno","Noto Color Emoji",cursive;font-size:84px;line-height:.95;
  text-shadow:0 2px 8px rgba(0,0,0,.5);}}
#title span{{display:inline-block;opacity:0;}}
#title #t2{{font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;letter-spacing:-0.03em;margin-top:14px;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="4.0"><span id="t1">Rumah Takde Orang? 👀</span><br><span id="t2">CCTV Kecil, Function Padu!</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_cork" src="sfx/cork.wav" data-start="0.15" data-duration="1.0" data-volume="0.55"></audio>
  <audio id="a_t2" src="sfx/sub_boom.wav" data-start="1.6" data-duration="1.0" data-volume="0.45"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,scale:.6,y:10}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.6)"}},0.15);
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:1.0,ease:"power3.out"}},0.15);
tl.fromTo("#t2",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},1.6);
tl.fromTo("#cam",{{scale:1.08}},{{scale:1.02,duration:.45,ease:"power3.out"}},1.6);
tl.to("#title span",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},3.72);
{chr(10).join(js)}
tl.to("#cam",{{scale:1.0,duration:1.0,ease:"sine.inOut"}},76.5);
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
