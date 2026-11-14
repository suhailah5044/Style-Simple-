# Jana banyak video dari footage yang sama. Setiap variasi: hook/intro lain, animasi & SFX minimum.
# Guna: python3 variants.py <main.mov> [nama...]
import os,sys,json
from cut import make_footage

V={
 "v2_harga":dict(
  seg=[(85.45,90.29),(106.00,116.75),(152.30,162.30),(163.65,167.05),(197.30,200.50),(217.63,222.30),(206.30,211.25),(226.90,228.95)],
  intro="slide", hook=["Harga murah,","tapi nampak mahal."], hook_dur=4.6,
  txt=[(109.60,2.6,"Anti-Slip Sole","R","ui_blip"),(112.70,3.5,"Waterproof","L",None),(158.40,3.0,"Everyday Sandals","R",None),
       (163.75,3.1,"Comfortable Fit","L","ui_blip"),(197.40,2.8,"Easy to Clean","R",None)],
  broll=[(112.50,3.9,"broll2.mp4",0.8),(163.65,3.4,"broll2.mp4",8.5)],
  punch=[109.60]),
 "v3_recommend":dict(
  seg=[(217.63,222.30),(37.85,41.05),(96.55,102.55),(106.00,116.75),(163.65,167.05),(152.30,162.30),(197.30,200.50),(206.30,211.25),(226.90,228.95)],
  intro="type", kicker="REVIEW JUJUR", hook=["Serius recommend!"], hook_dur=4.4, hook_top=150,
  txt=[(96.60,2.6,"Simple &amp; Stylish","R",None),(99.75,2.6,"Budget Friendly","L","ui_blip"),(107.55,1.9,"Soft &amp; Flexible","R",None),
       (163.75,3.1,"Comfortable Fit","L",None),(197.40,2.8,"Easy to Clean","R","ui_blip")],
  broll=[(96.60,3.9,"broll1.mp4",0.3),(112.50,3.9,"broll2.mp4",13.0)],
  punch=[99.75]),
 "v4_selesa":dict(
  seg=[(163.65,167.05),(96.55,102.55),(106.00,116.75),(152.30,162.30),(197.30,200.50),(37.85,41.05),(217.63,222.30),(206.30,211.25),(226.90,228.95)],
  intro="blur", hook=["Pakai seharian,","tetap selesa."], hook_dur=3.3,
  txt=[(96.60,2.6,"Simple &amp; Stylish","L",None),(106.00,1.5,"Lightweight Design","R",None),(109.60,2.6,"Anti-Slip Sole","L","ui_blip"),
       (158.40,3.0,"Everyday Sandals","R",None),(197.40,2.8,"Easy to Clean","L",None)],
  broll=[(112.50,3.9,"broll2.mp4",4.5),(158.90,3.0,"broll1.mp4",4.0)],
  punch=[109.60]),
}

def T(SEG,src):
    o=0
    for a,b in SEG:
        if a<=src<=b: return round(o+src-a,2)
        o+=b-a
    raise ValueError(src)

def intro_html_js(c):
    h=c["hook"]; d=c["hook_dur"]; js=[]
    if c["intro"]=="slide":   # baris 1 masuk dari kiri, baris 2 naik, garis halus
        html='<div id="hook" class="clip" data-start="0" data-duration="%s"><div class="l" id="h1">%s</div><div class="l" id="h2">%s</div><i id="hbar"></i></div>'%(d,h[0],h[1])
        js+=['tl.fromTo("#h1",{opacity:0,x:-40},{opacity:1,x:0,duration:0.5,ease:"power3.out"},0.1);',
             'tl.fromTo("#h2",{opacity:0,y:18},{opacity:1,y:0,duration:0.5,ease:"power3.out"},1.6);',
             'tl.fromTo("#hbar",{scaleX:0},{scaleX:1,duration:0.6,ease:"power2.out"},2.6);']
    elif c["intro"]=="type":  # kicker jarang huruf + taip huruf demi huruf
        chars="".join(f'<span class="c">{ch if ch!=" " else "&nbsp;"}</span>' for ch in h[0])
        html='<div id="hook" class="clip" data-start="0" data-duration="%s"><div id="kick">%s</div><div class="l">%s</div></div>'%(d,c["kicker"],chars)
        js+=['tl.fromTo("#kick",{opacity:0,y:8},{opacity:1,y:0,duration:0.6,ease:"power2.out"},0.05);',
             'tl.fromTo("#hook .c",{opacity:0},{opacity:1,duration:0.01,stagger:0.045},0.35);']
    else:                     # blur-in perkataan
        html='<div id="hook" class="clip" data-start="0" data-duration="%s"><div class="l" id="h1">%s</div><div class="l" id="h2">%s</div></div>'%(d,h[0],h[1])
        js+=['tl.fromTo("#h1",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:0.6,ease:"sine.out"},0.1);',
             'tl.fromTo("#h2",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:0.6,ease:"sine.out"},1.3);']
    js.append(f'tl.to("#hook",{{opacity:0,duration:0.3,ease:"power1.in"}},{d-0.35:.2f});')
    return html,js

def build(name,c,src):
    P=f"variants/{name}"; os.makedirs(P+"/assets",exist_ok=True)
    for f in ["LexendMega.woff2","broll1.mp4","broll2.mp4"]:
        l=f"{P}/assets/{f}"
        if not os.path.exists(l): os.symlink(os.path.abspath(f"assets/{f}"),l)
    if not os.path.exists(P+"/sfx"): os.symlink(os.path.abspath("sfx"),P+"/sfx")
    SEG=[(a,round(a+round((b-a)*30)/30,4)) for a,b in c["seg"]]
    if not os.path.exists(P+"/assets/footage.mp4"): make_footage(src,SEG,P+"/assets/footage.mp4")
    DUR=round(sum(b-a for a,b in SEG),2)
    ih,js=intro_html_js(c); ih=ih.replace('id="hook"','id="hook" style="top:%dpx"'%c.get('hook_top',230),1); ov=[];au=[];br=[]
    au.append('<audio id="a_h" src="sfx/glass_ting.wav" data-start="0.1" data-duration="0.9" data-volume="0.22"></audio>')
    for i,(s0,d,t,side,sfx) in enumerate(c["txt"]):
        s=T(SEG,s0); e=s+d
        ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{d}"><span class="tx">{t}</span><i class="bar"></i></div>')
        if sfx: au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{s:.2f}" data-duration="0.8" data-volume="0.2"></audio>')
        js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{s});')
        js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{s+0.1:.2f});')
        js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,duration:0.25,ease:"power1.in"}},{e-0.27:.2f});')
    for p in c["punch"]:
        js.append(f'tl.fromTo("#cam",{{scale:1.05}},{{scale:1.0,duration:0.5,ease:"power2.out"}},{T(SEG,p)});')
    for j,(s0,d,f,off) in enumerate(c["broll"]):
        s=T(SEG,s0)
        br.append(f'<video id="b{j}" class="broll" src="assets/{f}" data-start="{s}" data-duration="{d}" data-media-start="{off}" data-volume="0" muted></video>')
        js.append(f'tl.fromTo("#b{j}",{{opacity:0}},{{opacity:1,duration:0.12}},{s});')
        js.append(f'tl.to("#b{j}",{{opacity:0,duration:0.12}},{s+d-0.12:.2f});')
    html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:3;opacity:0;}}
.word{{position:absolute;top:250px;width:420px;z-index:5;}}
.word.L{{left:150px;text-align:left;}} .word.R{{right:150px;text-align:right;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:28px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5);opacity:0;}}
.word .bar{{display:block;height:2px;width:48px;background:#fff;margin-top:10px;transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#hook{{position:absolute;top:230px;left:120px;right:120px;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;text-shadow:0 2px 8px rgba(0,0,0,.5);}}
#hook .l{{font-weight:700;font-size:38px;line-height:1.35;letter-spacing:-0.04em;opacity:1;}}
#hook #h1,#hook #h2{{opacity:0;}}
#hook #hbar{{display:block;width:72px;height:2px;background:#fff;margin:16px auto 0;transform:scaleX(0);}}
#hook #kick{{font-size:18px;font-weight:500;letter-spacing:.3em;margin-bottom:14px;opacity:0;}}
#hook .c{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  {chr(10).join("  "+x for x in br)}
  {ih}
  {chr(10).join("  "+x for x in ov)}
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
    open(P+"/index.html","w").write(html)
    return P,DUR

if __name__=="__main__":
    src=sys.argv[1]; names=sys.argv[2:] or list(V)
    for n in names: print(n,*build(n,V[n],src))
