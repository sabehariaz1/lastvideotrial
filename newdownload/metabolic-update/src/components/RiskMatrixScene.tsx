import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, Card, Heading, Scene, useSpring} from './ui';
import {RISK_TICKS} from '../timing';

const FACTORS = ['Age 45 or older', 'Extra body weight', 'Family history of diabetes', 'Little exercise', 'High blood pressure', 'Diabetes during pregnancy'];
const COLORS = [C.coral, C.amber, C.green, C.coral, C.amber, C.green];

const Tile: React.FC<{label: string; color: string; i: number}> = ({label, color, i}) => {
  const s = useSpring(14 + i * 6, 9);
  const t = useSpring(RISK_TICKS[i] ?? 60, 8);
  return (
    <Card delay={8 + i * 6} from={i % 2 === 0 ? 'left' : 'right'} style={{display: 'flex', alignItems: 'center', gap: 18, padding: 22}}>
      <svg width="72" height="72" viewBox="0 0 84 84" style={{flexShrink: 0, transform: `rotate(${(1 - s) * -270}deg) scale(${Math.max(0, s)})`}}>
        <circle cx="42" cy="42" r="40" fill={color} />
        <path d="M42 24 V60 M24 42 H60" stroke="#fff" strokeWidth="10" strokeLinecap="round" />
      </svg>
      <div style={{fontSize: 34, fontWeight: 700, lineHeight: 1.2, flex: 1}}>{label}</div>
      <svg width="52" height="52" viewBox="0 0 52 52" style={{flexShrink: 0, transform: `scale(${Math.max(0, t)})`}}>
        <circle cx="26" cy="26" r="25" fill={C.green} />
        <path d="M14 27 L23 36 L39 17" stroke="#fff" strokeWidth="6" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </Card>
  );
};

export const RiskMatrixScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const fill = RISK_TICKS.reduce((a, t) => a + spring({frame: frame - t, fps, config: {damping: 200}}), 0) / 6;
  return (
    <Scene caption="Each one can add points to your score" source="Sources: [8] Prediabetes Risk Test; [2] NICE PH38">
      <Heading>What raises your score?</Heading>
      <div style={{display: 'flex', alignItems: 'center', gap: 20, flexShrink: 0}}>
        <div style={{fontSize: 28, fontWeight: 700, color: C.sub}}>Your risk</div>
        <div style={{flex: 1, height: 26, borderRadius: 13, background: C.border, overflow: 'hidden'}}>
          <div style={{height: '100%', width: `${4 + 96 * fill}%`, background: `linear-gradient(90deg, ${C.green}, ${C.amber}, ${C.coral})`}} />
        </div>
      </div>
      <div style={{flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gridTemplateRows: 'repeat(2, 1fr)', gap: 24}}>
        {FACTORS.map((f, i) => (
          <Tile key={f} label={f} color={COLORS[i] ?? C.green} i={i} />
        ))}
      </div>
    </Scene>
  );
};
