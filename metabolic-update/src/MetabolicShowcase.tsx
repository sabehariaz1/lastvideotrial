import React from 'react';
import {interpolate, staticFile, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {TransitionSeries, springTiming} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';

const DIRS = ['from-right', 'from-bottom', 'from-left', 'from-top'] as const;
import {ScoreHookScene} from './components/ScoreHookScene';
import {PrevalenceAndGaugeScene} from './components/PrevalenceAndGaugeScene';
import {InsulinMechanismScene} from './components/InsulinMechanismScene';
import {RiskMatrixScene} from './components/RiskMatrixScene';
import {DiagnosticsScene} from './components/DiagnosticsScene';
import {PreventionAndRefsScene} from './components/PreventionAndRefsScene';
import {ProgressionScene} from './components/ProgressionScene';
import {ReferencesScene} from './components/ReferencesScene';

export const SCENE_DURATIONS: readonly number[] = [330, 540, 540, 450, 540, 450, 450, 426];
export const TRANSITION_FRAMES = 18;
const SCENES: ReadonlyArray<React.FC> = [ScoreHookScene, PrevalenceAndGaugeScene, InsulinMechanismScene, RiskMatrixScene, DiagnosticsScene, ProgressionScene, PreventionAndRefsScene, ReferencesScene];

export const MetabolicShowcase: React.FC = () => {
  const {durationInFrames} = useVideoConfig();
  const items = SCENES.flatMap((Comp, i) => {
    const seq = (
      <TransitionSeries.Sequence key={`s${i}`} durationInFrames={SCENE_DURATIONS[i] ?? 0}>
        <Comp />
      </TransitionSeries.Sequence>
    );
    return i < SCENES.length - 1
      ? [seq, <TransitionSeries.Transition key={`t${i}`} presentation={slide({direction: DIRS[i % DIRS.length] ?? 'from-right'})} timing={springTiming({config: {damping: 200}, durationInFrames: TRANSITION_FRAMES})} />]
      : [seq];
  });
  return (
    <>
      <TransitionSeries>{items}</TransitionSeries>
      <Audio src={staticFile('voiceover.mp3')} volume={1} />
      <Audio
        src={staticFile('ambient-bed-v3.mp3')}
        loop
        volume={(f) =>
          interpolate(f, [0, 30, durationInFrames - 30, durationInFrames], [0, 0.11, 0.11, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
        }
      />
    </>
  );
};
