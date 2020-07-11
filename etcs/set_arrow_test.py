#!/usr/bin/env python

from manimlib.imports import *

# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.
# Use -r <number> to specify a resolution (for example, -r 1080
# for a 1920x1080 video)

class FiniteMapping(VMobject):
    def __init__(self, set_from, set_to, f, f_name=None, **kwargs):
        VMobject.__init__(self, **kwargs)
        if f_name:
            self.f_name = TextMobject(str(f_name), **kwargs).move_to(n/2 * UP)
            self.add(self.f_name)

        self.set_from = set_from
        self.set_to   = set_to

        self.arrows = []
        for i in range(len(set_from.elements)):
            x = set_from.elements[i]
            dot_from = set_from.dots[i]
            y = f(x)
            j = set_to.elements.index(y)
            dot_to = set_to.dots[j]
            arr = Arrow(dot_from, dot_to, tip_length = 0.15, stroke_width = 2, buff=0.1, **kwargs)
            self.arrows.append(arr)
            self.add(arr)

class FiniteNamedSetBag(VMobject):
    def __init__(self, names, set_name=None, set_boundary=False, set_orientation=DOWN,
            element_label_at=None, **kwargs):
        VMobject.__init__(self, **kwargs)

        if element_label_at is None:
            element_label_at = 0.7 * rotate_vector(set_orientation, np.pi/2)

        self.elements = names

        if set_name:
            self.set_name = TextMobject(str(set_name), **kwargs).move_to(n/2 * UP)
            self.add(self.set_name)

        n = len(names)
        self.dots = [Dot((i - (n-1)/2)/2 * set_orientation, **kwargs) for i in range(n)]

        for (dot, name) in zip(self.dots, names):
            label = TextMobject(str(name), **kwargs).scale(0.8).next_to(dot, element_label_at)
            self.add(dot)
            self.add(label)

        if set_boundary:
            self.bag = Circle(**kwargs)
            self.bag.surround(self)
            self.add(self.bag)

class FiniteSetBag(VMobject):
    def __init__(self, n, boundary=False, **kwargs):
        self.elements = [Dot(((n-1)/2 - i)/2 * UP, **kwargs) for i in range(n)]
        if boundary:
            self.bag = Circle(**kwargs).scale(0.25 + n/2/2)
        VMobject.__init__(self, **kwargs)
        for element in self.elements:
            self.add(element)
        if boundary:
            self.add(self.bag)

class FourSetsExample(Scene):
    def construct(self):
        title = TextMobject("Sets and mappings").move_to(3*UP)
        self.play(Write(title))

        setA = FiniteNamedSetBag(range(3), color=BLUE, set_orientation=0.6*(RIGHT+UP), set_boundary=True)
        setA.move_to(1.5*LEFT + 1*UP)
        setB = FiniteNamedSetBag(range(2), color=RED, set_orientation=0.6*(RIGHT+DOWN), set_boundary=True)
        setB.move_to(1.5*RIGHT + 1*UP)
        setC = FiniteNamedSetBag(range(2), color=BLUE, set_orientation=0.6*(LEFT+UP), set_boundary=True)
        setC.move_to(1.5*LEFT + 1*DOWN)
        setD = FiniteNamedSetBag(range(2), color=RED, set_orientation=0.6*(LEFT+DOWN), set_boundary=True)
        setD.move_to(1.5*RIGHT + 1*DOWN)

        AB_arrows = FiniteMapping(setA, setB, lambda x: x % 2, color=YELLOW)
        AC_arrows = FiniteMapping(setA, setC, lambda x: 1 - x % 2, color=BLUE)
        BD_arrows = FiniteMapping(setB, setD, lambda x: x, color=RED)
        CD_arrows = FiniteMapping(setC, setD, lambda x: 1 - x, color=YELLOW)


        f0_name = TexMobject(r"f_0", color=YELLOW).next_to(AB_arrows, UP)
        f1_name = TexMobject(r"f_1", color=YELLOW).next_to(CD_arrows, UP)
        X_name = TexMobject(r"X", color=BLUE).next_to(VGroup(AC_arrows, setA, setC), LEFT)
        Y_name = TexMobject(r"Y", color=RED).next_to(VGroup(BD_arrows, setB, setD), RIGHT)

        setA_name = TexMobject(r"\mathrm{dom}(X)", color=BLUE).next_to(setA, LEFT + UP)
        setB_name = TexMobject(r"\mathrm{dom}(Y)", color=RED).next_to(setB, RIGHT + UP)
        setC_name = TexMobject(r"\mathrm{cod}(X)", color=BLUE).next_to(setC, LEFT + DOWN)
        setD_name = TexMobject(r"\mathrm{cod}(Y)", color=RED).next_to(setD, RIGHT + DOWN)

        equation = TexMobject(r"f_1","(","X","(z))","=","Y","(","f_0","(z))",r"\\ \text{for all } z \in \mathrm{dom}(X)")
        equation[0:9].set_color(YELLOW)
        equation.move_to(3*DOWN)

        self.play(Write(setA), Write(setC))
        self.play(Write(AC_arrows))
        self.play(Write(X_name))
        self.play(Write(setA_name))
        self.play(Write(setC_name))

        self.play(Write(setB), Write(setD))
        self.play(Write(BD_arrows))
        self.play(Write(Y_name))
        self.play(Write(setB_name))
        self.play(Write(setD_name))

        self.play(*[Write(arrows) for arrows in [AB_arrows, CD_arrows]])
        self.play(*[Write(name) for name in [f0_name, f1_name]])
        self.play(Write(equation))

        z_dot = setA.dots[1]
        Xz_dot = setC.dots[0]
        fXz_dot = setD.dots[1]
        fz_dot = setB.dots[1]

        z_name   = TexMobject("z_1").next_to(z_dot, LEFT+UP)
        Xz_name  = TexMobject("X(z_1)").next_to(Xz_dot, LEFT+DOWN)
        fXz_name = TexMobject("f_1(X(z_1))"," = Y(f_0(z_1))").next_to(fXz_dot, DOWN+RIGHT)
        fz_name  = TexMobject("f_0(z_1)").next_to(fz_dot, RIGHT+UP)
        temp_names = VGroup(z_name, Xz_name, fXz_name, fz_name)

        parts = [ VGroup(z_dot, z_name)
                , VGroup(Xz_dot, Xz_name, AC_arrows.arrows[1])
                , VGroup(fXz_dot, fXz_name[0], CD_arrows.arrows[0])
                , VGroup(fz_dot, fz_name, AB_arrows.arrows[1])
                , VGroup(fXz_name[1], BD_arrows.arrows[1])
                ]

        everything = self.get_top_level_mobjects()
        self.play(
                *[ApplyMethod(mob.fade, 0.8) for mob in everything],
                ApplyMethod(equation[0:9].fade, 1 - 1 / (1 - 0.8))
                )
        temp_names.fade(0.8)
        for part in parts:
            self.play(ApplyMethod(part.fade, 1 - 1 / (1 - 0.8)))
        self.wait()
        self.play(
                *[ApplyMethod(mob.fade, 1 - 1 / (1 - 0.8)) for mob in everything],
                FadeOut(temp_names)
                )
        self.wait()

        title2 = TexMobject(r"\mathbf{Set}").move_to(3*UP)

        objA = Dot(1.5*LEFT + 1*UP, color=BLUE)
        objB = Dot(1.5*RIGHT + 1*UP, color=RED)
        objC = Dot(1.5*LEFT + 1*DOWN, color=BLUE)
        objD = Dot(1.5*RIGHT + 1*DOWN, color=RED)

        AB_arrow = Arrow(objA, objB, tip_length = 0.15, stroke_width = 2, color=YELLOW)
        AC_arrow = Arrow(objA, objC, tip_length = 0.15, stroke_width = 2, color=BLUE)
        BD_arrow = Arrow(objB, objD, tip_length = 0.15, stroke_width = 2, color=RED)
        CD_arrow = Arrow(objC, objD, tip_length = 0.15, stroke_width = 2, color=YELLOW)

        equation2 = TexMobject("f_1",r"\circ","X","=","Y",r"\circ","f_0", color=YELLOW)
        equation2.move_to(3*DOWN)

        self.play(
                ReplacementTransform(title, title2),
                ReplacementTransform(setA, objA),
                ReplacementTransform(setB, objB),
                ReplacementTransform(setC, objC),
                ReplacementTransform(setD, objD),

                ReplacementTransform(AB_arrows, AB_arrow),
                ReplacementTransform(AC_arrows, AC_arrow),
                ReplacementTransform(BD_arrows, BD_arrow),
                ReplacementTransform(CD_arrows, CD_arrow),

                ApplyMethod(setA_name.next_to, objA, LEFT),
                ApplyMethod(setB_name.next_to, objB, RIGHT),
                ApplyMethod(setC_name.next_to, objC, LEFT),
                ApplyMethod(setD_name.next_to, objD, RIGHT),

                ApplyMethod(f0_name.next_to, AB_arrow, UP),
                ApplyMethod(f1_name.next_to, CD_arrow, UP),
                ApplyMethod(X_name.next_to, AC_arrow, LEFT),
                ApplyMethod(Y_name.next_to, BD_arrow, RIGHT),

                ReplacementTransform(equation[0], equation2[0]),    # f_1
                ReplacementTransform(equation[1], equation2[1]),    # ( -> \circ
                ReplacementTransform(equation[2], equation2[2]),    # X
                ReplacementTransform(equation[4], equation2[3]),    # =
                ReplacementTransform(equation[5], equation2[4]),    # Y
                ReplacementTransform(equation[6], equation2[5]),    # ( -> \circ
                ReplacementTransform(equation[7], equation2[6]),    # f_0

                FadeOut(VGroup(equation[3], equation[8], equation[9]))
                )

        self.wait()
        title3 = TexMobject(r"\mathbf{Set^\to}").move_to(3*UP)

        objX = Dot(1.5 * LEFT,  color=BLUE)
        objY = Dot(1.5 * RIGHT, color=RED)
        XY_arrow = Arrow(objX, objY, tip_length = 0.15, stroke_width = 2, color=YELLOW)
        f_name = TexMobject(r"f", color=YELLOW).next_to(XY_arrow, UP)

        self.play(
                ReplacementTransform(title2, title3),
                ReplacementTransform(VGroup(objA, objC, AC_arrow), objX),
                ReplacementTransform(VGroup(objB, objD, BD_arrow), objY),
                ReplacementTransform(VGroup(AB_arrow, CD_arrow), XY_arrow),
                ReplacementTransform(VGroup(setA_name, setC_name), X_name),
                ReplacementTransform(VGroup(setB_name, setD_name), Y_name),
                ReplacementTransform(VGroup(f0_name, f1_name, equation2), f_name)
                )
        self.wait()

class SetArrowExample(Scene):
    CONFIG = { "tip_length": 0.5 }
    def construct(self):
        title = TextMobject("Here are some sets and mappings")

        setA = FiniteNamedSetBag(range(2), color=BLUE, element_label_at=LEFT)
        setA.move_to(2*LEFT)
        setB = FiniteNamedSetBag(range(3), color=RED, element_label_at=RIGHT)
        setB.move_to(2*RIGHT)
        self.play(Write(setA))
        self.play(Write(setB))

        f_arrows = FiniteMapping(setA, setB, lambda x: x + 1)
        self.play(Write(f_arrows))

        setA_name = TexMobject("A", color=BLUE).move_to(2*UP + 2*LEFT)
        setB_name = TexMobject("B", color=RED).move_to(2*UP + 2*RIGHT)
        self.play(Write(setA_name))
        self.play(Write(setB_name))

        f_name = TexMobject("f").move_to(1.2*UP)
        self.play(Write(f_name))

        f_tex = TexMobject("f",":","A",r"\to","B").move_to(1.2*DOWN)
        f_tex[2].set_color(BLUE) # A
        f_tex[4].set_color(RED)  # B

        self.play(
                ReplacementTransform(f_name.copy(), f_tex[0]),
                ReplacementTransform(setA_name.copy(), f_tex[2]),
                ReplacementTransform(setB_name.copy(), f_tex[4]),
                )
        self.play(Write(f_tex[1]), Write(f_tex[3]))

        objA = Dot(2*LEFT, color = BLUE)
        objB = Dot(2*RIGHT, color = RED)
        f_arrow = Arrow(objA, objB, tip_length = 0.15, stroke_width = 2)
        self.play(
                ReplacementTransform(setA, objA),
                ReplacementTransform(setB, objB),
                ReplacementTransform(f_arrows, f_arrow)
                )

#
#        a1 = Dot(np.array([0,2,0]), color = YELLOW)
#        b1 = Dot(np.array([0,-2,0]), color = RED)
#        VGroup(a1, b1).arrange(10 * DOWN)
#        a1b1 = CurvedArrow(a1.get_center(), b1.get_center())
#        a1b1.scale(0.9)
#        self.play(ShowCreation(a1), ShowCreation(b1))
#        a1b1.get_tip().length = 1;
#        self.play(Write(a1b1))
#
#        tikz="""
#        \\begin{tikzpicture}[pencildraw]
#          \\node[pencildraw,draw] {\\sc Shifting Graphs};
#        \\end{tikzpicture} 
#             """
#
#        diagram = TexMobject(r"""
#        \begin{tikzcd}[ampersand replacement = \&]
#            \bullet \ar[r, leftrightarrow, "\simeq"] \& \bullet
#        \end{tikzcd}
#        """)
#        diagram.set_fill(None, 0) \
#            .set_stroke(None, 2)
#        diagram[0].set_color(RED)
#
##        diagram[:].set_fill(None,0) \
##                .set_stroke(None,2) \
##                .set_color(RED)
#
#        self.play(Write(diagram))
        self.wait()

class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*map(FadeOutAndShiftDown, basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = TextMobject("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFromDown(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = TextMobject(
            "That was a non-linear function \\\\"
            "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=3,
        )
        self.wait()
        self.play(
            Transform(grid_title, grid_transform_title)
        )
        self.wait()


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
            square
        ))
        self.wait()


class WriteStuff(Scene):
    def construct(self):
        example_text = TextMobject(
            "This is a some text",
            tex_to_color_map={"text": YELLOW}
        )
        example_tex = TexMobject(
            "\\sum_{k=1}^\\infty {1 \\over k^2} = {\\pi^2 \\over 6}",
        )
        group = VGroup(example_text, example_tex)
        group.arrange(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()


class UpdatersExample(Scene):
    def construct(self):
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=True,
        )
        square = Square().to_edge(UP)

        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        self.add(square, decimal)
        self.play(
            square.to_edge, DOWN,
            rate_func=there_and_back,
            run_time=5,
        )
        self.wait()

# See old_projects folder for many, many more
