# Style Edit — Stand Phone (Overlay Putih Kecil + SFX + Zoom)

Template HyperFrames untuk video jualan TikTok 9:16 (1080x1920). Footage asal tak diubah warna, tiada filter.

## Gaya
- **Tajuk 0–3s**: font *Lexend Mega*, putih, kecil (kicker 20px + tajuk 34px), tengah atas (`top:255px`).
- **Overlay kata kunci**: font *Cweyons* 56px, putih, bayang nipis (`0 2px 6px rgba(0,0,0,.45)`).
  - Letak di ruang kosong atas (`top:235px`), sebelah bertentangan produk (`L`/`R`), **170px dari tepi** (tak tepi sangat), lebar kotak 400px.
  - Animasi masuk: pop `scale .55→1`, `back.out(2.4)`, 0.32s. Keluar: fade 0.18s.
  - Cweyons tiada nombor / `&` / `-` → nombor fallback ke *Fredoka 600*; tulis "dan", "Anti Slip".
- **Zoom**: `in` (perlahan ke 1.08), `out` (balik ke 1.0), `punch` (1.12→1.03, power3.out) untuk perkataan kuat ("Solid").
- **SFX** (dijana `sfx.py`): `tingting`, `ting`, `pop`, `whoosh`, `impact`, `sparkle`, `kaching` (harga). Volume 0.35–0.45, suara asal 1.0.
  - Panduan: harga → kaching · solid/berat → impact + punch zoom · worth it → sparkle · ciri biasa → pop/ting · naik/turun → whoosh.

## Cara guna
1. Transcribe dapat timing perkataan: `python3 tr.py` (faster-whisper, bahasa `ms`) → `words.json`.
2. Edit senarai `O` dalam `build.py`: `[mula, tamat, "Teks", "L|R", "sfx", "in|out|punch"]`.
3. Letak footage H.264 di `assets/footage.mp4` (tukar HEVC dulu: `ffmpeg -i in.mov -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac assets/footage.mp4`), set `DUR`.
4. `python3 build.py` → `npx hyperframes lint .` → preview: `npx hyperframes render . -q draft -o draft.mp4`
5. Final: `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`

## Lesen font
- Lexend Mega & Fredoka: SIL OFL (Google Fonts).
- Cweyons: DaFont — *free for personal use*. Beli lesen komersial jika untuk jualan.
