# Metabolic Score Studio – Prediabetes explainer (2:00)

## Run
```
npm install
npm start        # open Remotion Studio
npm run build    # renders out/prediabetes-explainer.mp4 (1920x1080, 30 fps, 3600 frames)
```

## Layout
- `src/index.ts` – entry, registers the root
- `src/Root.tsx` – composition `MetabolicMaster` (duration computed from `timing.ts`)
- `src/MetabolicShowcase.tsx` – scenes, slide transitions, progress bar, audio
- `src/timing.ts` – scene lengths and card cues, synced to `public/voiceover.mp3`
- `src/components/` – the 9 scenes + `ui.tsx` shared helpers
- `public/` – `voiceover.mp3` (120.8 s), `ambient-bed-v4.mp3`, `sfx.mp3`
- `index.html` – companion web page (not used by Remotion)

If the narration changes, update `timing.ts`: scene length = (next scene speech start − this scene start) + 18 frames,
and total frames = sum of durations − 18 × 8 = 3600.
