import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, Card, Heading, Scene, useSpring} from './ui';

const TIPS = ['Move at least 150 minutes a week [7]', 'Eat more whole foods [6]', 'Lose at least 5% of body weight if you carry extra [6]'];

const Tip: React.FC<{text: string; i: number}> = ({text, i}) => {
  const s = useSpring(16 + i * 8, 8);
  return (
    <Card delay={10 + i * 8} from="left" style={{display: 'flex', alignItems: 'center', gap: 22, padding: 24}}>
      <div style={{width: 56, height: 56, borderRadius: 28, background: C.green, color: '#fff', fontSize: 32, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, transform: `scale(${Math.max(0, s)})`}}>{i + 1}</div>
      <div style={{fontSize: 36, fontWeight: 700, lineHeight: 1.2}}>{text}</div>
    </Card>
  );
};

export const PreventionAndRefsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [40, 100], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <Scene caption="Small changes can make a big difference" source="Sources: [6] Tuomilehto et al., NEJM 2001; [7] WHO physical activity guidelines 2020">
      <Heading>Good news: you can lower your risk.</Heading>
      <div style={{flex: 1, minHeight: 0, display: 'flex', gap: 36}}>
        <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 22, justifyContent: 'center'}}>
          {TIPS.map((t, i) => <Tip key={t} text={t} i={i} />)}
        </div>
        <Card delay={30} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 14}}>
          <div style={{fontSize: 110, fontWeight: 800, color: C.green, lineHeight: 1}}>58%</div>
          <div style={{fontSize: 32, fontWeight: 700}}>lower risk of diabetes with lifestyle changes [6]</div>
          <div style={{fontSize: 24, color: C.sub, marginTop: 10}}>Usual advice</div>
          <div style={{height: 34, borderRadius: 17, background: C.amber, width: `${100 * w}%`}} />
          <div style={{fontSize: 24, color: C.sub}}>Lifestyle program</div>
          <div style={{height: 34, borderRadius: 17, background: C.green, width: `${42 * w}%`}} />
        </Card>
      </div>
    </Scene>
  );
};
