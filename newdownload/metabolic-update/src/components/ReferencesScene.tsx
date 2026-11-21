import React from 'react';
import {C, Card, Heading, Scene} from './ui';

const REFS: string[] = [
  'WHO/IDF (2006). Definition and diagnosis of diabetes mellitus and intermediate hyperglycaemia. Geneva: WHO.',
  'NICE (2012, updated 2017). Type 2 diabetes: prevention in people at high risk. PH38.',
  'International Diabetes Federation (2021). IDF Diabetes Atlas, 10th edition.',
  'Tabák AG et al. (2012). Prediabetes: a high-risk state for diabetes development. Lancet 379:2279-2290.',
  'Petersen MC, Shulman GI (2018). Mechanisms of insulin action and insulin resistance. Physiol Rev 98:2133-2223.',
  'Tuomilehto J et al. (2001). Prevention of type 2 diabetes by changes in lifestyle. N Engl J Med 344:1343-1350.',
  'WHO (2020). Guidelines on physical activity and sedentary behaviour.',
  'Prediabetes Risk Test (American Diabetes Association / CDC): a score of 5 or higher means higher risk.',
];

export const ReferencesScene: React.FC = () => (
  <Scene caption="For education only. Not medical advice.">
    <Heading>References</Heading>
    <div style={{flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: '1fr 1fr', gridTemplateRows: 'repeat(4, 1fr)', gridAutoFlow: 'column', gap: 18}}>
      {REFS.map((r, i) => (
        <Card key={r} delay={6 + i * 5} from={i < 4 ? 'left' : 'right'} style={{display: 'flex', alignItems: 'center', gap: 18, padding: 16}}>
          <div style={{width: 44, height: 44, borderRadius: 22, background: C.green, color: '#fff', fontSize: 24, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>{i + 1}</div>
          <div style={{fontSize: 23, lineHeight: 1.25}}>{r}</div>
        </Card>
      ))}
    </div>
  </Scene>
);
