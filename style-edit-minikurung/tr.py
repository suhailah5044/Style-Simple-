import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("small",compute_type="int8")
import numpy as np,wave;wf=wave.open(sys.argv[1]);aud=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
segs,_=m.transcribe(aud,language="ms",word_timestamps=True,vad_filter=False)
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
    out.append({"s":s.start,"e":s.end,"t":s.text,"w":[(w.start,w.end,w.word) for w in s.words]})
json.dump(out,open(sys.argv[2],"w"))
