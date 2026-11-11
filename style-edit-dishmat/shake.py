import sys,subprocess,numpy as np
W,H=90,160
p=subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-vf",f"scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout
f=np.frombuffer(p,np.uint8).reshape(-1,H,W).astype(np.float32)
win=np.outer(np.hanning(H),np.hanning(W))
sh=[0]
for i in range(1,len(f)):
    a=np.fft.fft2((f[i-1]-f[i-1].mean())*win);b=np.fft.fft2((f[i]-f[i].mean())*win)
    r=np.fft.ifft2(a*np.conj(b)/(abs(a*np.conj(b))+1e-6)).real
    y,x=np.unravel_index(r.argmax(),r.shape); y=y-H if y>H/2 else y; x=x-W if x>W/2 else x
    sh.append((x*x+y*y)**.5)
sh=np.array(sh)
for s in range(0,int(len(f)/30)):
    seg=sh[s*30:(s+1)*30]; print(f"{s:3d}s shake={seg.mean():.2f} jitter={np.abs(np.diff(seg)).mean():.2f}")
