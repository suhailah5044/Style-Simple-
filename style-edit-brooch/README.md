# Style Edit — Brooch (style v2: Intro Script + Subtitle UI)

Sama gaya dengan `style-edit-standphone-v2/` (font, saiz, animasi, SFX, zoom). Hanya teks & timing ditukar.

- **Hook 0–3.4s** (Italianno): "No more struggle / cucuk brooch!"
- **Kata kunci** (Lexend Mega, ikut prompt sebijik):
  Brooch yang lebih catchy · Jarum tajam, cucuk pun smooth! · Panjang & sturdy! · Banyak layer? No problem! ·
  Easy pin, easy styling! · Tak payah struggle! · Secure fit, kemas je! · Small but useful! · Cantik, practical & affordable!
- Kanan (R) bila produk dipegang kiri (0–34s), kiri (L) selepas itu.

Footage (`assets/footage.mp4`) tak di-commit — tukar dari .mov asal:
`ffmpeg -i in.mov -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac assets/footage.mp4`
Render: `python3 build.py && npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`
