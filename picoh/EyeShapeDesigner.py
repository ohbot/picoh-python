import tkinter as Tk
import tkinter.font as tkFont
from tkinter import ttk
# from tkinter import *
# from tkinter import messagebox
from tkinter import OptionMenu
import os.path
# from os import path
import numpy as np
# from PIL import Image, ImageFilter
# import math
from lxml import etree
import os
from picoh import picoh
from copy import deepcopy

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
    # pupilButtonHighlightColour = '#408bf9'
    pupilButtonHighlightColour = 'SkyBlue1'

    buttonWidth = 10
    tickWidth = 15

    tree = None



    def initialize(self):

        # Configure Window

        self.parent.title("Picoh Eye Shape Designer")
        self.parent.grid_rowconfigure(1, weight=0)
        self.parent.grid_columnconfigure(1, weight=0)

        self.customFont = tkFont.Font(family="Letter Gothic Std", size=12)

        self.frame = Tk.Frame(self.parent)
        self.frame.configure(bg=self.bgCol)

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        #Variables to track tick boxes:
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

        self.entryPopTwo = Tk.Entry(self.frame, width=30, text="Test", font=self.customFont)
        self.entryPopTwo.bind('<Return>', self.rename)

        self.entryPop = Tk.Entry(self.frame, width=30, text="Test", font=self.customFont)
        self.entryPop.bind('<Return>', self.newShape)

        # Add pupil overlay  and track checkboxes

        checkbox = Tk.Checkbutton(self.frame, text="Overlay Pupil", variable=self.pupilVar, command=self.checkBoxAction)
        checkbox.grid(row=4, rowspan=1, column=18, columnspan=5, sticky="w")
        checkbox.configure(bg=self.bgCol, font=self.customFont)

        pupilTrackBox = Tk.Checkbutton(self.frame, text="Mouse-Pupil", variable=self.pupilTrack,
                                       command=self.pupilTrackAction)
        pupilTrackBox.grid(row=8, rowspan=1, column=27, columnspan=4, sticky="w")
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
        #            self.filenamelabel.grid(row=13,column = 0,columnspan = 10,sticky = "W", padx = (10,0))

        #  Create 2D arrays with 0's to hold button states.
        for x in range(0, 6):
            for j in range(9):
                column = []
                for i in range(8):
                    column.append(0)
                self.getButtonArray(x).append(column)

        # New Button
        self.newButton = Tk.Button(self.frame, text="New", command=self.newButton, width=self.buttonWidth)
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

        #  Reset buttons for each grid

        self.resetButton = Tk.Button(self.frame, text='Clear', command=lambda: self.reset(0))
        self.resetButton.grid(row=0, column=5, columnspan=3, sticky="E")
        self.resetButton.configure(highlightbackground=self.bgCol, bg=self.bgCol, fg=self.textCol, font=self.customFont)

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
        else:
            chosenLogo = logo

        # Create Picoh logo button.
        self.picohButton = Tk.Button(self.frame, command=self.picohToggle, image=chosenLogo)
        self.picohButton.grid(row=0, column=27, columnspan=20, rowspan=3, sticky="s")
        self.picohButton.configure(highlightbackground=self.bgCol)

        picohPanel = Tk.Label(self.frame, image=picohGraphic)
        #  picohPanel.grid(row=9, column=8, columnspan=16, rowspan=16, sticky="sw")

        #  Generate button grids: (xStart,yStart,grid)
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

        self.xRangeEntry.grid(row=7, column=22, columnspan=5, sticky='w')
        self.xRangeEntry.config(bg='white', font=self.customFont)

        self.yRangeEntry = Tk.Entry(self.frame, width=2, textvariable=self.yRangeVar)

        self.yRangeEntry.grid(row=8, column=22, columnspan=5, sticky='w')
        self.yRangeEntry.config(bg='white', font=self.customFont)

        self.xRangeLabel = Tk.Label(self.frame, text="Pupil Range X", font=self.customFont)

        self.xRangeLabel.grid(row=7, column=18, columnspan=5, sticky='w')
        self.xRangeLabel.config(bg=self.bgCol, fg=self.textCol)

        self.yRangeLabel = Tk.Label(self.frame, text="Pupil Range Y")

        self.yRangeLabel.grid(row=8, column=18, columnspan=5, sticky='w')
        self.yRangeLabel.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        self.xRangeVar.trace_variable("w", self.updateRange)
        self.yRangeVar.trace_variable("w", self.updateRange)

        # Create check boxes

        self.mirrorCheckbox = Tk.Checkbutton(self.frame, text="Auto Mirror", variable=self.mirrorVar,
                                             command=self.mirrorChange)
        self.mirrorCheckbox.grid(row=7, rowspan=1, column=27, columnspan=4, sticky="w")
        self.mirrorCheckbox.config(bg=self.bgCol, highlightcolor=self.textCol, font=self.customFont,
                                   width=self.tickWidth)

        self.rangeCheckbox = Tk.Checkbutton(self.frame, text="Show Pupil Range", variable=self.rangeVar,
                                            command=self.displayRange)
        self.rangeCheckbox.grid(row=5, rowspan=1, column=18, columnspan=5, sticky="w")
        self.rangeCheckbox.config(bg=self.bgCol, fg=self.textCol, font=self.customFont)

        # Pack frame.
        self.frame.pack(fill=Tk.X, padx=0, pady=0)

        root.bind('<Motion>', self.motion)

        #Load first shape in the list.
        self.shapeIndex = 0
        self.loadShape(True, shapeName=self.shapeList[self.shapeIndex].name, loading=True)
        self.updatePicoh()

        self.checkBoxAction()
        checkbox.invoke()

        if self.picohConnected:
            picoh.reset()
            picoh.close()

        root.mainloop()

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    # Function to generate buttons
    def generateButtons(self, buttonStartX, buttonStartY, grid):
        for i in range(0, self.getGridArray(grid).shape[0]):
            for j in range(0, self.getGridArray(grid).shape[1]):

                b = Tk.Button(self.frame, highlightbackground=self.buttonCol, width=0, height=0, borderwidth=0,
                              highlightthickness=-2, padx=-2, pady=-2)

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

        #directory = picoh.dir

        #file = os.path.join(directory, 'Ohbot.obe')
        file = 'picohData/Ohbot.obe'

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
                    self.buttonArrayOne[i][j].config(highlightbackground='white')

                else:
                    self.buttonArrayOne[i][j].config(highlightbackground=self.buttonCol)

        for i in range(xStart, xStart + xRange):
            for j in range(yStart, yStart + yRange):
                if self.rangeVar.get():
                    self.getButtonArray(1)[j][i].config(highlightbackground=self.pupilButtonHighlightColour)

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

        self.popupMenu.grid(row=3, column=27, columnspan=15, sticky="w")

        self.popupMenu.configure(bg=self.bgCol, width=30, font=self.customFont)

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

        directory = picoh.dir

        #file = os.path.join(directory, 'Ohbot.obe')
        file = 'picohData/Ohbot.obe'

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
            self.buttonArray[i][j].config(highlightbackground='white')

        else:
            self.buttonArray[i][j].config(image=offImage)
            self.buttonArray[i][j].config(highlightbackground=self.buttonCol)

    # Turn pupil off at coordinate i,j
    def turnPupilOff(self, i, j):

        if self.pupilVar:
            self.buttonArray[i][j].config(highlightbackground=self.pupilButtonHighlightColour)
            self.buttonArray[i][j].config(image=offImage)

    # Turn button on at coordinate i,j
    def turnButtonOn(self, i, j, grid, loading):

        # Prevent eye shape from turning on if pupil is on at this location

        if self.gridArrayOne[i, j] and self.pupilVar and grid == 0 and not loading:
            return

        self.getGridArray(grid)[i][j] = 1
        self.getButtonArray(grid)[i][j].config(highlightbackground='white', image=onImage)

        self.saved = False

    # Turn button off at coordinate i,j
    def turnButtonOff(self, i, j, grid, loading):

        # Prevent eye shape from turning off if pupil is on at this location

        if self.gridArrayOne[i, j] and self.pupilVar and grid == 0 and not loading:
            return

        self.getGridArray(grid)[i][j] = 0
        self.getButtonArray(grid)[i][j].config(highlightbackground=self.buttonCol, image=offImage)

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
            picoh._setEyes(hexToSend, hexToSend)

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
        self.entryPop.grid(row=3, column=27, columnspan=15, sticky="w")

    #  print(self.entryPop.get())

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

        self.popupMenu.grid(row=3, column=27, columnspan=15, sticky="w")
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

        self.entryPopTwo.grid(row=3, column=27, columnspan=10, sticky="w")
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

        self.textLab.grid(row=3, column=27, columnspan=5, sticky="ws")
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
        self.parent.title("Picoh Eye Shape Designer - " + chosenShape.name)
        self.currentfilename = chosenShape.name

        self.displayRange()

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

    #  Action for mouse move
    def OnMouseMove(self, event, grid):

        # If mouse is not outside original button do nothing.

        if not self.startedMoving:
            return

        # Calculate an offset to account for the window being moved.

        offsetx = root.winfo_x() - self.rootx
        offsety = root.winfo_y() - self.rooty

        # Map the pixel coordinate of the event to the corresponding grid coordinate.

        coordinateX = ((event.x_root - 26 - offsetx) / 28)
        coordinateY = ((event.y_root - 50 - offsety) / 32) - 1

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
        #  Otherwise, turn off button at the coordinate and update Picoh's matrix.

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

        """
        x = root.winfo_pointerx()

        y = root.winfo_pointery()
        abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()

        abs_coord_y = root.winfo_pointery() - root.winfo_rooty()

        scaledX = abs_coord_x/x
        scaledX = scaledX*10

        scaledY = abs_coord_y/y
        scaledY = scaledY*10
        
        """

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


if __name__ == "__main__":
    root = Tk.Tk()
    xDim = 20
    yDim = 40
    hDim = 606
    wDim = 1000
    root.geometry('%dx%d+%d+%d' % (wDim, hDim, xDim, yDim))
    root.configure(bg='white')
    root.resizable(0, 0)

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

    app = PicohEyeDesigner(root)
    root.mainloop()
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
