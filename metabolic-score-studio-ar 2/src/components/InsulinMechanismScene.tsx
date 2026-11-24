import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, Card, Heading, Scene, ltr} from './ui';

const Panel: React.FC<{ok: boolean}> = ({ok}) => {
  const frame = useCurrentFrame() % 210;
  const col = ok ? C.green : C.coral;
  const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
  const keyY = ok ? interpolate(frame, [20, 60], [0, 70], clamp) : 12 * Math.sin(frame / 6) ** 2;
  const burst = ok ? interpolate(frame, [60, 90], [0, 1], clamp) : 0;
  const dots = [60, 120, 410, 460];
  return (
    <svg viewBox="0 0 520 420" width="100%" style={{flex: 1, minHeight: 0, direction: 'ltr'}}>
      <circle cx="40" cy="30" r="13" fill={C.coral} />
      <text x="62" y="40" fontSize="28" fill={C.sub}>سكر</text>
      <rect x="40" y="250" width="440" height="140" rx="48" fill={ok ? '#E6F4EA' : '#FDE8E5'} stroke={col} strokeWidth="5" />
      <text x="260" y="365" fontSize="32" fontWeight="700" fill={col} textAnchor="middle">خلية</text>
      <rect x="215" y="240" width="90" height="50" rx="12" fill={col} />
      <circle cx="260" cy="262" r="9" fill="#fff" />
      {ok && frame >= 60 ? <circle cx="260" cy="262" r={24 + burst * 70} fill="none" stroke={C.green} strokeWidth="5" opacity={1 - burst} /> : null}
      <g transform={`translate(0 ${keyY})`}>
        <circle cx="260" cy="105" r="30" fill={C.amber} />
        <rect x="253" y="132" width="14" height="70" rx="5" fill={C.amber} />
        <rect x="267" y="165" width="18" height="9" fill={C.amber} />
        <rect x="267" y="183" width="14" height="9" fill={C.amber} />
        <text x="302" y="114" fontSize="28" fontWeight="700" fill={C.amber}>إنسولين</text>
      </g>
      {dots.map((x, i) => {
        const y = ok ? interpolate(frame, [60 + i * 8, 105 + i * 8], [60, 305], clamp) : 70 + (i % 2) * 45 + 5 * Math.sin(frame / 8 + i);
        return <circle key={x} cx={x} cy={y} r="15" fill={C.coral} opacity="0.88" />;
      })}
    </svg>
  );
};

export const InsulinMechanismScene: React.FC = () => (
  <Scene caption="الإنسولين هو المفتاح. والسكر هو الوقود." source={`المصدر: ${ltr('[5]')} Petersen & Shulman, Physiological Reviews 2018`}>
    <Heading>الإنسولين يُدخل السكر إلى خلاياك.</Heading>
    <div style={{flex: 1, minHeight: 0, display: 'flex', gap: 36}}>
      <Card delay={8} from="left" style={{flex: 1, display: 'flex', flexDirection: 'column'}}>
        <div style={{fontSize: 38, fontWeight: 800, color: C.green, lineHeight: 1.3}}>المفتاح يناسب القفل: يدخل السكر</div>
        <Panel ok />
      </Card>
      <Card delay={18} from="right" style={{flex: 1, display: 'flex', flexDirection: 'column'}}>
        <div style={{fontSize: 38, fontWeight: 800, color: C.coral, lineHeight: 1.3}}>القفل عالق: يتراكم السكر</div>
        <Panel ok={false} />
      </Card>
    </div>
  </Scene>
);
