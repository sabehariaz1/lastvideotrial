# Metabolic Score Studio – Arabic (RTL) version

Right-to-left layout, Arabic on-screen text, Cairo font (Google Fonts, needs internet when rendering).

## Fully automatic render (GitHub Actions)
The workflow runs `scripts/build_audio.py`, which
1. generates the Arabic narration from `scripts/narration.json` with a free neural voice (edge-tts, voice `ar-AE-FatimaNeural`; falls back to gTTS),
2. measures every sentence and re-times all scenes, cards and sound effects to it (`src/timing.ts`, `public/sfx.mp3`),
3. fits the whole video to 2:00 (it only speeds the voice up, never more than x1.2),
4. then Remotion renders the video.

To change the wording, edit `scripts/narration.json` (numbers are written as words so the voice reads them correctly)
and re-run the workflow. To change the voice, edit `"voice"` there (e.g. `ar-AE-HamdanNeural`, `ar-SA-HamedNeural`, `ar-SA-ZariyahNeural`).

## Local run
```
npm install
pip install edge-tts gTTS imageio-ffmpeg
python3 scripts/build_audio.py
npm start          # Studio
npm run build      # out/prediabetes-explainer-ar.mp4
```
