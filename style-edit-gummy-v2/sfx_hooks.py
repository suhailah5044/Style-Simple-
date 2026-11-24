# Synthesize 4 loud, distinct hook SFX (+ 4 transition sounds). Output: sfx/hk_*.wav, sfx/tr_*.wav
import numpy as np, wave, os

SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx")
rng = np.random.default_rng(7)

def t(d): return np.arange(int(SR * d)) / SR
def env(n, a=0.005, r=0.3):
    x = np.arange(n) / SR
    return np.minimum(1, x / a) * np.exp(-x / r)
def pad(x, n): return np.pad(x, (0, max(0, n - len(x))))[:n]
def mix(*parts):
    n = max(len(p) for p in parts)
    return sum(pad(p, n) for p in parts)
def at(x, sec, n=None):
    y = np.concatenate([np.zeros(int(SR * sec)), x])
    return y if n is None else pad(y, n)
def lp(x, a):  # one-pole low-pass
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s += a * (v - s); y[i] = s
    return y
def hp(x, a): return x - lp(x, a)
def kick(d=0.6, f0=150, f1=42):
    tt = t(d); f = f1 + (f0 - f1) * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), 0.002, 0.22)
def sub(d=1.2, f0=70, f1=32):
    tt = t(d); f = f1 + (f0 - f1) * np.exp(-tt * 6)
    return np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(len(tt), 0.003, 0.5)
def noise(d): return rng.standard_normal(int(SR * d))
def clap():
    n = noise(0.25); e = np.zeros_like(n)
    for k in (0, 0.012, 0.024): e += np.exp(-np.clip(t(0.25) - k, 0, None) * 60) * (t(0.25) >= k)
    return hp(n, 0.25) * e * 0.6
def norm(x, peak=0.89):
    x = np.tanh(x * 1.4)
    return x / (np.max(np.abs(x)) + 1e-9) * peak
def save(name, x):
    x = norm(x); x = np.stack([x, x], 1)
    with wave.open(os.path.join(OUT, name), "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    print(name, round(len(x) / SR, 2), "s")

# 1) DROP: short noise riser -> sub boom + kick + clap (V5)
r = noise(0.35); rr = hp(r, 0.08) * np.linspace(0, 1, len(r)) ** 2 * 0.5
save("hk_drop.wav", mix(rr, at(sub(1.3), 0.33) * 1.0, at(kick(), 0.33), at(clap(), 0.33)))

# 2) BRAAM: detuned low saw chord, distorted, slow decay (V6)
tt = t(1.6); b = np.zeros_like(tt)
for f in (55, 55.6, 82.4, 110.3, 164.8):
    b += 2 * ((tt * f) % 1) - 1
b = lp(np.tanh(b * 0.9), 0.08) * env(len(tt), 0.03, 0.7)
save("hk_braam.wav", mix(b * 1.2, kick(0.5, 120, 40) * 0.9, sub(1.4, 60, 30) * 0.6))

# 3) SCRATCH + PUNCH: pitched noise wobble (vinyl-style) then hard kick + snare (V7)
d = 0.32; tt = t(d); wob = np.sin(2 * np.pi * 7 * tt)
car = np.sin(2 * np.pi * np.cumsum(500 + 900 * np.abs(wob)) / SR)
sc = hp(noise(d) * 0.6 + car, 0.2) * (0.4 + 0.6 * np.abs(wob)) * 0.7
snare = hp(noise(0.3), 0.3) * env(int(SR * 0.3), 0.001, 0.09) * 0.8 + np.sin(2 * np.pi * 190 * t(0.3)) * env(int(SR * 0.3), 0.001, 0.06) * 0.5
save("hk_scratch.wav", mix(sc, at(kick(0.7, 170, 45) * 1.1, d), at(snare, d), at(sub(0.9, 80, 38) * 0.6, d)))

# 4) FLASH: camera shutter click + bright bell chord shimmer + kick (V8)
sh = mix(hp(noise(0.05), 0.4) * env(int(SR * 0.05), 0.0005, 0.01), at(hp(noise(0.04), 0.4) * env(int(SR * 0.04), 0.0005, 0.008), 0.07))
tt = t(1.8); bell = np.zeros_like(tt)
for f, a in ((1046.5, 1), (1318.5, .7), (1568, .6), (2093, .4), (2637, .25)):
    bell += a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * (2.2 + f / 1500))
save("hk_flash.wav", mix(sh * 1.2, at(bell * 0.55, 0.08), at(kick(0.6, 160, 45) * 1.0, 0.08), at(sub(1.0, 75, 35) * 0.5, 0.08)))

# transitions (different per video)
save("tr_swish.wav", hp(noise(0.45), 0.15) * np.sin(np.pi * np.linspace(0, 1, int(SR * 0.45))) ** 2 * 0.6)
tt = t(0.5); save("tr_zap.wav", np.sin(2 * np.pi * np.cumsum(2400 * np.exp(-tt * 9) + 200) / SR) * env(len(tt), 0.002, 0.15))
save("tr_tape.wav", hp(noise(0.35), 0.1) * np.linspace(1, 0, int(SR * 0.35)) ** 1.5 * 0.7 + np.sin(2 * np.pi * np.cumsum(np.linspace(300, 60, int(SR * 0.35))) / SR) * 0.6)
tt = t(0.6); save("tr_chime.wav", sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 6) for f in (1760, 2349, 2637)) * 0.5)
