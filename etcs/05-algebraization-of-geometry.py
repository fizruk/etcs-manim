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

class Reverse(VMobject):
    def __init__(self, obj, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.obj = obj
        self.add(obj)

    def point_from_proportion(self, alpha):
        return self.obj.point_from_proportion(1 - alpha)

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
            arr = Arrow(dot_from, dot_to, tip_length = 0.1, stroke_width = 2, buff=0.1, **kwargs)
            self.arrows.append(arr)
            self.add(arr)

class FiniteNamedSetBag(VMobject):
    def __init__(self, names, set_name=None, set_boundary=False, set_draw_dots=True, set_element_lines=1, set_orientation=DOWN,
            element_label_at=None, **kwargs):
        VMobject.__init__(self, **kwargs)

        if element_label_at is None:
            if set_draw_dots:
                element_label_at = 0.7 * rotate_vector(set_orientation, np.pi/2)
            else:
                element_label_at = 0

        self.elements = names

        if set_name:
            self.set_name = TextMobject(str(set_name), **kwargs).move_to(n/2 * UP)
            self.add(self.set_name)

        n = len(names)
        line_k = 1 + (n - 1) // set_element_lines
        dx = set_orientation/2
        dy = rotate_vector(dx, np.pi/2)
        start = - ((line_k - 1) * dx / 2 + (set_element_lines - 1) * dy / 2)

        self.dots = [Dot(
            (start + (i % line_k + 0.5 * ((i // line_k) % 2)) * dx + (i // line_k) * dy)
            , **kwargs) for i in range(n)]
        self.labels = []

        for (dot, name) in zip(self.dots, names):
            label = TextMobject(str(name), **kwargs).scale(0.8).next_to(dot, element_label_at)
            self.labels.append(label)
            if set_draw_dots:
                self.add(dot)
            self.add(label)

        if not set_draw_dots:
            self.dots = self.labels

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

class Chapter5Wrapper(Scene):
    def construct(self):
        title = TextMobject("Chapter 4 chain rule intuition")
        title.to_edge(UP)
        rect = Rectangle(width = 16, height = 9)
        rect.set_height(1.5*FRAME_Y_RADIUS)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait(3)

class AlgebraisationOfGeometrySummary(Scene):
    def construct(self):
        Geometry_title = Title("Geometry", underline_width = FRAME_WIDTH/3 - 1).move_to(TOP+DOWN+LEFT*FRAME_WIDTH/3)
        Algebra_title = Title("Algebra", underline_width = FRAME_WIDTH/3 - 1).move_to(TOP+DOWN)
        Set_title = Title("Sets", underline_width = FRAME_WIDTH/3 - 1).move_to(TOP+DOWN+RIGHT*FRAME_WIDTH/3)

        A_dot = Dot(color=WHITE).next_to(Geometry_title, 5*DOWN)
        A_name = TexMobject("A", color=WHITE).next_to(A_dot, UP)
        A_named_dot = VGroup(A_dot, A_name).move_to(UP + LEFT*FRAME_WIDTH/3)
        A_coords = TexMobject("(2, 3)", color=WHITE).move_to(UP)
        A_set = TextMobject(r"\centering $X \times Y$\\","Cartesian product",r"\\of sets").move_to(UP + RIGHT*FRAME_WIDTH/3)
        A_set[1].set_color(YELLOW)

        parabola_function = lambda x: ((x/4)**3)
        grid = NumberPlane().scale(0.3)
        P_graph = grid.get_graph(parabola_function, color=WHITE, stroke_opacity=0.6).move_to(2*DOWN + LEFT*FRAME_WIDTH/3)

        P_eq = TexMobject("x^3 - 64 y = 0", color=WHITE).move_to(2*DOWN)
        P_set = TextMobject(r"\centering Equalizers\\","of mappings").move_to(2*DOWN + RIGHT*FRAME_WIDTH/3)
        P_set[0].set_color(YELLOW)

        self.play(Write(Geometry_title))
        self.play(Write(Algebra_title))
        self.play(Write(Set_title))
        self.wait()
        self.play(ShowCreation(A_dot), Write(A_name))
        self.play(Write(A_coords))
        self.play(Write(A_set))
        self.wait()
        self.play(ShowCreation(P_graph))
        self.play(Write(P_eq)) # Transform from a graph does not work :(
        self.play(Write(P_set))
        self.wait()

class ParabolaExample(Scene):
    def construct(self):
        c = 2 # parameter for parabola
        t = 2.5 # parameter for a point on a parabola
        t1 = -4
        t2 = 0
        t3 = 3

        grid = NumberPlane(y_max = 2*FRAME_Y_RADIUS).fade(0.6)

        OY = Line(10*UP, 10*DOWN, stroke_opacity=0.5, stroke_width=2)
        OX = Line(10*LEFT, 10*RIGHT, stroke_opacity=0.5, stroke_width=2)
        Y_name = TexMobject("Y").move_to(TOP + 0.3 * DL)
        X_name = TexMobject("X").move_to(RIGHT_SIDE + 0.3 * UL)
        O_dot = Dot(0)
        O_name = TexMobject("O").move_to(0.3 * DL)

        L_line = grid.get_graph(lambda x: -c, color=BLUE)
        L_name = TexMobject("D", color=BLUE).next_to(L_line, UP).shift(0.5*LEFT)
        directrix_name = TextMobject(r"\emph{directrix}", color=BLUE).next_to(L_name, RIGHT)
        L_eq   = TexMobject("y_D = -c", color=BLUE).next_to(L_line, DOWN).shift(0.5*LEFT)

        F_dot = Dot(c*UP, color=BLUE)
        F_name = TexMobject("F", "=(0, c)", color=BLUE).next_to(F_dot, UP).shift(0.5*RIGHT)
        focus_name = TextMobject(r"\emph{focus}", color=BLUE).next_to(F_name[0], RIGHT)

        E_dot = Dot(L_line.get_point_from_function(t))
        E_name = TexMobject("E").next_to(E_dot, DOWN)

        parabola_function = lambda x: (x**2)/(4*c)

        P_graph = grid.get_graph(parabola_function, color=YELLOW, stroke_opacity=0.6)
        P_graph_left = Reverse(grid.get_graph(parabola_function, color=YELLOW, stroke_opacity=0.6, x_min = t, x_max = t1))
        P_graph_right1 = grid.get_graph(parabola_function, color=YELLOW, stroke_opacity=0.6, x_min = t1, x_max = t2)
        P_graph_right2 = grid.get_graph(parabola_function, color=YELLOW, stroke_opacity=0.6, x_min = t2, x_max = t3)

        tangent = TangentLine(
                P_graph,
                inverse_interpolate(
                    grid.x_min,
                    grid.x_max,
                    t
                ),
                length=20,
                stroke_width=2,
                stroke_opacity=0.75,
            )
        vertical = Line(E_dot, E_dot.get_center() + 10*UP,
                stroke_width=2,
                stroke_opacity=0.75)
        EF = get_norm(E_dot.get_center() - F_dot.get_center())
        E_circle = Circle(radius=EF, stroke_width=1,stroke_opacity=0.5,color=WHITE).move_to(E_dot)
        F_circle = Circle(radius=EF, stroke_width=1,stroke_opacity=0.5,color=WHITE).move_to(F_dot)

        C_point = P_graph.get_point_from_function(t)
        C_dot = Dot(C_point, color=YELLOW)
        C_name = TexMobject("C", "=(x_C, y_C)").next_to(C_dot, RIGHT+0.5*DOWN)
        C_to_L = Line(C_dot, np.array([C_point[0],0,0])+c*DOWN)
        i_name = TexMobject("i", "= y_C + c").next_to(C_to_L)
        C_to_F = Line(C_dot.get_center(), F_dot.get_center())
        j_name = TexMobject("j", r"= \sqrt{x_C^2 + (y_C - c)^2}").next_to(C_to_F.get_center(), RIGHT+0.5*UP)

        C_circle = Circle(radius=C_point[1] + c, stroke_width=2, stroke_opacity=0.6).move_to(C_point)

        equation1 = TexMobject("i = j")
        equation2 = TexMobject("y_C + c"," = ",r"\sqrt{x_C^2 + (y_C - c)^2}")
        equation3 = TexMobject("(y_C + c)^2"," = ",r"x_C^2 + (y_C - c)^2")
        equation4 = TexMobject("y_C^2 + 2 y_C c + c^2"," = ",r"x_C^2 + y_C^2 - 2 y_C c + c^2")
        equation5 = TexMobject("2 y_C c"," = ",r"x_C^2 - 2 y_C c")
        equation6 = TexMobject("4 y_C c"," = ",r"x_C^2")
        equation7 = TexMobject("4 y_C c"," - ",r"x_C^2", "= 0")
        equation8 = TexMobject("y_C"," = ",r"\frac{1}{4 c} x_C^2")
        equations = VGroup(equation1, equation2, equation3, equation4, equation5, equation6, equation7, equation8)
        equations.set_color(YELLOW)
        equations.move_to(2*LEFT+UP)

        self.play(ShowCreation(L_line), Write(L_name))
        self.play(Write(directrix_name))
        self.wait()
        self.play(ShowCreation(F_dot), Write(F_name[0]))
        self.play(Write(focus_name))
        self.wait()
        self.play(FadeOut(focus_name), FadeOut(directrix_name))
        self.wait()
        self.play(ShowCreation(E_dot), Write(E_name))
        self.wait()
        self.play(ShowCreation(E_circle))
        self.play(ShowCreation(F_circle))
        self.play(ShowCreation(tangent))
        self.play(ShowCreation(vertical))
        self.play(ShowCreation(C_dot), Write(C_name[0]))
        self.wait()
        self.bring_to_front(F_dot)
        self.play(ShowCreation(C_to_L), Write(i_name[0]))
        self.play(ShowCreation(C_to_F), Write(j_name[0]))
        self.wait()
        self.play(Write(equation1))
        self.play(ShowCreation(C_circle))
        self.wait()

        dot_guide = Dot(C_dot.get_center(), color=YELLOW)
        group = VGroup(C_circle,C_to_L,C_to_F,C_dot,E_dot)
        def update_group(group):
            t = dot_guide.get_center()[0]
            C_circle,C_toL,C_to_F,C_dot,E_dot = group
            E_dot.move_to(L_line.get_point_from_function(t))
            E_name.next_to(E_dot, DOWN)

#            new_tangent = TangentLine(
#                    P_graph,
#                    inverse_interpolate(
#                        grid.x_min,
#                        grid.x_max,
#                        t
#                    ),
#                    length=20,
#                    stroke_width=2,
#                    stroke_opacity=0.75,
#                )
#            new_vertical = Line(E_dot, E_dot.get_center() + 10*UP,
#                    stroke_width=2,
#                    stroke_opacity=0.75)
#
            new_C_point = P_graph.get_point_from_function(t)
            new_C_dot = Dot(new_C_point, color=YELLOW)
            C_name.next_to(C_dot, RIGHT+0.5*DOWN)
            new_C_to_L = Line(new_C_dot, np.array([new_C_point[0],0,0])+c*DOWN)
            i_name.next_to(new_C_to_L)
            new_C_to_F = Line(new_C_dot.get_center(), F_dot.get_center())
            j_name.next_to(new_C_to_F.get_center(), RIGHT+0.5*UP)

            new_C_circle = Circle(radius=new_C_point[1] + c, stroke_width=2, stroke_opacity=0.8).move_to(new_C_point)

            C_dot.become(new_C_dot)
            C_to_L.become(new_C_to_L)
            C_to_F.become(new_C_to_F)
            C_circle.become(new_C_circle)
#            tangent.become(new_tangent)
#            vertical.become(new_vertical)
            self.bring_to_front(F_dot)

        group.add_updater(update_group)
        self.add(group)

        self.bring_to_front(F_dot)
        self.play(FadeOut(C_name[0]), FadeOut(E_name), FadeOut(i_name[0]), FadeOut(j_name[0]), FadeOut(equation1), FadeOut(tangent), FadeOut(vertical), FadeOut(E_circle), FadeOut(F_circle))
        self.play(MoveAlongPath(dot_guide,P_graph_left),run_time=2)
        self.wait(1)
        C_dot_trace = TracedPath(C_dot.get_center, color=YELLOW, stroke_width=2, stroke_opacity=0.6)
        self.add(C_dot_trace)
        self.play(MoveAlongPath(dot_guide,P_graph_right1),run_time=2)
        self.wait(1)
        self.play(MoveAlongPath(dot_guide,P_graph_right2),run_time=2)
        group.clear_updaters()
        self.play(FadeIn(C_name[0]), FadeIn(E_name), FadeIn(i_name[0]), FadeIn(j_name[0]), FadeIn(equation1))

        equation1.add_background_rectangle()
        self.bring_to_back(P_graph)
        self.play(Write(P_graph))
        self.wait()

        self.play(ShowCreation(OY))
        self.play(ShowCreation(O_dot), Write(O_name))
        self.play(ShowCreation(OX))
        self.play(Write(X_name), Write(Y_name))
        self.play(ShowCreation(grid))
        self.wait()

        for eq in equations:
            eq.add_background_rectangle()
        F_name[1].add_background_rectangle()
        C_name[1].add_background_rectangle()
        L_eq.add_background_rectangle()
        self.play(Write(F_name[1]))
        self.play(Write(L_eq))
        self.play(Write(C_name[1]))
        i_name[1].add_background_rectangle()
        self.play(Write(i_name[1]))
        j_name[1].add_background_rectangle()
        self.play(Write(j_name[1]))
        self.play(ReplacementTransform(equation1, equation2))
        self.play(ReplacementTransform(equation2, equation3))
        self.play(ReplacementTransform(equation3, equation4))
        self.play(ReplacementTransform(equation4, equation5))
        self.play(ReplacementTransform(equation5, equation6))
        self.play(ReplacementTransform(equation6, equation7))
        self.wait()
        self.play(ReplacementTransform(equation7, equation8))
        self.wait()

    def move_dot_path(self,parabola,anim_kwargs):
        h = 0; k = 1; p = 1
        parabola_copy = parabola.copy()
        focus = D0t(self.coords_to_point(0,2))
        dot_guide = D0t(self.coords_to_point(h,p))
        dot_d = D0t(self.coords_to_point(0,0))
        circle = Circle(radius=1).move_to(self.coords_to_point(h,p))
        line_f_d = DashedLine(focus.get_center(),dot_guide.get_center())
        line_d_d = DashedLine(dot_guide.get_center(),dot_d.get_center())


        group = VGroup(circle,line_f_d,line_d_d,dot_d)

        def update_group(group):
            c,f_d,d_d,d = group
            d.move_to(self.coords_to_point(dot_guide.get_center()[0],0))
            radius = get_norm(focus.get_center() - dot_guide.get_center())
            new_c = Circle(radius = radius)
            new_c.move_to(dot_guide)
            c.become(new_c)
            f_d.become(DashedLine(focus.get_center(),dot_guide.get_center()))
            d_d.become(DashedLine(dot_guide.get_center(),dot_d.get_center()))

        group.add_updater(update_group)

        self.play(
            FadeInFromLarge(circle,scale_factor=2),
            *[GrowFromCenter(mob) for mob in [line_f_d,line_d_d,dot_guide,dot_d,focus]],
            )
        self.add(
            group,
            focus,
            dot_guide,
            )
        self.wait()
        self.add(parabola)
        self.bring_to_back(parabola)
        self.bring_to_back(self.axes)
        self.play(
            MoveAlongPath(dot_guide,parabola_copy),
            ShowCreation(parabola),
            **anim_kwargs
            )
        group.clear_updaters()
        self.wait(1.2)
        self.play(FadeOut(VGroup(group,dot_guide,focus)))

class AxiomOfOrderedPairs(Scene):
    def construct(self):
        title = Title("Axiom of ordered pairs")

        axiom_text = TextMobject(
        r"For any sets ","$A$"," and ","$B$",
        r" there exists a set\\whose elements are ordered pairs ","$(a, b)$",
        r"\\of an element ","$a$ of $A$"," and an element ","$b$ of $B$",
        r".\\Moreover, \\if ","$a_1, a_2$"," are elements of ","$A$",
        r" and ","$b_1,b_2$"," are elements of ","$B$",
        r"\\then ","$(a_1,b_1) = (a_2,b_2)$"," if and only if ", "$a_1 = a_2$"," and ","$b_1 = b_2$","."
        )
        axiom_text[1].set_color(BLUE) # A
        axiom_text[3].set_color(BLUE) # B
        axiom_text[5].set_color(YELLOW) # (a, b)
        axiom_text[7].set_color(BLUE) # a of A
        axiom_text[9].set_color(BLUE) # b of B
        axiom_text[11].set_color(BLUE) # a_1, a_2
        axiom_text[13].set_color(BLUE) # A
        axiom_text[15].set_color(BLUE) # b_1, b_2
        axiom_text[17].set_color(BLUE) # B
        axiom_text[19].set_color(YELLOW) # (a_1,b_1) = (a_2,b_2)
        axiom_text[21].set_color(BLUE) # a_1 = a_2
        axiom_text[23].set_color(BLUE) # b_1 = b_2

        self.play(Write(title))
        for part in axiom_text:
            self.play(Write(part))

class CartesianProductOfSets(Scene):
    def construct(self):
        title = Title("Cartesian product of sets")

        self.play(Write(title))

        text = TextMobject(r"""
        For any sets $A$ and $B$, there exists a set $C$, whose
        elements are ordered pairs $(a, b)$
        """)

        suits = ["$\\clubsuit$", "$\\spadesuit$"]
        values = ["2", "3", "4"]

        setA = FiniteNamedSetBag(values, set_draw_dots=False, set_boundary=True, color=BLUE).move_to(4*LEFT+2*DOWN)
        A_name = TexMobject("A", color=BLUE).next_to(setA, 2*UP)

        setB = FiniteNamedSetBag(suits, set_draw_dots=False, set_boundary=True, color=BLUE).move_to(4*RIGHT+2*DOWN)
        B_name = TexMobject("B", color=BLUE).next_to(setB, 2*UP)

        AxB = [x + y for y in setB.elements for x in setA.elements]

        setC = FiniteNamedSetBag(AxB, set_element_lines=len(setB.elements), set_orientation=1.5*DOWN, set_boundary=True, set_draw_dots=False, color=YELLOW).move_to(2*DOWN)
        C_name = TexMobject(r"A \times B", color=YELLOW).next_to(setC, 2*UP)

        AxB_to_A = FiniteMapping(setC, setA, lambda s: s[:1], stroke_opacity=0.8)
        AxB_to_B = FiniteMapping(setC, setB, lambda s: s[1:], stroke_opacity=0.8)

        pi1_name = TexMobject("\pi_1", color=YELLOW).next_to(AxB_to_A, DOWN).shift(0.5*LEFT)
        pi2_name = TexMobject("\pi_2", color=YELLOW).next_to(AxB_to_B, DOWN).shift(0.5*RIGHT)

        self.play(ShowCreation(setA), Write(A_name))
        self.play(ShowCreation(setB), Write(B_name))
        self.wait()
        self.play(ShowCreation(setC), Write(C_name))
        self.wait()

        self.play(ShowCreation(AxB_to_A.arrows[0]))
        self.play(ShowCreation(AxB_to_B.arrows[0]))
        self.wait()

        self.play(*[ShowCreation(arr) for arr in AxB_to_A[1:]], Write(pi1_name))
        self.play(*[ShowCreation(arr) for arr in AxB_to_B[1:]], Write(pi2_name))
        self.wait()

        objA = Dot(setA.get_center(), color=setA.get_color())
        objB = Dot(setB.get_center(), color=setB.get_color())
        objC = Dot(setC.get_center(), color=setC.get_color())
        pi1_arrow = Arrow(objC, objA, tip_length = 0.15, stroke_width = 2, color=YELLOW)
        pi2_arrow = Arrow(objC, objB, tip_length = 0.15, stroke_width = 2, color=YELLOW)

        self.play(
                ReplacementTransform(setA, objA),
                ReplacementTransform(setB, objB),
                ReplacementTransform(setC, objC),
                ReplacementTransform(AxB_to_A, pi1_arrow),
                ReplacementTransform(AxB_to_B, pi2_arrow),

                ApplyMethod(A_name.next_to, objA, LEFT),
                ApplyMethod(B_name.next_to, objB, RIGHT),
                ApplyMethod(C_name.next_to, objC, UP),
                ApplyMethod(pi1_name.next_to, pi1_arrow, DOWN),
                ApplyMethod(pi2_name.next_to, pi2_arrow, DOWN)
                )

        objD = Dot(setC.get_center() + 3 * UP)
        D_name = TexMobject("D").next_to(objD, UP)
        f_arrow = Arrow(objD, objA, tip_length = 0.15, stroke_width = 2)
        g_arrow = Arrow(objD, objB, tip_length = 0.15, stroke_width = 2)
        f_name = TexMobject("f").move_to(f_arrow).shift(0.3*(LEFT+UP))
        g_name = TexMobject("g").move_to(g_arrow).shift(0.3*(RIGHT+UP))

        self.play(ShowCreation(objD), Write(D_name))
        self.play(ShowCreation(f_arrow), Write(f_name))
        self.play(ShowCreation(g_arrow), Write(g_name))

        h_arrow = DashedLine(objD, objC, tip_length = 0.15, stroke_width = 2, color=RED, buff=0.2).add_tip()
        h_name = TexMobject("h", color=RED).next_to(h_arrow, RIGHT)
        self.play(ShowCreation(h_arrow), Write(h_name), ApplyMethod(C_name.next_to, objC, RIGHT+UP))

        pi1_eq = TexMobject(r"\pi_1 \circ h = f", color=RED).next_to(pi1_name, 2*DOWN)
        pi2_eq = TexMobject(r"\pi_2 \circ h = g", color=RED).next_to(pi2_name, 2*DOWN)

        self.play(Write(pi1_eq))
        self.play(Write(pi2_eq))

        group = VGroup(
                objA,objB,objC,objD,
                A_name,B_name,C_name,D_name,
                f_arrow,g_arrow,h_arrow,pi1_arrow,pi2_arrow,
                f_name,g_name,h_name,pi1_name,pi2_name,
                pi1_eq,pi2_eq
                )
        self.play(ApplyMethod(group.scale, 0.6))
        self.play(ApplyMethod(group.move_to, UP + 4*RIGHT))

        h_def = TexMobject(r"""
        \end{align*}
        \centering
        \begin{alignat*}{2}
        h :\, & D & \,\to\, & A \times B \\
            & d & \,\mapsto\, & (f(d), g(d))
        \end{alignat*}
        \begin{align*}
        """).move_to(2.5*LEFT + UP)
        self.play(Write(h_def))

#        pi1_after_h = TexMobject("f","\stackrel{?}{=}","\pi_1 \circ h", color=RED)
#        pi1_after_h.next_to(h_def, 2*DOWN)
#        self.play(Write(pi1_after_h))

        pi1_after_h_check = TexMobject(
                r"(\pi_1 \circ h)(d) =",
                r"\pi_1(h(d)) = ",
                r"\pi_1((f(d), g(d))) = ",
                "f(d)")
        pi1_after_h_check.move_to(2*DOWN)
        for part in pi1_after_h_check:
            self.play(Write(part))
        self.wait()


        pi1_unique_question = TextMobject("Is $h$ unique?", color=RED).next_to(pi1_after_h_check, DOWN)
        self.play(Write(pi1_unique_question))
        self.wait()
        self.play(
                FadeOut(pi1_unique_question),
                FadeOut(pi1_after_h_check),
                FadeOut(group),
                FadeOut(h_def)
                )

        pi1_unique_check = TextMobject(
                r"Let ",r"$k$",r" be a mapping from ",r"$D$",r" to ",r"$A \times B$",
                r"\\such that ",r"$\pi_1 \circ k = f$",r" and ",r"$\pi_2 \circ k = g$",
                r"\\then for all elements ",r"$d$ of $D$",r" we have\\\quad\\",
                r"$\pi_1(k(d)) = $",r" $(\pi_1 \circ k)(d)$ ",r"$ = f(d)$",r"\\"
                r"$\pi_2(k(d)) = $",r" $(\pi_2 \circ k)(d)$ ",r"$ = g(d)$",r"\\\quad\\"
                r"$k(d) =$ ",r"$(\pi_1(k(d)), \pi_2(k(d))) =$ ",r"$(f(d), g(d)) =$ ",r"$h(d)$",r"\\"
                r"$k = h$"
                ).move_to(0.5*DOWN)
        pi1_unique_check[1].set_color(GREEN)    # k
        pi1_unique_check[3].set_color(WHITE)    # D
        pi1_unique_check[5].set_color(YELLOW)   # AxB
        pi1_unique_check[7].set_color(GREEN)    # pi_1 o k = f
        pi1_unique_check[9].set_color(GREEN)    # pi_2 o k = g
        for part in pi1_unique_check:
            self.play(Write(part))
