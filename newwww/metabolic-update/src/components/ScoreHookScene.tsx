import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, Scene, Words, useFloat, useIn, useSpring} from './ui';

export const ScoreHookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const art = useIn(8, 'right');
  const float = useFloat(8);
  const pop = useSpring(30, 9);
  const badge = useSpring(100, 9);
  const bar = interpolate(frame, [45, 100], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <Scene caption="Take the 1-minute risk test" source="Risk score cut-off of 5: Prediabetes Risk Test, American Diabetes Association / CDC [8]">
      <div style={{flex: 1, minHeight: 0, display: 'flex', alignItems: 'center', gap: 50}}>
        <div style={{flex: 1.25}}>
          <Words text="If your score is 5 or higher, you are at high risk of developing prediabetes." size={72} />
          <div style={{height: 26}} />
          <div style={{color: C.sub}}><Words text="So, what does that actually mean?" size={42} delay={160} /></div>
        </div>
        <div style={{flex: 1, height: 600, ...art}}>
          <svg viewBox="0 0 520 520" width="100%" height="100%" style={{transform: `translateY(${float}px)`}}>
            <defs>
              <linearGradient id="rk" x1="0" x2="1" y1="0" y2="0">
                <stop offset="0" stopColor={C.green} />
                <stop offset="0.55" stopColor={C.amber} />
                <stop offset="1" stopColor={C.coral} />
              </linearGradient>
            </defs>
            <circle cx="260" cy="260" r="245" fill={C.bg2} />
            <rect x="100" y="70" width="320" height="380" rx="36" fill="#fff" stroke={C.border} strokeWidth="6" />
            <text x="260" y="135" fontSize="26" fontWeight="700" fill={C.sub} textAnchor="middle" letterSpacing="3">YOUR RISK SCORE</text>
            <text x="260" y="290" fontSize={170 * Math.max(0.01, pop)} fontWeight="800" fill={C.coral} textAnchor="middle">5+</text>
            <rect x="140" y="325" width="240" height="26" rx="13" fill={C.border} />
            <rect x="140" y="325" width={240 * bar} height="26" rx="13" fill="url(#rk)" />
            <g transform={`translate(260 405) scale(${Math.max(0, badge)})`}>
              <rect x="-95" y="-24" width="190" height="48" rx="24" fill={C.coral} />
              <text x="0" y="9" fontSize="26" fontWeight="800" fill="#fff" textAnchor="middle">HIGH RISK</text>
            </g>
          </svg>
        </div>
      </div>
    </Scene>
  );
};
