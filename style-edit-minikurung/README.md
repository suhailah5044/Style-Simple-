# Style Edit: Mini Kurung (Bazla-style text)

TikTok/Reels 9:16 edit dengan 6 variant hook berbeza. Output dalam `video/minikurung/`.

## Gaya
- Teks: Lexend Mega, HURUF BESAR, jarak huruf renggang, putih tanpa kotak, shadow lembut, garis pendek bawah baris akhir (ikut rujukan Kemeja Bazla).
- Kedudukan: kiri atas (x=60, y≈290) dalam ruang kosong, tak tutup muka/baju. Dalam safe zone TikTok + IG.
- Gerakan: tiada zoom pada cut. Zoom halus 2.5% (0.9s) + whoosh perlahan (vol 0.22) HANYA bila overlay masuk.
- Audio cut: fade 60ms. Warna footage asal (bt709) tak diubah.

## Fail
- `build.py` — `python3 -I build.py variants/V1_FINAL.json out.mp4 1080:1920` (tanpa arg ke-3 = preview 540x960)
- `variants/*.json` — `hook` (teks hook) + `seg` (senarai [mula, tamat] saat dalam footage asal; segmen pertama = hook)
- `transcript.json` — transcript faster-whisper (word timestamps) footage asal
- `tr.py` — script transcribe

Overlay keyword (stripe+floral, simple but classy, dsb.) dipadankan automatik pada masa perkataan disebut; overlay yang jatuh dalam hook atau bertindih dilangkau.

Path dalam `build.py` (footage `src/raw.mov`, font, sfx) perlu diubah jika dijalankan di tempat lain.
