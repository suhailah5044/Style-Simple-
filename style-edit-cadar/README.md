# Style Edit — Cadar Floral (gaya Misty Brooch, versi lembut)

Template HyperFrames 9:16 (1080x1920, 50.7s). Footage asal tak diubah warna, tiada filter.

## Gaya
- **Font**: Lexend Mega 600, putih, bayang nipis + garis kecil bawah (sama macam style brooch). Hook 34px, kata kunci 30px.
- **Posisi teks**: tak atas sangat (300–600px dari atas), tak tepi sangat (150px dari tepi).
  Bertukar-tukar ikut ruang kosong (dinding / langsir / headboard): kiri atas, kiri tengah, tengah, kanan atas —
  tak tutup muka & tak tutup cadar.
- **Teks masuk**: fade + naik perlahan 0.7s (`power2.out`), keluar fade 0.45s.
- **Motion setiap tukar scene** (11 cut) — 4 jenis sahaja, bergilir, 1.2s `power2.out`:
  `settle` (zoom 1.045→1) · `driftL` (geser kanan→tengah) · `rise` (naik perlahan) · `driftR` (geser kiri→tengah).
- **SFX lembut** (`sfx_soft.py`, volume 0.08–0.2): `soft_bell` (hook), `soft_chime` / `soft_tap` (kata kunci),
  `soft_sparkle` (penutup), `air_whoosh` perlahan pada cut yang tiada teks. Suara asal 1.0.

## Versi
- `v1` — senarai utama: Floral Design, So Aesthetic! (hook) · Premium Soft Fabric · Sejuk & Lembut! · Tak Berbulu! ·
  Warna Tak Mudah Luntur · Getah 360° Keliling · Machine Wash Friendly · Fit Kemas, Tak Mudah Tercabut ·
  Easy Care, Tahan Lama · Bilik Terus Nampak Classy!
- `v2` — overlay pilihan (ikut susunan): Floral Design 🌼 · Soft & Cooling Fabric · 360° Elastic Fit ·
  No Loose Corners! · Easy Wash & Care · Long Lasting Colour · Sweet Dreams, Comfy Nights ✨

### Versi hook paling kuat di depan (V3–V6) — `hooks.py`
Footage sama, disusun semula supaya momen paling kuat jadi pembuka (setiap versi intro lain). Segmen "test fit" & "seriously cantik" dibuang → 43s.
Motion lembut pada setiap sambungan baru + cut asal. Teks kata kunci ikut segmen (posisi sama yang dah disemak).

| Versi | Buka dengan (ucapan asal) | Hook |
|---|---|---|
| V3 | "kalau beli dekat mall harga tak akan dapat semurah ini" | Beli kat mall pun / tak dapat harga ni! |
| V4 | "keliling cadar ni semuanya bergetah, terus fit, terus kemas" | Pasang je, terus / fit & kemas! |
| V5 | "korang akan dapat satu sarung tilam dan dua sarung bantal" | 1 set dapat / 3 helai terus! (hanya pada shot katil penuh, tak tutup produk) |
| V6 | "cotton yang bila kita basuh tak mudah pudar warna" | Dah basuh, / warna tak luntur! |

`python3 hooks.py cut v3` (buat `assets/footage_v3.mp4`) → `python3 build.py v3` → render.

## Cara guna
Footage (`assets/footage.mp4`) tak di-commit — tukar dari .mov asal:
`ffmpeg -i in.mov -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac assets/footage.mp4`
`python3 sfx_soft.py && python3 build.py v1 && npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`

Lesen font: Lexend Mega & Noto Color Emoji — SIL OFL.
