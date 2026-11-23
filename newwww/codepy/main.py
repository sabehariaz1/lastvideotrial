import os
import textwrap
import numpy as np
from manim import *

QUICK = os.environ.get("QUICK") == "1"
config.pixel_width, config.pixel_height = (854, 480) if QUICK else (1920, 1080)
config.frame_rate = 15 if QUICK else 30

DURS = [330, 689, 441, 514, 542, 499, 616, 523, 450]
RISK_TICKS = [77, 118, 163, 239, 287, 326]
DIAG_CARDS = [169, 220, 330]
LIFE_CARDS = [108, 309, 436]
NEXT_STEPS = [312, 355, 419]
PROG_CARDS = [107, 312]
GAUGE_SILENT = 394
GAUGE_STAT = 509

FPS = 30
STARTS = [(sum(DURS[:i]) - 18 * i) / FPS for i in range(len(DURS))]
TOTAL = (sum(DURS) - 18 * (len(DURS) - 1)) / FPS

BG = "#FFF9F1"
LINE = "#F1E1CC"
CORAL = "#E05244"
AMBER = "#F09D24"
GRN = "#2E9E5B"
TEA = "#2E8B57"
INK = "#3A2E2A"
SUB = "#7A6A5E"
LEFT_X = -6.3


def T(s, size=28, color=INK, bold=True):
    return Text(s, font="Sans", font_size=size, color=color, weight=BOLD if bold else NORMAL)


def card(w, h, x, y, stroke=LINE):
    return RoundedRectangle(corner_radius=0.22, width=w, height=h, fill_color=WHITE, fill_opacity=1,
                            stroke_color=stroke, stroke_width=2).move_to([x, y, 0])


def badge(x, y, col, r=0.2):
    c = Circle(radius=r, fill_color=col, fill_opacity=1, stroke_width=0)
    k = VMobject(stroke_color=WHITE, stroke_width=5).set_points_as_corners(
        [[-r * 0.5, 0, 0], [-r * 0.12, -r * 0.4, 0], [r * 0.55, r * 0.45, 0]])
    return VGroup(c, k).move_to([x, y, 0])


def plus(x, y, col, r=0.3):
    c = Circle(radius=r, fill_color=col, fill_opacity=1, stroke_width=0)
    p = VGroup(Line([-r * .5, 0, 0], [r * .5, 0, 0]), Line([0, -r * .5, 0], [0, r * .5, 0])).set_stroke(WHITE, 6)
    return VGroup(c, p).move_to([x, y, 0])


def num(x, y, n, col=GRN, r=0.22, size=18):
    return VGroup(Circle(radius=r, fill_color=col, fill_opacity=1, stroke_width=0), T(str(n), size, WHITE)).move_to([x, y, 0])


def TL(s, size, color=INK, bold=True):
    return VGroup(*[T(l, size, color, bold) for l in s.split("\n")]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)


def TC(s, size, color=INK, bold=True):
    return VGroup(*[T(l, size, color, bold) for l in s.split("\n")]).arrange(DOWN, buff=0.08)


class Explainer(Scene):
    def at(self, t):
        d = t - self.renderer.time
        if d > 1.0 / config.frame_rate:
            self.wait(d)

    def ab(self, i, frame):
        return STARTS[i] + frame / FPS

    def persistent(self):
        self.camera.background_color = BG
        self.keep = []
        for i, (x, y, col) in enumerate([(-4.5, -2.5, AMBER), (5.2, 3.2, CORAL), (0.5, 3.8, GRN)]):
            b = Circle(radius=2.2, fill_color=col, fill_opacity=0.10, stroke_width=0).move_to([x, y, 0])
            b.add_updater(lambda m, x=x, y=y, i=i: m.move_to(
                [x + 0.6 * np.sin(self.renderer.time / 1.3 + i * 2), y + 0.5 * np.cos(self.renderer.time / 1.7 + i), 0]))
            self.add(b)
            self.keep.append(b)

        def bar_updater(m):
            w = max(0.02, 14.222 * min(1, self.renderer.time / TOTAL))
            m.become(Rectangle(width=w, height=0.07, fill_color=AMBER, fill_opacity=1, stroke_width=0)
                     .move_to([-7.111 + w / 2, 3.965, 0]))
        bar = Rectangle(width=0.02, height=0.07, fill_color=AMBER, fill_opacity=1, stroke_width=0)
        bar.add_updater(bar_updater)
        self.add(bar)
        self.keep.append(bar)

    def start(self, i, caption, source="", heading=None):
        self.at(STARTS[i])
        pill = RoundedRectangle(corner_radius=0.27, width=12.6, height=0.55, fill_color=WHITE, fill_opacity=1,
                                stroke_color=LINE, stroke_width=2).move_to([0, -3.55, 0])
        items = [pill, T(caption, 22, SUB).move_to(pill)]
        if source:
            src = T(source, 13, SUB, False)
            if src.width > 12.6:
                src.scale_to_fit_width(12.6)
            items.append(src.move_to([LEFT_X, -3.07, 0], aligned_edge=LEFT))
        if heading:
            items.append(T(heading, 40).move_to([LEFT_X, 3.2, 0], aligned_edge=LEFT))
        self.play(FadeIn(VGroup(*items), shift=UP * 0.2), run_time=0.4)
        self.grp = VGroup()  # detached helper, never drawn

    def end(self, i):
        if i < len(STARTS) - 1:
            self.at(STARTS[i + 1] - 0.35)
            self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in self.keep], run_time=0.3)

    def show(self, *mobs, **kw):
        self.grp.add(*mobs)
        self.play(*[FadeIn(m, scale=0.85) for m in mobs], run_time=kw.get("rt", 0.45))

    # ---------- scenes ----------
    def s0(self):
        self.start(0, "Take the 1-minute risk test", "Risk score cut-off of 5: Prediabetes Risk Test, American Diabetes Association / CDC [8]")
        lines = [T(s, 44) for s in ["If your score is 5 or higher,", "you are at high risk of", "developing prediabetes."]]
        for k, l in enumerate(lines):
            l.move_to([-6.3, 1.0 - k * 0.85, 0], aligned_edge=LEFT)
        c = card(4.3, 5.2, 4.3, 0.0)
        lab = T("YOUR RISK SCORE", 20, SUB).move_to([4.3, 2.0, 0])
        big = T("5+", 120, CORAL).move_to([4.3, 0.75, 0])
        track = Rectangle(width=2.7, height=0.2, fill_color=LINE, fill_opacity=1, stroke_width=0).move_to([4.3, -0.55, 0])
        segs = VGroup(*[Rectangle(width=0.9, height=0.2, fill_color=col, fill_opacity=1, stroke_width=0).move_to([2.95 + 0.9 * j + 0.45, -0.55, 0])
                        for j, col in enumerate([GRN, AMBER, CORAL])])
        pill = RoundedRectangle(corner_radius=0.3, width=2.4, height=0.6, fill_color=CORAL, fill_opacity=1, stroke_width=0).move_to([4.3, -1.5, 0])
        hr = T("HIGH RISK", 24, WHITE).move_to(pill)
        self.grp.add(*lines, c, lab, big, track, segs, pill, hr)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.3) for l in lines], lag_ratio=0.35), FadeIn(VGroup(c, lab)), run_time=1.6)
        self.play(GrowFromCenter(big), run_time=0.6)
        self.play(FadeIn(track), LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in segs], lag_ratio=0.3), run_time=1.2)
        self.play(GrowFromCenter(VGroup(pill, hr)), run_time=0.5)
        sub = T("So, what does that actually mean?", 32, SUB).move_to([-6.3, -2.0, 0], aligned_edge=LEFT)
        self.at(self.ab(0, 160))
        self.show(sub)
        self.end(0)

    def s1(self):
        self.start(1, "Most people with prediabetes do not know it",
                   "Sources: [1] WHO/IDF 2006; [2] NICE PH38; [3] IDF Diabetes Atlas 2021. Values in mg/dL; cut-offs vary slightly by guideline.",
                   "Prediabetes is common, and often silent.")
        c = card(8.2, 5.3, -2.6, -0.05)
        self.show(c)
        ctr = np.array([-2.6, -0.2, 0.0])
        R = 2.4
        arcs = []
        for a, b, col in [(0, .4, TEA), (.4, .7, AMBER), (.7, 1, CORAL)]:
            arcs.append(Arc(radius=R, start_angle=PI * (1 - a), angle=-PI * (b - a), arc_center=ctr, stroke_width=30, stroke_color=col))
        self.grp.add(*arcs)
        self.play(*[Create(a_) for a_ in arcs], run_time=1.5)
        vt = ValueTracker(0.08)
        needle = always_redraw(lambda: Line(ctr, ctr + (R - 0.4) * np.array([np.cos(PI * (1 - vt.get_value())), np.sin(PI * (1 - vt.get_value())), 0]),
                                           color=INK, stroke_width=8))
        hub = Dot(ctr, radius=0.16, color=INK)
        self.grp.add(needle, hub)
        self.add(needle, hub)
        self.play(vt.animate.set_value(0.55), run_time=1.6, rate_func=rate_functions.ease_out_back)
        lab = T("Fasting blood sugar", 20, SUB).move_to([-2.6, -0.85, 0])
        leg = VGroup()
        for k, (n, r, col) in enumerate([("Normal", "< 100 mg/dL", TEA), ("Prediabetes", "100–125 mg/dL", AMBER), ("Diabetes", "≥ 126 mg/dL", CORAL)]):
            bar = Rectangle(width=0.09, height=0.6, fill_color=col, fill_opacity=1, stroke_width=0)
            txt = VGroup(T(n, 22), T(r, 17, SUB, False)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            leg.add(VGroup(bar, txt).arrange(RIGHT, buff=0.15))
        leg.arrange(RIGHT, buff=0.5).move_to([-2.6, -1.85, 0])
        self.show(lab, leg)
        c1 = card(5.1, 2.45, 4.5, 1.28)
        t1 = VGroup(T("Often silent", 34, CORAL), T("Most people feel completely fine.", 18, SUB, False)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(c1).align_to(c1, LEFT).shift(RIGHT * 0.4)
        self.at(self.ab(1, GAUGE_SILENT))
        self.show(c1, t1)
        c2 = card(5.1, 2.45, 4.5, -1.35)
        cnt = ValueTracker(0)
        num = always_redraw(lambda: T(f"~{int(cnt.get_value())} million", 40, AMBER).move_to([2.35, -0.9, 0], aligned_edge=LEFT))
        d2 = T("adults worldwide have impaired\nglucose tolerance [3]", 18, SUB, False).move_to([2.35, -1.75, 0], aligned_edge=LEFT)
        self.at(self.ab(1, GAUGE_STAT))
        self.grp.add(c2, d2, num)
        self.play(FadeIn(c2), FadeIn(d2), run_time=0.4)
        self.add(num)
        self.play(cnt.animate.set_value(540), run_time=1.6, rate_func=rate_functions.ease_out_cubic)
        self.end(1)

    def s2(self):
        self.start(2, "Insulin is the key. Sugar is the fuel.", "Source: [5] Petersen & Shulman, Physiological Reviews 2018", "Insulin lets sugar into your cells.")
        for cx, ok in [(-3.3, True), (3.3, False)]:
            col = GRN if ok else CORAL
            c = card(6.2, 5.3, cx, -0.05)
            title = T("Key fits: sugar gets in" if ok else "Lock sticks: sugar piles up", 28, col).move_to([cx, 2.2, 0])
            cell = RoundedRectangle(corner_radius=0.5, width=5.0, height=1.4, fill_color="#E6F4EA" if ok else "#FDE8E5", fill_opacity=1,
                                    stroke_color=col, stroke_width=5).move_to([cx, -1.9, 0])
            cl = T("Cell", 24, col).move_to([cx, -2.25, 0])
            lock = RoundedRectangle(corner_radius=0.1, width=0.9, height=0.45, fill_color=col, fill_opacity=1, stroke_width=0).move_to([cx, -1.2, 0])
            hole = Dot([cx, -1.2, 0], radius=0.07, color=WHITE)
            key = VGroup(Circle(radius=0.26, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([cx, 0.9, 0]),
                         Rectangle(width=0.13, height=0.85, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([cx, 0.25, 0]),
                         Rectangle(width=0.2, height=0.1, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([cx + 0.14, 0.1, 0]),
                         T("Insulin", 20, AMBER).move_to([cx + 0.9, 0.9, 0]))
            dots = VGroup(*[Dot([cx + dx, 1.2 - 0.35 * (j % 2), 0], radius=0.14, color=CORAL) for j, dx in enumerate([-2.2, -1.5, 1.5, 2.2])])
            sl = VGroup(Dot(radius=0.1, color=CORAL), T("Sugar", 18, SUB, False)).arrange(RIGHT, buff=0.12).move_to([cx - 2.0, 1.65, 0])
            self.play(FadeIn(VGroup(c, title, cell, cl, lock, hole, key, dots, sl), scale=0.9), run_time=0.6)
            if ok:
                self.okp = (key, dots, cx, lock)
            else:
                key.add_updater(lambda m, cx=cx: m.shift(UP * 0.0))
                self.badp = (key, dots)
        key, dots, cx, lock = self.okp
        self.at(STARTS[2] + 1.2)
        self.play(key.animate.shift(DOWN * 1.05), run_time=0.9)
        ring = Circle(radius=0.3, stroke_color=GRN, stroke_width=5).move_to([cx, -1.2, 0])
        self.add(ring)
        self.play(ring.animate.scale(3).set_stroke(opacity=0), *[d.animate.move_to([d.get_x(), -2.0, 0]) for d in dots], run_time=1.6, lag_ratio=0.15)
        self.remove(ring)
        bkey, bdots = self.badp
        for k, d in enumerate(bdots):
            d.add_updater(lambda m, k=k: m.shift(UP * 0.004 * np.sin(self.renderer.time * 3 + k)))
        bkey.add_updater(lambda m: m.shift(DOWN * 0.003 * np.sin(self.renderer.time * 4)))
        self.end(2)

    def s3(self):
        self.start(3, "Each one can add points to your score", "Sources: [8] Prediabetes Risk Test; [2] NICE PH38", "What raises your score?")
        lab = T("Your risk", 22, SUB).move_to([LEFT_X, 2.3, 0], aligned_edge=LEFT)
        track = Rectangle(width=10.7, height=0.28, fill_color=LINE, fill_opacity=1, stroke_width=0).move_to([0.45, 2.3, 0])
        f = ValueTracker(0.04)

        def fill_up(m):
            w = 10.7 * f.get_value()
            m.become(Rectangle(width=w, height=0.28, fill_color=interpolate_color(ManimColor(GRN), ManimColor(CORAL), f.get_value()),
                               fill_opacity=1, stroke_width=0).move_to([-4.9 + w / 2, 2.3, 0]))
        fill = Rectangle(width=0.4, height=0.28, fill_opacity=1, stroke_width=0)
        fill.add_updater(fill_up)
        self.add(track, fill)
        self.play(FadeIn(lab), run_time=0.4)
        labels = ["Age 40\nor older", "Extra body\nweight", "Family history\nof diabetes", "Little\nexercise", "High blood\npressure", "Diabetes during\npregnancy"]
        cols = [CORAL, AMBER, GRN, CORAL, AMBER, GRN]
        tiles, checks = [], []
        for k, s_ in enumerate(labels):
            x = [-4.4, 0, 4.4][k % 3]
            y = [0.5, -1.75][k // 3]
            tiles.append(VGroup(card(4.1, 2.0, x, y), plus(x - 1.55, y, cols[k]), TL(s_, 23).move_to([x - 1.1, y, 0], aligned_edge=LEFT)))
            checks.append(badge(x + 1.65, y, CORAL, 0.25))
        self.grp.add(*tiles, *checks)
        self.play(LaggedStart(*[FadeIn(t_, scale=0.85) for t_ in tiles], lag_ratio=0.15), run_time=1.4)
        for k in range(6):
            self.at(self.ab(3, RISK_TICKS[k]))
            self.play(GrowFromCenter(checks[k]), f.animate.set_value((k + 1) / 6), run_time=0.35)
        self.end(3)

    def s4(self):
        self.start(4, "Ask your doctor which test is right for you",
                   "Prediabetes range shown. Sources: [1] WHO/IDF 2006; [2] NICE PH38. Converted to mg/dL; ranges differ slightly between guidelines.",
                   "A blood test shows where you stand.")
        vial = VGroup(RoundedRectangle(corner_radius=0.4, width=1.0, height=3.0, fill_color=WHITE, fill_opacity=1, stroke_color=TEA, stroke_width=6),
                      RoundedRectangle(corner_radius=0.08, width=1.3, height=0.3, fill_color=TEA, fill_opacity=1, stroke_width=0).shift(UP * 1.5)).move_to([-5.2, -0.1, 0])
        liq = RoundedRectangle(corner_radius=0.3, width=0.78, height=1.5, fill_color=CORAL, fill_opacity=0.85, stroke_width=0).move_to([-5.2, -0.55, 0])
        clip = VGroup(RoundedRectangle(corner_radius=0.2, width=2.0, height=2.9, fill_color=WHITE, fill_opacity=1, stroke_color=LINE, stroke_width=5),
                      RoundedRectangle(corner_radius=0.1, width=0.8, height=0.3, fill_color=AMBER, fill_opacity=1, stroke_width=0).shift(UP * 1.45),
                      Rectangle(width=1.3, height=0.13, fill_color=LINE, fill_opacity=1, stroke_width=0).shift(UP * 0.7),
                      Rectangle(width=0.95, height=0.13, fill_color=LINE, fill_opacity=1, stroke_width=0).shift(UP * 0.4)).move_to([-3.2, -0.1, 0])
        chk = badge(-3.2, -0.55, GRN, 0.5)
        self.grp.add(vial, liq, clip, chk)
        self.play(FadeIn(vial), FadeIn(clip), run_time=0.5)
        self.play(GrowFromEdge(liq, DOWN), run_time=1.2)
        self.play(GrowFromCenter(chk), run_time=0.5)
        tests = [("Fasting blood sugar [2]", "100–125 mg/dL", "Diabetes: ≥ 126 mg/dL"),
                 ("A1C, 3-month average [2]", "6.0–6.4%", "Diabetes: ≥ 6.5%"),
                 ("2-hour sugar test [1]", "140–199 mg/dL", "Diabetes: ≥ 200 mg/dL")]
        for k, (n, r, d) in enumerate(tests):
            y = 1.5 - 1.7 * k
            c = card(7.4, 1.5, 2.5, y)
            txt = VGroup(T(n, 22, SUB), T(r, 36, AMBER), T(d, 20, CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([2.5, y, 0], aligned_edge=ORIGIN)
            txt.align_to(c, LEFT).shift(RIGHT * 0.4)
            self.at(self.ab(4, DIAG_CARDS[k]))
            self.grp.add(c, txt)
            self.play(FadeIn(VGroup(c, txt), shift=LEFT * 0.6), run_time=0.45)
        self.end(4)

    def s5(self):
        self.start(5, "Prediabetes is a warning, not a diagnosis", "Source: [4] Tabák et al., The Lancet 2012", "What happens next?")
        c = card(6.2, 5.3, -3.7, -0.05)
        dots = VGroup(*[Dot([-5.9 + 0.44 * (j % 10) + 0.0, 1.95 - 0.44 * (j // 10) - 0.1, 0], radius=0.17,
                            color=CORAL if j < 5 else AMBER if j < 10 else "#E7D9C6") for j in range(100)])
        dots.move_to([-3.7, -0.05, 0])
        self.grp.add(c, dots)
        self.play(FadeIn(c), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.012), run_time=2.4)
        for k, (big, col, small) in enumerate([("5 to 10 in 100", CORAL, "people with prediabetes develop\ntype 2 diabetes each year [4]"),
                                               ("Many go back to normal", GRN, "after healthy lifestyle changes [4]")]):
            y = 1.3 - 2.65 * k
            cc = card(6.6, 2.4, 3.55, y)
            tt = VGroup(T(big, 38, col), T(small, 22, SUB, False)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(cc)
            self.at(self.ab(5, PROG_CARDS[k]))
            self.grp.add(cc, tt)
            self.play(FadeIn(VGroup(cc, tt), shift=LEFT * 0.6), run_time=0.45)
        self.end(5)

    def s6(self):
        self.start(6, "Three habits that make a real difference",
                   "Sources: [6] Tuomilehto et al., NEJM 2001; [7] WHO physical activity guidelines 2020", "What actually helps?")

        def walk(x, y):
            p = [[0, -.2], [-.12, -1.0]]
            g = VGroup(Circle(radius=0.22, fill_color=GRN, fill_opacity=1, stroke_width=0).move_to([0, 0.75, 0]),
                       *[Line([a[0], a[1] + .55, 0], [b[0], b[1] + .55, 0]) for a, b in [([0, 0], [-.1, -.9]), ([0, 0], [-.4, -.3]), ([0, 0], [.4, -.15]),
                                                                                       ([-.1, -.9], [-.45, -1.45]), ([-.1, -.9], [.35, -1.3]), ([.35, -1.3], [.3, -1.55])]]).set_stroke(GRN, 9)
            g[0].set_stroke(width=0)
            return g.move_to([x, y, 0])

        def plate(x, y):
            return VGroup(Circle(radius=0.95, fill_color=WHITE, fill_opacity=1, stroke_color=AMBER, stroke_width=8),
                          Circle(radius=0.26, fill_color=CORAL, fill_opacity=1, stroke_width=0).shift(LEFT * 0.35 + UP * 0.2),
                          Circle(radius=0.3, fill_color=GRN, fill_opacity=1, stroke_width=0).shift(RIGHT * 0.35 + UP * 0.3),
                          Ellipse(width=0.8, height=0.45, fill_color=AMBER, fill_opacity=1, stroke_width=0).shift(DOWN * 0.35)).move_to([x, y, 0])

        def scale(x, y):
            return VGroup(RoundedRectangle(corner_radius=0.25, width=1.7, height=1.7, fill_color=WHITE, fill_opacity=1, stroke_color=TEA, stroke_width=8),
                          Arc(radius=0.45, start_angle=PI, angle=-PI, stroke_color=LINE, stroke_width=7).shift(UP * 0.25),
                          Line([0, .25, 0], [.25, .6, 0], color=CORAL, stroke_width=7),
                          Arrow([0, -.1, 0], [0, -.6, 0], buff=0, color=GRN, stroke_width=7, tip_length=0.2)).move_to([x, y, 0])
        items = [(walk, "150+ min a week", "Moderate activity, such as\nbrisk walking [7]", GRN),
                 (plate, "More fibre, less\nsaturated fat", "Whole grains, vegetables,\nfruit, beans [6]", AMBER),
                 (scale, "Lose ≥ 5% of\nbody weight", "If you carry extra weight [6]", TEA)]
        for k, (ic, head, sub, col) in enumerate(items):
            x = [-4.4, 0, 4.4][k]
            c = card(4.0, 5.2, x, -0.05)
            top = Rectangle(width=4.0, height=0.12, fill_color=col, fill_opacity=1, stroke_width=0).move_to([x, 2.49, 0])
            g = VGroup(c, top, ic(x, 0.95), TC(head, 28).move_to([x, -0.75, 0]), TC(sub, 19, SUB, False).move_to([x, -1.75, 0]))
            self.at(self.ab(6, LIFE_CARDS[k]))
            self.grp.add(g)
            self.play(FadeIn(g, scale=0.85), run_time=0.5)
        self.end(6)

    def s7(self):
        self.start(7, "Small changes can make a big difference", "Source: [6] Tuomilehto et al., New England Journal of Medicine 2001", "Does it work? Yes.")
        c = card(6.4, 5.2, -3.6, -0.05)
        big = T("58%", 86, GRN).move_to([-3.6, 1.5, 0])
        t1 = TC("lower risk of diabetes with\nlifestyle changes [6]", 24).move_to([-3.6, 0.2, 0])
        t2 = T("Finnish trial of adults with impaired glucose tolerance", 14, SUB, False).move_to([-3.6, -0.55, 0])
        l1 = T("Usual advice", 18, SUB, False).move_to([-6.2, -1.0, 0], aligned_edge=LEFT)
        b1 = Rectangle(width=5.2, height=0.3, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([-3.6, -1.4, 0])
        l2 = T("Lifestyle program", 18, SUB, False).move_to([-6.2, -1.85, 0], aligned_edge=LEFT)
        b2 = Rectangle(width=5.2 * 0.42, height=0.3, fill_color=GRN, fill_opacity=1, stroke_width=0).move_to([-6.2 + 5.2 * 0.21, -2.25, 0])
        b2.align_to(b1, LEFT)
        self.grp.add(c, big, t1, t2, l1, b1, l2, b2)
        self.play(FadeIn(VGroup(c, t1, t2, l1, l2)), GrowFromCenter(big), run_time=0.7)
        self.play(GrowFromEdge(b1, LEFT), run_time=0.6)
        self.play(GrowFromEdge(b2, LEFT), run_time=0.6)
        head = T("Your next steps", 32, TEA).move_to([0.5, 2.25, 0], aligned_edge=LEFT)
        self.show(head)
        for k, s_ in enumerate(["Check your risk score [8]", "Ask your doctor about\na blood test [2]", "Pick one small change\nthis week"]):
            y = 1.0 - 1.7 * k
            cc = card(6.3, 1.4, 3.65, y)
            g = VGroup(cc, num(1.2, y, k + 1, GRN, 0.3, 24), TL(s_, 22).move_to([1.75, y, 0], aligned_edge=LEFT))
            self.at(self.ab(7, NEXT_STEPS[k]))
            self.grp.add(g)
            self.play(FadeIn(g, shift=LEFT * 0.6), run_time=0.45)
        self.end(7)

    def s8(self):
        self.start(8, "For education only. Not medical advice.", "", "References")
        refs = ["WHO/IDF (2006). Definition and diagnosis of diabetes mellitus and intermediate hyperglycaemia. Geneva: WHO.",
                "NICE (2012, updated 2017). Type 2 diabetes: prevention in people at high risk. PH38.",
                "International Diabetes Federation (2021). IDF Diabetes Atlas, 10th edition.",
                "Tabák AG et al. (2012). Prediabetes: a high-risk state for diabetes development. Lancet 379:2279–2290.",
                "Petersen MC, Shulman GI (2018). Mechanisms of insulin action and insulin resistance. Physiol Rev 98:2133–2223.",
                "Tuomilehto J et al. (2001). Prevention of type 2 diabetes by changes in lifestyle. N Engl J Med 344:1343–1350.",
                "WHO (2020). Guidelines on physical activity and sedentary behaviour.",
                "Prediabetes Risk Test (American Diabetes Association / CDC): a score of 5 or higher means higher risk."]
        gs = []
        for k, r in enumerate(refs):
            x = -3.5 + 7.0 * (k // 4)
            y = 2.0 - 1.2 * (k % 4)
            gs.append(VGroup(card(6.7, 1.05, x, y), num(x - 2.95, y, k + 1, GRN, 0.22, 17),
                             T(textwrap.fill(r, 58), 15, INK, False).move_to([x - 2.5, y, 0], aligned_edge=LEFT)))
        self.grp.add(*gs)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in gs], lag_ratio=0.12), run_time=1.6)
        self.at(TOTAL - 0.05)

    def construct(self):
        self.persistent()
        for fn in [self.s0, self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8]:
            fn()
