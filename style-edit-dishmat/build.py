from edit import *
# Overlay subtitle: [masa sumber ucapan, teks, sfx, zoom]  (tiada overlay untuk 'bakul kuning')
O=[[9.22,"Banyak Kegunaan","prompt_up","in"],
 [12.1,"Lepas Basuh Pinggan","prompt_soft","out"],
 [14.5,"Countertop Basah Lencun?","click_soft","in"],
 [16.42,"Dish Drying Mat","ding_usp","punch"],
 [31.38,"Thickened Silicone","prompt_up","out"],
 [33.22,"Multi-Purpose Kitchen Mat","pop_bubble","in"],
 [36.6,"Sayur &amp; Buah Pun Boleh","prompt_soft","out"],
 [42.32,"Semua Boleh Letak","ding_usp","punch"],
 [46.26,"Tak Rosak, Tak Berkulat","prompt_up","in"],
 [53.08,"Practical Kitchen Essential","pop_bubble","out"],
 [55.96,"","ding_usp","punch"],
 [57.32,"Design Kemas","prompt_soft","in"],
 [59.04,"Tak Perlu Beli Banyak","prompt_up","out"],
 [76.96,"Lepas Basuh, Terus Letak","pop_bubble","in"],
 [79.48,"Keep Your Countertop Neat","prompt_soft","out"],
 [82.98,"Quick Water Drainage","ding_usp","punch"],
 [89.52,"Non-Slip Surface","prompt_up","in"],
 [93.3,"Large Size 50 × 40cm","impact_soft","punch"],
 [94.4,"Highly Recommended","sparkle_up","out"],
 [96.46,"Easy to Clean","prompt_soft","in"],
 [104.32,"Harga Serius Murah!","cash_tick","punch"],
 [107.66,"Upgrade Your Kitchen Today!","sparkle_up","out"],
 [111.54,"Cuci Je, Settle!","pop_bubble","in"]]
VOL={"prompt_up":.32,"prompt_soft":.34,"pop_bubble":.38,"click_soft":.4,"ding_usp":.26,"impact_soft":.45,"sparkle_up":.24,"cash_tick":.26,"whoosh_air":.3,"tingting":.3}
HOOK_END=2.9
cuts=[out_t(s) for (s,e),_ in CUT]          # masuk cutaway
backs=[out_t(e) for (s,e),_ in CUT if e<SEGS[-1][1]]
FB=[0.0,cuts[0],cuts[1],cuts[4]]              # frame break
ov=[];au=[];js=[]
times=[max(out_t(s),HOOK_END+0.12) for s,*_ in O]
for i,(s,txt,sfx,z) in enumerate(O):
    a=times[i]; nxt=times[i+1] if i+1<len(O) else DUR
    b=round(min(a+2.3,nxt-0.08,DUR-0.05),2); d=round(b-a,2)
    words=" ".join(f'<span class="w">{w}</span>' for w in txt.split(" "))
    if not txt:
        au.append(f'<audio id="x{i}" src="sfx/{sfx}.wav" data-start="{a:.2f}" data-duration="1.2" data-volume="{VOL[sfx]}"></audio>')
        js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:.5,ease:"power3.out"}},{a});'); continue
    ov.append(f'<div id="s{i}" class="clip sub" data-start="{a}" data-duration="{d}"><i class="dot"></i><span class="tx">{words}</span></div>')
    au.append(f'<audio id="x{i}" src="sfx/{sfx}.wav" data-start="{max(0,a-0.03):.2f}" data-duration="1.2" data-volume="{VOL[sfx]}"></audio>')
    js.append(f'tl.fromTo("#s{i} .dot",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:"back.out(3)"}},{a});')
    js.append(f'tl.fromTo("#s{i} .w",{{opacity:0,y:14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.42,ease:"power3.out",stagger:.06}},{a+0.04:.2f});')
    js.append(f'tl.to("#s{i}",{{opacity:0,y:-8,filter:"blur(6px)",duration:.2,ease:"power2.in"}},{b-0.21:.2f});')
    if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:.5,ease:"power3.out"}},{a});')
    elif z=="in": js.append(f'tl.to("#cam",{{scale:1.07,duration:{d},ease:"sine.inOut"}},{a});')
    else: js.append(f'tl.to("#cam",{{scale:1.0,duration:{d},ease:"sine.inOut"}},{a});')
fb_html=[]
for k,t0 in enumerate(FB):
    for j,(top,bot,dx) in enumerate([(0,62,-46),(38,30,52),(70,0,-34)]):
        fb_html.append(f'<div id="fb{k}_{j}" class="fb" style="clip-path:inset({top}% 0 {bot}% 0)"><video id="fbv{k}_{j}" src="assets/footage.mp4" data-start="{t0}" data-duration="0.3" data-media-start="{t0}" muted></video></div>')
        js.append(f'tl.set("#fb{k}_{j}",{{opacity:1}},{t0});tl.fromTo("#fb{k}_{j}",{{x:{dx},scale:1.04}},{{x:0,scale:1,duration:.26,ease:"expo.out"}},{t0});tl.set("#fb{k}_{j}",{{opacity:0}},{t0+0.29:.2f});')
for t0 in cuts: au.append(f'<audio id="wh{t0:.0f}_{int(t0*100)}" src="sfx/whoosh_air.wav" data-start="{max(0,t0-0.28):.2f}" data-duration="0.7" data-volume="{VOL["whoosh_air"]}"></audio>')
for t0 in backs: au.append(f'<audio id="ck_{int(t0*100)}" src="sfx/click_soft.wav" data-start="{t0:.2f}" data-duration="0.2" data-volume="0.25"></audio>')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
video{{width:100%;height:100%;object-fit:cover;display:block;}}
.fb{{position:absolute;inset:0;z-index:3;opacity:0;}}
.sub{{position:absolute;top:255px;left:90px;right:90px;z-index:5;display:flex;align-items:center;justify-content:center;gap:14px;}}
.sub .dot{{width:7px;height:7px;border-radius:50%;background:#fff;box-shadow:0 0 6px rgba(255,255,255,.7),0 1px 3px rgba(0,0,0,.4);flex:none;}}
.sub .tx{{font-family:"Lexend Mega",sans-serif;font-weight:500;font-size:26px;line-height:1.3;letter-spacing:-0.035em;color:#fff;text-align:center;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);}}
.sub .w{{display:inline-block;margin:0 .14em;opacity:0;}}
#hook{{position:absolute;top:215px;left:0;right:0;z-index:6;text-align:center;color:#fff;font-family:"Lexend Mega",sans-serif;text-shadow:0 2px 8px rgba(0,0,0,.5);}}
#h1{{font-weight:600;font-size:40px;letter-spacing:-0.04em;}}
#h1 span{{display:inline-block;opacity:0;}}
#hl{{width:64px;height:2px;background:#fff;margin:16px auto 14px;transform:scaleX(0);box-shadow:0 1px 3px rgba(0,0,0,.4);}}
#h2{{font-weight:300;font-size:21px;letter-spacing:-0.02em;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video>
  {chr(10).join("  "+x for x in fb_html)}
  </div>
  <div id="hook" class="clip" data-start="0" data-duration="{HOOK_END}"><div id="h1">{"".join(f"<span>{c if c!=' ' else '&nbsp;'}</span>" for c in "Silicone Dish Mat")}</div><div id="hl"></div><div id="h2">Cepat kering &amp; mudah guna</div></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="bgm" src="sfx/bgm_lofi.wav" data-start="0" data-duration="{DUR}" data-volume="0.15" data-fade-out="1.5"></audio>
  <audio id="h_imp" src="sfx/impact_soft.wav" data-start="0.02" data-duration="0.9" data-volume="0.4"></audio>
  <audio id="h_ting" src="sfx/tingting.wav" data-start="0.35" data-duration="1.0" data-volume="0.3"></audio>
  <audio id="h_pr" src="sfx/prompt_soft.wav" data-start="1.05" data-duration="0.4" data-volume="0.3"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:.45,ease:"power3.out"}},0);
tl.fromTo("#h1 span",{{opacity:0,y:18,scale:.7}},{{opacity:1,y:0,scale:1,duration:.4,ease:"back.out(2.2)",stagger:.025}},0.3);
tl.fromTo("#hl",{{scaleX:0}},{{scaleX:1,duration:.45,ease:"expo.out"}},0.85);
tl.fromTo("#h2",{{opacity:0,y:10,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"power3.out"}},1.05);
tl.to("#cam",{{scale:1.06,duration:2.4,ease:"sine.inOut"}},0.46);
tl.to("#hook",{{opacity:0,y:-10,filter:"blur(6px)",duration:.25,ease:"power2.in"}},{HOOK_END-0.27});
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("DUR",DUR,"cuts",cuts)
for i,t in enumerate(times): print(f"{t:6.2f} {O[i][1]}")
