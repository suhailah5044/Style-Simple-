# Variasi hook dari footage yang sama. Semua masa di sini = masa SOURCE (in.mov).
# python3 variants.py <path/in.mov>  -> variants/<id>/index.html + assets/footage.mp4
import os, sys, subprocess, json
SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

# Overlay asal (masa source): [s, e, tajuk, sub, side, sfx, zoom]
O = [
 [7.45,9.65,"Budget-Friendly","Bawah RM3, lagi murah dari teh ais","C","coin","punch"],
 [10.0,12.0,"Stainless Steel","Silver clean, vibe minimalist","C","glass_ting","in"],
 [12.55,16.0,"Grip Dia Ketat","Batang mop tak melurut jatuh","C","ui_tap","none"],
 [18.95,21.6,"Pilihan 2–5 Hook","Ikut berapa batang nak sangkut","C","ui_blip","in"],
 [21.8,23.45,"No Drill, No Drama","Lekat je, dinding tak rosak","C","sub_boom","punch"],
 [26.77,29.67,"Hygiene Level Up","Berus tak kena lantai, cepat kering","C","ui_confirm","none"],
 [32.57,36.1,"Gam Super Kuat","Confirm tak tercabut","C","sub_boom","none"],
 [37.67,41.55,"Tekan Beg Kuning","Hook stainless toilet","L","riser_shimmer","in"],
]
BR = [[12.3,"broll1"],[32.32,"broll2"]]   # [src start, file], 4s setiap satu

V = {
 "A_murah": dict(
   segs=[(7.45,9.72,1),(0,7.45,0),(9.72,23.5,0),(26.667,44.6,0)],
   anim="pop", hookpos="C",
   kin=[[7.48,"Serius,",1,0,0],[7.92,"harga dia",1,0,0],[8.54,"sangat-sangat",2,0,0],[9.0,"MURAH.",2,1,0]],
   hsfx=[[7.46,"ui_tap",.35],[9.0,"coin",.4]], broll=BR),
 "B_sakitmata": dict(
   segs=[(3.167,5.22,1),(0,3.167,1),(5.22,23.5,0),(26.667,44.6,0)],
   anim="slide", hookpos="C",
   kin=[[3.28,"Sangkut macam ni…",1,0,0],[4.04,"sakit mata",2,1,0],
        [0.0,"Bila dah sangkut,",1,0,1],[0.9,"barulah",2,0,1],[1.2,"cantik!",2,1,1]],
   hsfx=[[3.26,"swoosh",.3],[4.02,"sub_boom",.45],[0.0,"ui_notif",.4],[1.18,"glass_ting",.4]], broll=BR),
 "C_gamkuat": dict(
   segs=[(32.367,36.167,1),(0,23.5,0),(26.667,32.367,0),(36.167,44.6,0)],
   anim="blur", hookpos="C",
   kin=[[32.58,"Takkan",1,0,0],[32.92,"tercabut!",1,1,0],[33.96,"gam dia",2,0,0],[35.24,"kuat gila",2,1,0]],
   hsfx=[[32.56,"ui_tap",.35],[32.9,"sub_boom",.5],[35.22,"sub_boom",.45]],
   broll=[[12.3,"broll1"],[29.9,"broll2"]]),
 "D_tahan": dict(
   segs=[(41.6,44.6,1),(0,23.5,0),(26.667,41.6,0)],
   anim="drop", hookpos="L",
   kin=[[41.6,"Rata-rata cakap…",1,0,0],[42.58,"hook ni",2,0,0],[43.24,"MEMANG",3,1,0],[43.72,"TAHAN!",3,1,0]],
   hsfx=[[41.58,"ui_notif",.4],[43.22,"sub_boom",.45],[43.7,"riser_shimmer",.35]], broll=BR),
}
VOL={"sub_boom":0.5,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
ANIM={ # from-state untuk teks masuk
 "pop":  ('{opacity:0,y:22,scale:.85}','{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2.2)"}'),
 "slide":('{opacity:0,x:-40}','{opacity:1,x:0,duration:0.45,ease:"expo.out"}'),
 "blur": ('{opacity:0,filter:"blur(12px)",scale:1.15}','{opacity:1,filter:"blur(0px)",scale:1,duration:0.45,ease:"power3.out"}'),
 "drop": ('{opacity:0,y:-34,scaleX:1.12}','{opacity:1,y:0,scaleX:1,duration:0.5,ease:"back.out(1.6)"}'),
}

def mk(vid, cfg):
    d = os.path.join(HERE, "variants", vid); os.makedirs(d+"/assets", exist_ok=True)
    for f in ["LexendMega.woff2","broll1.mp4","broll2.mp4"]:
        p=f"{d}/assets/{f}"
        if not os.path.exists(p): os.symlink(f"{HERE}/assets/{f}", p)
    if not os.path.exists(d+"/sfx"): os.symlink(HERE+"/sfx", d+"/sfx")
    segs=cfg["segs"]; outs=[]; t=0
    for a,b,h in segs: outs.append(t); t+=b-a
    DUR=round(t,2)
    def m(s, hook_ok=False, end=None):
        for (a,b,h),o in zip(segs,outs):
            if a<=s<b and (hook_ok or not h):
                e=None if end is None else o+min(end,b)-a
                return round(o+s-a,2), (None if e is None else round(e,2))
        return None, None
    # footage
    fc=[];cat=""
    for i,(a,b,h) in enumerate(segs):
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03[a{i}]")
        cat+=f"[v{i}][a{i}]"
    fc.append(f"{cat}concat=n={len(segs)}:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",";".join(fc),"-map","[v]","-map","[a]",
        "-c:v","libx264","-crf","15","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
        "-r","30","-c:a","aac","-b:a","192k",f"{d}/assets/footage.mp4"],check=True)
    fr,to=ANIM[cfg["anim"]]
    ov=[];au=[];js=[];br=[]
    for i,(s,e,tt,sub,side,sfx,z) in enumerate(O):
        s2,e2=m(s,end=e)
        if s2 is None: continue
        ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s2}" data-duration="{round(e2-s2,2)}"><span class="tx">{tt}</span><span class="sb">{sub}</span><i class="bar"></i></div>')
        au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s2-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.45)}"></audio>')
        js.append(f'tl.fromTo("#w{i} .tx",{fr},{to},{s2});')
        js.append(f'tl.fromTo("#w{i} .sb",{{opacity:0,y:12}},{{opacity:.92,y:0,duration:0.38,ease:"expo.out"}},{s2+0.12:.2f});')
        js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s2+0.08:.2f});')
        js.append(f'tl.to("#w{i} .tx,#w{i} .sb,#w{i} .bar",{{opacity:0,y:-10,duration:0.22,ease:"power2.in"}},{e2-0.24:.2f});')
        if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s2});')
        elif z=="in":
            js.append(f'tl.to("#cam",{{scale:1.06,duration:{round(e2-s2-0.1,2)},ease:"sine.inOut"}},{s2});')
            js.append(f'tl.to("#cam",{{scale:1.0,duration:0.4,ease:"sine.inOut"}},{e2-0.1:.2f});')
    # punch kecil di setiap sambungan supaya smooth
    for o in outs[1:]:
        js.append(f'tl.fromTo("#cam",{{scale:1.07}},{{scale:1.0,duration:0.4,ease:"power3.out"}},{o:.2f});')
    for j,(s,f) in enumerate(cfg["broll"]):
        s2,_=m(s)
        if s2 is None: continue
        dd=min(4.0,DUR-s2-0.3)
        br.append(f'<video id="b{j}" class="clip broll" src="assets/{f}.mp4" data-start="{s2}" data-duration="{dd:.2f}" data-has-audio="false" muted></video>')
        au.append(f'<audio id="ab{j}" src="sfx/swoosh.wav" data-start="{max(0,s2-0.05):.2f}" data-duration="1.0" data-volume="0.25"></audio>')
        js.append(f'tl.fromTo("#b{j}",{{opacity:0,scale:1.08}},{{opacity:1,scale:1.04,duration:0.35,ease:"sine.out"}},{s2});')
        js.append(f'tl.to("#b{j}",{{scale:1.0,duration:{dd-0.35:.2f},ease:"sine.out"}},{s2+0.35:.2f});')
        js.append(f'tl.to("#b{j}",{{opacity:0,duration:0.35,ease:"sine.in"}},{s2+dd-0.35:.2f});')
    # hook kinetic, ikut kumpulan (g)
    groups={}
    for k,(s,w,ln,big,g) in enumerate(cfg["kin"]):
        groups.setdefault(g,[]).append((k,m(s,True)[0],w,ln,big))
    hk=[];gend={}
    gs=sorted(groups); hookend=outs[[i for i,(a,b,h) in enumerate(segs) if h][-1]+1]
    for gi,g in enumerate(gs):
        items=groups[g]; st=items[0][1]
        en=groups[gs[gi+1]][0][1] if gi+1<len(gs) else hookend
        lines={}
        for k,t0,w,ln,big in items: lines.setdefault(ln,[]).append(f'<span id="k{k}" class="kw{" big" if big else ""}">{w}</span>')
        hk.append(f'<div id="hg{g}" class="clip hook {cfg["hookpos"]}" data-start="{st}" data-duration="{round(en-st,2)}">'+"<br>".join(" ".join(v) for _,v in sorted(lines.items()))+'</div>')
        for k,t0,w,ln,big in items:
            if big: js.append(f'tl.fromTo("#k{k}",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}},{t0});'); js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.02,duration:0.5,ease:"power3.out"}},{t0});')
            else: js.append(f'tl.fromTo("#k{k}",{fr},{to.replace("0.4,","0.32,")},{t0});')
        js.append(f'tl.to("#hg{g} .kw",{{opacity:0,y:-12,duration:.22,stagger:.03,ease:"power2.in"}},{en-0.3:.2f});')
    for s,f,v in cfg["hsfx"]:
        t0=m(s,True)[0]; au.append(f'<audio src="sfx/{f}.wav" data-start="{max(0,t0-0.02):.2f}" data-duration="1.0" data-volume="{v}"></audio>')
    au=[x.replace('<audio src',f'<audio id="h{n}" src') if 'id=' not in x else x for n,x in enumerate(au)]
    html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:3;opacity:0;}}
.word{{position:absolute;top:250px;z-index:5;}}
.word.C{{left:140px;right:140px;text-align:center;}}
.word.L{{left:120px;width:430px;text-align:left;}}
.word span{{display:block;font-family:"Lexend Mega",sans-serif;color:#fff;letter-spacing:-0.03em;opacity:0;text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);}}
.word .tx{{font-weight:600;font-size:30px;line-height:1.3;}}
.word .sb{{font-weight:400;font-size:19px;line-height:1.4;margin-top:6px;letter-spacing:-0.04em;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.C .bar{{margin:10px auto 0;}} .word.L .bar{{transform-origin:0 50%;}}
.hook{{position:absolute;top:250px;z-index:6;font-family:"Lexend Mega",sans-serif;font-weight:600;color:#fff;font-size:32px;line-height:1.4;letter-spacing:-0.03em;text-shadow:0 2px 8px rgba(0,0,0,.5);}}
.hook.C{{left:0;right:0;text-align:center;}} .hook.L{{left:110px;width:560px;text-align:left;}}
.hook .kw{{display:inline-block;opacity:0;}}
.hook .big{{font-size:50px;font-weight:800;letter-spacing:-0.04em;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
{chr(10).join("  "+x for x in br)}
{chr(10).join("  "+x for x in hk)}
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
    open(f"{d}/index.html","w").write(html)
    return DUR

for k,c in V.items(): print(k, mk(k,c))
