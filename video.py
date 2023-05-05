from time import sleep
from manim import *
from collections import deque

from event_selector import EventSelector2, Event
from pprint import pprint

class Scenario(Scene):
    def construct(self):
        self.setup()
        self.scene4()

    def setup(self):
        self.data_source = EventSelector2("media\\audio\\out2.txt")
        self.events_to_process = []
        self.actual_frame_number = -1
        self.actual_frame_time = 0.0
        self.actual_frame_time_end = 0.0

    def u(self, dt):
        self.actual_frame_number += 1
        self.actual_frame_time = dt * self.actual_frame_number
        self.actual_frame_time_end = self.actual_frame_time + dt
        result = self.data_source.select_events_in_time_frame(dt)
        print(f"FRAME_{self.actual_frame_time}:{self.actual_frame_time_end}")
        # pprint(result)
        # print("EVENTS: ", end='')
        if result == None:
            # print("EOF")
            self.events_to_process = None
            return
        if len(result) > 0:
            # print(f"NEW {self.get_run_time}")
            # pprint(result)
            self.events_to_process.append(result)
        else:
            # print("NO")
            pass

    def scene2(self):
        t = Text("_").to_edge(LEFT)
        self.add(t)
        self.add_updater(self.u)
        self.add_sound("media\\audio\\out2.wav")
        def events_waiting_to_process():
            return self.events_to_process or self.events_to_process == None
        while True:
            self.wait_until(events_waiting_to_process, )
            if self.events_to_process == None:
                return
            new_groups = ""
            for event in self.events_to_process:
                pprint(event)
                for p in event:
                    new_groups += p[2]
                    print(f"FRAME_{self.actual_frame_time}:{self.actual_frame_time_end} : EVENT TIME {p[0]}")
            new_t = Text(new_groups).next_to(t, RIGHT)
            self.add(new_t)
            t = new_t

            # pprint(["PROCESSING", self.events_to_process])
            self.events_to_process = []

    def u3(self, dt):

        if dt==0.0:
            print("ZERO")
            return
        self.actual_frame_number += 1
        self.actual_frame_time = self.actual_frame_time_end
        self.actual_frame_time_end += dt
        result = self.data_source.select(self.actual_frame_time, self.actual_frame_time_end, ["EXIT GROUP"])
        print(f"FRAME_{self.actual_frame_number}_{self.actual_frame_time}:{self.actual_frame_time_end}")
        # pprint(result)
        # print("EVENTS: ", end='')
        if result == None:
            # print("EOF")
            self.events_to_process = None
            return
        if len(result) > 0:
            # print(f"NEW {self.get_run_time}")
            # pprint(result)
            self.events_to_process.append(result)
        else:
            # print("NO")
            pass

    def scene3(self):
        t = Text("_").to_edge(LEFT)
        self.add(t)
        self.add_updater(self.u3)
        self.add_sound("media\\audio\\out2.wav")
        def events_waiting_to_process():
            return self.events_to_process or self.events_to_process == None
        while True:
            # if not events_waiting_to_process():
            #     self.wait(0.1, frozen_frame=False)
            #     continue
            self.wait_until(events_waiting_to_process)
            if self.events_to_process == None:
                return
            new_groups = ""
            for events in self.events_to_process:
                for event in events:
                    new_groups += event.data
                    print(f"FRAME_{self.actual_frame_number}_{self.actual_frame_time}:{self.actual_frame_time_end} : EVENT TIME {event.time}")
            new_t = Text(new_groups).next_to(t, RIGHT)
            self.add(new_t)
            t = new_t

            # pprint(["PROCESSING", self.events_to_process])
            self.events_to_process = []

    def u4(self, dt):
        if dt==0.0:
            # print("ZERO")
            return
        self.actual_frame_number += 1
        self.actual_frame_time = self.actual_frame_time_end
        self.actual_frame_time_end += dt
        result = self.data_source.select_data(self.actual_frame_time, self.actual_frame_time_end, ["EXIT GROUP"])
        # print(f"FRAME_{self.actual_frame_number}_{self.actual_frame_time}:{self.actual_frame_time_end}")
        # pprint(result)
        # print("EVENTS: ", end='')
        if result == None:
            # print("EOF")
            return
        if len(result) > 0:
            # print(f"NEW {self.get_run_time}")
            # pprint(result)
            if self.last_mobject2:
                t = self.last_mobject2.fade(1)
                self.remove(self.last_mobject2)
                self.add(t)
                self.remove(t)
                t = self.last_mobject.fade(0.5).move_to(UP)
                self.add(t)
                self.last_mobject2 = t


            if self.last_mobject:
                t = self.last_mobject.fade(1)
                self.remove(self.last_mobject)
                self.add(t)
                if self.last_mobject2:
                    # 
                    t = self.last_mobject2.fade(1)
                    self.remove(self.last_mobject2)
                    self.add(t)
                    # 
                self.last_mobject2 = Text(self.last_mobject.text).shift(UP).fade(0.5)
                self.add(self.last_mobject2)
                

            # self.update_mobjects(0)
            t = Text(result)
            self.add(t)
            self.last_mobject = t
            self.events_to_process.append(result)
        else:
            # print("NO")
            pass

    def scene4(self):
        self.add_sound("media\\audio\\out2.wav")        
        self.last_mobject = None
        self.last_mobject2 = None
        self.add_updater(self.u4)


        # self.play(FadeIn(t))
        # self.wait(1)
        # self.update_self(0)
        # self.wait(2)
        # self.update_self(0)
        # self.play(Transform(Circle(1, RED).to_edge(LEFT), Triangle().to_edge(LEFT), run_time=5))
        # self.clear()    
        self.wait(15)

    def refresh(self):
        print(".")
        return False

class MoveVerticallyText(Scene):

    def construct(self):
        script = deque()

        t = Text("Morse receiving training (25WPM)", font='Serif').to_edge(DOWN).shift(UP)
        self.play(Create(t))
        
        script.append(t.animate.to_edge(UP))

        self.play(*script)

        t = Text("2", font='Serif').to_edge(DOWN)
        self.play(Create(t))
        for idx, element in enumerate(script):
            script[idx].set_opacity(0.3)
            script[idx].shift(UP)
        script.append(t.animate.shift(UP))
        self.play(*script)

        self.test_time = 0

        def update(mobj: Mobject, dt):
            self.test_time += dt
            if self.test_time > 1 and self.test_time < 1.2:
                t = Text("+++", font='Serif').to_edge(DOWN)
                self.animate_papirus(t, script)
                print(self.test_time)
                self.test_time = 3
                mobj.updating_suspended()

            # mobj.rotate(dt * PI)
            return

        t = Text("ABC \nDEF DEF GHJ").scale(2)    
        t.add_updater(update) 
        self.add(t)
        self.wait(3)

    def animate_papirus(self, new_text, container, new_text_time=4, roll_time=2):
        # self.play(Create(new_text).set_run_time(new_text_time))
        self.add(new_text)
        for idx, element in enumerate(container):
            container[idx].set_opacity(0.3)
            container[idx].shift(UP).set_run_time(roll_time)
        container.append(new_text.animate.shift(UP).set_run_time(5))
        self.play(*container)
        self.wait()

        # t = Text("Darek", font='Serif')
        # ct = Create(t)
        # self.play(Create(t).set_run_time(4))
        # self.play(t.animate.shift(UP).set_run_time(0.5), )
        # # self.wait(1)
        # t2 = Text("Chilimoniuk", font='Serif')
        # ct = Create(t2)
        # self.play(Create(t2).set_run_time(1))
        # self.play(t.animate.shift(UP).set_run_time(1), t2.animate.shift(UP).set_run_time(1))
        # self.wait(2)
        # self.play(t.animate.shift(UP).set_run_time(1), t2.animate.shift(UP).set_run_time(1))

class CreateCircle(Scene):
    def construct(self):
        t = Text("555")  # create a circle
        t.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(t))  # show the circle on screen

class ContinuousMotion(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(func, stroke_width=2, max_anchors_per_line=30)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        text = Text("CQ CQ CQ DE SP5DD SP5DD SP5DD K")
        square.rotate(PI / 2)  # rotate a certain amount

        self.add_sound(sound_file="media\\audio\\out.wav", gain=1)
        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation
        # self.play(FadeIn(text))
        self.play(Transform(Text("asdjgjhgsd"), Text("7657576576253742")))  # interpolate the square into the circle

class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            Swap(
            left_square, right_square, angle=PI, run_time=2)
        )
        self.wait()


class MarkupElaborateExample(Scene):
    def construct(self):
        text = MarkupText(
            '<span foreground="purple">abc</span><span foreground="red">َ</span>'
            'ل<span foreground="blue">bcn</span>ع<span foreground="red">َ</span>ر'
            '<span foreground="red">mnk</span>ب<span foreground="red">ِ</span>ي'
            '<span foreground="green">uty</span><span foreground="red">َ</span>ة'
            '<span foreground="blue">637</span>'
        )
        self.add(text)

class TableExamples(Scene):
    def construct(self):
        t0 = Table(
            [["First", "Second"],
            ["Third","Fourth"]],
            row_labels=[Text("R1"), Text("R2")],
            col_labels=[Text("C1"), Text("C2")],
            top_left_entry=Text("TOP"))
        t0.add_highlighted_cell((2,2), color=GREEN)
        x_vals = np.linspace(-2,2,5)
        y_vals = np.exp(x_vals)
        t1 = DecimalTable(
            [x_vals, y_vals],
            row_labels=[MathTex("x"), MathTex("f(x)")],
            include_outer_lines=True)
        t1.add(t1.get_cell((2,2), color=RED))
        t2 = MathTable(
            [["+", 0, 5, 10],
            [0, 0, 5, 10],
            [2, 2, 7, 12],
            [4, 4, 9, 14]],
            include_outer_lines=True)
        t2.get_horizontal_lines()[:3].set_color(BLUE)
        t2.get_vertical_lines()[:3].set_color(BLUE)
        t2.get_horizontal_lines()[:3].set_z_index(1)
        cross = VGroup(
            Line(UP + LEFT, DOWN + RIGHT),
            Line(UP + RIGHT, DOWN + LEFT))
        a = Circle().set_color(RED).scale(0.5)
        b = cross.set_color(BLUE).scale(0.5)
        t3 = MobjectTable(
            [[a.copy(),b.copy(),a.copy()],
            [b.copy(),a.copy(),a.copy()],
            [a.copy(),b.copy(),b.copy()]])
        t3.add(Line(
            t3.get_corner(DL), t3.get_corner(UR)
        ).set_color(RED))
        vals = np.arange(1,21).reshape(5,4)
        t4 = IntegerTable(
            vals,
            include_outer_lines=True
        )
        g1 = Group(t0, t1).scale(0.5).arrange(buff=1).to_edge(UP, buff=1)
        g2 = Group(t2, t3, t4).scale(0.5).arrange(buff=1).to_edge(DOWN, buff=1)
        self.add(g1, g2)