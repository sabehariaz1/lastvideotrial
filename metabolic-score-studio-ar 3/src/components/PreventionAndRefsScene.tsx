import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, Card, Heading, Ltr, Scene, ltr, useSpring} from './ui';
import {NEXT_STEPS} from '../timing';

const STEPS = [`افحص درجة خطرك ${ltr('[8]')}`, `اسأل طبيبك عن فحص الدم ${ltr('[2]')}`, 'اختر تغييرًا صغيرًا واحدًا هذا الأسبوع'];

const Step: React.FC<{text: string; i: number}> = ({text, i}) => {
  const s = useSpring((NEXT_STEPS[i] ?? 60) + 4, 8);
  return (
    <Card delay={NEXT_STEPS[i] ?? 60} from="right" style={{display: 'flex', alignItems: 'center', gap: 22, padding: 24}}>
      <div style={{width: 56, height: 56, borderRadius: 28, background: C.green, color: '#fff', fontSize: 32, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, transform: `scale(${Math.max(0, s)})`}}>{i + 1}</div>
      <div style={{fontSize: 36, fontWeight: 700, lineHeight: 1.35}}>{text}</div>
    </Card>
  );
};

export const PreventionAndRefsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [30, 90], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <Scene caption="التغييرات الصغيرة قد تصنع فرقًا كبيرًا" source={`المصدر: ${ltr('[6]')} Tuomilehto et al., New England Journal of Medicine 2001`}>
      <Heading>هل ينجح الأمر؟ نعم.</Heading>
      <div style={{flex: 1, minHeight: 0, display: 'flex', gap: 36}}>
        <Card delay={10} from="left" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 12}}>
          <div style={{fontSize: 110, fontWeight: 800, color: C.green, lineHeight: 1.1}}><Ltr>58%</Ltr></div>
          <div style={{fontSize: 32, fontWeight: 700, lineHeight: 1.4}}>انخفاض في خطر الإصابة بالسكري مع تغيير نمط الحياة {ltr('[6]')}</div>
          <div style={{fontSize: 24, color: C.sub, lineHeight: 1.4}}>دراسة فنلندية على بالغين يعانون من ضعف تحمّل الجلوكوز</div>
          <div style={{fontSize: 24, color: C.sub, marginTop: 8}}>النصائح المعتادة</div>
          <div style={{height: 32, borderRadius: 16, background: C.amber, width: `${100 * w}%`}} />
          <div style={{fontSize: 24, color: C.sub}}>برنامج نمط الحياة</div>
          <div style={{height: 32, borderRadius: 16, background: C.green, width: `${42 * w}%`}} />
        </Card>
        <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 22, justifyContent: 'center'}}>
          <div style={{fontSize: 40, fontWeight: 800, color: C.teal}}>خطواتك التالية</div>
          {STEPS.map((t, i) => <Step key={i} text={t} i={i} />)}
        </div>
      </div>
    </Scene>
  );
};
