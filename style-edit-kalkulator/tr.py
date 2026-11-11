import sys,json,numpy as np,wave
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else "small",device="cpu",compute_type="int8")
wf=wave.open(sys.argv[1]);a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
segs,_=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
out=[]
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}",flush=True)
    for w in s.words: out.append([round(w.start,2),round(w.end,2),w.word,round(w.probability,2)])
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False)
