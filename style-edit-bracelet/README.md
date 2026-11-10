# Style Edit v3 — Bracelet Titanium (Lavis)

HyperFrames 9:16 (1080x1920), 63.1s. Warna footage asal kekal, tiada filter.

## Potongan (cut.py → segs.json)
Buang ayat berulang ("Kak So ada satu je koleksi" x3, "baru sampai stock" x3, "tak luntur tak berkarat" x2, "titanium" x3), gagap & pause > 0.35s (silencedetect -32dB). 116s → 63s.

## Gaya
- **Intro 0–3s**: "Bracelet" Cormorant Garamond Italic 64px + "TITANIUM" Lexend Mega 17px (tracking lebar) + garisan nipis. Putih, tengah atas. SFX `intro_pan` (shimmer pan kiri→kanan, best dengan headphone) + loceng.
- **Overlay kata kunci (UI Prompt)**: Lexend Mega 500, 26px, putih, 4 bucu "focus bracket" snap masuk + teks blur-in. Top 262px (bumbung kereta = ruang kosong). 14 overlay (~50%), tiada overlay atas B-roll.
- **Digital zoom**: in / out / punch (Tak Berkarat, Ada Adjuster, Tahan Lama, Grab).
- **Frame break**: B-roll 1 & 3 masuk sebagai 3 jalur bersilang (`frame_break.wav`); B-roll 2 masuk sebagai kad berbingkai putih → pecah ke skrin penuh (`pop` + `soft_impact`). Keluar: `whoosh`.
- **B-roll** distabilkan (vidstab 2-pass, smoothing 40), mute.
- **BGM**: `bgm.py` (luxe lo-fi 88bpm dijana sendiri) volume 0.09.
- **SFX** (`sfx3.py`): ui_prompt, click, pop, ding (USP), tingting, sparkle, soft_impact, whoosh, frame_break, intro_pan.

## Cara guna
1. `python3 cut.py words.json` → render `assets/aroll_cut.mp4` (lihat filter dalam sejarah sesi) ; B-roll: vidstabdetect → vidstabtransform → `assets/b1947.mp4`, `b1948.mp4`.
2. `python3 sfx3.py && python3 bgm.py 64 && python3 build.py`
3. Preview gambar: `npx hyperframes snapshot . --at 1,7,8.75,...`
4. Render: `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`

Fail video dalam `assets/` tak di-commit (terlalu besar untuk GitHub).
Lesen font: Cormorant Garamond & Lexend Mega — SIL OFL.
