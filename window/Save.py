import tkinter as tk
from tkinter import filedialog
from window.Frame import Frame
from functools import partial
from functions import to_only_int, to_max_size


class Save(Frame):
    def __init__(self, window_tool, window_options, variables: dict):
        super().__init__(window_tool, window_options, variables, btntxt="Save options")

    def window_options(self):
        self.variables["dir_path"] = tk.StringVar(self.options_frame, value="")
        self.variables["file_name"] = tk.StringVar(self.options_frame, value="output")
        self.variables["duration"] = tk.StringVar(self.options_frame, value="100")

        self.variables["duration"].trace("w", partial(self.entry_test, self.variables["duration"], 5, only_int=True))

        label01 = tk.Label(self.options_frame, text="Directory")
        entry01 = tk.Entry(self.options_frame, textvariable=self.variables["dir_path"])
        btn01 = tk.Button(self.options_frame, text="Choose directory", command=self.open_filedialog)

        label02 = tk.Label(self.options_frame, text="File name")
        entry02 = tk.Entry(self.options_frame, textvariable=self.variables["file_name"])

        duration = tk.Frame(self.options_frame)
        tk.Label(duration, text="duration").grid(column=0, row=0)
        tk.Entry(duration, width=5, textvariable=self.variables["duration"]).grid(column=1, row=0)

        self.variables["infinite_loop"] = tk.IntVar()
        tk.Checkbutton(self.options_frame, text="Infinite loop", variable=self.variables["infinite_loop"]).pack()
        generate_button = tk.Button(self.options_frame, text="Save GIF", command=self.variables["GifManager"].save_gif)

        self.pack_all(label01, entry01, btn01, label02, entry02, duration, generate_button)

    def open_filedialog(self):
        self.variables["dir_path"].set(filedialog.askdirectory())

    def entry_test(self, text_var: tk.StringVar, limit: int, a, b, c, only_int=False):
        if only_int:
            text_var.set(to_only_int(text_var.get()))

        text_var.set(to_max_size(text_var.get(), 5))
