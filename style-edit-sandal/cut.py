# Potong footage cakap -> assets/footage.mp4, b-roll -> assets/brollN.mp4
# Sumber (Drive folder "Sandal 2"): A=11c06b..(10OO) B=4568d3..(1Sf4) C=ed0ef7..(1Wjc) D=9ba45e..(1wNT) E=3de8a7..(1zTG)
import subprocess,sys,json
SRC=sys.argv[1]
F={"A":"10OOMKGa_pmPillbprIcGOxYurIiuUHir","B":"1Sf4y1GUM5VA57OxTK8Yzu5kKX_kmlX67","C":"1WjczG8ICgiP68pfT1AOo4WAhw5EWZJVk","D":"1wNTB8uK78Tt4wdcLureW522Et2Ah-fol","E":"1zTGiPwrS4hr5TFxpn7MzpFj61G6APyGI"}
CUTS=[("B",16.45,19.6),("B",20.65,21.6),("B",22.4,23.0),("B",24.6,27.6),("B",27.75,33.9),
      ("E",17.45,20.65),("D",12.25,18.6),("C",29.0,34.75),("C",36.3,38.5),("C",44.55,45.9),("C",46.75,49.5),
      ("A",9.2,11.05),("A",14.85,20.95),("A",52.1,61.9)]
BROLL=[("E",26.5,30.5),("A",3.5,7.5),("E",43.0,47.0),("C",65.0,68.9)]
VF="scale=1080:1920:flags=lanczos,setsar=1,fps=30"
def run(a): subprocess.run(["ffmpeg","-v","error","-y"]+a,check=True)
ins=[];fc=[];t=0;edl=[]
for i,(k,s,e) in enumerate(CUTS):
    ins+=["-ss",str(s),"-to",str(e),"-i",f"{SRC}/{F[k]}.mov"]
    d=e-s;edl.append([k,s,e,round(t,3)]);t+=d
    fc.append(f"[{i}:v]{VF},setpts=PTS-STARTPTS[v{i}];[{i}:a]asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.03:.3f}:d=0.03[a{i}]")
fc.append("".join(f"[v{i}][a{i}]" for i in range(len(CUTS)))+f"concat=n={len(CUTS)}:v=1:a=1[v][a]")
run(ins+["-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","assets/footage.mp4"])
for i,(k,s,e) in enumerate(BROLL):
    run(["-ss",str(s),"-to",str(e),"-i",f"{SRC}/{F[k]}.mov","-vf",VF,"-an","-c:v","libx264","-crf","15","-pix_fmt","yuv420p",f"assets/broll{i}.mp4"])
json.dump(edl,open("edl.json","w"));print("total",round(t,2))
