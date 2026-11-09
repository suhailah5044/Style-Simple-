from faster_whisper import WhisperModel
import numpy as np,wave,json
m=WhisperModel("small",device="cpu",compute_type="int8")
wf=wave.open("audio.wav");a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
segs,_=m.transcribe(a,language="ms",word_timestamps=True)
out=[]
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    for w in s.words: out.append([round(w.start,2),round(w.end,2),w.word])
json.dump(out,open("words.json","w"),ensure_ascii=False)
