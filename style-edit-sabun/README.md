# Style Edit — Sabun Basuh Baju (Hook depan + Pill Hook + Subtitle UI)

Template HyperFrames 9:16 (1080x1920). Footage asal: tiada filter, warna tak diubah.

## Aliran
1. `python3 cut.py <footage.mov>` — potong ikut senarai `SEG` (buang pause/gagap/ayat ulang, hook paling kuat diletak di depan 0–3s), speed 1.1, suara dikuatkan (compressor + loudnorm -13 LUFS) → `assets/footage.mp4` + `edl.json`.
2. Sahkan potongan: transcribe semula (`../style-edit-standphone-v2/tr.py`) → `words.json`.
3. `python3 sfx3.py` — set SFX baru: `air_whoosh`, `bubble_pop`, `soft_click`, `bell_ding`, `soft_impact`, `sparkle_rise`, `hook_hit`, `cash_ting`.
4. `python3 build.py` → `npx hyperframes lint .` → `npx hyperframes snapshot . --at ...` → preview `render -q draft`.
5. Final (bila dah lulus): `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`.

## Gaya
- Overlay: Lexend Mega 600, 30px, putih, tengah atas (`top:300px`) di ruang kosong kabinet — tak tutup produk. Masuk: blur→jelas + naik.
- Hook / USP penting (`pill`): 32px, latar kaca gelap separa telus + garis putih nipis, pop `back.out`.
- Digital zoom setiap potongan (`ZM`: hold / zoom 1.08 / push perlahan / punch) — sorok jump cut.
- Frame break pada 4 potongan (`FB`): goncang x/skew 0.26s + garis kilat + whoosh.
