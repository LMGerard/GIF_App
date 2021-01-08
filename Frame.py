import tkinter as tk
from functools import partial


class Frame:
    __window_tool_button = None

    def __init__(self, window_tool, window_options, variables: dict, btntxt="by Loupio"):
        self.tool_frame = tk.Frame(window_tool)
        self.options_frame = tk.Frame(window_options)
        self.variables = variables

        self.window_tool(btntxt)
        self.window_options()

    def window_tool(self, text="by Loupio"):
        self.__window_tool_button = tk.Button(self.tool_frame, text=text,
                                              command=partial(self.show, self.options_frame))
        self.__window_tool_button.pack()

    def window_options(self):
        pass

    def create_elements(self):
        return []

    def show(self, frame: tk.Frame):
        if "CurrentToolsPanel" in self.variables.keys():
            self.variables["CurrentToolsPanel"].hide()
        self.variables["CurrentToolsPanel"] = self
        self.__window_tool_button.config(bg="green")
        frame.pack()

    def hide(self):
        self.__window_tool_button.config(bg="white")
        self.options_frame.pack_forget()

    @staticmethod
    def pack_all(*widgets):
        for widget in widgets:
            widget.pack()
