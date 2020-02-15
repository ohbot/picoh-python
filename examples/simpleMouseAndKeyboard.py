# Picoh - simple mouse and keyboard control example.
# Pioch will follow mouse movements and speak when 'a','b' or 'c' keys are pressed. 

from tkinter import *
from picoh import picoh

# Create a 600x600 window. 
win=Tk()
win.geometry("600x600")

# Function that is called when the mouse is moved. 
def xy(event):
    # Get the coordinates of where the mouse movement happened. 
    xm, ym = event.x, event.y

    # Scale the coordniate so it is between 0-10. Divide by 60 as window is 600 x 600. 
    xm = xm/60
    ym = ym/60

    # Use the scaled position to set Picoh's motor and pupil positions and base colour. 
    picoh.move(picoh.HEADTURN,xm)
    picoh.move(picoh.HEADNOD,ym)
    picoh.move(picoh.EYETURN,xm)
    picoh.move(picoh.EYETILT,ym)
    picoh.setBaseColour(10-ym,ym,xm)

# Function for when the 'a' key is pressed
def aKey(event):
    picoh.say("Hello I am Picoh",untilDone = False)
    picoh.setBaseColour(3,3,10)

# Function for when the 'b' key is pressed
def bKey(event):
    picoh.playSound('spring',untilDone = True)
    picoh.say("What's going on ?",untilDone = False)
    picoh.setBaseColour(10,3,3)

# Function for when the 'c' key is pressed
def cKey(event):
    picoh.say("Hello humans",untilDone = False)
    picoh.setBaseColour(3,10,3)

# Function called when window is closed. 
def on_closing():
    picoh.reset()
    picoh.wait(1)
    picoh.close()
    win.destroy()
    
# Bind the close button to the on_closing function.
win.protocol("WM_DELETE_WINDOW", on_closing)
    
# Bind windows Motion Action to xy function. Call the xy function whenever the mouse is moved.  
win.bind("<Motion>",xy)

# Bind keys to their functions. 
win.bind("a",aKey)
win.bind("b",bKey)
win.bind("c",cKey)

# Start the loop to make the window active.  
mainloop()
