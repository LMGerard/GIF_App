import tkinter as tk
from Frame import Frame
from functools import partial


class Colors(Frame):
    def __init__(self, window, tool, variables: dict):
        super().__init__(window, tool, variables, btntxt="Colors options")

    def window_options(self):
        label01 = tk.Label(self.options_frame, text="Font color (default: white)")

        self.variables["font_color"] = tk.StringVar(self.options_frame, value="")
        font_color = tk.Entry(self.options_frame, textvariable=self.variables["font_color"])
        label02 = tk.Label(self.options_frame, text="Background color (default: black)")

        self.variables["background_color"] = tk.StringVar(self.options_frame, value="")
        background_color = tk.Entry(self.options_frame, textvariable=self.variables["background_color"])

        self.pack_all(label01, font_color, label02, background_color)
