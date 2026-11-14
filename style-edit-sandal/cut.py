# Potong footage cakap -> assets/footage.mp4, b-roll -> assets/brollN.mp4
# Sumber (Drive folder "Sandal 2"): A=11c06b..(10OO) B=4568d3..(1Sf4) C=ed0ef7..(1Wjc) D=9ba45e..(1wNT) E=3de8a7..(1zTG)
import subprocess,sys,json
SRC=sys.argv[1]
F={"A":"10OOMKGa_pmPillbprIcGOxYurIiuUHir","B":"1Sf4y1GUM5VA57OxTK8Yzu5kKX_kmlX67","C":"1WjczG8ICgiP68pfT1AOo4WAhw5EWZJVk","D":"1wNTB8uK78Tt4wdcLureW522Et2Ah-fol","E":"1zTGiPwrS4hr5TFxpn7MzpFj61G6APyGI"}
CUTS=[("A",8.92,10.86),("A",14.6,20.94),("A",23.53,29.65),("A",44.15,51.05),("A",52.25,62.2)]  # titik potong dalam celah senyap
# B-roll produk sahaja, penuh skrin 9:16 (crop tanpa muka): (klip, mula, tamat, crop w:h:x:y)
BROLL=[("C",14.5,18.5,"540:960:270:640"),("C",64.0,68.0,"432:768:330:1152"),("E",26.5,30.5,"480:853:600:900")]
VF="scale=1080:1920:flags=lanczos,setsar=1,fps=30"
X=0.08  # crossfade antara cut (smooth)
def run(a): subprocess.run(["ffmpeg","-v","error","-y"]+a,check=True)
ins=[];fc=[];edl=[];t=0
for i,(k,s,e) in enumerate(CUTS):
    ins+=["-ss",str(s),"-to",str(e),"-i",f"{SRC}/{F[k]}.mov"]
    fc.append(f"[{i}:v]{VF},setpts=PTS-STARTPTS[v{i}];[{i}:a]asetpts=PTS-STARTPTS[a{i}]")
    edl.append([k,s,e,round(t,3)]); t+=(e-s)-X
t+=X
pv,pa="v0","a0";acc=CUTS[0][2]-CUTS[0][1]
for i in range(1,len(CUTS)):
    off=acc-X
    fc.append(f"[{pv}][v{i}]xfade=transition=fade:duration={X}:offset={off:.3f}[xv{i}];[{pa}][a{i}]acrossfade=d={X}[xa{i}]")
    pv,pa=f"xv{i}",f"xa{i}"; acc=off+(CUTS[i][2]-CUTS[i][1])
run(ins+["-filter_complex",";".join(fc),"-map",f"[{pv}]","-map",f"[{pa}]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","assets/footage.mp4"])
for i,(k,s,e,cr) in enumerate(BROLL):
    run(["-ss",str(s),"-to",str(e),"-i",f"{SRC}/{F[k]}.mov","-vf",f"scale=1080:1920,crop={cr},scale=1080:1920:flags=lanczos,setsar=1,fps=30","-an","-c:v","libx264","-crf","15","-pix_fmt","yuv420p",f"assets/broll{i}.mp4"])
json.dump(edl,open("edl.json","w"));print("total",round(acc,2))
