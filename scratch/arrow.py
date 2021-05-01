import math
from functools import partial
from tkinter import *


# dummy controller class


class Controller(object):

    name = None
    position = 0
    min_position = 0
    max_position = 100

    def __init__(self, **kwargs):
        for kwarg, param in kwargs.items():
            if param is not None:
                print(f"Setting param {kwarg}={param}")
                setattr(self, kwarg, param)

    def render(self, **kwargs):
        # TODO: need a way to update *decr* button to enable it after *incr* action triggered
        # condition = [self.at_min, self.at_max][limit == "max"]
        # button["state"] = DISABLED if condition() else ACTIVE
        kwargs["label"]["text"] = str(self)

    def increment(self, **kwargs):
        print(f"Incrementing {self.name}")
        if self.position < self.max_position:
            self.position += 1
        else:
            print(f"Cannot increment {self.name}: limit reached!")
        self.render(limit="max", **kwargs)

    def decrement(self, **kwargs):
        print(f"Decrementing {self.name}")
        if self.position > self.min_position:
            self.position -= 1
        else:
            print(f"Cannot decrement {self.name}: limit reached!")
        self.render(limit="min", **kwargs)

    def at_min(self):
        return self.position == self.min_position

    def at_max(self):
        return self.position == self.max_position

    def __repr__(self):
        return "<Controller name={} position={}>".format(repr(self.name), self.position)


X = Controller(name="X", position=0, min_position=-100, max_position=100)
Y = Controller(name="Y", position=0, min_position=-100, max_position=100)
Z = Controller(name="Z", position=0, min_position=-45, max_position=45)


# gui logic

root = Tk()
root.geometry("800x480")
root.title("Arrow Pad")

kwargs = {
    "height": 2,
    "width": 4,
    "padx": 5,
    "pady": 5,
    "font": ("Calibri 18"),
    "repeatdelay": 500,     # need to factor in the stepper delay to these values (ms)
    "repeatinterval": 25,
}

label_x = Label(root, text=str(X))
label_y = Label(root, text=str(Y))
label_z = Label(root, text=str(Y))

label_x.grid(row=0, column=4, padx=20)
label_y.grid(row=1, column=4, padx=20)
label_z.grid(row=2, column=4, padx=20)

btn_x_decr = Button(root, text="←", **kwargs)
btn_x_incr = Button(root, text="→", **kwargs)
btn_y_incr = Button(root, text="↑", **kwargs)
btn_y_decr = Button(root, text="↓", **kwargs)
btn_z_decr = Button(root, text="↶", **kwargs)
btn_z_incr = Button(root, text="↷", **kwargs)
# btn_a = Button(root, text="A", bg="#ffb8b8", command=partial(print, "Button A"), **kwargs)
# btn_b = Button(root, text="B", bg="#b8d9ff", command=partial(print, "Button B"), **kwargs)

btn_x_decr["command"] = partial(X.decrement, label=label_x)
btn_x_incr["command"] = partial(X.increment, label=label_x)
btn_y_incr["command"] = partial(Y.increment, label=label_y)
btn_y_decr["command"] = partial(Y.decrement, label=label_y)
btn_z_decr["command"] = partial(Z.decrement, label=label_z)
btn_z_incr["command"] = partial(Z.increment, label=label_z)

btn_x_decr.grid(row=1, column=0)
btn_x_incr.grid(row=1, column=2)
btn_y_incr.grid(row=0, column=1)
btn_y_decr.grid(row=2, column=1)
btn_z_incr.grid(row=0, column=2)
btn_z_decr.grid(row=0, column=0)
# btn_a.grid(row=2, column=0)
# btn_b.grid(row=2, column=2)

root.mainloop()


"""
      0:  1:  2:
0:  | ↶ | U | ↷ |
1:  | L |   | R |
2:  |   | D |   |

X & Y axes are just simple cartesian coordinates,
whereas Z is the angle of approach in degrees [-45, 45]
so in order to normalize the slope we divide the value by 45
and draw a unit line with that slope

"""
point = (28, 71, -13)

