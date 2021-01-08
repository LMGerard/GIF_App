import tkinter as tk
from window.Frame import Frame
from functools import partial
from PIL import Image, ImageTk


class Preview(Frame):
    def __init__(self, window, tool, variables: dict):
        super().__init__(window, tool, variables)

    def window_tool(self, text="by Loupio"):
        pass

    def window_options(self):
        self.variables["preview_current"] = 0

        self.gif_preview = tk.Canvas(self.options_frame, width=300, height=300)
        self.gif_preview.create_rectangle(0, 0, 300, 300)
        self.gif_preview.grid(row=0, columnspan=3)
        previous_image = tk.Button(self.options_frame, text="<-", command=partial(self.change_preview, -1)).grid(
            column=0, row=1)
        next_image = tk.Button(self.options_frame, text="->", command=partial(self.change_preview, 1)).grid(column=2,
                                                                                                            row=1)
        reload_btn = tk.Button(self.options_frame, text="reload", command=self.update_preview).grid(column=1, row=1)
        self.variables["preview_label"] = tk.StringVar(self.options_frame, value="-_-")
        label = tk.Label(self.options_frame, textvariable=self.variables["preview_label"]).grid(column=1, row=2)

    def update_preview(self):
        self.variables["GifManager"].create_gif()
        self.variables["GifManager"].save_gif(temp=True)
        self.change_preview(0)

    def change_preview(self, dir):
        tempImages = self.variables["GifManager"].tempImages
        if len(tempImages) == 0: return

        self.variables["preview_current"] += dir
        if self.variables["preview_current"] >= len(tempImages): self.variables["preview_current"] = 0
        if self.variables["preview_current"] < 0: self.variables["preview_current"] = len(tempImages) - 1

        self.variables["preview_label"].set(
            str(self.variables["preview_current"] + 1) + "/" + str(len(tempImages)))

        global image
        with Image.open(tempImages[self.variables["preview_current"]].name, "r") as image:
            image = image.resize((300, 300))
            image = ImageTk.PhotoImage(image)
        self.gif_preview.create_image(0, 0, anchor=tk.NW, image=image)
