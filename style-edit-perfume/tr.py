from faster_whisper import WhisperModel
import json,wave,numpy as np
a=np.frombuffer(wave.open("audio.wav").readframes(10**9),np.int16).astype(np.float32)/32768
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,_=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False)
out=[]
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    out.append({"s":s.start,"e":s.end,"t":s.text,"w":[[w.start,w.end,w.word] for w in s.words]})
json.dump(out,open("transcript.json","w"),ensure_ascii=False)
