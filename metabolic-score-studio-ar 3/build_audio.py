#!/usr/bin/env python3
"""Builds the Arabic narration, re-times the whole video to it and rebuilds the sound effects.

Writes:  public/voiceover-ar.mp3, public/sfx.mp3, src/timing.ts, src/config.ts
Needs:   ffmpeg (or `pip install imageio-ffmpeg`), and `pip install edge-tts gTTS`  (set MOCK_TTS=1 to test without internet)
"""
import array, asyncio, json, math, os, shutil, subprocess, sys, tempfile, time, wave

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
F, T, SR = 30, 18, 44100          # fps, transition frames, sample rate
TARGET_FRAMES = 3600              # 2:00
LEAD, GAP_IN, GAP_SCENE, TAIL, CUE_LEAD = 0.5, 0.35, 0.8, 2.5, 0.12
MAX_SPEEDUP = 1.2

# ---- Arabic narration: one tuple per sentence: (text, cue). Edit the wording here. ----
SCENES = [
    [
        ('إذا كانت درجتك خمسة أو أكثر، فأنت معرَّض لخطرٍ مرتفع للإصابة بما قبل السكري.'),
        ('فماذا يعني هذا فعلًا؟', 'hook'),
    ],
    [
        ('ما قبل السكري يعني أن سكر دمك أعلى من الطبيعي.'),
        ('الطبيعي أقل من مئة، وما قبل السكري من مئة إلى مئة وخمسة وعشرين، والسكري من مئة وستة وعشرين فأكثر.'),
        ('وهو غالبًا بلا أعراض.', 'silent'),
        ('ونحو خمسمئة وأربعين مليون بالغ حول العالم يعانون من ضعف تحمّل الجلوكوز.', 'stat'),
    ],
    [
        ('الإنسولين هو المفتاح الذي يُدخل السكر إلى خلاياك.'),
        ('وعند مقاومة الإنسولين يعلق القفل، فيتراكم السكر في الدم.'),
    ],
    [
        ('فما الذي يرفع درجتك؟'),
        ('العمر أربعون سنة أو أكثر.', 'risk'),
        ('زيادة الوزن.', 'risk'),
        ('تاريخ عائلي للسكري.', 'risk'),
        ('قلة النشاط البدني.', 'risk'),
        ('ارتفاع ضغط الدم.', 'risk'),
        ('والسكري أثناء الحمل.', 'risk'),
        ('وكل عامل قد يضيف نقاطًا إلى درجتك.'),
    ],
    [
        ('فحص الدم يوضّح أين تقف.'),
        ('سكر الدم الصائم من مئة إلى مئة وخمسة وعشرين يعني ما قبل السكري.', 'diag'),
        ('والسكر التراكمي من ستة إلى ستة فاصلة أربعة بالمئة.', 'diag'),
        ('واختبار السكر بعد ساعتين من مئة وأربعين إلى مئة وتسعة وتسعين.', 'diag'),
        ('اسأل طبيبك أي فحص يناسبك.'),
    ],
    [
        ('فماذا يحدث بعد ذلك؟'),
        ('من كل مئة مصاب بما قبل السكري، يُصاب من خمسة إلى عشرة بالسكري كل عام.', 'prog'),
        ('لكن كثيرين يعودون إلى المعدل الطبيعي بتغيير نمط حياتهم.', 'prog'),
        ('فهو إنذار، وليس تشخيصًا.'),
    ],
    [
        ('فما الذي يساعد فعلًا؟'),
        ('مئة وخمسون دقيقة أسبوعيًا من النشاط المعتدل، مثل المشي السريع.', 'life'),
        ('ألياف أكثر ودهون مشبعة أقل.', 'life'),
        ('وخسارة خمسة بالمئة من الوزن الزائد تصنع فرقًا.', 'life'),
    ],
    [
        ('هل ينجح الأمر؟ نعم.'),
        ('في دراسة فنلندية، خفّضت هذه التغييرات خطر السكري بنسبة ثمانية وخمسين بالمئة.'),
        ('خطواتك التالية:'),
        ('أولًا، افحص درجة خطرك.', 'next'),
        ('ثانيًا، اسأل طبيبك عن فحص الدم.', 'next'),
        ('وثالثًا، اختر تغييرًا صغيرًا هذا الأسبوع.', 'next'),
    ],
    [
        ('المراجع على الشاشة. هذا الفيديو للتثقيف فقط، وليس نصيحة طبية.'),
    ],
]
def _seg(t):
    t = (t,) if isinstance(t, str) else t
    return {'text': t[0], **({'cue': t[1]} if len(t) > 1 else {})}


CFG_SCENES = [[_seg(t) for t in sc] for sc in SCENES]
cfg = {'scenes': CFG_SCENES}
VOICE = os.environ.get('VOICE') or 'ar-AE-FatimaNeural'  # other: ar-AE-HamdanNeural, ar-SA-HamedNeural, ar-SA-ZariyahNeural
MOCK = os.environ.get('MOCK_TTS') == '1'
work = tempfile.mkdtemp(prefix='narr_')


def _ffmpeg():
    found = shutil.which('ffmpeg')
    if found:
        return found
    import imageio_ffmpeg  # pip install imageio-ffmpeg (ships a static ffmpeg)
    return imageio_ffmpeg.get_ffmpeg_exe()


FFMPEG = _ffmpeg()


def run(*cmd):
    cmd = (FFMPEG,) + cmd[1:] if cmd[0] == 'ffmpeg' else cmd
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def wav_dur(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


async def _edge(text, out):
    import edge_tts
    await edge_tts.Communicate(text, VOICE).save(out)


def _gtts(text, out):
    from gtts import gTTS
    gTTS(text=text, lang='ar').save(out)


def synth(text, out):
    if MOCK:  # stand-in tone so the timing maths can be tested offline
        run('ffmpeg', '-y', '-f', 'lavfi', '-i', f'sine=frequency=220:duration={0.075 * len(text):.2f}', out)
        return 'mock'
    last = None
    for attempt in range(3):
        try:
            asyncio.run(_edge(text, out))
            if os.path.getsize(out) > 1000:
                return 'edge-tts'
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    print(f'  edge-tts failed ({last}); falling back to gTTS', flush=True)
    _gtts(text, out)
    return 'gTTS'


TRIM = ('silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,'
        'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse')

# 1) synthesise every segment
segs = []  # dict(scene, text, cue, wav)
engine = None
for si, scene in enumerate(cfg['scenes']):
    for k, s in enumerate(scene):
        raw = os.path.join(work, f's{si}_{k}.mp3')
        wav = os.path.join(work, f's{si}_{k}.wav')
        engine = synth(s['text'], raw)
        run('ffmpeg', '-y', '-i', raw, '-ar', str(SR), '-ac', '1', '-af', TRIM, wav)
        segs.append({'scene': si, 'text': s['text'], 'cue': s.get('cue'), 'wav': wav, 'dur': wav_dur(wav)})
        print(f'scene {si + 1} seg {k + 1}: {segs[-1]["dur"]:.2f}s', flush=True)
print(f'voice engine: {engine} ({VOICE})')

# 2) speed up if needed so the whole video is 2:00
n_in = sum(len(sc) - 1 for sc in cfg['scenes'])
fixed = LEAD + n_in * GAP_IN + (len(cfg['scenes']) - 1) * GAP_SCENE
speech = sum(s['dur'] for s in segs)
allowed = TARGET_FRAMES / F - TAIL - fixed
speed = speech / allowed
if speed > 1.01:
    speed = min(speed, MAX_SPEEDUP)
    print(f'speech {speech:.1f}s too long for {allowed:.1f}s -> speeding up x{speed:.3f}')
    for i, s in enumerate(segs):
        fast = s['wav'].replace('.wav', '_fast.wav')
        run('ffmpeg', '-y', '-i', s['wav'], '-af', f'atempo={speed:.4f}', fast)
        s['wav'], s['dur'] = fast, wav_dur(fast)
else:
    speed = 1.0

# 3) lay everything out on the timeline
t = LEAD
scene_first = {}
for si, scene in enumerate(cfg['scenes']):
    items = [s for s in segs if s['scene'] == si]
    for k, s in enumerate(items):
        s['start'] = t
        if k == 0:
            scene_first[si] = t
        t += s['dur'] + (GAP_IN if k < len(items) - 1 else 0)
    speech_end = t
    t += GAP_SCENE
n_scenes = len(cfg['scenes'])
start = [0] + [round(scene_first[i] * F) - T for i in range(1, n_scenes)]
dur = [start[i + 1] - start[i] + T for i in range(n_scenes - 1)]
last = max(TARGET_FRAMES - start[-1], math.ceil((speech_end + TAIL) * F) - start[-1])
dur.append(last)
total_frames = start[-1] + dur[-1]
print(f'scene durations: {dur}\ntotal frames: {total_frames} = {total_frames / F:.2f}s')

# 4) cues (frame inside its own scene)
cues = {k: [] for k in ('hook', 'silent', 'stat', 'risk', 'diag', 'prog', 'life', 'next')}
pops = []
for s in segs:
    if not s['cue']:
        continue
    local = max(0, round((s['start'] - CUE_LEAD) * F) - start[s['scene']])
    cues[s['cue']].append(local)
    if s['cue'] != 'hook':
        pops.append((start[s['scene']] + local) / F)


def arr(name):
    return ', '.join(map(str, cues[name]))


timing = f"""// Generated by scripts/build_audio.py from the Arabic narration. Do not edit by hand.
export const TRANSITION_FRAMES = {T};
export const SCENE_DURATIONS: readonly number[] = [{', '.join(map(str, dur))}];
export const HOOK_SECOND = {cues['hook'][0]};
export const RISK_TICKS: readonly number[] = [{arr('risk')}];
export const DIAG_CARDS: readonly number[] = [{arr('diag')}];
export const LIFE_CARDS: readonly number[] = [{arr('life')}];
export const NEXT_STEPS: readonly number[] = [{arr('next')}];
export const PROG_CARDS: readonly number[] = [{arr('prog')}];
export const GAUGE_SILENT = {cues['silent'][0]};
export const GAUGE_STAT = {cues['stat'][0]};
"""
os.makedirs(os.path.join(ROOT, 'src'), exist_ok=True)
open(os.path.join(ROOT, 'src', 'timing.ts'), 'w').write(timing)
open(os.path.join(ROOT, 'src', 'config.ts'), 'w').write(
    '// Set automatically by scripts/build_audio.py once public/voiceover-ar.mp3 exists.\nexport const HAS_VOICEOVER = true;\n')

# 5) voiceover (mono)
n = int((total_frames / F + 0.5) * SR)
voice = array.array('h', [0]) * n
for s in segs:
    with wave.open(s['wav']) as w:
        data = array.array('h')
        data.frombytes(w.readframes(w.getnframes()))
    i0 = int(s['start'] * SR)
    for j, v in enumerate(data):
        if i0 + j < n:
            voice[i0 + j] = v
tmp = os.path.join(work, 'voice.wav')
with wave.open(tmp, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(voice.tobytes())
pub = os.path.join(ROOT, 'public')
os.makedirs(pub, exist_ok=True)
run('ffmpeg', '-y', '-i', tmp, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(SR), '-b:a', '128k',
    os.path.join(pub, 'voiceover-ar.mp3'))

# 6) sound effects: a whoosh at every scene change, a pop at every card
def make_whoosh():
    import random
    random.seed(1)
    n, lp, raw = int(0.65 * SR), 0.0, []
    for i in range(n):
        x = i / n
        a = 0.02 + 0.5 * math.sin(math.pi * x)           # filter sweeps up and back down
        lp += a * (random.uniform(-1, 1) - lp)
        raw.append(lp * math.sin(math.pi * x) ** 2)
    peak = max(abs(v) for v in raw) or 1
    out = array.array('h')
    for v in raw:
        s = int(v / peak * 16000)
        out.extend((s, s))
    return out


def make_pop():
    n, out = int(0.1 * SR), array.array('h')
    for i in range(n):
        t = i / SR
        s = int(math.sin(2 * math.pi * (1100 - 5000 * t) * t) * math.exp(-t * 45) * 5000)
        out.extend((s, s))
    return out


whoosh, pop = make_whoosh(), make_pop()
sfx = array.array('h', [0]) * (n * 2)
events = [(start[i] / F, whoosh) for i in range(1, n_scenes)] + [(p, pop) for p in pops]
for ts, clip in events:
    i0 = max(0, int((ts - 0.02) * SR)) * 2
    for j, v in enumerate(clip):
        if i0 + j < len(sfx):
            x = sfx[i0 + j] + v
            sfx[i0 + j] = max(-32768, min(32767, x))
tmp = os.path.join(work, 'sfx.wav')
with wave.open(tmp, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(sfx.tobytes())
run('ffmpeg', '-y', '-i', tmp, '-b:a', '128k', os.path.join(pub, 'sfx.mp3'))
print('done: public/voiceover-ar.mp3, public/sfx.mp3, src/timing.ts, src/config.ts')
