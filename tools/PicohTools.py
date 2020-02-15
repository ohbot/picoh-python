import tkinter as Tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import OptionMenu
import os.path
import numpy as np
from lxml import etree
import os
from picoh import picoh
from copy import deepcopy
import platform
import threading
import csv
import os
import random
import sys
from threading import Timer


# Class to hold Eyeshape information. Same fields as Picoh.obe xml file.

class EyeShape(object):

    def __init__(self, name_value, hexString_value, autoMirror_value, pupilRangeX_value, pupilRangeY_value):
        self.name = name_value
        self.hexString = hexString_value
        self.autoMirror = autoMirror_value
        self.pupilRangeX = pupilRangeX_value
        self.pupilRangeY = pupilRangeY_value

class PicohEyeDesigner(Tk.Frame):
    # Class variables

    operatingSystem = platform.system()

    # %%%%
    picohConnected = picoh.connected

    # Setup variables.
    clickedDown = False
    pupilActive = True
    drawing = False
    startedMoving = False

    currentfilename = ""

    # Binary grids, one for each button.
    gridArray = np.zeros((9, 8))
    gridArrayOne = np.zeros((9, 8))
    gridArrayTwo = np.zeros((9, 8))
    gridArrayThree = np.zeros((9, 8))
    gridArrayFour = np.zeros((9, 8))
    gridArrayFive = np.zeros((9, 8))

    buttonArray = []
    buttonArrayOne = []
    buttonArrayTwo = []
    buttonArrayThree = []
    buttonArrayFour = []
    buttonArrayFive = []

    # List of EyeShape objects.
    shapeList = []

    # Coordinates for top left of window
    rootx = 20
    rooty = 40

    # Variables to hold colour and size preferences.
    bgCol = 'white'
    textCol = 'black'
    buttonCol = 'white'

    if operatingSystem == 'Windows':
        buttonCol = 'grey'

    # pupilButtonHighlightColour = '#408bf9'
    pupilButtonHighlightColour = 'SkyBlue1'

    buttonWidth = 10
    buttonHeight = 3

    if operatingSystem == "Linux":
        tickWidth = 11
    else:
        tickWidth = 15

    tree = None

    def __init__(self, parent,frameIn):
        #Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = frameIn
      #  Tk.Frame.__init__(self.frame, parent)
        #self.initialize()
        # Configure Window

        #self.parent.title("Picoh Eye Shape Designer")
        self.parent.grid_rowconfigure(1, weight=0)
        self.parent.grid_columnconfigure(1, weight=0)

        if self.operatingSystem == "Darwin":
            self.customFont = tkFont.Font(family="Letter Gothic Std", size=11)
        if self.operatingSystem == "Windows" or self.operatingSystem == "Linux":
            self.customFont = tkFont.Font(family="Helvetica", size=8)

        self.frame.configure(bg=self.bgCol)
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Variables to track tick boxes:
        self.pupilVar = Tk.BooleanVar()
        self.pupilVar.set(True)

        self.pupilTrack = Tk.BooleanVar()
        self.pupilTrack.set(False)

        self.mirrorVar = Tk.IntVar()
        self.mirrorVar.set(0)

        self.speak = Tk.IntVar()
        self.speak.set(0)

        self.rangeVar = Tk.IntVar()
        self.rangeVar.set(0)

        # Create popups for rename and new shape.

        self.entryPopTwo = Tk.Entry(self.frame, width=20, text="Test", font=self.customFont)
        self.entryPopTwo.bind('<Return>', self.rename)
        self.entryPop = Tk.Entry(self.frame, width=20, text="Test", font=self.customFont)
        self.entryPop.bind('<Return>', self.newShape)

        # Add pupil overlay and pupil track checkboxes

        checkbox = Tk.Checkbutton(self.frame, text="Overlay Pupil", variable=self.pupilVar, command=self.checkBoxAction)
        checkbox.grid(row=1, rowspan=1, column=18, columnspan=7, sticky="w")
        checkbox.configure(bg=self.bgCol, font=self.customFont)

        pupilTrackBox = Tk.Checkbutton(self.frame, text="Mouse-Pupil", variable=self.pupilTrack,
                                       command=self.pupilTrackAction)
        pupilTrackBox.grid(row=8, rowspan=1, column=27, columnspan=6, sticky="w")
        pupilTrackBox.configure(bg=self.bgCol, font=self.customFont, width=self.tickWidth)

        # Labels

        l1 = Tk.Label(self.frame, text="Eyeshape")
        l1.grid(row=0, column=0, columnspan=4, sticky="W", padx=(10, 0))
        l1.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        l2 = Tk.Label(self.frame, text="Pupil")
        l2.grid(row=0, column=9, columnspan=3, sticky="W")
        l2.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        l3 = Tk.Label(self.frame, text="Blink 1")
        l3.grid(row=10, column=0, columnspan=4, sticky="W", padx=(10, 0))
        l3.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        l4 = Tk.Label(self.frame, text="Blink 2")
        l4.grid(row=10, column=9, columnspan=3, sticky="W")
        l4.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        l5 = Tk.Label(self.frame, text="Blink 3")
        l5.grid(row=10, column=18, columnspan=3, sticky="W")
        l5.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        l6 = Tk.Label(self.frame, text="Blink 4")
        l6.grid(row=10, column=27, columnspan=3, sticky="W")
        l6.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        self.textLab = Tk.Label(self.frame, text='Are You Sure?', font=self.customFont)

        self.filenamelabel = Tk.Label(self.frame, text="")
        # self.filenamelabel.grid(row=13,column = 0,columnspan = 10,sticky = "W", padx = (10,0))

        #  Create 2D arrays with 0's to hold button states.
        for x in range(0, 6):
            for j in range(9):
                column = []
                for i in range(8):
                    column.append(0)
                self.getButtonArray(x).append(column)

        # New Button
        self.newButton = Tk.Button(self.frame, text="New", image="", command=self.newButton, width=self.buttonWidth)
        self.newButton.grid(row=4, column=27, columnspan=4, sticky="w")
        self.newButton.configure(highlightbackground=self.bgCol, font=self.customFont)

        # Rename Button
        self.renameButton = Tk.Button(self.frame, text="Rename", command=self.renameButton)
        self.renameButton.grid(row=4, column=31, columnspan=4, sticky="e")
        self.renameButton.configure(highlightbackground=self.bgCol, font=self.customFont, width=self.buttonWidth)

        # Duplicate Button
        self.dupButton = Tk.Button(self.frame, text="Duplicate", command=self.duplicate, width=self.buttonWidth)
        self.dupButton.grid(row=5, column=31, columnspan=4, sticky="e")
        self.dupButton.configure(highlightbackground=self.bgCol, font=self.customFont)

        # Delete button
        self.delButton = Tk.Button(self.frame, text="Delete", command=self.deleteShapeButton, width=self.buttonWidth)
        self.delButton.grid(row=5, column=27, columnspan=4, sticky="w")
        self.delButton.configure(highlightbackground=self.bgCol, font=self.customFont)

        # Test blink button
        self.blinkButton = Tk.Button(self.frame, text="Test Blink", command=self.testBlink, width=self.buttonWidth)
        self.blinkButton.grid(row=7, column=31, columnspan=4, sticky="e")
        self.blinkButton.configure(highlightbackground=self.bgCol, font=self.customFont, width=9)

        # Speak tick box, have picoh read out file names and changes.
        self.speakTickBox = Tk.Checkbutton(self.frame, text="Speak", variable=self.speak)
        # self.speakTickBox.grid(row=8, column=31, columnspan = 4, sticky="e")
        self.speakTickBox.config(bg=self.bgCol, highlightcolor=self.textCol, font=self.customFont, width=self.tickWidth)

        #  Reset buttons for each grid

        self.resetButton = Tk.Button(self.frame, text='Clear', command=lambda: self.reset(0))
        self.resetButton.grid(row=0, column=5, columnspan=3, sticky="E")
        self.resetButton.configure(highlightbackground=self.bgCol, fg=self.textCol, font=self.customFont)

        self.resetButtonOne = Tk.Button(self.frame, text="Clear", command=lambda: self.reset(1))
        self.resetButtonOne.grid(row=0, column=14, columnspan=3, sticky="E")
        self.resetButtonOne.configure(highlightbackground=self.bgCol, font=self.customFont)

        self.resetButtonTwo = Tk.Button(self.frame, text="Clear", command=lambda: self.reset(2))
        self.resetButtonTwo.grid(row=10, column=5, columnspan=3, sticky="E")
        self.resetButtonTwo.configure(highlightbackground=self.bgCol, font=self.customFont)

        self.resetButtonThree = Tk.Button(self.frame, text="Clear", command=lambda: self.reset(3))
        self.resetButtonThree.grid(row=10, column=14, columnspan=3, sticky="E")
        self.resetButtonThree.configure(highlightbackground=self.bgCol, font=self.customFont)

        self.resetButtonFour = Tk.Button(self.frame, text="Clear", command=lambda: self.reset(4))
        self.resetButtonFour.grid(row=10, column=23, columnspan=3, sticky="E")
        self.resetButtonFour.configure(highlightbackground=self.bgCol, font=self.customFont)

        self.resetButtonFive = Tk.Button(self.frame, text="Clear", command=lambda: self.reset(5))
        self.resetButtonFive.grid(row=10, column=32, columnspan=3, sticky="E")
        self.resetButtonFive.configure(highlightbackground=self.bgCol, font=self.customFont)

        # copy buttons
        copyDownButton = Tk.Button(self.frame, width=0, height=0, borderwidth=0,
                                   highlightthickness=-2, image=copyDown, padx=-2, pady=-2)

        copyDownButton.configure(highlightbackground=self.bgCol)

        copyRightOneButton = Tk.Button(self.frame, width=0, height=0, borderwidth=0,
                                       highlightthickness=-2, image=copyRight, padx=-2, pady=-2)

        copyRightOneButton.configure(highlightbackground=self.bgCol)

        copyRightTwoButton = Tk.Button(self.frame, width=0, height=0, borderwidth=0,
                                       highlightthickness=-2, image=copyRight, padx=-2, pady=-2)

        copyRightTwoButton.configure(highlightbackground=self.bgCol)

        copyRightThreeButton = Tk.Button(self.frame, width=0, height=0, borderwidth=0,
                                         highlightthickness=-2, image=copyRight, padx=-2, pady=-2)

        copyRightThreeButton.configure(highlightbackground=self.bgCol)

        # Buttons used during renaming or the creation of a new shape.
        self.but = Tk.Button(self.frame, text="Yes",
                             command=self.deleteShape, font=self.customFont, width=self.buttonWidth)

        self.butCancel = Tk.Button(self.frame, text="No",
                                   command=self.cancel, font=self.customFont, width=self.buttonWidth)

        self.okayOne = Tk.Button(self.frame, text="Okay", highlightbackground=self.bgCol,
                                 command=self.newShape, font=self.customFont, width=self.buttonWidth)

        self.cancelOne = Tk.Button(self.frame, text="Cancel", highlightbackground=self.bgCol,
                                   command=self.cancel, font=self.customFont, width=self.buttonWidth)

        self.okayTwo = Tk.Button(self.frame, text="Okay", highlightbackground=self.bgCol,
                                 command=self.rename, font=self.customFont, width=self.buttonWidth)

        self.cancelTwo = Tk.Button(self.frame, text="Cancel",
                                   command=self.cancel, highlightbackground=self.bgCol, font=self.customFont,
                                   width=self.buttonWidth)

        # Add copy buttons to grid.

        copyDownButton.grid(row=10, column=3)
        copyRightOneButton.grid(row=15, column=8)
        copyRightTwoButton.grid(row=15, column=17)
        copyRightThreeButton.grid(row=15, column=26)

        # Bind commands to copy buttons.
        copyDownButton.bind("<Button>", lambda event, grid=0: self.copyGrid(event, grid, grid + 2))
        copyDownButton.bind("<ButtonRelease-1>", self.OnMouseUp)
        copyRightOneButton.bind("<Button>", lambda event, grid=2: self.copyGrid(event, grid, grid + 1))
        copyRightOneButton.bind("<ButtonRelease-1>", self.OnMouseUp)
        copyRightTwoButton.bind("<Button>", lambda event, grid=3: self.copyGrid(event, grid, grid + 1))
        copyRightTwoButton.bind("<ButtonRelease-1>", self.OnMouseUp)
        copyRightThreeButton.bind("<Button>", lambda event, grid=4: self.copyGrid(event, grid, grid + 1))
        copyRightThreeButton.bind("<ButtonRelease-1>", self.OnMouseUp)

        # Picoh button, toggles sending data to Picoh. If not Picoh detected default to off.
        if self.picohConnected:
            chosenLogo = logoOn
            picoh.reset()
            picoh.close()
        else:
            chosenLogo = logo

        # Create Picoh logo button.
        self.picohButton = Tk.Button(self.frame, command=self.picohToggle, image=chosenLogo)
        self.picohButton.grid(row=0, column=27, columnspan=20, rowspan=3, sticky="s")
        if self.operatingSystem == "Windows":
            self.picohButton.grid(rowspan=3, sticky="n", row=0)
        self.picohButton.configure(highlightbackground=self.bgCol)

        # picohPanel = Tk.Label(self.frame, image=picohGraphic)
        #  picohPanel.grid(row=9, column=8, columnspan=16, rowspan=16, sticky="sw")

        #  Generate button grids: (xStart,yStart,grid)
        self.generateButtons(0, 1, 0)
        self.generateButtons(9, 1, 1)
        self.generateButtons(0, 11, 2)
        self.generateButtons(9, 11, 3)
        self.generateButtons(18, 11, 4)
        self.generateButtons(27, 11, 5)

        # Create a Tkinter variable

        self.tkvar = Tk.StringVar(self.frame)

        # Read in data from Picoh.obe xml file.
        self.xmlReadin()

        # Load the Shapelist with
        self.refreshShapeList()

        # Trace tkvar to enable shape chosen in drop down to be loaded
        self.tkvar.trace_id = self.tkvar.trace_variable("w", self.loadShape)

        self.saved = True

        # x and y range entry boxes

        self.xRangeVar = Tk.StringVar()
        self.xRangeVar.set('5')

        self.yRangeVar = Tk.StringVar()
        self.yRangeVar.set('5')

        self.xRangeEntry = Tk.Entry(self.frame, width=2, textvariable=self.xRangeVar)

        # self.xRangeEntry.grid(row=7, column=23, columnspan=5, sticky='w')
        self.xRangeEntry.config(bg='white', font=self.customFont)

        self.yRangeEntry = Tk.Entry(self.frame, width=2, textvariable=self.yRangeVar)

        # self.yRangeEntry.grid(row=8, column=23, columnspan=5, sticky='w')
        self.yRangeEntry.config(bg='white', font=self.customFont)

        self.xRangeLabel = Tk.Label(self.frame, text="Pupil Range X", height=1, font=self.customFont)

        # self.xRangeLabel.grid(row=7, column=18, columnspan=5, sticky='w')
        self.xRangeLabel.config(bg=self.bgCol, fg=self.textCol)

        self.yRangeLabel = Tk.Label(self.frame, text="Pupil Range Y")

        #  self.yRangeLabel.grid(row=8, column=18, columnspan=5, sticky='w')
        self.yRangeLabel.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        self.xRangeVar.trace_variable("w", self.updateRange)
        self.yRangeVar.trace_variable("w", self.updateRange)

        # Create check boxes

        self.mirrorCheckbox = Tk.Checkbutton(self.frame, text="Auto Mirror", variable=self.mirrorVar,
                                             command=self.mirrorChange)
        self.mirrorCheckbox.grid(row=7, rowspan=1, column=27, columnspan=6, sticky="w")
        self.mirrorCheckbox.config(bg=self.bgCol, highlightcolor=self.textCol, font=self.customFont,
                                   width=self.tickWidth)

        self.rangeCheckbox = Tk.Checkbutton(self.frame, text="Show Pupil Range", variable=self.rangeVar,
                                            command=self.displayRange)
        # self.rangeCheckbox.grid(row=5, rowspan=1, column=18, columnspan=7, sticky="w")
        self.rangeCheckbox.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        # Pack frame.
        #self.frame.pack(fill=Tk.X, padx=0, pady=0)

        root.bind('<Motion>', self.motion)

        # Load first shape in the list.
        self.shapeIndex = 0
        self.loadShape(True, shapeName=self.shapeList[self.shapeIndex].name, loading=True)
        # self.updatePicoh()

        self.checkBoxAction()
        checkbox.invoke()

        if self.operatingSystem == "Windows" or self.operatingSystem == "Linux":

            if self.operatingSystem == "Linux":
                winRowheight = 11

            if self.operatingSystem == "Windows":
                winRowheight = 13

            self.newButton.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.renameButton.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.dupButton.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.delButton.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)

            self.blinkButton.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)

            self.okayOne.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.okayTwo.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.cancelOne.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.cancelTwo.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)

            self.but.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.butCancel.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)

            self.resetButton.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 5)
            self.resetButtonOne.configure(compound="c", image=pixelImage, height=winRowheight,
                                          width=self.buttonWidth * 5)
            self.resetButtonTwo.configure(compound="c", image=pixelImage, height=winRowheight,
                                          width=self.buttonWidth * 5)
            self.resetButtonThree.configure(compound="c", image=pixelImage, height=winRowheight,
                                            width=self.buttonWidth * 5)
            self.resetButtonFour.configure(compound="c", image=pixelImage, height=winRowheight,
                                           width=self.buttonWidth * 5)
            self.resetButtonFive.configure(compound="c", image=pixelImage, height=winRowheight,
                                           width=self.buttonWidth * 5)
            if self.operatingSystem != "Linux":
                self.mirrorCheckbox.configure(compound="c", image=pixelImage, height=winRowheight,
                                              width=self.buttonWidth * 7)
                pupilTrackBox.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 7)
                checkbox.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 7)

            self.rangeCheckbox.configure(compound="c", image=pixelImage, height=winRowheight,
                                         width=self.buttonWidth * 7)

            if self.operatingSystem == "Linux":
                self.mirrorCheckbox.config(width=self.tickWidth)
                pupilTrackBox.config(width=self.tickWidth)
                checkbox.config(width=self.tickWidth)

            self.yRangeLabel.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 7)
            self.xRangeLabel.configure(compound="c", image=pixelImage, height=winRowheight, width=self.buttonWidth * 7)

            self.popupMenu.configure(compound="c", image=pixelImage, height=8, width=self.buttonWidth * 14)

            self.textLab.configure(compound="c", image=pixelImage, height=8, width=self.buttonWidth * 7)


        self.updatePicoh()


    # Function to generate buttons
    def generateButtons(self, buttonStartX, buttonStartY, grid):
        for i in range(0, self.getGridArray(grid).shape[0]):
            for j in range(0, self.getGridArray(grid).shape[1]):

                b = Tk.Button(self.frame, highlightbackground=self.buttonCol, height=0, borderwidth=0,
                              highlightthickness=2, padx=0, pady=0)
                if self.operatingSystem == "Windows":
                    b.config(bg=self.buttonCol)

                if j == 0 and grid == 0 or j == 0 and grid == 2:
                    b.grid(row=i + buttonStartY, column=j + buttonStartX, padx=(10, 0))

                else:
                    b.grid(row=i + buttonStartY, column=j + buttonStartX)

                b.config(image=offImage)

                # Bind events
                b.bind("<B1-Motion>", lambda event, grid=grid: self.OnMouseMove(event, grid))
                b.bind("<Leave>", self.OnMouseLeave)
                b.bind("<Button>", lambda event, grid=grid, x=i, y=j: self.OnMouseDown(event, x, y, grid))
                b.bind("<ButtonRelease-1>", self.OnMouseUp)

                # Add button to button array
                self.getButtonArray(grid)[i][j] = b

    # Copies grid to destination.
    def copyGrid(self, event, grid, destination):

        if grid == 0:

            for i in range(0, 9):
                for j in range(0, 8):
                    if self.getGridArray(grid)[i][j]:
                        self.turnButtonOn(i, j, destination, loading=False)
                    else:
                        self.turnButtonOff(i, j, destination, loading=False)
        else:
            for i in range(0, 9):
                for j in range(0, 8):
                    if self.getGridArray(grid)[i][j]:
                        self.turnButtonOn(i, j, destination, loading=False)
                    else:
                        self.turnButtonOff(i, j, destination, loading=False)

        self.saved = False

    def removeFromXML(self, nameToDelete):

        root = self.tree.getroot()
        for channel in root:
            for item in channel:
                if item[0].text == nameToDelete:
                    channel.remove(item)
                    self.writeToFile()
                    return

    def renameInXML(self, nameToChange, newName):

        root = self.tree.getroot()
        for channel in root:
            for item in channel:
                if item[0].text == nameToChange:
                    item[0].text = newName
                    self.writeToFile()
                    return

    def updateXML(self, eyeShape):
        root = self.tree.getroot()
        for channel in root:
            for item in channel:
                if item[0].text == eyeShape.name:
                    item[2].text = str(eyeShape.pupilRangeX)
                    item[3].text = str(eyeShape.pupilRangeY)
                    item[5].text = eyeShape.hexString
                    if eyeShape.autoMirror:
                        item[6].text = 'true'
                    else:
                        item[6].text = 'false'

                    self.writeToFile()
                    return
        return

    def addToXML(self, eyeShape):

        root = self.tree.getroot()
        for channel in root:
            for item in channel:
                if item[0].text == self.tkvar.get():
                    newElement = deepcopy(item)
                    newElement[0].text = eyeShape.name
                    newElement[2].text = str(eyeShape.pupilRangeX)
                    newElement[3].text = str(eyeShape.pupilRangeY)
                    newElement[5].text = eyeShape.hexString
                    if eyeShape.autoMirror:
                        newElement[6].text = 'true'
                    else:
                        newElement[6].text = 'false'

                    channel.append(newElement)
                    self.writeToFile()
                    # print(eyeShape.name)
                    return

    def writeToFile(self):

        my_tree = self.tree

        # directory = picoh.dir

        # file = os.path.join(directory, 'Ohbot.obe')
        file = picoh.eyeShapeFile

        with open(file, 'wb') as f:
            f.write(etree.tostring(my_tree))
            f.close()

    # Shows highlighted blue squares on pupil grid to indicate range.
    def displayRange(self):

        xRange = self.shapeList[self.shapeIndex].pupilRangeX
        yRange = self.shapeList[self.shapeIndex].pupilRangeY

        if xRange > 8:
            xRange = 8

        if yRange > 9:
            yRange = 9

        if xRange < 0:
            xRange = 0

        if yRange < 0:
            yRange = 0

        yStart = (3 - int(yRange / 2))
        xStart = (3 - int(xRange / 2))

        if xStart < 0:
            xStart = 0
        if yStart < 0:
            yStart = 0

        for i in range(0, 9):
            for j in range(0, 8):

                if self.gridArrayOne[i][j]:
                    self.buttonArrayOne[i][j].config(highlightbackground='grey')
                    if self.operatingSystem == "Windows":
                        self.buttonArrayOne[i][j].config(bg=self.buttonCol)

                else:
                    self.buttonArrayOne[i][j].config(highlightbackground='grey')
                    if self.operatingSystem == "Windows":
                        self.buttonArrayOne[i][j].config(bg=self.buttonCol)

        for i in range(xStart, xStart + xRange):
            for j in range(yStart, yStart + yRange):
                if self.rangeVar.get():
                    self.getButtonArray(1)[j][i].config(highlightbackground=self.pupilButtonHighlightColour)
                    if self.operatingSystem == "Windows":
                        self.getButtonArray(1)[j][i].config(bg=self.pupilButtonHighlightColour)

        if self.operatingSystem != "Linux":
            self.xRangeVar.set(str(xRange))
            self.yRangeVar.set(str(yRange))

    def pupilTrackAction(self):
        if self.pupilTrack.get():
            return
        else:
            picoh.move(picoh.EYETURN, 5)
            picoh.move(picoh.EYETILT, 5)

    # Sets pupil range, called when value is changed in entry box.
    def updateRange(self, *args):

        if self.xRangeVar.get() == '' or self.yRangeVar.get() == '':
            return
        self.shapeList[self.shapeIndex].pupilRangeX = int(self.xRangeVar.get())
        self.shapeList[self.shapeIndex].pupilRangeY = int(self.yRangeVar.get())
        self.displayRange()
        self.updateXML(self.shapeList[self.shapeIndex])

    def refreshShapeList(self):

        self.choices = []
        for entry in self.shapeList:
            self.choices.append(entry.name)

        # Get first item in list of choices and set as default
        self.choices.sort()

        # first = next(iter(self.choices), None)
        # self.tkvar.set(self.shapeList[0].name)

        # update popup menu with names from shapelist.

        self.popupMenu = Tk.OptionMenu(self.frame, self.tkvar, *self.choices)

        self.popupMenu.grid(row=3, column=27, columnspan=14, sticky="w")

        self.popupMenu.configure(width=20, font=self.customFont)

        if self.operatingSystem == "Windows" or self.operatingSystem == "Linux":
            self.popupMenu.configure(compound="c", image=pixelImage, height=8, width=self.buttonWidth * 14,justify=Tk.LEFT)
            self.popupMenu.grid(columnspan=15)

    def duplicate(self):

        currentShape = self.shapeList[self.shapeIndex]
        newEyeShape = EyeShape("New", "", False, 5, 5)
        newEyeShape.autoMirror = currentShape.autoMirror
        newEyeShape.hexString = currentShape.hexString
        newEyeShape.name = currentShape.name + " (Copy)"
        newEyeShape.pupilRangeX = currentShape.pupilRangeX
        newEyeShape.pupilRangeY = currentShape.pupilRangeY

        self.shapeList.append(newEyeShape)

        self.addToXML(newEyeShape)
        if self.speak.get() == 1:
            picoh.say(currentShape.name + " Duplicated")
        self.loadShape(shapeName=currentShape.name + " (Copy)", internal=True)
        self.updatePicoh()
        self.popupMenu.destroy()
        self.refreshShapeList()
        self.cancelNewShape()

    # Function to read XML files
    def xmlReadin(self):

        file = picoh.eyeShapeFile

        self.tree = etree.parse(file)

        index = 0

        for element in self.tree.iter():

            if element.tag == "Name":
                self.shapeList.append(EyeShape(str(element.text), "", False, 5, 5))

            if element.tag == "PupilRangeX":
                self.shapeList[index].pupilRangeX = int(element.text)

            if element.tag == "PupilRangeY":
                self.shapeList[index].pupilRangeY = int(element.text)

            if element.tag == "Hex":
                self.shapeList[index].hexString = element.text

            if element.tag == "AutoMirror":
                if element.text == "true":
                    self.shapeList[index].autoMirror = True

                else:
                    self.shapeList[index].autoMirror = False

                index = index + 1

    def openHex(self, hexString, loading=False):

        # Empty binary strings

        shapeBinary = ''
        pupilBinary = ''
        blinkOneBinary = ''
        blinkTwoBinary = ''
        blinkThreeBinary = ''
        blinkFourBinary = ''

        # Load into binary strings for each char

        for hexBit in hexString[:18]:
            shapeBinary = shapeBinary + self.hexToBin(hexBit)

        for hexBit in hexString[90:108]:
            pupilBinary = pupilBinary + self.hexToBin(hexBit)

        for hexBit in hexString[18:36]:
            blinkOneBinary = blinkOneBinary + self.hexToBin(hexBit)
        for hexBit in hexString[36:54]:
            blinkTwoBinary = blinkTwoBinary + self.hexToBin(hexBit)
        for hexBit in hexString[54:72]:
            blinkThreeBinary = blinkThreeBinary + self.hexToBin(hexBit)
        for hexBit in hexString[72:90]:
            blinkFourBinary = blinkFourBinary + self.hexToBin(hexBit)

        # Load Matrix with binary strings.

        self.loadMatrix(pupilBinary, 1, loading)
        self.loadMatrix(shapeBinary, 0, loading)
        self.loadMatrix(blinkOneBinary, 2, loading)
        self.loadMatrix(blinkTwoBinary, 3, loading)
        self.loadMatrix(blinkThreeBinary, 4, loading)
        self.loadMatrix(blinkFourBinary, 5, loading)

    # Function to flip the state of a button at given coordinate.
    def flipButton(self, i, j, grid):

        if grid == 1:
            if self.gridArrayOne[i][j] == 0:
                self.turnPupilOff(i, j)
            else:
                self.turnPupilOn(i, j)

        if self.getGridArray(grid)[i][j] == 0:
            self.turnButtonOn(i, j, grid, loading=False)
        else:
            self.turnButtonOff(i, j, grid, loading=False)

        if grid == 1:
            self.updateRange()

        self.updatePicoh()

        # Turn pupil on at coordinate i, j

    # Turn pupil on at coordinate i,j
    def turnPupilOn(self, i, j):

        if self.gridArray[i][j]:
            self.buttonArray[i][j].config(image=onImage)
            self.buttonArray[i][j].config(highlightbackground='grey')

        else:
            self.buttonArray[i][j].config(image=offImage)
            self.buttonArray[i][j].config(highlightbackground='grey')

        if self.operatingSystem == "Windows":
            self.buttonArray[i][j].config(bg=self.buttonCol)

    # Turn pupil off at coordinate i,j
    def turnPupilOff(self, i, j):

        if self.pupilVar:
            self.buttonArray[i][j].config(highlightbackground=self.pupilButtonHighlightColour)
            if self.operatingSystem == "Windows":
                pass
                # self.buttonArray[i][j].config(bg=self.pupilButtonHighlightColour)
            self.buttonArray[i][j].config(image=offImage)

    # Turn button on at coordinate i,j
    def turnButtonOn(self, i, j, grid, loading):

        # Prevent eye shape from turning on if pupil is on at this location

        if self.gridArrayOne[i, j] and self.pupilVar and grid == 0 and not loading:
            return

        self.getGridArray(grid)[i][j] = 1
        self.getButtonArray(grid)[i][j].config(highlightbackground='grey', image=onImage)
        if self.operatingSystem == "Windows":
            bg = self.buttonCol
        self.saved = False

    # Turn button off at coordinate i,j
    def turnButtonOff(self, i, j, grid, loading):

        # Prevent eye shape from turning off if pupil is on at this location

        if self.gridArrayOne[i, j] and self.pupilVar and grid == 0 and not loading:
            return

        self.getGridArray(grid)[i][j] = 0
        self.getButtonArray(grid)[i][j].config(highlightbackground='grey', image=offImage)
        if self.operatingSystem == "Windows":
            bg = self.buttonCol
        self.saved = False

    """
    Returns a hex string representing the current state of all grids
    9 pairs of hex bits for each grid. Order: Eye,Pupil,Blink1,Blink2,Blink3,Blink4
    """

    def hexFromGrids(self):

        # Create an empty binary string and read each grid into it.
        binaryStringIn = ''
        order = [0, 2, 3, 4, 5, 1]

        for grid in order:

            for i in range(0, self.getGridArray(grid).shape[0]):
                for j in range(0, self.getGridArray(grid).shape[1]):
                    binaryStringIn = str(binaryStringIn) + str(int(self.getGridArray(grid)[i][j]))
                    hd = (len(binaryStringIn) + 3) // 4

        string = '%.*x' % (hd, int('0b' + binaryStringIn, 0))
        return string

    # Get hex string from grids and set Picoh's eyes to it.
    def updatePicoh(self):
        if self.picohConnected:
            hexToSend = self.hexFromGrids()
            picoh._setEyes(hexToSend, hexToSend, self.shapeList[self.shapeIndex].autoMirror)

    # Toggle sending data to Picoh.
    def picohToggle(self):

        if self.picohConnected:
            self.picohButton.config(image=logo)
            self.picohConnected = False
        else:
            self.picohButton.config(image=logoOn)
            self.picohConnected = True
            self.updatePicoh()

    # Function refresh all grids

    def newButton(self):

        self.newButton.grid_remove()
        self.renameButton.grid_remove()

        self.dupButton.grid_remove()
        self.delButton.grid_remove()

        self.popupMenu.destroy()

        self.okayOne.grid(row=4, column=27, columnspan=4, sticky="w")
        self.cancelOne.grid(row=4, column=31, columnspan=4, sticky="e")
        self.entryPop.grid(row=3, column=27, columnspan=15,rowspan=2, sticky="nw")

    def cancel(self):
        self.refreshShapeList()
        self.cancelNewShape()

    def cancelNewShape(self):
        self.entryPop.grid_remove()
        self.entryPopTwo.grid_remove()
        self.textLab.grid_remove()
        self.but.grid_remove()
        self.butCancel.grid_remove()
        self.okayOne.grid_remove()
        self.cancelOne.grid_remove()
        self.okayTwo.grid_remove()
        self.cancelTwo.grid_remove()

        self.popupMenu.grid(row=3, column=27, columnspan=14, sticky="w")
        self.newButton.grid(row=4, column=27, columnspan=4, sticky="w")
        self.renameButton.grid(row=4, column=31, columnspan=4, sticky="e")
        self.delButton.grid(row=5, column=27, columnspan=4, sticky="w")
        self.dupButton.grid(row=5, column=31, columnspan=4, sticky="e")

        self.entryPop.delete(0, Tk.END)
        self.entryPopTwo.delete(0, Tk.END)

    def newShape(self, *args):

        newName = self.entryPop.get()

        if newName == "":
            self.cancelNewShape()
            print("Please enter a name")
            return

        newEyeShape = EyeShape("New", "", False, 5, 5)
        newEyeShape.autoMirror = "False"
        newEyeShape.hexString = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        newEyeShape.name = newName
        newEyeShape.pupilRangeX = 5
        newEyeShape.pupilRangeY = 5

        self.addToXML(newEyeShape)

        self.shapeList.append(newEyeShape)

        self.refreshShapeList()

        self.loadShape(shapeName=newName, internal=True)

        self.cancelNewShape()

        self.updatePicoh()

    def renameButton(self):

        self.newButton.grid_remove()
        self.renameButton.grid_remove()
        self.dupButton.grid_remove()
        self.delButton.grid_remove()
        self.popupMenu.destroy()

        self.entryPopTwo.grid(row=3, column=27, columnspan=10,rowspan = 2, sticky="nw")
        self.okayTwo.grid(row=4, column=27, columnspan=4, sticky="w")
        self.cancelTwo.grid(row=4, column=31, columnspan=4, sticky="e")

        self.entryPopTwo.delete(0, Tk.END)
        self.entryPopTwo.insert(0, self.tkvar.get())

    def rename(self, *args):
        if self.entryPopTwo.get() == "":
            print("Please enter a name")
            self.cancelNewShape()
            return

        oldName = self.shapeList[self.shapeIndex].name
        newName = self.entryPopTwo.get()
        self.shapeList[self.shapeIndex].name = self.entryPopTwo.get()
        self.refreshShapeList()
        self.tkvar.set(self.entryPopTwo.get())
        self.cancelNewShape()
        self.renameInXML(oldName, newName)
        if self.speak.get() == 1:
            picoh.say(oldName + " renamed to " + newName)

    def deleteShapeButton(self):

        self.newButton.grid_remove()
        self.renameButton.grid_remove()
        self.dupButton.grid_remove()
        self.delButton.grid_remove()
        self.popupMenu.destroy()

        self.textLab.grid(row=3, column=27, columnspan=7, sticky="ws")
        self.textLab.config(bg=self.bgCol, font=self.customFont)

        self.but.grid(row=4, column=27, columnspan=4, sticky="w")
        self.but.configure(highlightbackground=self.bgCol, font=self.customFont)

        self.butCancel.grid(row=4, column=31, columnspan=4, sticky="e")
        self.butCancel.configure(highlightbackground=self.bgCol, font=self.customFont)

    def deleteShape(self):

        for idx, shape in enumerate(self.shapeList):
            if shape.name == self.shapeList[self.shapeIndex].name:
                self.removeFromXML(shape.name)
                del self.shapeList[idx]
                break
        self.refreshShapeList()
        self.loadShape(True, self.shapeList[0].name)
        self.cancelNewShape()
        # self.tkvar.set(self.shapeList[0].name)
        self.updatePicoh()

        if self.speak.get() == 1:
            picoh.say(shape.name + " deleted")

    # Load shape and set grids to it.
    def loadShape(self, internal, shapeName, loading=False, *args):

        if shapeName:
            for index, shape in enumerate(self.shapeList):
                if shape.name == shapeName:
                    chosenShape = shape
                    self.shapeIndex = index
        else:
            for index, shape in enumerate(self.shapeList):
                if shape.name == self.tkvar.get():
                    chosenShape = shape
                    self.shapeIndex = index

        # if loading == True:
        if self.speak.get() == 1:
            picoh.say(chosenShape.name + " loaded")

        self.openHex(chosenShape.hexString, loading)

        self.filenamelabel.config(text=chosenShape.name, font=self.customFont)
        #self.parent.title("Picoh Eye Shape Designer - " + chosenShape.name)
        self.currentfilename = chosenShape.name

        self.displayRange()

        if self.operatingSystem != "Linux":
            self.xRangeVar.set(str(chosenShape.pupilRangeX))
            self.yRangeVar.set(str(chosenShape.pupilRangeY))

        if chosenShape.autoMirror:
            self.mirrorVar.set(1)
        else:
            self.mirrorVar.set(0)

        picoh.move(picoh.EYETILT, 5)
        picoh.move(picoh.EYETURN, 5)
        self.updatePicoh()
        self.pupilTrackAction()

        self.tkvar.trace_vdelete("w", self.tkvar.trace_id)
        self.tkvar.set(chosenShape.name)

        self.tkvar.trace_id = self.tkvar.trace_variable("w", self.loadShape)

        self.checkBoxAction()
        self.checkBoxAction()

    # Check box action for automirror check box.
    def mirrorChange(self):

        if self.mirrorVar.get() == 1:
            self.shapeList[self.shapeIndex].autoMirror = True
        else:
            self.shapeList[self.shapeIndex].autoMirror = False
        self.updatePicoh()
        picoh.move(picoh.EYETURN, 5)
        picoh.move(picoh.EYETILT, 5)
        self.updateXML(self.shapeList[self.shapeIndex])

    # For a given hex bit return the binary string.
    @staticmethod
    def hexToBin(hexBit):

        if hexBit == '0':
            return "0000"
        elif hexBit == '1':
            return "0001"
        elif hexBit == '2':
            return "0010"
        elif hexBit == '3':
            return "0011"
        elif hexBit == '4':
            return "0100"
        elif hexBit == '5':
            return "0101"
        elif hexBit == '6':
            return "0110"
        elif hexBit == '7':
            return "0111"
        elif hexBit == '8':
            return "1000"
        elif hexBit == '9':
            return "1001"
        elif hexBit == 'a' or hexBit == 'A':
            return "1010"
        elif hexBit == 'b' or hexBit == 'B':
            return "1011"
        elif hexBit == 'c' or hexBit == 'C':
            return "1100"
        elif hexBit == 'd' or hexBit == 'D':
            return "1101"
        elif hexBit == 'e' or hexBit == 'E':
            return "1110"
        elif hexBit == 'f' or hexBit == 'F':
            return "1111"
        else:
            print("not a hex char:")
            print(hexBit)
            return '0000'

    # Reset a given grid, clearing all buttons.
    def reset(self, grid):
        for j in range(8):
            for i in range(9):
                self.turnButtonOff(i, j, grid, loading=False)
                if grid == 1:
                    self.turnPupilOn(i, j)
                if grid == 0:
                    self.gridArray[i][j] = 0
        if grid == 1:
            self.updateRange()
        self.updatePicoh()
        self.updateXML(self.shapeList[self.shapeIndex])

    # Load a given grid with a binary string.
    def loadMatrix(self, string, grid, loading=False):
        count = 0
        for char in string:

            y = count % 8
            x = int(count / 8)

            if grid == 1:

                if char == '1':
                    self.turnButtonOn(x, y, grid, loading)
                    self.turnPupilOff(x, y)
                else:
                    self.turnButtonOff(x, y, grid, loading)
                    self.turnPupilOn(x, y)
            else:
                if char == '1':
                    self.turnButtonOn(x, y, grid, loading)
                else:
                    self.turnButtonOff(x, y, grid, loading)
            count += 1

    # Return the gridArray Object for a given grid number
    def getGridArray(self, grid):
        if grid == 0:
            return self.gridArray
        if grid == 1:
            return self.gridArrayOne
        if grid == 2:
            return self.gridArrayTwo
        if grid == 3:
            return self.gridArrayThree
        if grid == 4:
            return self.gridArrayFour
        if grid == 5:
            return self.gridArrayFive

    # Return the buttonArray Object for a given grid number
    def getButtonArray(self, grid):
        if grid == 0:
            return self.buttonArray
        if grid == 1:
            return self.buttonArrayOne
        if grid == 2:
            return self.buttonArrayTwo
        if grid == 3:
            return self.buttonArrayThree
        if grid == 4:
            return self.buttonArrayFour
        if grid == 5:
            return self.buttonArrayFive

    # Action for mouse down
    def OnMouseDown(self, event, x, y, grid):

        # Hasn't left a square yet so started moving is False
        startedMoving = False

        # Decided if the stroke should draw or erase nodes
        if self.getGridArray(grid)[x, y]:
            self.drawing = False
        else:
            self.drawing = True

        # Flip the button that triggered the event
        self.flipButton(x, y, grid)

        # Send new grid to Picoh
        if grid == 0 or grid == 1:
            self.updatePicoh()

    #  Action for mouse move
    def OnMouseMove(self, event, grid):

        # If mouse is not outside original button do nothing.

        if not self.startedMoving:
            return

        # Calculate an offset to account for the window being moved.

        offsetx = root.winfo_x() - self.rootx
        offsety = root.winfo_y() - self.rooty

        # Map the pixel coordinate of the event to the corresponding grid coordinate.

        coordinateX = ((event.x_root - 56 - offsetx) / 24)
        coordinateY = ((event.y_root - 100 - offsety) / 24) - 1

        if self.operatingSystem == "Windows":
            coordinateX = ((event.x_root - 28 - offsetx) / 25)
            coordinateY = ((event.y_root - 85 - offsety) / 25) - 1

            if grid > 3:
                coordinateX = coordinateX + 1

        if self.operatingSystem == "Linux":
            coordinateX = ((event.x_root - 32 - offsetx) / 26)
            coordinateY = ((event.y_root - 70 - offsety) / 26) - 1

        # print(str(coordinateX)+"\n"+str(coordinateY))

        if coordinateY > 9:
            coordinateY = coordinateY + 0.5
            coordinateY = coordinateY % 10
        if coordinateX > 8:
            coordinateX = coordinateX % 9

        # Constrain coordinates to between 0 - 8.
        if coordinateX > 8:
            return
        if coordinateX > 7:
            coordinateX = 7
        if coordinateX < 0:
            coordinateX = 0

        if coordinateY > 8:
            coordinateY = 8

        if coordinateY < 0:
            coordinateY = 0

        # If in drawing mode, turn on the button at the coordinate and update Picoh's matrix.
        #  Otherwise, turn off button at the coordinate and update Picoh's matrix.

        if self.drawing:
            self.turnButtonOn(int(coordinateY), int(coordinateX), grid, loading=False)
            if grid == 1:
                self.turnPupilOff(int(coordinateY), int(coordinateX))
        else:
            self.turnButtonOff(int(coordinateY), int(coordinateX), grid, loading=False)
            if grid == 1:
                self.turnPupilOn(int(coordinateY), int(coordinateX))

        self.updatePicoh()

    def motion(self, event):

        if not self.pupilTrack.get():
            return

        x, y = event.x, event.y

        x = root.winfo_pointerx() - root.winfo_rootx()
        y = root.winfo_pointery() - root.winfo_rooty()

        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName)  # event.widget is your widget

        scaledX = x / parent.winfo_width()
        scaledX = scaledX * 10

        scaledY = y / parent.winfo_height()
        scaledY = scaledY * 10

        if scaledX < 10 or scaledX > 0 or scaledY < 10 or scaledY > 0:
            picoh.move(picoh.EYETURN, scaledX)
            picoh.move(picoh.EYETILT, 10 - scaledY)

    def saveShape(self):
        self.shapeList[self.shapeIndex].hexString = self.hexFromGrids()
        self.saved = True

        # self.updateRange()
        self.updateXML(self.shapeList[self.shapeIndex])

    #    print("saved!")
    # print(self.shapeList[self.shapeIndex].hexString)

    # Mouse up action for buttons.
    def OnMouseUp(self, event):
        self.updateRange()
        self.clickedDown = False

        # self.uRange()

        if not self.saved:
            t = Timer(0.3, self.saveShape)
            t.start()  # after 1 second save.

    def testBlink(self):
        for x in range(10, 0, -2):
            picoh.move(picoh.LIDBLINK, x)
            picoh.wait(0.04)

        for x in range(0, 10, 2):
            picoh.move(picoh.LIDBLINK, x)
            picoh.wait(0.04)

    # Mouse leave action for buttons.
    def OnMouseLeave(self, event):
        self.startedMoving = True

    # Pupil toggle check box callback.
    def checkBoxAction(self):
        if self.pupilVar:
            self.pupilVar = False
            for j in range(8):
                for i in range(9):
                    self.turnPupilOn(i, j)
        else:
            self.pupilVar = True
            for j in range(8):
                for i in range(9):
                    if self.gridArrayOne[i][j] == 1:
                        self.turnPupilOff(i, j)


class SpeechDatabasePage(Tk.Frame):

    global phraseList, rowList, numberOfRows

    class Phrase(object):
        def __init__(self, set, variable, text):
            self.set = set
            self.variable = variable
            self.text = text

    def generateRow(self,phrase, rowNo, frame):
        row = []
        # print(phrase.text)
        e = Tk.Entry(frame, font=self.customFont)
        e.insert(0, phrase.set)
        e.config(width=5)
        e.bind("<Return>", self.callback)
        e.bind("<FocusOut>", self.callback)
        e.grid(column=0, row=rowNo+1)
        row.append(e)
        e1 = Tk.Entry(frame, font=self.customFont)
        e1.insert(0, phrase.variable)
        e1.config(width=8)
        e1.bind("<Return>", self.callback)
        e1.bind("<FocusOut>", self.callback)
        e1.grid(column=1, row=rowNo+1)
        row.append(e1)
        e2 = Tk.Entry(frame, font=self.customFont)
        e2.insert(0, phrase.text)
        e2.config(width=89)
        e2.bind("<Return>", self.callback)
        e2.bind("<FocusOut>", self.callback)
        e2.grid(column=2, row=rowNo+1)
        e2.bind('<Control-a>', self.selAll)
        e2.bind('<Control-a>', self.selAll)
        row.append(e2)

        b1 = Tk.Button(frame, font=self.customFont, text="Speak",command=lambda text=1:picoh.say(e2.get()))


        b1.grid(column=3, row=rowNo+1)
        b1.bind('<Control-a>', self.selAll)
        row.append(e2)


        return row

    def selectall(event):
        event.widget.tag_add("sel", "1.0", "end")
        return "break"


    def selAll(event):
        event.widget.select_range(0, len(event.widget.get()))
        return "break"


    def new(self):
        global numberOfRows, phraseList, rowList
        newPhrase = self.Phrase(0, 0, "")
        row = self.generateRow(newPhrase, self.numberOfRows + 1, self.frame)
        self.phraseList.append(newPhrase)
        self.rowList.append(row)
        self.numberOfRows = self.numberOfRows + 1
        self.refreshCanvas()
        self.canvas.yview_moveto(1)

    def refreshCanvas(self):
        self.canvas.delete("all")
        self.canvas.create_window(0, 0, anchor='n', window=self.frame)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scroll_y.set)
        rowHeight = 26
        blockMax = 400
        offset = blockMax - (rowHeight * self.numberOfRows)


    def callbackWin(self,*args):
        with open(self.file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(["Set", "Variable", "Phrase"])
            #print("Win")
            for row in self.rowList:
                set = row[0].get()
                variable = row[1].get()
                phrase = row[2].get()
                if phrase:
                    writer.writerow([set, variable, phrase])


    def callback(self,*args):
        if platform.system() == "Windows":
            self.callbackWin(self)
        else:
            with open(self.file, 'w') as writeFile:
                writer = csv.writer(writeFile, delimiter=',')
                writer.writerow(["Set", "Variable", "Phrase"])
                for row in self.rowList:
                    set = row[0].get()
                    variable = row[1].get()
                    phrase = row[2].get()
                    if phrase:
                        writer.writerow([set, variable, phrase])


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            callback()
            root.destroy()

    def _on_mousewheel(self, event):
        if event.delta < 0:
            self.canvas.yview_moveto(self.canvas.yview()[0]+0.01)
        else:
            self.canvas.yview_moveto(self.canvas.yview()[0]-0.01)

    def __init__(self,parent,frameIn):

        operatingSystem = platform.system()

        if operatingSystem == "Darwin":
            self.customFont = tkFont.Font(family="Letter Gothic Std", size=11)
        if operatingSystem == "Windows" or operatingSystem == "Linux":
            self.customFont = tkFont.Font(family="Helvetica", size=8)

        speechFile = 'picohData/PicohSpeech.csv'
        # directory = picoh.dir
        self.numberOfRows = 0
        self.phraseList = []
        self.rowList = []
        self.file = speechFile
        self.parent = parent

        self.canvas = Tk.Canvas(frameIn)

        self.scroll_y = Tk.Scrollbar(frameIn, orient="vertical", command=self.canvas.yview)
        self.canvas.config(width=830, height=420, bg='white', highlightthickness=0)

        self.frame = Tk.Frame(self.canvas)

        self.canvas.create_window(0, 0, anchor='nw', window=self.frame)

        # make sure everything is displayed before configuring the scrollregion
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),
                 yscrollcommand=self.scroll_y.set)

        self.canvas.grid(column=0, row=1)
        self.scroll_y.grid(column=1, row=1, sticky="ns")

        with open(self.file, 'r')as f:
            data = csv.reader(f)
            for row in data:
                if row[0] != '' and row[0] != 'Set':
                    if row[0] == '' and row[1] == '':
                        newPhrase = self.Phrase('', '', row[2])
                        self.phraseList.append(newPhrase)
                    elif row[0] == '' and row[1] != '':
                        newPhrase = self.Phrase('', int(row[1]), row[2])
                        self.phraseList.append(newPhrase)
                    elif row[0] != '' and row[1] == '':
                        newPhrase = self.Phrase(row[0], '', row[2])
                        self.phraseList.append(newPhrase)
                    else:
                        newPhrase = self.Phrase(row[0], row[1], row[2])
                        self.phraseList.append(newPhrase)

        #self.parent.title("Picoh Speech DB")
        self.parent.grid_rowconfigure(1, weight=0)
        self.parent.grid_columnconfigure(1, weight=0)
        root.title("Picoh - Tools")
        root.configure(bg='white')
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        #root.protocol("WM_DELETE_WINDOW", on_closing)

         # group of widgets
        for phrase in self.phraseList:
            row = self.generateRow(phrase, self.numberOfRows, self.frame)
            self.numberOfRows = self.numberOfRows + 1
            self.rowList.append(row)
        rowHeight = 26
        blockMax = 400
        offset = blockMax - (rowHeight * self.numberOfRows)

        directory = picoh.directory

        saveButton = Tk.Button(self.frame, text="Save", command=self.callback, font=self.customFont)
        # saveButton.grid(column=1, row=1, sticky='w')
        addButton = Tk.Button(frameIn, image= plusImage, command=self.new, font=self.customFont)
        addButton.grid(column=0, row=2, sticky='w')

        picohLabel = Tk.Label(frameIn, image=picohImage)
        picohLabel.grid(column=0, row=3)

        setLabel = Tk.Label(frameIn, text="Set", font=self.customFont, width=3, bg='white')
        setLabel.grid(column=0, row=0, sticky='w')
        variableLabel = Tk.Label(frameIn, text="Variable", font=self.customFont, width=10, bg='white')
        variableLabel.grid(column=0, row=0, sticky='w',padx=40)
        phraseLabel = Tk.Label(frameIn, text="Phrase (Leave blank to delete)", font=self.customFont, bg='white')
        phraseLabel.grid(column=0, row=0, sticky='w',padx=115)

        self.canvas.yview_moveto(1)
        self.refreshCanvas()


class Calibrate(Tk.Frame):
    global button, stage, lipMinRaw, lipMaxRaw, tempMin, tempMax


    def setLipPos(self,*args):

        if self.started:
            picoh.attach(picoh.BOTTOMLIP)

            # Convert position (0-10) to a motor position in degrees

            # Scale range of speed
            spd = (250 / 10) * 2

            # Construct message from values
            msg = "m0" + str(picoh.BOTTOMLIP) + "," + str(self.var.get()) + "," + str(spd) + "\n"

            # Write message to serial port
            picoh._serwrite(msg)

            # Update motor positions list
            picoh.motorPos[picoh.BOTTOMLIP] = self.var.get()


    def ResetRangeToRawCentre(self):
        # Find the range

        lipRange = self.lipMaxRaw - self.lipMinRaw
        center = self.var.get()
        # Limit to 1000 if something's gone wrong
        if lipRange > 1000:
            lipRange = 1000

        # If raw plus half the range goes over 1000 limit the range to stop it

        over = center + (lipRange / 2) - 1000
        if over > 0:
            lipRange = over - (over * 2)

        # If raw minus half the range goes below 0 limit the range to stop it
        under = lipRange / 2 - center
        if under > 0:
            lipRange = lipRange - (under * 2)

        self.tempMin = int(center - (lipRange / 2))
        self.tempMax = int(center + (lipRange / 2))


    def writeToXML(self,minimum, maximum):
        file = 'picohData/MotorDefinitionsPicoh.omd'

        tree = etree.parse(file)
        root = tree.getroot()

        for child in root:
            if child.get("Name") == "BottomLip":
                child.set("Min", str(minimum))
                child.set("Max", str(maximum))

        with open(file, 'wb') as f:
            f.write(etree.tostring(tree))
            f.close()


    def ResetRangeToRawMin(self):


        smilePos = self.var.get()

        # Find the mid position which was hopefully set by step 1
        midRaw = self.tempMin + ((self.tempMax - self.tempMin) / 2)
        lipRange = (midRaw - smilePos) * 2

        # Stop the max being more than 1000
        if smilePos + lipRange > 1000:
            lipRange = 1000 - smilePos

        # The current position should set the new min
        minimum = int(smilePos)
        maximum = int(smilePos + lipRange)

        scaledMinimum = int(minimum / 180 * 1000)
        scaledMaximum = int(maximum / 180 * 1000)

        self.writeToXML(scaledMinimum, scaledMaximum)


    def sel(self):
        global frameUsed

        if self.stage == 2:
            picoh.reset()
            return
            #root.destroy()

           # c

            #picoh.wait(1)

           # picoh.close()

            #sys.exit()
        if self.stage == 1:
            self.ResetRangeToRawMin()
            self.label.config(text="All done!")
            self.started = False

        if self.stage == 0:
            selection = "Value = " + str(self.var.get())
            self.label.config(
                text="Slowly move the slider to the right, stop when the bottom lip pops the top lip into a smile.")
            self.button.config(text="Set Smile Point")

            self.ResetRangeToRawCentre()
            self.stage = 1

            # Set headnod to 5
            picoh.move(picoh.HEADNOD, 10)
            # Move bottom lip to 4
            picoh.move(picoh.BOTTOMLIP, 4)

            # Wait 250ms
            picoh.wait(0.25)

            # Move bottom lip to 6
            picoh.move(picoh.BOTTOMLIP, 6)

        if self.stage == -1:
            picoh.move(picoh.HEADNOD, 8)

            # Move bottom lip to 4
            picoh.move(picoh.BOTTOMLIP, 4)

            # Wait 250ms
            picoh.wait(0.25)

            # Move bottom lip to 8
            picoh.move(picoh.BOTTOMLIP, 8)

            self.label.config(text='Slowly move the slider to the left until the bottom lip just touches the top lip')
            self.button.config(text='Set Mid-point.')
            self.stage = 0
            self.started = True

            root.after(0, self.update, 0)

    def update(self,ind):

        if self.stage == 0:
            frame = frames[ind]
            self.graphic.configure(image=frame)
        if self.stage == 1:
            frame = framesTwo[ind]
            self.graphic.configure(image=frame)
            
        ind += 1
        
        if ind == len(frames) and self.stage == 0:
            ind = 0

        if ind == len(framesTwo) and self.stage == 1:
            ind = 0

        if ind == 0:
            root.after(2000,self.update, ind)
        else:
            root.after(20,self.update, ind)

    def __init__(self,parent,frameIn):

        self.started = False

        self.stage = -1

        self.graphic = Tk.Label(frameIn)

        self.graphic.config(width=10000)

        frame = frames[len(frames)-1]
        self.graphic.configure(image=frame)


        self.graphic.pack(anchor='ne')

        operatingSystem = platform.system()

        if operatingSystem == "Darwin":
            self.customFont = tkFont.Font(family="Letter Gothic Std", size=11)
        if operatingSystem == "Windows" or operatingSystem == "Linux":
            self.customFont = tkFont.Font(family="Helvetica", size=8)



        # Get min and max positions.
        self.lipMinRaw = picoh.motorMins[picoh.BOTTOMLIP]
        self.lipMaxRaw = picoh.motorMaxs[picoh.BOTTOMLIP]
        lipRange = self.lipMaxRaw - self.lipMinRaw

        # Extend Ranges

        if self.lipMinRaw - lipRange / 5 > 0:
            self.lipMinRaw = self.lipMinRaw - lipRange / 5
        else:
            self.lipMinRaw = 0

        if self.lipMaxRaw + lipRange / 5 < 1000:
            self.lipMaxRaw = self.lipMaxRaw + lipRange / 5
        else:
            self.lipMaxRaw = 1000

        self.parent = parent

        self.frame = frameIn


        self.var = Tk.IntVar()
        self.var.set(picoh._getPos(picoh.BOTTOMLIP, picoh.motorPos[picoh.BOTTOMLIP]))
        scale = Tk.Scale(self.frame, variable=self.var, from_=self.lipMaxRaw, length=wDim - 140, to=self.lipMinRaw, orient=Tk.HORIZONTAL)

        self.var.trace_variable("w", self.setLipPos)
        scale.pack(anchor='s')

        self.label = Tk.Label(self.frame,font=self.customFont, text='')
        self.label.pack()

        self.button = Tk.Button(self.frame, text="Start", command=self.sel,font=self.customFont)
        self.button.pack(anchor=Tk.CENTER)

        #root.after(0, self.update, 0)

class SettingsPage(Tk.Frame):
    def __init__(self,parent,frameIn):

        operatingSystem = platform.system()

        if operatingSystem == "Darwin":
            self.customFont = tkFont.Font(family="Letter Gothic Std", size=11)
        if operatingSystem == "Windows" or operatingSystem == "Linux":
            self.customFont = tkFont.Font(family="Helvetica", size=8)

        label1 = Tk.Label(frameIn,text="Default Eye Shape:",font=self.customFont)
        label1.grid(row=0,column=0)
        self.entry1 = Tk.Entry(frameIn,width = 50,font=self.customFont)
        self.entry1.insert(0, picoh.defaultEyeShape)
        self.entry1.grid(row=0, column = 1)
        self.entry1.bind("<Return>", self.writeToXML)
        self.entry1.bind("<FocusOut>", self.writeToXML)

        label2 = Tk.Label(frameIn,text="Default Speech Synth:",font=self.customFont)
        label2.grid(row=1,column=0)
        self.entry2 = Tk.Entry(frameIn,width = 50,font=self.customFont)
        self.entry2.insert(0,picoh.synthesizer)
        self.entry2.grid(row=1, column = 1)

        self.entry2.bind("<Return>", self.writeToXML)
        self.entry2.bind("<FocusOut>", self.writeToXML)

        label3 = Tk.Label(frameIn,text="Default Voice:",font=self.customFont)
        label3.grid(row=2,column=0)
        self.entry3 = Tk.Entry(frameIn,width = 50,font=self.customFont)
        self.entry3.insert(0,picoh.voice)
        self.entry3.grid(row=2, column = 1)

        self.entry3.bind("<Return>", self.writeToXML)
        self.entry3.bind("<FocusOut>", self.writeToXML)

        label5 = Tk.Label(frameIn,text="Default Language/Voice (gTTS):",font=self.customFont)
        label5.grid(row=3,column=0)
        self.entry5 = Tk.Entry(frameIn,width = 50,font=self.customFont)
        self.entry5.insert(0,picoh.language)
        self.entry5.grid(row=3, column = 1)

        self.entry5.bind("<Return>", self.writeToXML)
        self.entry5.bind("<FocusOut>", self.writeToXML)

        label6 = Tk.Label(frameIn,text="Port:",font=self.customFont)
        label6.grid(row=4,column=0)

        label11 = Tk.Text(frameIn,width=50,font=self.customFont,height =1, highlightthickness=0)
        label11.insert('1.0', picoh.port)
        label11.config(state="disabled")
        label11.grid(row=4, column = 1)

        label4 = Tk.Label(frameIn,text="Sounds Folder:",font=self.customFont)
        #label4.grid(row=5,column=0)
        self.entry4 = Tk.Entry(frameIn,width=50,font=self.customFont)
        self.entry4.insert(0,picoh.soundFolder + "/")

        #self.entry4.grid(row=5, column = 1)

        label7 = Tk.Label(frameIn,text="SpeechDB File:",font=self.customFont)
        label7.grid(row=6,column=0)
        self.entry7 = Tk.Entry(frameIn,width=50,font=self.customFont)
        self.entry7.insert(0,picoh.speechDatabaseFile)
        self.entry7.grid(row=6, column = 1)
        self.entry7.bind("<Return>", self.writeToXML)
        self.entry7.bind("<FocusOut>", self.writeToXML)

        label8 = Tk.Label(frameIn,text="EyeShape List:",font=self.customFont)
        label8.grid(row=7,column=0)
        self.entry8 = Tk.Entry(frameIn,width=50,font=self.customFont)
        self.entry8.insert(0,picoh.eyeShapeFile)
        self.entry8.grid(row=7, column = 1)
        self.entry8.bind("<Return>", self.writeToXML)
        self.entry8.bind("<FocusOut>", self.writeToXML)

        label9 = Tk.Label(frameIn,text="Motor Def File:",font=self.customFont)
        label9.grid(row=8,column=0)
        self.entry9 = Tk.Entry(frameIn,width=50,font=self.customFont)
        self.entry9.insert(0,picoh.picohMotorDefFile)
        self.entry9.grid(row=8, column = 1)
        self.entry9.bind("<Return>", self.writeToXML)
        self.entry9.bind("<FocusOut>", self.writeToXML)

        label9 = Tk.Label(frameIn,text="Picoh Python library:",font=self.customFont)
        label9.grid(row=9,column=0)

        label10 = Tk.Text(frameIn,width=50,font=self.customFont, height =2, highlightthickness=0)
        label10.insert('1.0', picoh.directory)
        label10.config(state="disabled")
        label10.grid(row=9, column = 1)



        label10.bind('<1>', lambda event: label10.focus_set())
        label11.bind('<1>', lambda event: label11.focus_set())

        button = Tk.Button(frameIn,text = "Save",command = self.writeToXML)
        button.grid(row=10,column=0)

    def writeToXML(self,*args):
            file = picoh.settingsFile

            tree = etree.parse(file)
            root = tree.getroot()

            for child in root:
                if child.get("Name") == "DefaultEyeShape":
                    child.set("Value", self.entry1.get())
                    picoh.defaultEyeShape = self.entry1.get()

                if child.get("Name") == "DefaultSpeechSynth":
                    child.set("Value", self.entry2.get())
                    picoh.setSynthesizer(self.entry2.get())

                if child.get("Name") == "DefaultVoice":
                    child.set("Value", self.entry3.get())
                    picoh.setVoice(self.entry3.get())

                if child.get("Name") == "DefaultLang":
                    child.set("Value", self.entry5.get())
                    picoh.setLanguage(self.entry5.get())

                if child.get("Name") == "SpeechDBFile":
                    child.set("Value", self.entry7.get())

                if child.get("Name") == "EyeShapeList":
                    child.set("Value", self.entry8.get())

                if child.get("Name") == "MotorDefFile":
                    child.set("Value", self.entry9.get())


            with open(file, 'wb') as f:
                f.write(etree.tostring(tree))
                f.close()



if __name__ == "__main__":

    root = Tk.Tk()
    directory = picoh.directory

    imageFile = os.path.join(directory, 'Images/onsmaller.gif')
    onImage = Tk.PhotoImage(file=imageFile)
    imageFile = os.path.join(directory, 'Images/offsmaller.gif')
    offImage = Tk.PhotoImage(file=imageFile)
    imageFile = os.path.join(directory, 'Images/picohlogo.gif')
    logo = Tk.PhotoImage(file=imageFile)
    imageFile = os.path.join(directory, 'Images/picohlogoOn.gif')
    logoOn = Tk.PhotoImage(file=imageFile)
    imageFile = os.path.join(directory, 'Images/movedown.gif')
    copyDown = Tk.PhotoImage(file=imageFile)
    imageFile = os.path.join(directory, 'Images/moveright.gif')
    copyRight = Tk.PhotoImage(file=imageFile)
    imageFile = os.path.join(directory, 'Images/pixel.gif')
    pixelImage = Tk.PhotoImage(file=imageFile)

    imageFile = os.path.join(directory, 'Images/plus.gif')
    plusImage = Tk.PhotoImage(file=imageFile)
    imageFile = os.path.join(directory, 'Images/picohlogoSmall.gif')
    picohImage = Tk.PhotoImage(file=imageFile)

    imageFile = os.path.join(directory, 'Images/calibrate400.gif')
    frames = [Tk.PhotoImage(file=imageFile,format = 'gif -index %i' %(i)) for i in range(52)]

    imageFile = os.path.join(directory, 'Images/calibrate2400.gif')
    framesTwo = [Tk.PhotoImage(file=imageFile,format = 'gif -index %i' %(i)) for i in range(53)]

    if platform.system() == "Darwin":
        xDim = 120
        yDim = 140
        hDim = 560
        wDim = 903
    if platform.system() == "Windows":
        xDim = 20
        yDim = 40
        hDim = 495
        wDim = 850

    if platform.system() == "Linux":
        xDim = 20
        yDim = 40
        hDim = 560
        wDim = 915

    root.geometry('%dx%d+%d+%d' % (wDim, hDim, xDim,  yDim))
    root.configure(bg='white')
   # root.resizable(1, 1)

    nb = ttk.Notebook(root,width=wDim,height=hDim)          # Create Tab Control
    tab1 = Tk.Frame(nb,width = wDim,height = hDim)
    nb.add(tab1, text='Eye Designer')

    tab2 = Tk.Frame(nb)

    nb.add(tab2, text='SpeechDB')

    tab3 = Tk.Frame(nb)

    nb.add(tab3, text='Calibrate')

    tab4 = Tk.Frame(nb)

    nb.add(tab4, text='Settings')

    nb.enable_traversal()

    if platform.system() == "Darwin":
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    eyeApp = PicohEyeDesigner(root,tab1)
    speechApp = SpeechDatabasePage(root,tab2)
    calibrateApp = Calibrate(root,tab3)

    settingsApp = SettingsPage(root,tab4)

    nb.pack()
    root.mainloop()

