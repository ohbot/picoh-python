from picoh import picoh

picoh._revertMotorDefsFile()

import tkinter as Tk

from lxml import etree

global button, stage, lipMinRaw, lipMaxRaw, tempMin, tempMax
import sys

stage = 0

picoh.move(picoh.HEADNOD, 8)

# Move bottom lip to 4
picoh.move(picoh.BOTTOMLIP, 4)

# Wait 250ms
picoh.wait(0.25)

# Move bottom lip to 8
picoh.move(picoh.BOTTOMLIP, 8)

# Get min and max positions.
lipMinRaw = picoh.motorMins[picoh.BOTTOMLIP]
lipMaxRaw = picoh.motorMaxs[picoh.BOTTOMLIP]
lipRange = lipMaxRaw - lipMinRaw

# Extend Ranges

if lipMinRaw - lipRange / 5 > 0:
    lipMinRaw = lipMinRaw - lipRange / 5
else:
    lipMinRaw = 0

if lipMaxRaw + lipRange / 5 < 1000:
    lipMaxRaw = lipMaxRaw + lipRange / 5
else:
    lipMaxRaw = 1000


def setLipPos(*args):
    picoh.attach(picoh.BOTTOMLIP)

    # Convert position (0-10) to a motor position in degrees

    # Scale range of speed
    spd = (250 / 10) * 2

    # Construct message from values
    msg = "m0" + str(picoh.BOTTOMLIP) + "," + str(var.get()) + "," + str(spd) + "\n"

    # Write message to serial port
    picoh._serwrite(msg)

    # Update motor positions list
    picoh.motorPos[picoh.BOTTOMLIP] = var.get()


def ResetRangeToRawCentre():
    global lipMinRaw, lipMaxRaw, tempMin, tempMax

    # Find the range

    lipRange = lipMaxRaw - lipMinRaw
    center = var.get()
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

    tempMin = int(center - (lipRange / 2))
    tempMax = int(center + (lipRange / 2))


def writeToXML(minimum, maximum):
    file = 'picohData/MotorDefinitionsPicoh.omd'

    tree = etree.parse(file)
    root = tree.getroot()

    for child in root:
        if child.get("Name") == "BottomLip":
            # print("Hoorah")
            child.set("Min", str(minimum))
            child.set("Max", str(maximum))

    with open(file, 'wb') as f:
        f.write(etree.tostring(tree))
        f.close()


def ResetRangeToRawMin():
    global tempMin, tempMax

    smilePos = var.get()

    # Find the mid position which was hopefully set by step 1
    midRaw = tempMin + ((tempMax - tempMin) / 2)
    lipRange = (midRaw - smilePos) * 2

    # Stop the max being more than 1000
    if smilePos + lipRange > 1000:
        lipRange = 1000 - smilePos

    # The current position should set the new min
    minimum = int(smilePos)
    maximum = int(smilePos + lipRange)

    scaledMinimum = int(minimum / 180 * 1000)
    scaledMaximum = int(maximum / 180 * 1000)

    writeToXML(scaledMinimum, scaledMaximum)


def sel():
    global button, stage, lipMaxRaw, lipMinRaw

    if stage == 2:
        root.destroy()

        picoh.reset()

        picoh.wait(1)

        picoh.close()

        sys.exit()

    if stage == 1:
        ResetRangeToRawMin()
        label.config(text="All done!")
        stage = 2
        button.config(text="Close")

    if stage == 0:
        selection = "Value = " + str(var.get())
        label.config(
            text="Slowly move the slider to the right, stop when the bottom lip pops the top lip into a smile.")

        button.config(text="Set Smile Point")

        ResetRangeToRawCentre()
        stage = 1

        # Set headnod to 5
        picoh.move(picoh.HEADNOD, 10)
        # Move bottom lip to 4
        picoh.move(picoh.BOTTOMLIP, 4)

        # Wait 250ms
        picoh.wait(0.25)

        # Move bottom lip to 6
        picoh.move(picoh.BOTTOMLIP, 6)


root = Tk.Tk()

xDim = 20
yDim = 40
hDim = 110
wDim = 670
root.geometry('%dx%d+%d+%d' % (wDim, hDim, xDim, yDim))
root.configure(bg='white')
root.resizable(0, 0)
root.title("Picoh - Calibration")

var = Tk.IntVar()
var.set(picoh._getPos(picoh.BOTTOMLIP, picoh.motorPos[picoh.BOTTOMLIP]))
scale = Tk.Scale(root, variable=var, from_=lipMaxRaw, length=wDim - 40, to=lipMinRaw, orient=Tk.HORIZONTAL)

var.trace_variable("w", setLipPos)
scale.pack(anchor=Tk.CENTER)

label = Tk.Label(root, text='Slowly move the slider to the left until the bottom lip just touches the top lip')
label.pack()

button = Tk.Button(root, text="Set Mid Point", command=sel)
button.pack(anchor=Tk.CENTER)

root.mainloop()