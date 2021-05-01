from functools import partial
from tkinter import *

# Props
default_text = ""
def handle_submit(text):
    print(text)

# the main Tkinter window
root = Tk()
# setting the title
root.title("On-Screen Keyboard")
# dimensions of the main window
# root.geometry("800x480")

# print(root.winfo_screenwidth(), root.winfo_screenheight())

field = Entry(root, width=40, borderwidth=2, font=("Calibri 16"))
field.insert(END, default_text)
field.grid(row=0, column=0, padx=20, pady=20, columnspan=10)

def keyin(key):
    text = field.get()
    field.delete(0, END)
    field.insert(0, f"{text}{key}")

def backspace():
    text = field.get()
    field.delete(0, END)
    field.insert(0, text[:-1])

def enter(callback):
    # pass a callable, which is given field state as argument
    # root.quit() # or close secondary window
    return callback(field.get())

clear = Button(root, text="CLEAR", bg="red", command=partial(field.delete, 0, END))
clear.grid(row=0, column=0)

enter = Button(root, text="ENTER", bg="green", command=partial(enter, handle_submit))
enter.grid(row=0, column=9)

kwargs = {"height": 3, "width": 6, "padx": 4, "pady": 4, "repeatinterval": 100, "repeatdelay": 500}
# Keyboard Row 1
Button(root, text="1", command=partial(keyin, "1"), **kwargs).grid(row=1, column=0, columnspan=1)
Button(root, text="2", command=partial(keyin, "2"), **kwargs).grid(row=1, column=1, columnspan=1)
Button(root, text="3", command=partial(keyin, "3"), **kwargs).grid(row=1, column=2, columnspan=1)
Button(root, text="4", command=partial(keyin, "4"), **kwargs).grid(row=1, column=3, columnspan=1)
Button(root, text="5", command=partial(keyin, "5"), **kwargs).grid(row=1, column=4, columnspan=1)
Button(root, text="6", command=partial(keyin, "6"), **kwargs).grid(row=1, column=5, columnspan=1)
Button(root, text="7", command=partial(keyin, "7"), **kwargs).grid(row=1, column=6, columnspan=1)
Button(root, text="8", command=partial(keyin, "8"), **kwargs).grid(row=1, column=7, columnspan=1)
Button(root, text="9", command=partial(keyin, "9"), **kwargs).grid(row=1, column=8, columnspan=1)
Button(root, text="0", command=partial(keyin, "0"), **kwargs).grid(row=1, column=9, columnspan=1)
# Keyboard Row 2
Button(root, text="Q", command=partial(keyin, "Q"), **kwargs).grid(row=2, column=0, columnspan=1)
Button(root, text="W", command=partial(keyin, "W"), **kwargs).grid(row=2, column=1, columnspan=1)
Button(root, text="E", command=partial(keyin, "E"), **kwargs).grid(row=2, column=2, columnspan=1)
Button(root, text="R", command=partial(keyin, "R"), **kwargs).grid(row=2, column=3, columnspan=1)
Button(root, text="T", command=partial(keyin, "T"), **kwargs).grid(row=2, column=4, columnspan=1)
Button(root, text="Y", command=partial(keyin, "Y"), **kwargs).grid(row=2, column=5, columnspan=1)
Button(root, text="U", command=partial(keyin, "U"), **kwargs).grid(row=2, column=6, columnspan=1)
Button(root, text="I", command=partial(keyin, "I"), **kwargs).grid(row=2, column=7, columnspan=1)
Button(root, text="O", command=partial(keyin, "O"), **kwargs).grid(row=2, column=8, columnspan=1)
Button(root, text="P", command=partial(keyin, "P"), **kwargs).grid(row=2, column=9, columnspan=1)
# Keyboard Row 3
Button(root, text="A", command=partial(keyin, "A"), **kwargs).grid(row=3, column=0, columnspan=2)
Button(root, text="S", command=partial(keyin, "S"), **kwargs).grid(row=3, column=1, columnspan=2)
Button(root, text="D", command=partial(keyin, "D"), **kwargs).grid(row=3, column=2, columnspan=2)
Button(root, text="F", command=partial(keyin, "F"), **kwargs).grid(row=3, column=3, columnspan=2)
Button(root, text="G", command=partial(keyin, "G"), **kwargs).grid(row=3, column=4, columnspan=2)
Button(root, text="H", command=partial(keyin, "H"), **kwargs).grid(row=3, column=5, columnspan=2)
Button(root, text="J", command=partial(keyin, "J"), **kwargs).grid(row=3, column=6, columnspan=2)
Button(root, text="K", command=partial(keyin, "K"), **kwargs).grid(row=3, column=7, columnspan=2)
Button(root, text="L", command=partial(keyin, "L"), **kwargs).grid(row=3, column=8, columnspan=2)
# Keyboard Row 4
Button(root, text="Shift", state=DISABLED, **kwargs).grid(row=4, column=0, columnspan=1)
Button(root, text="Z", command=partial(keyin, "Z"), **kwargs).grid(row=4, column=1, columnspan=1)
Button(root, text="X", command=partial(keyin, "X"), **kwargs).grid(row=4, column=2, columnspan=1)
Button(root, text="C", command=partial(keyin, "C"), **kwargs).grid(row=4, column=3, columnspan=1)
Button(root, text="V", command=partial(keyin, "V"), **kwargs).grid(row=4, column=4, columnspan=1)
Button(root, text="B", command=partial(keyin, "B"), **kwargs).grid(row=4, column=5, columnspan=1)
Button(root, text="N", command=partial(keyin, "N"), **kwargs).grid(row=4, column=6, columnspan=1)
Button(root, text="M", command=partial(keyin, "M"), **kwargs).grid(row=4, column=7, columnspan=1)
Button(root, text="⎵", command=partial(keyin, " "), **kwargs).grid(row=4,column=8, columnspan=1)
Button(root, text="Delete", command=backspace, **kwargs).grid(row=4, column=9, columnspan=1)

# run the gui
root.mainloop()

