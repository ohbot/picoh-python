import csv
import os
import random
import tkinter as Tk
import tkinter.font as tkFont
from tkinter import messagebox
from picoh import picoh
import platform

global phraseList, rowList, numberOfRows
speechFile = 'picohData/PicohSpeech.csv'
# directory = picoh.dir
numberOfRows = 0
phraseList = []
rowList = []
file = speechFile


class Phrase(object):
    def __init__(self, set, variable, text):
        self.set = set
        self.variable = variable
        self.text = text


def generateRow(phrase, rowNo, frame):
    row = []
    # print(phrase.text)
    e = Tk.Entry(frame, font=customFont)
    e.insert(0, phrase.set)
    e.config(width=5)
    e.bind("<Return>", callback)
    e.bind("<FocusOut>", callback)
    e.grid(column=0, row=rowNo)
    row.append(e)
    e1 = Tk.Entry(frame, font=customFont)
    e1.insert(0, phrase.variable)
    e1.config(width=8)
    e1.bind("<Return>", callback)
    e1.bind("<FocusOut>", callback)
    e1.grid(column=1, row=rowNo)
    row.append(e1)
    e2 = Tk.Entry(frame, font=customFont)
    e2.insert(0, phrase.text)
    e2.config(width=89)
    e2.bind("<Return>", callback)
    e2.bind("<FocusOut>", callback)
    e2.grid(column=2, row=rowNo)
    e2.bind('<Control-a>', selAll)
    e2.bind('<Control-a>', selAll)
    row.append(e2)
    return row


def refreshCanvas():
    canvas.delete("all")
    canvas.create_window(0, 0, anchor='n', window=frame)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)
    rowHeight = 26
    blockMax = 400
    offset = blockMax - (rowHeight * numberOfRows)
    if numberOfRows * rowHeight < blockMax:
        frame.config(width=750, height=26 * numberOfRows, bg='white', highlightthickness=0)
        canvas.config(width=750, height=26 * numberOfRows, bg='white', highlightthickness=0)
        canvasSpacer.config(width=750, height=offset, bg='white', highlightthickness=0)
    else:
        frame.config(width=750, height=400, bg='white', highlightthickness=0)
        canvas.config(width=750, height=400, bg='white', highlightthickness=0)
        canvasSpacer.config(width=750, height=0, bg='white', highlightthickness=0)


def selectall(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"


def selAll(event):
    event.widget.select_range(0, len(event.widget.get()))
    return "break"


def new():
    global numberOfRows, phraseList, rowList
    newPhrase = Phrase(0, 0, "")
    row = generateRow(newPhrase, numberOfRows + 1, frame)
    phraseList.append(newPhrase)
    rowList.append(row)
    numberOfRows = numberOfRows + 1
    refreshCanvas()
    canvas.yview_moveto(1)


def callbackWin():
    with open(file, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(["Set", "Variable", "Phrase"])
        print("Win")
        for row in rowList:
            set = row[0].get()
            variable = row[1].get()
            phrase = row[2].get()
            if phrase:
                writer.writerow([set, variable, phrase])


def callback(*args):
    if platform.system() == "Windows":
        callbackWin()
    else:
        with open(file, 'w') as writeFile:
            writer = csv.writer(writeFile, delimiter=',')
            writer.writerow(["Set", "Variable", "Phrase"])
            for row in rowList:
                set = row[0].get()
                variable = row[1].get()
                phrase = row[2].get()
                if phrase:
                    writer.writerow([set, variable, phrase])


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        callback()
        root.destroy()


with open(file, 'r')as f:
    data = csv.reader(f)
    for row in data:

        if row[0] != '' and row[0] != 'Set':
            if row[0] == '' and row[1] == '':
                newPhrase = Phrase('', '', row[2])
                phraseList.append(newPhrase)
            elif row[0] == '' and row[1] != '':
                newPhrase = Phrase('', int(row[1]), row[2])
                phraseList.append(newPhrase)
            elif row[0] != '' and row[1] == '':
                newPhrase = Phrase(row[0], '', row[2])
                phraseList.append(newPhrase)
            else:
                newPhrase = Phrase(row[0], row[1], row[2])
                phraseList.append(newPhrase)
root = Tk.Tk()
root.title("Picoh - Speech Database")
root.geometry('776x470')
operatingSystem = platform.system()
root.configure(bg='white')
root.resizable(0, 0)
root.protocol("WM_DELETE_WINDOW", on_closing)
##customFont = tkFont.Font(root, family="Letter Gothic Std", size=12)
if operatingSystem == "Darwin":
    customFont = tkFont.Font(family="Letter Gothic Std", size=11)
if operatingSystem == "Windows" or operatingSystem == "Linux":
    customFont = tkFont.Font(family="Helvetica", size=8)
canvasThree = Tk.Canvas(root)
canvas = Tk.Canvas(root)
canvasTwo = Tk.Canvas(root)
canvasSpacer = Tk.Canvas(root)
canvasTwo.config(width=750, height=75, bg='white')
canvasThree.config(width=750, height=25, bg='white')
# canvasTwo.geometry('200x150')
scroll_y = Tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = Tk.Frame(canvas)
frameTwo = Tk.Frame(canvasTwo)
frameThree = Tk.Frame(canvasThree)
frame.bind_class("Text", "<Control-a>", selectall)
frameTwo.config(width=750, height=75, bg='white')
frameThree.config(width=750, height=25, bg='white')
# group of widgets
for phrase in phraseList:
    row = generateRow(phrase, numberOfRows, frame)
    numberOfRows = numberOfRows + 1
    rowList.append(row)
rowHeight = 26
blockMax = 400
offset = blockMax - (rowHeight * numberOfRows)
if numberOfRows * rowHeight < blockMax:
    frame.config(width=750, height=26 * numberOfRows, bg='white', highlightthickness=0)
    canvas.config(width=750, height=26 * numberOfRows, bg='white', highlightthickness=0)
    canvasSpacer.config(width=750, height=offset, bg='white', highlightthickness=0)
else:
    frame.config(width=750, height=400, bg='white', highlightthickness=0)
    canvas.config(width=750, height=400, bg='white', highlightthickness=0)
    canvasSpacer.config(width=750, height=0, bg='white', highlightthickness=0)
# put the frame in the canvas
canvas.create_window(0, 0, anchor='nw', window=frame)
canvasTwo.create_window(0, 0, anchor='nw', window=frameTwo)
canvasThree.create_window(0, 0, anchor='nw', window=frameThree)
# make sure everything is displayed before configuring the scrollregion
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox('all'),
                 yscrollcommand=scroll_y.set)
canvas.grid(column=0, row=1)
scroll_y.grid(column=1, row=1, sticky="ns")
canvasTwo.grid(column=0, row=3)
canvasSpacer.grid(column=0, row=2)
canvasThree.grid(column=0, row=0)
directory = picoh.directory
imageFile = os.path.join(directory, 'Images/plus.gif')
plusImage = Tk.PhotoImage(file=imageFile)
saveButton = Tk.Button(frameTwo, text="Save", command=callback, font=customFont)
# saveButton.grid(column=1, row=1, sticky='w')
addButton = Tk.Button(frameTwo, image=plusImage, command=new, font=customFont)
addButton.grid(column=0, row=1, sticky='w')
imageFile = os.path.join(directory, 'Images/picohlogoSmall.gif')
picohImage = Tk.PhotoImage(file=imageFile)
picohLabel = Tk.Label(frameTwo, image=picohImage)
picohLabel.grid(column=2, row=1, sticky='w')
setLabel = Tk.Label(frameThree, text="Set", font=customFont, width=5, bg='white')
setLabel.grid(column=0, row=0, sticky='w')
variableLabel = Tk.Label(frameThree, text="Variable", font=customFont, width=10, bg='white')
variableLabel.grid(column=1, row=0, sticky='w')
phraseLabel = Tk.Label(frameThree, text="Phrase (Leave blank to delete)", font=customFont, bg='white')
phraseLabel.grid(column=2, row=0, sticky='w')

# Launch the GUI
root.mainloop()


def getPhrase(set, variable):
    possiblePhrases = []
    for phrase in phraseList:
        if phrase.set == set and phrase.variable == variable:
            possiblePhrases.append(phrase.text)
    length = len(possiblePhrases)
    if length == 0:
        print("No matching phrase found for set: " + str(set) + " variable: " + str(variable) + " in: " + speechFile)
        return ""
    elif length == 1:
        return possiblePhrases[0]
    else:
        return possiblePhrases[random.randint[0, length]]
