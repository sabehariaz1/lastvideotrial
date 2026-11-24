import React from 'react';
import {C, Card, Heading, Scene, ltr, useSpring} from './ui';
import {PROG_CARDS} from '../timing';

const Dot: React.FC<{i: number}> = ({i}) => {
  const s = useSpring(10 + i * 0.7, 12);
  const col = i < 5 ? C.coral : i < 10 ? C.amber : '#E7D9C6';
  // mirrored: the first dots start at the right-hand side
  return <circle cx={(9 - (i % 10)) * 56 + 28} cy={Math.floor(i / 10) * 56 + 28} r={20 * Math.max(0, s)} fill={col} />;
};

export const ProgressionScene: React.FC = () => (
  <Scene caption="ما قبل السكري إنذار، وليس تشخيصًا بالسكري" source={`المصدر: ${ltr('[4]')} Tabák et al., The Lancet 2012`}>
    <Heading>ماذا يحدث بعد ذلك؟</Heading>
    <div style={{flex: 1, minHeight: 0, display: 'flex', gap: 36}}>
      <Card delay={6} from="left" style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <svg viewBox="0 0 560 560" width="100%" height="560" style={{direction: 'ltr'}}>
          {Array.from({length: 100}, (_, i) => <Dot key={i} i={i} />)}
        </svg>
      </Card>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 28, minHeight: 0}}>
        <Card delay={PROG_CARDS[0] ?? 30} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
          <div style={{fontSize: 48, fontWeight: 800, color: C.coral, lineHeight: 1.3}}>من 5 إلى 10 من كل 100</div>
          <div style={{fontSize: 30, color: C.sub, lineHeight: 1.45}}>من المصابين بما قبل السكري يُصابون بالسكري من النوع 2 كل عام {ltr('[4]')}</div>
        </Card>
        <Card delay={PROG_CARDS[1] ?? 50} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
          <div style={{fontSize: 48, fontWeight: 800, color: C.green, lineHeight: 1.3}}>كثيرون يعودون إلى المعدل الطبيعي</div>
          <div style={{fontSize: 30, color: C.sub, lineHeight: 1.45}}>بعد تغييرات صحية في نمط الحياة {ltr('[4]')}</div>
        </Card>
      </div>
    </div>
  </Scene>
);
