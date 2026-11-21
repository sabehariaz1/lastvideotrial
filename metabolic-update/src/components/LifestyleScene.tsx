import React from 'react';
import {C, Card, Heading, Scene, useFloat} from './ui';
import {LIFE_CARDS} from '../timing';

const Walk: React.FC = () => (
  <svg viewBox="0 0 120 140" width="220" height="245" fill="none" stroke={C.green} strokeWidth="9" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="62" cy="22" r="13" fill={C.green} stroke="none" />
    <path d="M60 40 L54 86 M60 52 L38 70 M60 52 L84 62 M54 86 L34 120 M54 86 L80 112 L78 128" />
  </svg>
);
const Plate: React.FC = () => (
  <svg viewBox="0 0 120 140" width="220" height="245">
    <circle cx="60" cy="70" r="54" fill="#fff" stroke={C.amber} strokeWidth="8" />
    <circle cx="42" cy="58" r="15" fill={C.coral} />
    <circle cx="76" cy="52" r="17" fill={C.green} />
    <ellipse cx="62" cy="92" rx="22" ry="13" fill={C.amber} />
  </svg>
);
const Scale: React.FC = () => (
  <svg viewBox="0 0 120 140" width="220" height="245" fill="none" strokeLinecap="round">
    <rect x="14" y="26" width="92" height="94" rx="20" fill="#fff" stroke={C.teal} strokeWidth="8" />
    <path d="M34 66 A26 26 0 0 1 86 66" stroke={C.border} strokeWidth="8" />
    <path d="M60 66 L72 46" stroke={C.coral} strokeWidth="7" />
    <path d="M60 88 V106 M50 98 L60 108 L70 98" stroke={C.green} strokeWidth="7" strokeLinejoin="round" />
  </svg>
);

const ITEMS: Array<[React.FC, string, string, string]> = [
  [Walk, '150+ min a week', 'Moderate activity, such as brisk walking [7]', C.green],
  [Plate, 'More fibre, less saturated fat', 'Whole grains, vegetables, fruit, beans [6]', C.amber],
  [Scale, 'Lose ≥ 5% of body weight', 'If you carry extra weight [6]', C.teal],
];

const Col: React.FC<{i: number}> = ({i}) => {
  const f = useFloat(6, 20, i);
  const item = ITEMS[i];
  if (!item) return null;
  const [Icon, head, sub, col] = item;
  return (
    <Card delay={LIFE_CARDS[i] ?? 30} from="pop" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', gap: 14, borderTop: `10px solid ${col}`}}>
      <div style={{transform: `translateY(${f}px)`}}><Icon /></div>
      <div style={{fontSize: 40, fontWeight: 800, lineHeight: 1.15}}>{head}</div>
      <div style={{fontSize: 28, color: C.sub, lineHeight: 1.25}}>{sub}</div>
    </Card>
  );
};

export const LifestyleScene: React.FC = () => (
  <Scene caption="Three habits that make a real difference" source="Sources: [6] Tuomilehto et al., NEJM 2001; [7] WHO physical activity guidelines 2020">
    <Heading>What actually helps?</Heading>
    <div style={{flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 28}}>
      {[0, 1, 2].map((i) => <Col key={i} i={i} />)}
    </div>
  </Scene>
);
