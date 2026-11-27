# Style Edit — Flower Bracelet (ikut style Misty Brooch)

Gaya sama macam `style-edit-brooch` (Misty): hook Lexend Mega 34px, kata kunci Lexend Mega 600 30px putih + garis kecil, zoom in/out/punch, SFX UI.

Beza dari Misty:
- Teks **tak terlalu atas** (hook top 340px) dan **tak rapat tepi** (140–160px dari tepi).
- **Kedudukan berubah-ubah** ikut ruang kosong setiap shot (atas kanan / atas kiri / bawah kiri / bawah kanan) supaya tak tutup muka & gelang.
- Emoji 🌸 🎁 guna Noto Color Emoji (`assets/NotoColorEmoji.ttf`, SIL OFL).

| Masa | Teks | Ikut ayat |
|---|---|---|
| 0–3.4 | Flower design, / so classy! (hook) | "awak cantik…" |
| 4.0 | Pretty Flower Design 🌸 | "keluarkan semua desain cantik" |
| 7.5 | Sparkling Crystal Details | "yang ada batu-batu macam ni" |
| 11.05 | Premium Gift Box Included | kotak LAVIS dibuka |
| 17.46 | Elegant Gold Finish | gelang dipakai di tangan |
| 23.2 | Classy & Timeless Look | "nampak mahal… look yang mahal" |
| 30.8 | Easy To Match Any Outfit | "suka pakai asesori" |
| 45.3 | Perfect For Daily Wear | "pakai hari-hari tak mudah luntur" |
| 48.82 | Adjustable Length | "bahagian sini ada extender" |
| 50.95 | 16CM + 5CM Extension | "tangan besar, tangan kecil" |
| 59.66 | Sweet Gift For Her 🎁 | "cantik… kita memang love" |

Ubah dalam `build.py`: `[mula, tamat, "Teks", (L|R, jarak-dari-tepi, top), sfx, zoom]`.

Footage (`assets/footage.mp4`) tak di-commit — tukar dari .mov asal:
`ffmpeg -i in.mov -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac assets/footage.mp4`
Render: `python3 build.py && npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`
