import tkinter as tk
import window.Colors, window.Preview, window.Save, window.Text, window.Images
import GifManager


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.window.title("Gif App")
        self.variables = {}
        self.create_components()
        self.window.mainloop()

    def create_components(self):
        self.variables["GifManager"] = GifManager.GifManager(self.variables)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        self.tools = tk.Frame(highlightbackground="black", highlightthickness=1)
        self.tools_panel = tk.Frame(highlightbackground="black", highlightthickness=1)

        self.tools.grid(column=0, row=0, sticky=tk.NS + tk.EW)
        self.tools_panel.grid(column=0, sticky=tk.NS + tk.EW)

        save = window.Save.Save(self.tools, self.tools_panel, self.variables)
        colors = window.Colors.Colors(self.tools, self.tools_panel, self.variables)
        text = window.Text.Text(self.tools, self.tools_panel, self.variables)
        images = window.Images.Images(self.tools, self.tools_panel, self.variables)

        save.pack_all(save.tool_frame, colors.tool_frame, text.tool_frame, images.tool_frame)
        self.variables["CurrentToolsPanel"] = text
        text.show(text.options_frame)

        window.Preview.Preview(self.tools, self.window, self.variables).options_frame.grid(column=1, row=0, rowspan=2,
                                                                                           sticky=tk.E)

    def save_gif(self):
        pass


if __name__ == '__main__':
    App()
