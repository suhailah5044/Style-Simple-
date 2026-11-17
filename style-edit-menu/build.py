# Style "Menu Card" — tajuk serif elegan 3 lapis (atas kecil kiri · besar tengah · bawah kecil kanan)
# ikut rujukan kafe. Animasi "zap-zup" lembut ~30%: blur+fade masuk, tolak zoom 3%, swish perlahan.
FOOT=59.73
END=2.6
DUR=round(FOOT+END,2)
# [mula, atas, besar, bawah, sfx_tambahan]
S=[
 [0.0,  "Baju Raya",   "Bawah RM100",  "Tapi Nampak Mahal", "glint"],
 [5.42, "Jangan",      "Sold Out",     "Macam Tahun Lepas", ""],
 [9.6,  "Pilihan",     "Kurung Raya",  "Tengok Sendiri", ""],
 [13.22,"Sangat",      "Cantik",       "Memang Love", ""],
 [19.98,"Cutting",     "Real",         "Efek Badan Kurus", ""],
 [25.54,"Material",    "Chiffon",      "Siap Berlining", ""],
 [28.9, "Ada Pesak",   "Tersorok",     "Jatuh Flowy", ""],
 [34.94,"Kain",        "Soft Brocade", "Tak Jarang · Tak Gatal", ""],
 [40.9, "Ringan &",    "Selesa",       "Sangat-Sangat Cantik", ""],
 [43.6, "Kakak Suka",  "Nampak Kurus", "Sebab Cutting Dia", ""],
 [46.3, "Belakang",    "Berzip",       "Lengan Lebar", ""],
 [50.0, "Tinggi 165cm","Ngam-Ngam",    "Cantik Jatuhnya", ""],
 [53.44,"Harga",       "Bawah RM100",  "Serius Murah", "glint"],
 [57.84,"Cepat",       "Grab",         "Sebelum Sold Out", ""],
]
END_CARD=("Kurung","Raya","Bawah RM100")

def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
items=[];js=[];au=[]
def audio(src,t0,vol,d=1.0):
    au.append(f'<audio id="s{len(au)}" src="sfx/{src}.wav" data-start="{max(0,t0):.2f}" data-duration="{d}" data-volume="{vol}"></audio>')

PUSH=0.03   # 30%: zoom kecil
for i,(s,top,big,bot,extra) in enumerate(S):
    e=S[i+1][0] if i+1<len(S) else FOOT
    d=round(e-s,2)
    items.append(f'<div id="k{i}" class="clip card" style="top:{40 if i==0 else 95}px" data-start="{s}" data-duration="{d}"><div class="lk">'
                 f'<div class="t">{esc(top)}</div><div class="b">{esc(big)}</div><div class="u">{esc(bot)}</div></div></div>')
    # masuk: blur + fade + naik sikit, berperingkat
    js.append(f'tl.fromTo("#k{i} .t,#k{i} .b,#k{i} .u",{{opacity:0,y:18,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.55,ease:"power3.out",stagger:.09}},{s+0.05:.2f});')
    js.append(f'tl.fromTo("#k{i} .b",{{scaleX:1.05}},{{scaleX:1,duration:.8,ease:"power3.out"}},{s+0.05:.2f});')
    # keluar: blur + naik
    js.append(f'tl.to("#k{i} .lk",{{opacity:0,y:-10,filter:"blur(6px)",duration:.25,ease:"power2.in"}},{e-0.27:.2f});')
    # kamera: "zup" lembut (3% + blur nipis) kemudian hanyut perlahan
    base=1.0 if i%2==0 else 1.03
    drift=base+0.025 if i%2==0 else base-0.025
    js.append(f'tl.fromTo("#cam",{{scale:{base+PUSH:.3f},filter:"blur(3px)"}},{{scale:{base},filter:"blur(0px)",duration:.4,ease:"power2.out",immediateRender:false}},{s});')
    js.append(f'tl.to("#cam",{{scale:{drift:.3f},duration:{max(0.1,d-0.45):.2f},ease:"sine.inOut"}},{s+0.4:.2f});')
    if i>0: audio("swish",s-0.12,0.25,0.5)
    if extra: audio(extra,s+0.15,0.22,0.9)

# penutup: pudar ke hitam + kad akhir
js.append(f'tl.fromTo("#fade",{{opacity:0}},{{opacity:1,duration:.7,ease:"power1.inOut"}},{FOOT-0.2:.2f});')
js.append(f'tl.fromTo("#endk .t,#endk .b,#endk .u",{{opacity:0,y:18,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.6,ease:"power3.out",stagger:.12}},{FOOT+0.5:.2f});')
audio("glint",FOOT+0.55,0.25,0.9)
t_,b_,u_=END_CARD
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Playfair Display";src:url("assets/PlayfairDisplay.woff2") format("woff2");font-weight:400 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 30%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.card{{position:absolute;left:0;right:0;top:95px;text-align:center;z-index:5;}}
.lk{{display:inline-block;color:#fff;font-family:"Playfair Display",serif;font-variant-numeric:lining-nums;font-feature-settings:"lnum" 1;text-shadow:0 2px 14px rgba(0,0,0,.35),0 1px 3px rgba(0,0,0,.35);}}
.lk .t{{text-align:left;font-size:50px;font-weight:500;line-height:1;margin-bottom:-4px;padding-left:6px;}}
.lk .b{{font-size:124px;font-weight:600;line-height:1.02;letter-spacing:0;white-space:nowrap;}}
.lk .u{{text-align:right;font-size:44px;font-weight:500;line-height:1.1;padding-right:6px;}}
.lk .t,.lk .b,.lk .u{{opacity:0;}}
#fade{{position:absolute;inset:0;background:#000;opacity:0;z-index:8;}}
#endk{{position:absolute;left:0;right:0;top:780px;text-align:center;z-index:9;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{FOOT}" data-has-audio="true" data-volume="1"></video></div>
{chr(10).join("  "+x for x in items)}
  <div id="fade"></div>
  <div id="endk" class="clip" data-start="{FOOT}" data-duration="{END}"><div class="lk"><div class="t">{t_}</div><div class="b">{b_}</div><div class="u">{u_}</div></div></div>
{chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok",DUR,len(au),"audio")
