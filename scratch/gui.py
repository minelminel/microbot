from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# need to use Pillow to handle modern image formats
from PIL import ImageTk, Image

# plot function is created for
# plotting the graph in
# tkinter window
def plot():
    print(f"calling command: plot")
    # the figure that will contain the plot
    fig = Figure(figsize=(4, 4), dpi=100)
    # list of squares
    y = [i ** 2 for i in range(101)]
    # adding the subplot
    plot1 = fig.add_subplot(111)
    # plotting the graph
    plot1.plot(y)
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


def quit():
    print("quitting program")
    # shutdown logic
    root.quit()

# the main Tkinter window
root = Tk()
# setting the title
root.title("Plotting in Tkinter")
# dimensions of the main window
root.geometry("800x480")

# my_img = ImageTk.PhotoImage(Image.open("trees.jpg"))
# my_label = Label(image=my_img)
# my_label.pack()

# button that displays the plot
plot_button = Button(
    master=root,
    command=plot,
    height=2,
    width=10,
    padx=5,
    pady=5,
    text="Plot",
    state=ACTIVE,  # DISABLED
)
quit_button = Button(root, text="Exit Program", command=quit)
quit_button.pack()

input_field = Entry(root, width=50, borderwidth=5)
# input_field.get()
# input_field.delete(0, END)
# input_field.insert(0, "some string")

# place the button
# in main window
plot_button.pack()
input_field.pack()

# run the gui
root.mainloop()

"""
use partials for these:  from functools import partial; command=partial(myFunction, argument))
<<all these are 'widgets'>>
Button
Image
Frame
Label
Entry (text field)
RadioButton
messagebox.
    - showinfo
    - showwarning
    - showerror
    - askquestion
    - askokcancel
    - askyesno
Additional Windows: Toplevel() if you can't get secondary elements to display, make shit global
    - to close, call <window>.destroy
Scale (slider)
Checkbutton
OptionMenu (select field)

"""
