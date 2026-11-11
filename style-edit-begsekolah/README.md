# Style Edit — Beg Sekolah Tahan Lasak (HyperFrames, 9:16)

Footage asal: warna TAK diubah, tiada filter (encode bt709, crf 14).

## Edit audio/potongan (`prep.py`)
- Potong ayat ulang, gagap, pause. Titik potong di-snap ke bahagian paling senyap (tiada klik).
- Susun: Hook → water resistant (demo sinki) → tak tembus → 2 tahun → corak → kompartmen → combo pen → design/jahitan → anak suka/selesa/span → sesuai sekolah/travel → recommend → kualiti → harga murah → CTA "cepat-cepat grab" (dialih ke hujung).
- B-roll stabil: "kualiti elok tau cantik" guna footage pegang beg (src 73.6s) sebab asal goyang.
- Speed 1.1 (`setpts` + `atempo`), suara dikuatkan: highpass 70Hz + compressor + loudnorm -13 LUFS.

## Visual (`build.py`)
- Hook 0–3s: "Beg Sekolah Tahan Lasak" dalam pill kaca (pop-up), Lexend Mega 34px putih + SFX `hook` (whoosh kiri→kanan stereo + impact + shimmer).
- Overlay kata: Lexend Mega 28px putih, ruang kosong atas (kabinet), garis kecil bawah, sub-line 16px untuk spec (20L, 16", Adjustable straps).
- Digital zoom in/out/punch, **frame break** (frame jadi kad + background navy grid pro + garis retak) di 7.0s, 23.3s, 50.6s.
- **PiP (Picture-in-Picture)** = video kecil atas video: demo air (5.5s) & dalam beg (10.0s).
- Tiada overlay "bakul kuning".

## SFX (`sfx3.py`, set baru stereo)
whoosh (tukar babak), pop (teks), click (ciri/visual), ding (USP), impact (penting), sparkle, tick a/b/c naik (Sekolah Rendah→Menengah→Travel), cash (harga), riser (CTA), swipe (PiP), snap (frame break). Volume 0.22–0.5, suara 1.0.

## Cara guna
`python3 prep.py raw.mov audio16k.wav` → `python3 sfx3.py` → `python3 build.py` → `npx hyperframes lint .` → `npx hyperframes preview .`
Render (lepas preview OK): `npx hyperframes render . -q delivery --video-frame-format png -o BegSekolah_FINAL.mp4`
