import subprocess,sys,json,math,numpy as np,wave
from PIL import Image,ImageDraw,ImageFont,ImageFilter
SR="../src/";SFX="/home/user/Style-Simple-/style-edit-standphone-v2/sfx/"
LIB={"A":("5205",0.3,1,"L",(1.06,.5,.45)),"B":("main",8.8,0,"L",(1.18,.5,.6)),"C":("5206",6.6,1,"L",(1.32,.45,.5)),
"D":("5206",10.4,1,"L",(1.18,.5,.8)),"E":("5211",0.5,1,"R",(1.06,.5,.45)),"F":("main",34.6,0,None,(1.3,.5,.55)),
"G":("5206",2.2,1,"L",(1.12,.5,.5)),"H":("5212",2.3,1,"L",(1.22,.45,.55)),"I":("main",28.7,0,None,(1.06,.5,.45)),
"J":("5211",5.2,1,"L",(1.05,.5,.45)),"K":("main",43.6,0,"L",(1.08,.5,.45))}
TM="zscale=t=linear:npl=400,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,"
def music(path,bpm,prog,D,seed):
    sr=44100;b=60/bpm;n=int(sr*D);out=np.zeros(n);t=lambda d:np.arange(int(sr*d))/sr
    def add(x,s):
        i=int(s*sr)
        if i>=n:return
        j=min(n,i+len(x));out[i:j]+=x[:j-i]
    rng=np.random.default_rng(seed)
    kick=np.sin(2*np.pi*(50+90*np.exp(-t(.3)*25))*t(.3))*np.exp(-t(.3)*9)
    hat=np.diff(rng.standard_normal(int(sr*.05)),prepend=0)*np.exp(-t(.05)*90)*.25
    clap=rng.standard_normal(int(sr*.15))*np.exp(-t(.15)*30)*.3
    f=lambda m:440*2**((m-69)/12)
    P=[([[65,69,72],[60,64,67],[62,65,69],[58,62,65]],[41,36,38,34]),([[62,65,69],[58,62,65],[60,64,67],[57,60,64]],[38,34,36,33]),
       ([[67,71,74],[64,67,71],[60,64,67],[62,66,69]],[43,40,36,38]),([[60,64,67],[57,60,64],[53,57,60],[55,59,62]],[36,33,29,31]),
       ([[64,68,71],[61,64,68],[57,61,64],[59,63,66]],[40,37,33,35])][prog]
    pl=lambda fr,d=.35:sum(np.sin(2*np.pi*fr*k*t(d))/k for k in (1,2,3))*np.exp(-t(d)*7)
    beat=0;s=0
    while s<D:
        bar=int(beat//4)%4;add(kick*.8,s);add(hat,s+b/2)
        if prog%2:add(hat*.6,s+b/4);add(hat*.6,s+3*b/4)
        if beat%4 in(1,3):add(clap,s)
        if beat%2==0:
            for m in P[0][bar]:add(pl(f(m))*.09,s+b/2)
        add(np.sin(2*np.pi*f(P[1][bar])*t(b*.9))*np.exp(-t(b*.9)*3)*.35,s);beat+=1;s+=b
    out=out/np.abs(out).max()*.8;k=int(sr*1.2);out[-k:]*=np.linspace(1,0,k)
    w=wave.open(path,"w");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes())
def run(cfg,K,out):
    name=cfg["name"];L=round(4*60/cfg["bpm"],3);sh=[LIB[c] for c in cfg["shots"]];D=L*len(sh)
    base=f"base_{name}.mp4";ins=[];f=[]
    for i,(fn,ss,h,_,_) in enumerate(sh):
        ins+=["-ss",str(ss),"-t",str(L+0.1),"-i",SR+fn+".mov"]
        f.append(f"[{i}:v]trim=0:{L},setpts=PTS-STARTPTS,fps=30,{TM if h else ''}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p[v{i}]")
    f.append("".join(f"[v{i}]" for i in range(len(sh)))+f"concat=n={len(sh)}:v=1:a=0[o]")
    subprocess.run(["ffmpeg","-v","error","-y"]+ins+["-filter_complex",";".join(f),"-map","[o]","-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",base],check=True)
    music(f"music_{name}.wav",cfg["bpm"],cfg["prog"],D,cfg["prog"])
    # texts: hook on shot0, then facts on shots with a side
    O=[];side0=sh[0][3] or "L"
    O.append((0.15,L-0.1,cfg["hook"][0],side0,"k",0));O.append((0.4,L-0.1,cfg["hook"][1],side0,"h",0))
    facts=list(cfg["facts"])
    for i in range(1,len(sh)):
        sd=sh[i][3]
        if not sd or not facts:continue
        s0=i*L+0.12;span=L-0.17
        if len(facts)>=2 and i in cfg.get("double",[]):
            O.append((s0,s0+span/2-0.03,facts.pop(0),sd,"t",0));O.append((s0+span/2+0.02,s0+span,facts.pop(0),sd,"t",0))
        else:
            tx=facts.pop(0);O.append((s0,s0+span,tx,sd,"p" if "±" in tx or tx in("FULL BUTTON","FREE SIZE") else "t",0))
    W,H=int(1080*K),int(1920*K)
    def font(sz):
        ft=ImageFont.truetype("lexend.ttf",int(sz*K))
        try:ft.set_variation_by_axes([600])
        except Exception:pass
        return ft
    FN={"t":font(30),"p":font(30),"k":font(20),"h":font(36)}
    X0,X1,Y=70*K,1010*K,250*K
    eo=lambda x:1-2**(-10*max(0,min(1,x)))
    def layer(t):
        im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
        for s,e,tx,side,k,_ in O:
            if not(s<=t<e):continue
            p=(t-s)/0.38;fo=max(0,min(1,(t-(e-0.2))/0.2));a=eo(p)*(1-fo)
            if a<=0:continue
            y=Y+(1-eo(p))*22*K-fo*10*K+(34*K if k=="h" else 0)
            ft=FN[k];al="left" if side=="L" else "right"
            bb=d.multiline_textbbox((0,0),tx,font=ft,spacing=int(8*K),align=al);tw,th=bb[2],bb[3]
            x=X0 if side=="L" else X1-tw
            lay=Image.new("RGBA",(W,H),(0,0,0,0));ld=ImageDraw.Draw(lay);shd=Image.new("RGBA",(W,H),(0,0,0,0));sd=ImageDraw.Draw(shd)
            if k=="p":
                pad=14*K;box=(x-pad,y-pad*.8,x+tw+pad,y+th+pad)
                ld.rounded_rectangle(box,radius=int(18*K),outline=(255,255,255,255),width=max(1,int(2*K)));sd.rounded_rectangle(box,radius=int(18*K),outline=(0,0,0,110),width=max(1,int(3*K)))
            sd.multiline_text((x,y+2*K),tx,font=ft,fill=(0,0,0,170),spacing=int(8*K),align=al)
            ld.multiline_text((x,y),tx,font=ft,fill=(255,255,255,255),spacing=int(8*K),align=al)
            if k in("t","h"):
                bw=56*K*eo((t-s-0.08)/0.4);by=y+th+10*K;bx=x if side=="L" else x+tw-bw
                if bw>0:ld.rectangle((bx,by,bx+bw,by+3*K),fill=(255,255,255,255));sd.rectangle((bx,by+K,bx+bw,by+4*K),fill=(0,0,0,90))
            c=Image.alpha_composite(shd.filter(ImageFilter.GaussianBlur(3*K)),lay)
            if a<1:c.putalpha(c.getchannel("A").point(lambda v:int(v*a)))
            im=Image.alpha_composite(im,c)
        return im
    def zoom(t):
        k=min(len(sh)-1,int(t/L));p=(t-k*L)/L;ze,cx,cy=sh[k][4];e=p*p*(3-2*p)
        return 1+(ze-1)*e+0.05*math.exp(-(t-k*L)/0.18),cx,cy
    dec=subprocess.Popen(["ffmpeg","-v","error","-i",base,"-vf",f"scale={W}:{H}:in_color_matrix=bt709:in_range=tv:flags=bicubic","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
    sfx=[(s,"ui_blip",.22) for s,e,tx,sd,k,_ in O if k!="h"]+[(0.12,"swoosh",.3)]
    ain=["-i",f"music_{name}.wav"];af=[]
    for i,(s,n,v) in enumerate(sfx):
        ain+=["-i",SFX+n+".wav"];af.append(f"[{i+2}:a]adelay={int(s*1000)}|{int(s*1000)},volume={v}[s{i}]")
    af.append("[1:a]volume=0.8[m]");af.append("[m]"+"".join(f"[s{i}]" for i in range(len(sfx)))+f"amix=inputs={len(sfx)+1}:normalize=0:duration=first,alimiter=limit=0.95[a]")
    enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-"]+ain+["-filter_complex",";".join(af),"-map","0:v","-map","[a]","-vf","scale=out_color_matrix=bt709:out_range=tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-c:v","libx264","-crf","18" if K==1 else "24","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest",out],stdin=subprocess.PIPE)
    i=0;fs=W*H*3
    while True:
        b=dec.stdout.read(fs)
        if len(b)<fs:break
        t=i/30;fr=Image.frombytes("RGB",(W,H),b);z,cx,cy=zoom(t)
        if z>1.001:
            zw,zh=int(W*z),int(H*z);fr=fr.resize((zw,zh),Image.BILINEAR);ox=int((zw-W)*cx);oy=int((zh-H)*cy);fr=fr.crop((ox,oy,ox+W,oy+H))
        enc.stdin.write(Image.alpha_composite(fr.convert("RGBA"),layer(t)).convert("RGB").tobytes());i+=1
    enc.stdin.close();enc.wait();return D,L
if __name__=="__main__":
    cfgs=json.load(open("variants.json"));K=float(sys.argv[1]);only=sys.argv[2:] or [c["name"] for c in cfgs]
    for c in cfgs:
        if c["name"] in only:
            D,L=run(c,K,f"{c['name']}_{'final' if K==1 else 'preview'}.mp4");print(c["name"],round(D,2),L)
