from tkinter import *

root = Tk()
root.title("Canvas")
root.geometry("500x500")

canvas = Canvas(root, width=240, height=240, bg="white")
canvas.pack(padx=20, pady=20)

# canvas.create_line(x1, y1, x2, y2, fill="color", ...)
canvas.create_line(0, 0, 200, 200, fill="red")

# canvas.create_rectangle(x1, y1, x2, y2, fill="color")
canvas.create_rectangle(50, 50, 150, 150, fill="gray")

root.mainloop()
