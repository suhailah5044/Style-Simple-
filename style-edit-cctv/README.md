# Style Edit — CCTV (style v2 + kad gambar overlay)

Asas: `style-edit-standphone-v2` (Lexend Mega + garis kecil, SFX UI, zoom in/out/punch).

- Intro: "Rumah Takde Orang? 👀" (Italianno) + "CCTV Kecil, Function Padu!" (Lexend Mega).
- Overlay USP tengah atas (`top:230px`), font Lexend Mega 32px.
- Kad gambar: bingkai putih radius 28px, masuk pop `back.out` + swoosh, Ken Burns 1.0→1.06. Posisi setiap gambar boleh ditukar dalam senarai `IMG` (kolum ke-4).
- Emoji: `assets/NotoColorEmoji.ttf` (SIL OFL).

Footage: tukar HEVC → `assets/footage.mp4` (lihat README v1). `python3 build.py` → `npx hyperframes lint .` → `npx hyperframes snapshot . --at ...`.
Render (bila diluluskan): `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`
