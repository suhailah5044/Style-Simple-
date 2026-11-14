# Style Edit — Hook Toilet (v2 style + kinetic hook + b-roll)

9:16 1080x1920, ~41.4s. Footage asal tak diubah warna (bt709, tiada filter).

- **Cut**: buang ayat ulang "Bila dah sangkut, barulah cantik…" (src 23.5–26.67s). Hook kuat kekal di 0–3s.
- **Hook kinetic**: Lexend Mega putih, perkataan pop ikut masa sebut, "cantik!" besar + zoom punch.
- **Overlay**: tajuk 30px + subline 19px, putih, top 250px (atas kepala), CTA kiri di shot akhir.
- **B-roll full screen 4s** (tanpa muka, fade 0.35s): `broll1` = close-up hook (src 36.2s), `broll2` = crop kiri wide shot slow-mo.
- **SFX**: dari `style-edit-standphone-v2/sfx`.

Build: `python3 build.py` → `npx hyperframes lint .` → preview `npx hyperframes render . -q draft -o PREVIEW_draft.mp4`
Final (bila diluluskan): `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`
