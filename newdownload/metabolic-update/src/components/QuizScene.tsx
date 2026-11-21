import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, Card, Heading, Scene} from './ui';
import {QUIZ_READY, QUIZ_REVEAL} from '../timing';

const OPTS: Array<[string, string]> = [['A. Normal', 'under 5.5'], ['B. Prediabetes', '5.5 to 6.9'], ['C. Diabetes', '7.0 or more']];

export const QuizScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rev = spring({frame: frame - QUIZ_REVEAL, fps, config: {damping: 10}});
  const revealed = frame >= QUIZ_REVEAL;
  const counting = frame >= QUIZ_READY && !revealed;
  const left = Math.max(1, Math.ceil((QUIZ_REVEAL - frame) / fps));
  return (
    <Scene caption="Pause and think before the answer" source="Sources: [1] WHO/IDF 2006; [2] NICE PH38">
      <Heading>Quick check</Heading>
      <Card delay={6} from="left" style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
        <div style={{fontSize: 54, fontWeight: 800}}>Fasting blood sugar: <span style={{color: C.coral}}>6.2 mmol/L</span></div>
        <div style={{width: 110, height: 110, borderRadius: 55, background: counting ? C.amber : 'transparent', color: '#fff', fontSize: 64, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{counting ? left : ''}</div>
      </Card>
      <div style={{flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 28}}>
        {OPTS.map(([name, range], i) => {
          const win = i === 1;
          return (
            <Card key={name} delay={14 + i * 8} from="pop" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 12, border: revealed && win ? `6px solid ${C.green}` : `2px solid ${C.border}`, ...(revealed && !win ? {opacity: 0.4} : {})}}>
              <div style={{fontSize: 46, fontWeight: 800}}>{name}</div>
              <div style={{fontSize: 34, color: C.sub, height: 44}}>{revealed ? `${range} mmol/L` : ''}</div>
              {revealed && win ? <div style={{fontSize: 36, fontWeight: 800, color: '#fff', background: C.green, borderRadius: 30, padding: '6px 26px', transform: `scale(${Math.max(0, rev)})`}}>Correct</div> : <div style={{height: 52}} />}
            </Card>
          );
        })}
      </div>
    </Scene>
  );
};
