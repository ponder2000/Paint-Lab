import tkinter
import tkinter.filedialog
import tkinter.colorchooser

import turtle
import xml.dom.minidom

from commands import *


class DrawingApp(tkinter.Frame):
    """
    A class extended from tkinter.Frame which will add some feature to the Frame
    """

    def __init__(self, master = None):
        """Creating the frame """
        super().__init__(master=master)
        self.pack()
        self.buildWindow()
        self.graphicsCommands = list()

    
    def buildWindow(self):
        """Functions that places the widgets and handle all the work"""


        def newWindow():
            """A function that tells what to do when new window is selected from menubar """
            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto(0,0)
            theTurtle.pendown()
            screen.update()
            screen.listen()
            self.graphicsCommands = list()


        def parse(filename):
            """A function to read the xml file.
            All the drawings will be saved in xml format hence on opening them we need a function to read them"""

            xmldoc = xml.dom.minidom.parse(filename)
            graphicsCommandElement = xmldoc.getElementsByTagName("GraphicsCommands")[0]
            graphicsCommands = graphicsCommandElement.getElementsByTagName("Command")

            for commandElement in graphicsCommands:
                print(type(commandElement))
                command = commandElement.firstChild.data.strip()
                attr = commandElement.attributes

                if command == "GoTo":
                    x = float(attr['x'].value)
                    y = float(attr['y'].value)
                    wdth = float(attr['width'].value)
                    color = attr['color'].value.strip()
                    cmd = GoToCommand(x,y,wdth, color)
                
                elif command == "Circle":
                    radius = float(attr['radius'].value)
                    wdth = float(attr['width'].value)
                    color = attr['color'].value.strip()
                    cmd = CircleCommand(radius, wdth, color)

                elif command == "BeginFill":
                    color = attr['color'].value.strip()
                    cmd = BeginFillCommand(color)

                elif command == "EndFill":
                    cmd = EndFillCommand()

                elif command == "PenUp":
                    cmd = PenUpCommand()

                elif command == "PenDown":
                    cmd = PenDownCommand()

                else:
                    raise RuntimeError("Unknown Command: " + command)
                self.graphicsCommands.append(cmd)


        def loadFile():
            """ A function that will load files into our application"""

            filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")
            newWindow()

            self.graphicsCommands = list()
            parse(filename)

            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)
            screen.update()


        def addToFile():
            """ A function that will add file to the existing application kind of merging the two xml files"""

            filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")

            theTurtle.penup()
            theTurtle.goto(0,0)
            theTurtle.pendown()
            theTurtle.pencolor("#000000")
            theTurtle.fillcolor("#000000")

            cmd = PenUpCommand()
            self.graphicsCommands.append(cmd)

            cmd = GoToCommand(0,0,1,"#000000")
            self.graphicsCommands.append(cmd)

            cmd = PenDownCommand()
            self.graphicsCommands.append(cmd)

            screen.update()
            parse(filename)

            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)
                screen.update()


        def write(filename):
            """A function that will convert the paint into xml file"""

            file = open(filename, "w")
            file.write('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n''')
            file.write('<GraphicsCommands>\n')

            for cmd in self.graphicsCommands:
                file.write('    '+str(cmd)+'\n')
            
            file.write('</GraphicsCommands>\n')
            file.close()


        def saveFile():
            """ Saving a file """

            filename = tkinter.filedialog.asksaveasfilename(title="Save Pictures As...")
            write(filename)
        

        def circleHandler():
            """ Creating a circle using one click """

            cmd = CircleCommand(float(radiusSize.get()), float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

            screen.update()
            screen.listen()
      

        def getPenColor():
            """ Get the pen color from tkinter colorchooser"""

            color = tkinter.colorchooser.askcolor()
            if color != None:
                penColor.set(str(color)[-9:-2])
     

        def getFillColor():
            """ Get the fill color from tkinter colorchooser """

            color = tkinter.colorchooser.askcolor()
            if color != None:
                fillColor.set(str(color)[-9:-2])


        def beginFillHandler():
            """ Get the fill color from tkinter colorchooser """

            cmd = BeginFillCommand(fillColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)


        def endFillHandler():
            """ Closing the file """

            cmd = EndFillCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)


        def penUpHandler():
            """ A function to handle the penup acction """

            cmd = PenUpCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)


        def penDownHandler():
            """ A function to handle the pendown acction """

            cmd = PenDownCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)


        def clickHandler(x,y):
            """ A function to handle the click acction to draw """

            cmd = GoToCommand(x,y,float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()
        

        def dragHandler(x,y):
            """ A function to handle the drag acction for drawing """

            cmd = GoToCommand(x,y,float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()
        

        def undoHandler():
            """ press u to undo the recent contents """

            if len(self.graphicsCommands):
                self.graphicsCommands.removeLast()
                theTurtle.clear()
                theTurtle.penup()
                theTurtle.goto(0,0)

                for cmd in self.graphicsCommands:
                    cmd.draw(theTurtle)
                screen.update()
                screen.listen()



        # Craeting the appUI
        self.master.title("Ponder's Drawing Board")

        # adding a menubar
        bar = tkinter.Menu(self.master)
        file_menu = tkinter.Menu(bar, tearoff=0)

        file_menu.add_command(label="New", command=newWindow)
        file_menu.add_command(label="Load...", command=loadFile)
        file_menu.add_command(label="Load Into...", command = addToFile)
        file_menu.add_command(label="Save As...", command=saveFile)
        file_menu.add_command(label="Exit", command=self.master.quit)

        bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=bar)

        # craeting the canvas
        canvas = tkinter.Canvas(self, width=600, height=600)
        canvas.pack(side=tkinter.LEFT)

        # adding the turtle into the frame
        theTurtle = turtle.RawTurtle(canvas)
        theTurtle.shape("circle")
        screen = theTurtle.getscreen()
        screen.tracer(0)


        # Creating the sideBar
        sideBar = tkinter.Frame(self, padx=5, pady=5)
        sideBar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)


        # A textvar for the width of the drawing
        pointLabel = tkinter.Label(sideBar, text = "width")
        pointLabel.pack()

        widthSize = tkinter.StringVar()
        widthEntry = tkinter.Entry(sideBar, textvariable=widthSize)
        widthEntry.pack()
        widthSize.set(str(1))


        #  A textvar for radius of the circle
        radiusLabel = tkinter.Label(sideBar, text="Radius")
        radiusLabel.pack()
        radiusSize = tkinter.StringVar()
        radiusEntry = tkinter.Entry(sideBar, textvariable=radiusSize)
        radiusSize.set(str(20))
        radiusEntry.pack()

        circleButton = tkinter.Button(sideBar, text = "Draw Circle", command=circleHandler)
        circleButton.pack(fill=tkinter.BOTH)

        # Adding turtle color option
        screen.colormode(255)
        penLabel = tkinter.Label(sideBar, text="Pen Color")
        penLabel.pack()
        penColor = tkinter.StringVar()
        penEntry = tkinter.Entry(sideBar, textvariable=penColor)
        penEntry.pack()

        penColor.set("#000000")

        penColorButton = tkinter.Button(sideBar, text = "Pick Pen Color", command=getPenColor)
        penColorButton.pack(fill=tkinter.BOTH)


        # fillcolor label
        fillLabel = tkinter.Label(sideBar, text = "Fill Color")
        fillLabel.pack()

        fillColor = tkinter.StringVar()
        fillEntry = tkinter.Entry(sideBar, textvariable=fillColor)
        fillEntry.pack()
        fillColor.set("#000000")

        fillColorButton = tkinter.Button(sideBar, text = "Pick Fill Color", command=getFillColor)
        fillColorButton.pack(fill=tkinter.BOTH)

        beginFillButton = tkinter.Button(sideBar, text="Begin Fill", command=beginFillHandler)
        beginFillButton.pack(fill=tkinter.BOTH)

        endFillButton = tkinter.Button(sideBar, text="End Fill", command=endFillHandler)
        endFillButton.pack(fill=tkinter.BOTH)

        # penup and pendown
        penLabel = tkinter.Label(sideBar, text="Pen Is Down")
        penLabel.pack()

        penUpButton = tkinter.Button(sideBar, text="Pen Up", command=penUpHandler)
        penUpButton.pack(fill=tkinter.BOTH)

        penDownButton = tkinter.Button(sideBar, text="Pen Down", command=penDownHandler)
        penDownButton.pack(fill=tkinter.BOTH)


        theTurtle.onclick(clickHandler)
        theTurtle.ondrag(dragHandler)

        # undo feature
        screen.onkeypress(undoHandler, "u")
        screen.listen()



# the main function
def main():
    root = tkinter.Tk()
    drawingApp = DrawingApp(root)
    drawingApp.mainloop()
    print("execution completed")

if __name__ == "__main__":
    main()



        

