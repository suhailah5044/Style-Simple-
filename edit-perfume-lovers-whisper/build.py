# Edit: Perfume "Lover's Whisper" — TikTok 9:16, gaya Stand Phone v2 (tulisan kecil putih, ruang kosong atas)
import json
MAP=json.load(open("map.json"))  # [src_start, src_end, out_start]
def T(src):
    for s,e,o in MAP:
        if s<=src<=e: return round(o+src-s,2)
    raise ValueError(src)
CUTS=[o for s,e,o in MAP][1:]
DUR=39.09

# [masa_sumber(ikut transcript), tamat_sumber, "Teks", posisi L|R|C, sfx, zoom in|out|punch]
O=[
 [4.72,5.40,"Mahal?","C","ui_blip","in"],
 [5.48,6.98,"Murah Sangat-Sangat!","C","coin","punch"],
 [15.02,16.20,"Memang Worth It","C","riser_shimmer","in"],
 [16.32,17.10,"Pergi Kerja","R","ui_tap","out"],
 [17.14,18.10,"Keluar Dating","R","ui_tap","in"],
 [18.18,19.08,"Memang Ngam!","R","sub_boom","punch"],
 [19.56,20.60,"Daily Perfume","L","ui_notif","in"],
 [20.72,22.96,"Sangat Sesuai","L","ui_confirm","out"],
 [24.30,25.36,"Wangi Sangat-Sangat!","C","glass_ting","punch"],
 [27.81,28.80,"Nak Spray Banyak Kali","L","swoosh","in"],
 [28.86,30.40,"Suka Bau Manis?","L","ui_blip","out"],
 [30.80,31.50,"You All Nak Try?","C","ui_notif","in"],
 [33.26,35.20,"Tengah Murah Sekarang","R","coin","punch"],
 [35.24,36.60,"Wajib Grab!","R","sub_boom","punch"],
 [37.18,38.40,"Harga Terlajak Murah","C","coin","punch"],
 [40.66,41.50,"Wangi Tahan Lama","L","glass_ting","in"],
 [41.66,43.25,"Dah Repeat Banyak Kali","L","riser_shimmer","out"],
]
# B-roll full screen (masa output), fade lembut
BR=[ ["broll1",T(12.20),2.45], ["broll2",T(38.48),2.2] ]
# Pop-up grafik fakta kecil (masa sumber)
POP=[ [11.92,14.60,"notes"], [38.48,40.40,"besar"] ]

VOL={"sub_boom":0.45,"swoosh":0.3,"riser_shimmer":0.35,"coin":0.35,"ui_tap":0.4}
ov=[];au=[];js=[]
for i,(s0,e0,t,side,sfx,z) in enumerate(O):
    s,e=T(s0),T(e0)
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.4)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22,scale:.92}},{{opacity:1,y:0,scale:1,duration:0.38,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.06,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    else:
        js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
# jump cut: selang-seli zoom halus supaya potongan nampak sengaja
for k,c in enumerate(CUTS):
    js.append(f'tl.set("#cut",{{scale:{1.05 if k%2==0 else 1.0}}},{c});')
br=[];
for n,(src,s,d) in enumerate(BR):
    br.append(f'<div id="br{n}" class="broll"><video id="brv{n}" src="assets/{src}.mp4" data-start="{s}" data-duration="{d}" data-has-audio="false" muted></video></div>')
    au.append(f'<audio id="abr{n}" src="sfx/swoosh.wav" data-start="{max(0,s-0.05):.2f}" data-duration="0.8" data-volume="0.28"></audio>')
    js.append(f'tl.fromTo("#br{n}",{{opacity:0}},{{opacity:1,duration:0.3,ease:"sine.out"}},{s});')
    js.append(f'tl.fromTo("#br{n} video",{{scale:1.04}},{{scale:1.12,duration:{d},ease:"none"}},{s});')
    js.append(f'tl.to("#br{n}",{{opacity:0,duration:0.35,ease:"sine.in"}},{s+d-0.35:.2f});')
# pop-up grafik
popd=[]
for n,(s0,e0,kind) in enumerate(POP):
    s,e=T(s0),T(e0)
    if kind=="notes":
        items=[("Sweet",T(12.36)),("Fruity",T(13.38)),("Feminine",T(14.14))]
        inner="".join(f'<span class="chip" id="p{n}c{j}"><i></i>{w}</span>' for j,(w,_) in enumerate(items))
        popd.append(f'<div id="p{n}" class="clip pop notes" data-start="{s}" data-duration="{round(e-s,2)}"><div class="kick">Bau Dia</div>{inner}</div>')
        for j,(w,t) in enumerate(items):
            js.append(f'tl.fromTo("#p{n}c{j}",{{opacity:0,scale:.4,y:14}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.6)"}},{t});')
            au.append(f'<audio id="ap{n}{j}" src="sfx/ui_tap.wav" data-start="{t:.2f}" data-duration="0.5" data-volume="0.4"></audio>')
        js.append(f'tl.fromTo("#p{n} .kick",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"expo.out"}},{s});')
    else:
        popd.append(f'<div id="p{n}" class="clip pop big" data-start="{s}" data-duration="{round(e-s,2)}"><div class="badge"><b>100</b><span>ML</span></div><div class="cap">Besar Pula Tu!</div></div>')
        js.append(f'tl.fromTo("#p{n} .badge",{{opacity:0,scale:.3,rotate:-12}},{{opacity:1,scale:1,rotate:0,duration:0.45,ease:"back.out(2.2)"}},{s});')
        js.append(f'tl.fromTo("#p{n} .cap",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.35,ease:"expo.out"}},{s+0.15:.2f});')
        au.append(f'<audio id="ap{n}" src="sfx/sub_boom.wav" data-start="{s:.2f}" data-duration="1.0" data-volume="0.4"></audio>')
    js.append(f'tl.to("#p{n}",{{opacity:0,y:-10,duration:0.25,ease:"power2.in"}},{e-0.27:.2f});')

H1,H2,H3=T(7.36),T(8.98),T(9.78)
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Italianno";src:url("assets/Italianno.woff2") format("woff2");}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam,#cut{{position:absolute;inset:0;transform-origin:50% 40%;}}
#cut video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;inset:0;z-index:4;overflow:hidden;opacity:0;}}
.broll video{{width:100%;height:100%;object-fit:cover;display:block;transform-origin:50% 45%;}}
/* Safe zone: atas 250px+, tepi 150px, tak masuk bawah 1500px */
.word{{position:absolute;top:255px;width:440px;z-index:6;}}
.word.L{{left:150px;text-align:left;}}
.word.R{{right:150px;text-align:right;}}
.word.C{{left:0;right:0;width:auto;text-align:center;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#ff8fc8;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
.word.C .bar{{margin:10px auto 0;}}
#title{{position:absolute;top:250px;left:0;right:0;text-align:center;z-index:7;color:#fff;}}
#title .k{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:44px;letter-spacing:-0.04em;opacity:0;
  text-shadow:0 3px 10px rgba(0,0,0,.5);}}
#title .k.pink{{color:#ff8fc8;}}
#title .s{{display:block;margin-top:8px;font-family:"Italianno",cursive;font-size:64px;line-height:1;opacity:0;text-shadow:0 2px 8px rgba(0,0,0,.5);}}
.pop{{position:absolute;z-index:6;}}
.pop.notes{{top:255px;left:0;right:0;text-align:center;}}
.pop.notes .kick{{font-family:"Italianno",cursive;font-size:54px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.5);margin-bottom:10px;opacity:0;}}
.chip{{display:inline-flex;align-items:center;gap:8px;margin:0 6px;padding:8px 16px;border-radius:999px;background:rgba(255,255,255,.92);
  font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:20px;letter-spacing:-0.03em;color:#2b1430;opacity:0;box-shadow:0 4px 14px rgba(0,0,0,.25);}}
.chip i{{width:10px;height:10px;border-radius:50%;background:#ff5fae;display:inline-block;}}
#p0c1 i{{background:#ffb347;}} #p0c2 i{{background:#c58cff;}}
.pop.big{{top:250px;right:150px;text-align:center;}}
.badge{{width:130px;height:130px;border-radius:50%;background:#fff;color:#e2368d;display:flex;flex-direction:column;align-items:center;justify-content:center;
  box-shadow:0 6px 20px rgba(0,0,0,.3);font-family:"Lexend Mega",sans-serif;opacity:0;margin:0 auto;}}
.badge b{{font-size:44px;letter-spacing:-0.06em;line-height:1;}} .badge span{{font-size:18px;font-weight:600;}}
.cap{{margin-top:12px;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:22px;letter-spacing:-0.03em;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.5);opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><div id="cut"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div></div>
  {chr(10).join("  "+x for x in br)}
  <div id="title" class="clip" data-start="0" data-duration="{T(10.9)}"><span class="k" id="t1">100ML</span> <span class="k pink" id="t2">JE?!</span><span class="s" id="t3">harga tak masuk akal langsung</span></div>
  {chr(10).join("  "+x for x in ov)}
  {chr(10).join("  "+x for x in popd)}
  <audio id="bgm" src="sfx/bgm_duck.wav" data-start="0" data-duration="{DUR}" data-volume="0.75"></audio>
  <audio id="a_h1" src="sfx/sub_boom.wav" data-start="{H1}" data-duration="1.0" data-volume="0.5"></audio>
  <audio id="a_h2" src="sfx/ui_notif.wav" data-start="{H2}" data-duration="0.9" data-volume="0.35"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);tl.set("#cut",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.35,ease:"expo.out"}},{H1});
tl.fromTo("#cam",{{scale:1.14}},{{scale:1.03,duration:.5,ease:"power3.out"}},{H1});
tl.fromTo("#t2",{{opacity:0,scale:.4,rotate:-10}},{{opacity:1,scale:1,rotate:0,duration:.4,ease:"back.out(3)"}},{H1+0.45:.2f});
tl.fromTo("#t3",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},{H2});
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:.45,ease:"power3.out"}},{H3});
tl.to("#title > *",{{opacity:0,y:-10,duration:.22,ease:"power2.in"}},{T(10.9)-0.24:.2f});
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok")
