# Style Edit — Silkelle Bra (30s)

Ikut gaya v2 (Stand Phone): teks kecil putih Lexend Mega 30px + garis nipis, Italianno untuk hook. Footage asal, warna tak diubah. Tiada muzik latar.

- `cut.py` — senarai babak `SEG` (masa sumber) → `assets/footage.mp4`
- `build.py` — overlay `O` (teks, sisi L/R/C, SFX, `P`=zoom punch, `S`=statik); masa dikira automatik dari `SEG`
- Kamera statik, zoom punch pada point penting sahaja, flash putih lembut tiap potongan.

```
python3 cut.py <sumber.mov> && python3 build.py
npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4
```
