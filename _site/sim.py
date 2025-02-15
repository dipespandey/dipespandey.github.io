from manim import *

class DimensionalProgression(Scene):
    def construct(self):
        # Title
        title = Text("Understanding Dimensions", font_size=40)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))
        
        # 0D - Point
        point = Dot().shift(LEFT * 4)
        point_label = Text("0D: Point", font_size=24).next_to(point, DOWN)
        
        # 1D - Line
        line = Line(LEFT * 3, LEFT * 2)
        line_label = Text("1D: Line", font_size=24).next_to(line, DOWN)
        
        # 2D - Square
        square = Square(side_length=1).shift(RIGHT * 0)
        square_label = Text("2D: Square", font_size=24).next_to(square, DOWN)
        
        # 3D - Cube
        cube = Cube(side_length=1).shift(RIGHT * 3)
        cube.set_fill(BLUE, opacity=0.1)
        cube_label = Text("3D: Cube", font_size=24).next_to(cube, DOWN)
        
        # Show progression
        for obj, label in [(point, point_label), (line, line_label), 
                          (square, square_label), (cube, cube_label)]:
            self.play(Create(obj), Write(label))
            self.wait()
        
        self.wait(2)