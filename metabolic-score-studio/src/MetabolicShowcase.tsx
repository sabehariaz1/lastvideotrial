import React from 'react';
import {AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {TransitionSeries, springTiming} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {C} from './components/ui';
import {SCENE_DURATIONS, TRANSITION_FRAMES} from './timing';
import {ScoreHookScene} from './components/ScoreHookScene';
import {PrevalenceAndGaugeScene} from './components/PrevalenceAndGaugeScene';
import {InsulinMechanismScene} from './components/InsulinMechanismScene';
import {RiskMatrixScene} from './components/RiskMatrixScene';
import {DiagnosticsScene} from './components/DiagnosticsScene';
import {ProgressionScene} from './components/ProgressionScene';
import {LifestyleScene} from './components/LifestyleScene';
import {PreventionAndRefsScene} from './components/PreventionAndRefsScene';
import {ReferencesScene} from './components/ReferencesScene';

export {SCENE_DURATIONS, TRANSITION_FRAMES};

const DIRS = ['from-right', 'from-bottom', 'from-left', 'from-top'] as const;

const SCENES: ReadonlyArray<React.FC> = [
  ScoreHookScene,
  PrevalenceAndGaugeScene,
  InsulinMechanismScene,
  RiskMatrixScene,
  DiagnosticsScene,
  ProgressionScene,
  LifestyleScene,
  PreventionAndRefsScene,
  ReferencesScene,
];

export const MetabolicShowcase: React.FC = () => {
  const {durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const items = SCENES.flatMap((Comp, i) => {
    const seq = (
      <TransitionSeries.Sequence key={`s${i}`} durationInFrames={SCENE_DURATIONS[i] ?? 0}>
        <Comp />
      </TransitionSeries.Sequence>
    );
    return i < SCENES.length - 1
      ? [
          seq,
          <TransitionSeries.Transition
            key={`t${i}`}
            presentation={slide({direction: DIRS[i % DIRS.length] ?? 'from-right'})}
            timing={springTiming({config: {damping: 200}, durationInFrames: TRANSITION_FRAMES})}
          />,
        ]
      : [seq];
  });
  return (
    <>
      <TransitionSeries>{items}</TransitionSeries>
      <AbsoluteFill style={{pointerEvents: 'none'}}>
        <div style={{height: 8, width: `${(frame / durationInFrames) * 100}%`, background: `linear-gradient(90deg, ${C.amber}, ${C.coral})`}} />
      </AbsoluteFill>
      <Audio src={staticFile('voiceover.mp3')} volume={1} />
      <Audio
        src={staticFile('ambient-bed-v4.mp3')}
        loop
        volume={(f) =>
          interpolate(f, [0, 30, durationInFrames - 30, durationInFrames], [0, 0.22, 0.22, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
        }
      />
      <Audio src={staticFile('sfx.mp3')} volume={0.6} />
    </>
  );
};
