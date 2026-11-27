# Style Edit — Misty (Kaftan Zebra / Baju Tidur)

Template HyperFrames 9:16 (1080x1920). Footage asal tak diubah warna. Outro CapCut dipotong (video tamat 81.9s).

## Gaya "misty"
- **Hook 0–2.9s**: "Floral Design, / So Aesthetic!" — *Cormorant Garamond* italic 600, putih bercahaya lembut, kanan (ruang kosong langsir), garis halus di bawah. SFX `airy_swell` + `sparkle` perlahan.
- **Kad teks**: kaca berkabus (backdrop blur 14px, gradien putih→mauve lut sinar, sempadan putih nipis, bucu 24px), *Montserrat* 500 36px putih.
  Hiasan kecil ✦ "brooch" bersinar di bucu atas kad.
- **Posisi**: berubah ikut ruang kosong setiap babak (kiri/kanan, top 350–560px), 110px dari tepi — tak terlalu atas, tak terlalu tepi, tak tutup muka/produk.
- **Motion (4 jenis sahaja)**: `mist` (blur→jelas + naik), `slide` (hanyut dari sisi), `bloom` (membesar lembut), `spread` (huruf merapat). Keluar: kabur + pudar. Kad terapung perlahan semasa dipapar.
- **Kamera**: zum lembut silih ganti 1.0 ↔ 1.045 setiap tukar teks.
- **SFX lembut** (`sfx_soft.py`): `mist_whoosh`, `bubble_pop`, `soft_chime`, `sparkle`, `airy_swell` — volum 0.14–0.28.

## Cara guna
Edit senarai `O` dalam `build.py` → `python3 build.py` → `npx hyperframes snapshot . --at ...` untuk semak → `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`.

`assets/footage.mp4` tidak disertakan dalam repo (saiz besar) — letak footage sendiri di situ.

Lesen font: Cormorant Garamond & Montserrat — SIL OFL.
