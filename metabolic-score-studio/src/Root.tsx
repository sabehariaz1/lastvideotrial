import React from 'react';
import {Composition} from 'remotion';
import {MetabolicShowcase} from './MetabolicShowcase';
import {SCENE_DURATIONS, TRANSITION_FRAMES} from './timing';

// Sum of scene durations minus one overlap per transition (see timing.ts).
// With the current timing.ts this is exactly 3600 frames = 2:00 at 30 fps.
export const TOTAL_DURATION_IN_FRAMES =
  SCENE_DURATIONS.reduce((a, b) => a + b, 0) - TRANSITION_FRAMES * (SCENE_DURATIONS.length - 1);

export const RemotionRoot: React.FC = () => (
  <Composition
    id="MetabolicMaster"
    component={MetabolicShowcase}
    durationInFrames={TOTAL_DURATION_IN_FRAMES}
    fps={30}
    width={1920}
    height={1080}
  />
);
