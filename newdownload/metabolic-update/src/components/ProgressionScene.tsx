import React from 'react';
import {C, Card, Heading, Scene, useSpring} from './ui';

const Dot: React.FC<{i: number}> = ({i}) => {
  const s = useSpring(10 + i * 0.7, 12);
  const col = i < 5 ? C.coral : i < 10 ? C.amber : '#E7D9C6';
  return <circle cx={(i % 10) * 56 + 28} cy={Math.floor(i / 10) * 56 + 28} r={20 * Math.max(0, s)} fill={col} />;
};

export const ProgressionScene: React.FC = () => (
  <Scene caption="Prediabetes is a warning, not a diagnosis" source="Source: [4] Tabák et al., The Lancet 2012">
    <Heading>What happens next?</Heading>
    <div style={{flex: 1, minHeight: 0, display: 'flex', gap: 36}}>
      <Card delay={6} from="left" style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <svg viewBox="0 0 560 560" width="100%" height="560">
          {Array.from({length: 100}, (_, i) => <Dot key={i} i={i} />)}
        </svg>
      </Card>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 28, minHeight: 0}}>
        <Card delay={30} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
          <div style={{fontSize: 48, fontWeight: 800, color: C.coral, lineHeight: 1.1}}>5 to 10 in 100</div>
          <div style={{fontSize: 30, color: C.sub}}>people with prediabetes develop type 2 diabetes each year [4]</div>
        </Card>
        <Card delay={50} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
          <div style={{fontSize: 48, fontWeight: 800, color: C.green, lineHeight: 1.1}}>Many go back to normal</div>
          <div style={{fontSize: 30, color: C.sub}}>with healthy changes and regular checks [4]</div>
        </Card>
      </div>
    </div>
  </Scene>
);
