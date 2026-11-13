# Edit: Baju Tidur Cute — TikTok 9:16, tulisan kecil putih di ruang kosong atas (tak tutup baju)
import json
MAP=json.load(open("map.json"))  # [src_start, src_end, out_start]
def T(src):
    for s,e,o in MAP:
        if s<=src<=e: return round(o+src-s,2)
    raise ValueError(src)
CUTS=[o for s,e,o in MAP][1:]
DUR=49.9

# [masa_sumber, tamat_sumber, "Teks", L|R|C, sfx, zoom in|out|punch]
O=[
 [45.5,46.40,"Cantik, Cute!","C","glass_ting","punch"],
 [3.15,4.22,"Tak Panas Langsung","C","ui_confirm","in"],
 [6.86,7.90,"Pyjamas Ni...","C","ui_blip","out"],
 [7.98,10.20,"Selesa Waktu Tidur","C","ui_notif","in"],
 [10.32,12.30,"Suka Material Dia","C","ui_tap","out"],
 [20.53,21.40,"Cantik!","C","glass_ting","punch"],
 [21.58,23.80,"Ambil Saiz 2XL / 3XL","C","ui_tap","out"],
 [30.10,31.50,"Pakai Nampak Cute","C","riser_shimmer","in"],
 [33.66,37.20,"Saiz Kecil → Besar","C","swoosh","out"],
 [37.30,40.60,"Cari Baju Tidur Selesa?","C","ui_blip","in"],
 [40.76,41.30,"Grab This One!","C","sub_boom","punch"],
 [41.43,42.95,"","C","",""],  # placeholder (hook dikendali #title)
 [46.62,48.40,"Set Macam Ni Biasa Mahal","C","ui_notif","in"],
 [48.48,51.20,"Ni Murah Gila!","C","coin","punch"],
 [51.82,53.90,"Comel & Cantik","C","glass_ting","out"],
 [57.32,58.10,"Memang Best!","C","sub_boom","punch"],
 [58.16,59.30,"Tak Panas Langsung","C","ui_confirm","in"],
 [59.38,60.04,"Pergi Grab!","C","coin","punch"],
]
O=[x for x in O if x[2]]
# B-roll full screen (masa output, tempoh) — sementara: close-up dari footage sendiri
BR=[ ["broll1",T(12.40),2.3,"Sangat Lembut"], ["broll2",T(28.10),2.4,"Ada Ribbon Depan"] ]
# Pop-up grafik fakta (masa sumber)
POP=[ [15.96,20.30,"set"], [31.58,33.60,"warna"] ]

VOL={"sub_boom":0.45,"swoosh":0.3,"riser_shimmer":0.35,"coin":0.35,"ui_tap":0.4}
ov=[];au=[];js=[]
def word(i,s,e,t,side,sfx,z):
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
    if sfx: au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.4)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22,scale:.92}},{{opacity:1,y:0,scale:1,duration:0.38,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.06,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    elif z=="out":
        js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
for i,(s0,e0,t,side,sfx,z) in enumerate(O):
    word(i,T(s0),T(e0),t,side,sfx,z)
for k,c in enumerate(CUTS):
    js.append(f'tl.set("#cut",{{scale:{1.05 if k%2==0 else 1.0}}},{c});')
br=[]
for n,(src,s,d,label) in enumerate(BR):
    br.append(f'<div id="br{n}" class="broll"><video id="brv{n}" src="assets/{src}.mp4" data-start="{s}" data-duration="{d}" data-has-audio="false" muted></video></div>')
    au.append(f'<audio id="abr{n}" src="sfx/swoosh.wav" data-start="{max(0,s-0.05):.2f}" data-duration="0.8" data-volume="0.28"></audio>')
    js.append(f'tl.fromTo("#br{n}",{{opacity:0}},{{opacity:1,duration:0.3,ease:"sine.out"}},{s});')
    js.append(f'tl.fromTo("#br{n} video",{{scale:1.03}},{{scale:1.1,duration:{d},ease:"none"}},{s});')
    js.append(f'tl.to("#br{n}",{{opacity:0,duration:0.35,ease:"sine.in"}},{s+d-0.35:.2f});')
    word(100+n,round(s+0.15,2),round(s+d-0.1,2),label,"C","glass_ting","")
popd=[]
for n,(s0,e0,kind) in enumerate(POP):
    s,e=T(s0),T(e0)
    if kind=="set":
        items=[("Seluar Panjang",T(16.56)),("Baju",T(19.68))]
        inner="".join(f'<span class="chip" id="p{n}c{j}"><i></i>{w}</span>' for j,(w,_) in enumerate(items))
        popd.append(f'<div id="p{n}" class="clip pop notes" data-start="{s}" data-duration="{round(e-s,2)}"><div class="kick">Dapat</div>{inner}</div>')
    else:
        items=[("",T(31.98)),("",T(32.14)),("",T(32.30))]
        inner="".join(f'<span class="dot" id="p{n}c{j}"></span>' for j in range(3))
        popd.append(f'<div id="p{n}" class="clip pop notes" data-start="{s}" data-duration="{round(e-s,2)}"><div class="kick">Ada 2–3 Warna Lagi</div>{inner}</div>')
    for j,(w,t) in enumerate(items):
        js.append(f'tl.fromTo("#p{n}c{j}",{{opacity:0,scale:.4,y:14}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.6)"}},{t});')
        au.append(f'<audio id="ap{n}{j}" src="sfx/ui_tap.wav" data-start="{t:.2f}" data-duration="0.5" data-volume="0.4"></audio>')
    js.append(f'tl.fromTo("#p{n} .kick",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"expo.out"}},{s});')
    js.append(f'tl.to("#p{n}",{{opacity:0,y:-10,duration:0.25,ease:"power2.in"}},{e-0.27:.2f});')

H1,H2,HE=T(41.6),T(43.22),T(44.80)
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
.broll video{{width:100%;height:100%;object-fit:cover;display:block;transform-origin:50% 50%;}}
/* Safe zone TikTok/Reels: atas 250px+, tepi 150px, bawah 1500px+ dikosongkan */
.word{{position:absolute;top:255px;width:440px;z-index:6;}}
.word.L{{left:150px;text-align:left;}}
.word.R{{right:150px;text-align:right;}}
.word.C{{left:150px;right:150px;width:auto;text-align:center;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.55),0 0 2px rgba(0,0,0,.4);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#ff8fd0;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
.word.C .bar{{margin:10px auto 0;}}
#title{{position:absolute;top:250px;left:0;right:0;text-align:center;z-index:7;color:#fff;}}
#title .k{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:40px;letter-spacing:-0.04em;opacity:0;text-shadow:0 3px 10px rgba(0,0,0,.55);}}
#title .k.pink{{color:#ff8fd0;margin-left:14px;}}
#title .s{{display:block;margin-top:6px;font-family:"Italianno",cursive;font-size:62px;line-height:1;opacity:0;text-shadow:0 2px 8px rgba(0,0,0,.55);}}
.pop{{position:absolute;z-index:6;}}
.pop.notes{{top:255px;left:0;right:0;text-align:center;}}
.pop.notes .kick{{font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:26px;letter-spacing:-0.03em;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.55);margin-bottom:12px;opacity:0;}}
.chip{{display:inline-flex;align-items:center;gap:8px;margin:0 6px;padding:8px 16px;border-radius:999px;background:rgba(255,255,255,.92);
  font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:19px;letter-spacing:-0.03em;color:#3a0f2e;opacity:0;box-shadow:0 4px 14px rgba(0,0,0,.25);}}
.chip i{{width:10px;height:10px;border-radius:50%;background:#c2187a;display:inline-block;}}
.dot{{display:inline-block;width:34px;height:34px;border-radius:50%;margin:0 7px;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,.3);opacity:0;}}
#p1c0{{background:#c2187a;}} #p1c1{{background:#1d2b4f;}} #p1c2{{background:#f3b6c8;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><div id="cut"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div></div>
  {chr(10).join("  "+x for x in br)}
  <div id="title" class="clip" data-start="0" data-duration="{HE}"><span class="k" id="t1">MENYESAL</span> <span class="k pink" id="t2">BELI SATU!</span><span class="s" id="t3">patutnya beli banyak lagi</span></div>
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
tl.fromTo("#t2",{{opacity:0,scale:.4,rotate:-10}},{{opacity:1,scale:1,rotate:0,duration:.4,ease:"back.out(3)"}},{H1+0.5:.2f});
tl.fromTo("#t3",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},{H2});
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:.45,ease:"power3.out"}},{H2});
tl.to("#title > *",{{opacity:0,y:-10,duration:.22,ease:"power2.in"}},{HE-0.24:.2f});
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok")
