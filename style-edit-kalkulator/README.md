# Style Edit — Kalkulator Solar (3 video, gaya v2)

Sama gaya dengan `style-edit-standphone-v2/`: hook skrip *Italianno* 0–3.4s + subtitle *Lexend Mega* dengan garis putih kecil + SFX UI + zoom in/out/punch. Footage asal, tiada filter.

| Video | Sumber | Hook 0–3s (baru) | Durasi |
|---|---|---|---|
| v1 | Footage 1 | *Tak perlu bateri? / kalkulator ni pakai solar!* | 41.8s |
| v2 | Footage 2 | *Kalkulator paling cute / teracun dekat TikTok!* | 49.6s |
| v3 | Footage 1 + 2 (gabung) | *Bunyi dia satisfying / sampai tak nak berhenti tekan!* | 48.6s |

## Aliran kerja
1. `tr.py <audio.wav> <out.json> medium` — transcribe (faster-whisper, `ms`, timing perkataan).
2. `cuts.py` — senarai segmen yang disimpan (buang gagap, ayat ulang, pause > ~0.4s).
   `cutter.py V1|V2|V3` — snap titik potong ke senyap, fade audio 25ms setiap potongan, keluar H.264 `cut/V*.mp4`.
3. Semak semula: transcribe hasil potong, pastikan tiada perkataan terpotong / ulang / jurang.
4. `videos.py` — hook + overlay `[mula, tamat, teks, L|R, sfx, zoom]` per video.
   `python3 build.py v1` → `v1/index.html` (salin `assets/` + `sfx/`). Letak footage potong di `v1/assets/footage.mp4`.
5. Preview: `npx hyperframes render v1 -q draft -o v1_PREVIEW.mp4`
6. Final: `npx hyperframes render v1 -q delivery --video-frame-format png -o v1_FINAL.mp4`
