import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, Card, CountUp, Heading, Ltr, Scene, ltr, useSpring} from './ui';
import {GAUGE_SILENT, GAUGE_STAT} from '../timing';

const CX = 400;
const CY = 400;
const R = 300;
// Mirrored gauge: "normal" is on the right, "diabetes" on the left (right-to-left reading order).
const pt = (t: number, r: number): [number, number] => [CX - r * Math.cos(Math.PI * (1 - t)), CY - r * Math.sin(Math.PI * (1 - t))];
const arc = (a: number, b: number): string => {
  const [x1, y1] = pt(a, R);
  const [x2, y2] = pt(b, R);
  return `M${x1} ${y1} A${R} ${R} 0 0 0 ${x2} ${y2}`;
};

export const PrevalenceAndGaugeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
  const t = 0.08 + 0.47 * useSpring(80, 7);
  const [nx, ny] = pt(t, R - 50);
  const zones: Array<[string, string, string]> = [
    ['طبيعي', '< 100 mg/dL', C.teal],
    ['ما قبل السكري', '100–125 mg/dL', C.amber],
    ['السكري', '≥ 126 mg/dL', C.coral],
  ];
  const segs: Array<[number, number, string, number]> = [[0, 0.4, C.teal, 10], [0.4, 0.7, C.amber, 30], [0.7, 1, C.coral, 50]];
  return (
    <Scene caption="معظم المصابين بما قبل السكري لا يعلمون بذلك" source={`المصادر: ${ltr('[1]')} WHO/IDF 2006؛ ${ltr('[2]')} NICE PH38؛ ${ltr('[3]')} IDF Diabetes Atlas 2021. القيم بوحدة mg/dL وقد تختلف الحدود قليلًا.`}>
      <Heading>ما قبل السكري شائع، وغالبًا بلا أعراض.</Heading>
      <div style={{flex: 1, minHeight: 0, display: 'flex', gap: 36}}>
        <Card delay={6} from="left" style={{flex: 1.5, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'space-between'}}>
          <svg viewBox="30 50 740 400" width="100%" height="420" style={{direction: 'ltr'}}>
            {segs.map(([a, b, col, s]) => (
              <path key={col} d={arc(a, b)} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - interpolate(frame, [s, s + 25], [0, 1], clamp)} stroke={col} strokeWidth="56" fill="none" />
            ))}
            <line x1={CX} y1={CY} x2={nx} y2={ny} stroke={C.ink} strokeWidth="12" strokeLinecap="round" />
            <circle cx={CX} cy={CY} r="26" fill={C.ink} />
          </svg>
          <div style={{fontSize: 26, color: C.sub, fontWeight: 600}}>سكر الدم الصائم</div>
          <div style={{display: 'flex', gap: 26}}>
            {zones.map(([name, range, col]) => (
              <div key={name} style={{borderRight: `10px solid ${col}`, paddingRight: 14, fontSize: 28, fontWeight: 700}}>
                {name}
                <div style={{fontSize: 22, fontWeight: 500, color: C.sub}}><Ltr>{range}</Ltr></div>
              </div>
            ))}
          </div>
        </Card>
        <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 28, minHeight: 0}}>
          <Card delay={GAUGE_SILENT} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
            <div style={{fontSize: 46, fontWeight: 800, color: C.coral, lineHeight: 1.3}}>غالبًا بلا أعراض</div>
            <div style={{fontSize: 30, color: C.sub, lineHeight: 1.4}}>معظم الناس يشعرون بأنهم بخير تمامًا.</div>
          </Card>
          <Card delay={GAUGE_STAT} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
            <div style={{fontSize: 50, fontWeight: 800, color: C.amber, lineHeight: 1.3}}><Ltr>~<CountUp to={540} start={GAUGE_STAT} /></Ltr> مليون</div>
            <div style={{fontSize: 28, color: C.sub, lineHeight: 1.4}}>بالغ حول العالم يعانون من ضعف تحمّل الجلوكوز {ltr('[3]')}</div>
          </Card>
        </div>
      </div>
    </Scene>
  );
};
