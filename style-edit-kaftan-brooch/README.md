# Style Edit — Kaftan Zebra v2 (gaya Misty Brooch, sebijik edit Cadar)

Template HyperFrames 9:16 (1080x1920, 81.9s). Footage asal tak diubah warna; outro CapCut dipotong.

## Gaya (ikut `style-edit-cadar` / brooch)
- **Font**: Lexend Mega 600, putih, bayang nipis + garis putih kecil (56x3px) bawah teks. Hook 34px tengah (top 420px), kata kunci 30px.
- **Posisi**: 330–560px dari atas, 150px dari tepi, bertukar kiri/kanan ikut ruang kosong — tak tutup muka & produk.
- **Teks masuk**: fade + naik 0.7s `power2.out`, garis memanjang; keluar fade 0.45s.
- **Motion kamera** (4 jenis bergilir, 1.2s): `settle` · `driftL` · `rise` · `driftR` — pada setiap cut scene (2.93, 16.7, 30.47, 34.97, 63.7, 68.27s) dan bila teks bertukar.
- **SFX lembut**: `soft_chime` / `soft_tap` (kata kunci), `soft_sparkle` (teks emoji), `air_whoosh` perlahan pada cut tanpa teks.
- **Hook audio BARU**: `harp_rise` — petikan harp naik C-E-G-C-E (berbeza dari video pertama `airy_swell` + `sparkle`, dan dari `soft_bell` Cadar).

## Cara guna
`python3 sfx_soft.py && python3 build.py && npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`
Footage (`assets/footage.mp4`) tak di-commit.

Lesen font: Lexend Mega — SIL OFL.
