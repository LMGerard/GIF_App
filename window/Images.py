import tkinter as tk
from window.Frame import Frame
from functools import partial
from functions import to_max_size, to_only_int
from tkinter import filedialog


class Images(Frame):
    __images_listbox = None
    __image__panel = {}

    def __init__(self, window, tool, variables: dict):
        super().__init__(window, tool, variables, btntxt="Images options")
        self.images = []

    def window_options(self):
        self.variables["images"] = []

        label = tk.Label(self.options_frame, text="Images")

        options = tk.Frame(self.options_frame)

        btn01 = tk.Button(options, text="new", command=self.ask_image)
        btn02 = tk.Button(options, text="dup", command=self.duplicate_image)

        btn01.grid(column=0, row=0)
        btn02.grid(column=1, row=0)

        # sentence listbox
        text_frame = tk.Frame(self.options_frame)

        self.__images_listbox = tk.Listbox(text_frame, selectmode=tk.SINGLE)
        self.__images_listbox.bind('<<ListboxSelect>>', self.on_change_sentence_selection)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.__images_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.__images_listbox.yview)

        # sentence panel
        sentence_panel = tk.Frame(self.options_frame, highlightbackground="black", highlightthickness=1)
        coords = tk.Frame(sentence_panel)
        position = tk.Frame(sentence_panel)

        self.__image__panel = {
            "x": tk.Entry(coords, state=tk.DISABLED, width=3),
            "y": tk.Entry(coords, state=tk.DISABLED, width=3),
            "width": tk.Entry(position, state=tk.DISABLED, width=4),
            "height": tk.Entry(position, state=tk.DISABLED, width=4)
        }

        tk.Label(coords, text="Position").grid(column=0, columnspan=4, row=0)
        tk.Label(coords, text="x:").grid(column=0, row=1)
        self.__image__panel["x"].grid(column=1, row=1)
        tk.Label(coords, text="y:").grid(column=2, row=1)
        self.__image__panel["y"].grid(column=3, row=1)

        tk.Label(position, text="Size").grid(column=0, columnspan=4, row=0)
        tk.Label(position, text="width:").grid(column=0, row=1)
        self.__image__panel["width"].grid(column=1, row=1)
        tk.Label(position, text="height:").grid(column=0, row=2)
        self.__image__panel["height"].grid(column=1, row=2)

        settings = tk.Frame(sentence_panel)
        self.__image__panel["delete"] = tk.Button(settings, state=tk.DISABLED, text="D", command=self.del_image)
        self.__image__panel["edit"] = tk.Button(settings, state=tk.DISABLED, text="E",
                                                command=partial(self.ask_image, edit=True))

        self.__image__panel["delete"].grid(column=0, row=4)
        self.__image__panel["edit"].grid(column=1, row=4)

        self.pack_all(label, options, self.__images_listbox, text_frame, sentence_panel, coords, position, settings)

    def on_change_sentence_selection(self, event):
        select = self.__images_listbox.curselection()
        if len(select) == 0: return

        for widget in self.__image__panel.values():
            widget.config(state=tk.NORMAL)

        sentence = self.variables["images"][select[0]]
        self.__image__panel["x"].config(textvariable=sentence.x)
        self.__image__panel["y"].config(textvariable=sentence.y)
        self.__image__panel["color"].config(textvariable=sentence.color)
        self.__image__panel["font_size"].config(textvariable=sentence.font_size)
        self.__image__panel["font_family"].config(textvariable=sentence.font_family)

        sentence.entry_test(sentence.color, 20, None, None, None, color=True)
        sentence.entry_test(sentence.font_size, 4, None, None, None, only_int=True)
        sentence.entry_test(sentence.font_family, 100, None, None, None, font=True)

    def ask_image(self, edit=False):
        if edit:
            image = self.variables["images"][self.__images_listbox.curselection()[0]]
        else:
            image = ImageW(self.__image__panel)

        print(image)

        popup = tk.Toplevel()
        popup.geometry('300x150')
        popup.resizable(False, True)
        popup.grab_set()

        text = tk.Frame(popup)

        entry = tk.Entry(text, width="280", textvariable=image.name)
        btn01 = tk.Button(popup, text="Select image", command=self.choose_image)

        btn02 = tk.Button(popup, text="Confirm", command=partial(self.add_image, image, popup=popup, edit=edit))

        self.pack_all(text, entry, btn01, btn02)

    def choose_image(self):
        image_url = filedialog.askopenfile(filetypes=[('Image Files', ['.jpeg', '.jpg', '.png'])]).name


    def del_image(self):
        select = self.__images_listbox.curselection()
        del self.variables["images"][select[0]]

        for widget in self.__image__panel.values():
            widget.config(state=tk.DISABLED)

        self.reload_images()

    def duplicate_image(self):
        select = self.__images_listbox.curselection()
        if len(select) == 0: return
        image = self.variables["images"][select[0]]

        dupe = ImageW(self.__image__panel)
        dupe.name.set(image.name.get())
        dupe.x.set(image.x.get())
        dupe.y.set(image.y.get())
        dupe.width.set(image.width.get())
        dupe.height.set(image.height.get())

        self.add_image(dupe)

    def add_image(self, sentence, popup=None, edit=False):
        if not edit:
            self.variables["images"].append(sentence)
            self.__images_listbox.insert(self.variables["images"].index(sentence), sentence.name.get())
        else:
            self.reload_images()

        if popup is not None:
            popup.destroy()

    def reload_images(self):
        self.__images_listbox.delete(0, tk.END)

        for sentence in self.variables["images"]:
            self.__images_listbox.insert(self.variables["images"].index(sentence), sentence.name.get())


class ImageW:
    def __init__(self, panel):
        self.name = tk.StringVar(value="")
        self.panel = panel
        self.x = tk.StringVar(value=0)
        self.y = tk.StringVar(value=0)
        self.width = tk.StringVar(value=50)
        self.height = tk.StringVar(value=50)

        self.name.trace("w", partial(self.entry_test, self.name, 20))
        self.x.trace("w", partial(self.entry_test, self.x, 4, only_int=True))
        self.y.trace("w", partial(self.entry_test, self.y, 4, only_int=True))
        self.width.trace("w", partial(self.entry_test, self.width, 4, only_int=True))
        self.height.trace("w", partial(self.entry_test, self.height, 4, only_int=True))

    def position(self):
        return int(self.x.get()), int(self.y.get())

    def entry_test(self, text_var: tk.StringVar, limit: int, a, b, c, only_int=False):
        if only_int:
            text_var.set(to_only_int(text_var.get()))

        text_var.set(to_max_size(text_var.get(), limit))
