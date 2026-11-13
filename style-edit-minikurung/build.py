import json,subprocess,sys,os
from PIL import Image,ImageDraw,ImageFont
S='src/'; d=json.load(open(S+'tr.json'))
V=json.load(open(sys.argv[1])); OUT=sys.argv[2]; RES=sys.argv[3] if len(sys.argv)>3 else '540:960'
words=[w for s in d for w in s['w']]
def wt(word,lo,hi):
    for a,b,w in words:
        if lo<=a<=hi and word.lower() in w.lower(): return a
    raise SystemExit(f'no {word}')
SEG=[tuple(x) for x in V['seg']]
off=[];t=0
for a,b in SEG: off.append(t); t+=b-a
TOTAL=t
def m(src):
    for (a,b),o in zip(SEG,off):
        if a<=src<=b: return o+src-a
    raise SystemExit(f'{src} not in cut')
def mm(src):
    try: return m(src)
    except SystemExit: return None
KW=[("stripe + floral combo \U0001F60D",'baju',3,5),("simple but classy",'simple',23,26),("comfy outfit vibes",'kerja',26,29),
 ("nampak sweet sangat!",'Warna',36,39),("murah tapi nampak mahal",'collection',42,45),("effortless pretty look \u2728",'kipas',78,86),
 ("harga pun friendly!",'cari',87,92),("mini kurung girlies, this one for you!",'Grab',96,99)]
HE=SEG[0][1]-SEG[0][0]
OV=[(V['hook'],0.15,max(2.4,min(HE-0.2,3.2)))]
for txt,kw,lo,hi in KW:
    t0=mm(wt(kw,lo,hi))
    if t0 is None or t0<HE+0.3: continue
    if t0<OV[-1][1]+OV[-1][2]+0.4: continue
    OV.append((txt,t0,2.6))
OV.sort(key=lambda o:o[1])
OV=[(x,t0,min(D,(OV[i+1][1]-t0-0.2) if i+1<len(OV) else min(3.5,TOTAL-t0))) for i,(x,t0,D) in enumerate(OV)]
F=ImageFont.truetype('ov/Poppins-SemiBold.ttf',44)
E=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',109)
from PIL import ImageFilter
LF=ImageFont.truetype('/home/user/Style-Simple-/style-edit-standphone-v2/assets/LexendMega.woff2',38)
TRK=3; LH=54; MAXW=760
def glyph_w(ch): return 40 if ord(ch)>0x2500 else LF.getlength(ch)+TRK
def pill(txt,fn):
    txt=txt.upper().replace(' \u2728','\u00a0\u2728').replace(' \U0001F60D','\u00a0\U0001F60D'); lines=[]; cur=''
    for w in txt.split(' '):
        t=(cur+' '+w).strip()
        if cur and sum(glyph_w(c) for c in t)>MAXW: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur)
    W=int(max(sum(glyph_w(c) for c in l) for l in lines))+40; H=LH*len(lines)+40
    txtL=Image.new('RGBA',(W,H),(0,0,0,0)); dr=ImageDraw.Draw(txtL)
    for i,l in enumerate(lines):
        x=10; y=10+i*LH+40
        for ch in l:
            if ord(ch)>0x2500:
                im=Image.new('RGBA',(136,128),(0,0,0,0)); ImageDraw.Draw(im).text((0,0),ch,font=E,embedded_color=True)
                im=im.crop(im.getbbox()).resize((34,34),Image.LANCZOS); txtL.paste(im,(int(x)+2,y-32),im); x+=40
            else:
                dr.text((x,y),ch,font=LF,fill=(255,255,255,255),anchor='ls'); x+=LF.getlength(ch)+TRK
    uy=10+(len(lines)-1)*LH+40+12
    dr.rectangle((10,uy,10+44,uy+3),fill=(255,255,255,255))
    a=txtL.split()[3]; sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(a.point(lambda v:min(255,v*0.8)).filter(ImageFilter.GaussianBlur(3)))
    out=Image.new('RGBA',(W,H),(0,0,0,0)); out.alpha_composite(sh,(2,3)); out.alpha_composite(txtL); out.save(fn)
inp=['-i',S+'raw.mov']; fc=[]
n=len(SEG)
fc.append(f"[0:v]split={n}"+''.join(f'[v{i}]' for i in range(n))+f";[0:a]asplit={n}"+''.join(f'[a{i}]' for i in range(n)))
for i,(a,b) in enumerate(SEG):
    D=b-a
    fc.append(f"[v{i}]trim={a}:{b},setpts=PTS-STARTPTS[c{i}];[a{i}]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.06,afade=t=out:st={D-0.06:.3f}:d=0.06[b{i}]")
fc.append(''.join(f'[c{i}][b{i}]' for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca]")
# zoom punch: at every cut + every overlay pop
P=sorted(set(round(o[1],2) for o in OV))
Z='1'+''.join(f'+0.025*between(t,{p},{p+0.9})*sin(PI*(t-{p})/0.9)' for p in P)
fc.append(f"[cv]scale=w='trunc(1080*({Z})/2)*2':h=-2:eval=frame:flags=bicubic,crop=1080:1920[z0]")
last='z0'
for k,(txt,t0,D) in enumerate(OV):
    fn=f'ov/{os.path.basename(OUT)}_o{k}.png'; pill(txt,fn); inp+=['-loop','1','-framerate','30','-t',f'{D:.2f}','-i',fn]
    j=k+1
    fc.append(f"[{j}:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={D-0.3:.2f}:d=0.3:alpha=1,setpts=PTS+{t0:.2f}/TB[p{k}];"
              f"[{last}][p{k}]overlay=x=60:y='290+20*max(0\\,1-(t-{t0:.2f})/0.25)':eof_action=pass[z{j}]")
    last=f'z{j}'
SFX='/home/user/Style-Simple-/style-edit-standphone-v2/sfx/swoosh.wav'
k0=len(OV)+1
inp+=['-i',SFX]
fc.append(f"[{k0}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=0.22,asplit={len(OV)}"+''.join(f'[s{i}]' for i in range(len(OV))))
for i,(txt,t0,D) in enumerate(OV): fc.append(f"[s{i}]adelay={int(t0*1000)}:all=1[d{i}]")
fc.append("[ca]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[cb];[cb]"+''.join(f'[d{i}]' for i in range(len(OV)))+f"amix=inputs={len(OV)+1}:normalize=0:duration=first[am]")
fc.append(f"[{last}]scale={RES},setsar=1[vo]")
open(OUT+'.plan.txt','w').write('\n'.join(f'{t0:5.1f}s  {txt}' for txt,t0,D in OV)+f'\nTOTAL {TOTAL:.1f}s\n')
cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[vo]','-map','[am]','-c:v','libx264','-preset','medium' if RES!='540:960' else 'veryfast','-crf','20' if RES!='540:960' else '26',
 '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','128k','-t',f'{TOTAL:.2f}',OUT]
subprocess.run(cmd,check=True)
