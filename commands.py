import turtle

class Command:
    """ Base class for all commands """
    def __init__(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError



class GoToCommand(Command):
    """ Command that moves from turtle position to given position """
    def __init__(self, x,y, width=1, color='black'):
        self.x = x
        self.y = y
        self.width = width
        self.color = color

    def draw(self,turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x, self.y)

    def __str__(self):
        return "<Command x=" + str(self.x) + " y=" + str(self.y) + " width=" + str(self.width) + " color=" + self.color + ">GoTo</Command>"



class CircleCommand(Command):
    """ Command to draw a circle of given width and radius """
    def __init__(self, radius, width=1, color='black'):
        self.radius = radius
        self.width = width
        self.color = color

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.circle(self.radius)
    
    def __str__(self):
        return "<Command radius=" + str(self.radius) + " width=" + str(self.width) + " color=" + self.color + ">Circle</Command>"



class BeginFillCommand(Command):
    """ Command that start the beginfill from turtle position """
    def __init__(self, color):
        self.color = color

    def draw(self, turtle):
        turtle.fillcolor(self.color)
        turtle.begin_fill()

    def __str__(self):
        return "<Command color=" + self.color + ">BeginFill</Command>"



class EndFillCommand(Command):
    """ Command that fills the color from the beginfill position """
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.end_fill()

    def __str__(self):
        return "<Command>EndFill</Command>"


class PenUpCommand(Command):
    """ Penup command for elivating the turtle from the drawing """
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.penup()

    def __str__(self):
        return "<Command>PenUp</Command>"


class PenDownCommand:
    """ Pendown command to stuck the turtle with the drawings """
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.pendown()

    def __str__(self):
        return "<Command>PenDown</Command>"
