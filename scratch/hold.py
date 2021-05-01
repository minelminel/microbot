import tkinter as tk


class MyBtn(tk.Button):
    # set function to call when pressed
    def set_down(self, fn):
        self.bind("<Button-1>", fn)

    # set function to be called when released
    def set_up(self, fn):
        self.bind("<ButtonRelease-1>", fn)


class Mainframe(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        # create the button and set callback functions
        btn = MyBtn(self, text="Press & Hold")
        btn.set_up(self.on_up)
        btn.set_down(self.on_down)
        btn.pack()

    # function called when pressed
    def on_down(self, x):
        print("Button down")

    # function called when released
    def on_up(self, x):
        print("Button up")


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("My Button")
        self.geometry("250x50")

        Mainframe(self).pack()


# create and run an App object
App().mainloop()
