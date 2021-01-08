import tkinter as tk
from window.Frame import Frame
from functions import is_color
from functools import partial


class Colors(Frame):
    def __init__(self, window, tool, variables: dict):
        super().__init__(window, tool, variables, btntxt="Background options")

    def window_options(self):
        label01 = tk.Label(self.options_frame, text="Background color (default: black)")

        self.variables["background_color"] = tk.StringVar(self.options_frame, value="")

        background_color = tk.Entry(self.options_frame, textvariable=self.variables["background_color"])

        self.variables["background_color"].trace("w", partial(self.test_color, background_color,
                                                              self.variables["background_color"]))

        self.pack_all(label01, background_color)

    @staticmethod
    def test_color(entry: tk.Entry, text_var: tk.StringVar, a, b, c):
        if len(text_var.get()) > 0:
            if is_color(text_var.get()):
                entry.config(fg="black")
            else:
                entry.config(fg="red")
