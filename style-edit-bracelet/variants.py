# 4 versi ~20s daripada A-roll 1 (A1), A-roll 2 (A2) + B-roll. Skrip tak berulang antara versi.
# python3 variants.py <scratch_dir>  -> v1..v4/ (index.html + assets/footage.mp4)
import json, os, subprocess, sys
S=sys.argv[1]; HERE=os.path.dirname(os.path.abspath(__file__))
SRC={"A1":(f"{S}/raw/aroll.mov",f"{S}/words_raw.json",f"{S}/sil.txt"),
     "A2":(f"{S}/raw/aroll2.mov",f"{S}/a2/words.json",f"{S}/a2/sil.txt")}
W={k:json.load(open(v[1])) for k,v in SRC.items()}
SIL={k:[tuple(map(float,l.split())) for l in open(v[2]) if len(l.split())==2] for k,v in SRC.items()}

V={
 "v1":dict(title=("Tak Perlu","EMAS 916"),
   phrases=[("A2",67.45,71.3),("A1",18.9,23.65),("A2",23.9,28.3),("A1",60.1,65.0),("A2",94.5,96.6)],
   ov=[("A2",70.3,"Pakai Ni Dah Cukup","ding","punch"),("A1",23.2,"Tak Berkarat","click","in"),
       ("A2",26.0,"Pakai Basahan","ui_prompt","out"),("A2",95.9,"Sangat Recommend","sparkle","punch")],
   broll=("A1",62.6,65.0,"b1948",0.3,"card")),
 "v2":dict(title=("Pakai Tak","PERNAH BUKA"),
   phrases=[("A2",8.6,14.2),("A2",14.2,17.5),("A1",90.7,94.3),("A1",66.7,72.9)],
   ov=[("A2",12.2,"Still Elok","ui_prompt","in"),("A2",16.4,"Batu Tak Tertanggal","ding","punch"),
       ("A1",92.9,"Tahan Lama","click","out"),("A1",71.6,"Ada Adjuster","pop","punch")],
   broll=("A2",14.2,16.4,"b1947",0.3,"slice")),
 "v3":dict(title=("Harga","RM20+ JE"),
   phrases=[("A2",31.15,35.7),("A2",37.7,39.6),("A1",1.28,8.3),("A2",49.85,55.2),("A1",51.6,55.58)],
   ov=[("A2",31.2,"RM20+ – RM30+","tingting","punch"),("A2",38.3,"Harga Tengah Murah","ui_prompt","in"),
       ("A1",7.8,"Titanium","click","out"),("A2",54.9,"Kotak Nampak Mahal","sparkle","in"),("A1",55.0,"Pakai Daily","pop","out")],
   broll=("A1",1.9,5.5,"b1947",2.0,"slice")),
 "v4":dict(title=("Baru","RESTOCK"),
   phrases=[("A1",75.3,77.9),("A1",84.1,86.9),("A2",0.55,3.8),("A1",28.9,32.35),("A2",88.5,94.5),("A1",110.4,115.4)],
   ov=[("A1",85.5,"Takut Sold Out","ding","punch"),
       ("A2",91.3,"Masih Shiny","sparkle","out"),("A1",110.9,"Grab Sementara Ada","soft_impact","punch")],
   broll=("A2",2.5,3.75,"b1948",0.5,"card")),
}
def phrase_segs(src,a,b):
    ws=[w for w in W[src] if a-0.05<=w[0]<b]
    s,e=ws[0][0]-0.08,ws[-1][1]+0.12
    out=[];cur=s
    for x,y in SIL[src]:
        x2,y2=x+0.1,y-0.1
        if y2-x2<0.2: continue
        if x2>cur and y2<e: out.append([cur,x2]);cur=y2
        elif x2<=cur<y2: cur=y2
    if e-cur>0.15: out.append([cur,e])
    return [(src,round(p,3),round(q,3)) for p,q in out if q-p>0.15]
def tmap(segs,src,t):
    acc=0
    for s,a,b in segs:
        if s==src and a-0.15<=t<=b+0.15: return round(acc+max(0,t-a),2)
        acc+=b-a
    raise ValueError((src,t))
VOL={"ui_prompt":.4,"click":.45,"ding":.3,"tingting":.28,"pop":.4,"sparkle":.25,"soft_impact":.5}
tpl=open(f"{HERE}/variant_tpl.html").read()
for name,c in V.items():
    d=f"{HERE}/{name}"; os.makedirs(f"{d}/assets",exist_ok=True)
    segs=[x for p in c["phrases"] for x in phrase_segs(*p)]
    DUR=round(sum(b-a for _,a,b in segs),2)
    if not os.path.exists(f"{d}/assets/footage.mp4"):
        parts=[]
        for i,(s_,a,b) in enumerate(segs):
            p=f"{S}/seg_{name}_{i}.mkv"; parts.append(p)
            subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",SRC[s_][0],"-t",f"{b-a:.3f}","-af",f"afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03",
                "-c:v","libx264","-crf","12","-preset","fast","-pix_fmt","yuv420p","-c:a","pcm_s16le",p],check=True)
        lst=f"{S}/list_{name}.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-crf","15","-preset","fast","-pix_fmt","yuv420p",
            "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","aac","-b:a","256k",f"{d}/assets/footage.mp4"],check=True)
        for p in parts: os.remove(p)
    for f in ["LexendMega.woff2","CormorantItalic.woff2","b1947.mp4","b1948.mp4"]:
        if not os.path.exists(f"{d}/assets/{f}"): os.symlink(f"{HERE}/assets/{f}",f"{d}/assets/{f}")
    if not os.path.exists(f"{d}/sfx"): os.symlink(f"{HERE}/sfx",f"{d}/sfx")
    el=[];au=[];js=[]
    for i,(src,t,text,sfx,z) in enumerate(c["ov"]):
        s=max(3.3,tmap(segs,src,t)); e=min(DUR-0.1,s+1.6)
        el.append(f'<div id="w{i}" class="clip w" data-start="{s}" data-duration="{e-s:.2f}"><div class="box"><i class="k tl"></i><i class="k tr"></i><i class="k bl"></i><i class="k br"></i><span class="tx">{text}</span></div></div>')
        au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-.03):.2f}" data-duration="1.2" data-volume="{VOL[sfx]}"></audio>')
        js+=[f'tl.fromTo("#w{i} .tx",{{opacity:0,filter:"blur(8px)",scale:1.18}},{{opacity:1,filter:"blur(0px)",scale:1,duration:.42,ease:"expo.out"}},{s});',
             f'tl.fromTo("#w{i} .k",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.32,ease:"back.out(2)",stagger:.03}},{s+.04:.2f});',
             f'tl.to("#w{i} .k",{{opacity:0,duration:.25}},{s+.75:.2f});',
             f'tl.to("#w{i} .tx",{{opacity:0,filter:"blur(6px)",duration:.2,ease:"power2.in"}},{e-.22:.2f});']
        if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:.45,ease:"power3.out"}},{s});')
        elif z=="in": js.append(f'tl.to("#cam",{{scale:1.07,duration:{e-s:.2f},ease:"sine.inOut"}},{s});')
        else: js.append(f'tl.to("#cam",{{scale:1.0,duration:{e-s:.2f},ease:"sine.inOut"}},{s});')
    src,ta,tb,f,ms,sty=c["broll"]; s=tmap(segs,src,ta); e=tmap(segs,src,tb)
    dd=f'data-start="{s}" data-duration="{e-s:.2f}" data-playback-start="{ms}" muted data-volume="0" data-has-audio="false"'
    if sty=="slice":
        inner="".join(f'<div class="sl s{k}"><video id="vb{k}" src="assets/{f}.mp4" {dd}></video></div>' for k in range(3))
        js+=[f'tl.fromTo("#b0 .s{k}",{{xPercent:{(-1)**k*100}}},{{xPercent:0,duration:.34,ease:"expo.out"}},{s+k*.05:.2f});' for k in range(3)]
        au.append(f'<audio id="fb0" src="sfx/frame_break.wav" data-start="{s-.02:.2f}" data-duration=".6" data-volume=".35"></audio>')
    else:
        inner=f'<div class="card"><video id="vb0" src="assets/{f}.mp4" {dd}></video></div>'
        js+=[f'tl.fromTo("#b0 .card",{{scale:.55,rotation:-5,opacity:0}},{{scale:.84,rotation:0,opacity:1,duration:.38,ease:"back.out(1.6)"}},{s});',
             f'tl.to("#b0 .card",{{scale:1,borderRadius:0,outlineColor:"rgba(255,255,255,0)",duration:.32,ease:"power3.inOut"}},{s+.6:.2f});']
        au+=[f'<audio id="fp0" src="sfx/pop.wav" data-start="{s:.2f}" data-duration=".3" data-volume=".35"></audio>',
             f'<audio id="fi0" src="sfx/soft_impact.wav" data-start="{s+.6:.2f}" data-duration=".7" data-volume=".4"></audio>']
    el.append(f'<div id="b0" class="broll"><div class="push">{inner}</div></div>')
    js+=[f'tl.set("#b0",{{opacity:1}},{s});',f'tl.fromTo("#b0 .push",{{scale:1}},{{scale:1.08,duration:{e-s:.2f},ease:"none"}},{s});',f'tl.to("#b0",{{opacity:0,duration:.16}},{e-.16:.2f});']
    au.append(f'<audio id="wo0" src="sfx/whoosh.wav" data-start="{e-.3:.2f}" data-duration=".6" data-volume=".28"></audio>')
    html=(tpl.replace("%DUR%",str(DUR)).replace("%T1%",c["title"][0]).replace("%T2%",c["title"][1])
          .replace("%EL%","\n  ".join(el)).replace("%AU%","\n  ".join(au)).replace("%JS%","\n".join(js)))
    open(f"{d}/index.html","w").write(html)
    print(name,DUR,len(segs))
