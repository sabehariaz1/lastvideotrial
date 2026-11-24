# Metabolic Score Studio – Arabic (RTL) version

Same video as the English one, with right-to-left layout, Arabic on-screen text and the Cairo font
(loaded from Google Fonts at render time, so the machine needs internet access).

## Run
```
npm install
npm start        # Remotion Studio
npm run build    # out/prediabetes-explainer-ar.mp4
```

## Adding the Arabic voiceover
1. Record or generate the narration from `narration-ar.md`.
2. Save it as `public/voiceover-ar.mp3`.
3. Set `HAS_VOICEOVER = true` in `src/config.ts`.
4. Re-time `src/timing.ts` to the new audio (the scene lengths and card cues are currently the English timing).
