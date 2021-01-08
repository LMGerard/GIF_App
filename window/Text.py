import tkinter as tk
from Frame import Frame
from functools import partial
from PIL import ImageColor, ImageFont
from functions import is_color, is_font_family, to_max_size, to_only_int


class Text(Frame):
    __texts_listbox = None
    __sentence__panel = {}

    def __init__(self, window, tool, variables: dict):
        super().__init__(window, tool, variables, btntxt="Text options")
        self.sentences = []

    def window_options(self):
        self.variables["sentences"] = []

        label = tk.Label(self.options_frame, text="Sentence")

        options = tk.Frame(self.options_frame)

        btn01 = tk.Button(options, text="new", command=self.ask_text)
        btn02 = tk.Button(options, text="dup", command=self.duplicate_text)

        btn01.grid(column=0, row=0)
        btn02.grid(column=1, row=0)

        # sentence listbox
        text_frame = tk.Frame(self.options_frame)

        self.__texts_listbox = tk.Listbox(text_frame, selectmode=tk.SINGLE)
        self.__texts_listbox.bind('<<ListboxSelect>>', self.on_change_sentence_selection)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.__texts_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.__texts_listbox.yview)

        # sentence panel
        sentence_panel = tk.Frame(self.options_frame, highlightbackground="black", highlightthickness=1)
        coords = tk.Frame(sentence_panel)

        self.__sentence__panel = {
            "x": tk.Entry(coords, state=tk.DISABLED, width=3),
            "y": tk.Entry(coords, state=tk.DISABLED, width=3)
        }
        tk.Label(coords, text="Position").grid(column=0, columnspan=4, row=0)
        tk.Label(coords, text="x:").grid(column=0, row=1)
        self.__sentence__panel["x"].grid(column=1, row=1)
        tk.Label(coords, text="y:").grid(column=2, row=1)
        self.__sentence__panel["y"].grid(column=3, row=1)

        font = tk.Frame(sentence_panel)
        self.__sentence__panel["color"] = tk.Entry(font, state=tk.DISABLED)
        self.__sentence__panel["font_size"] = tk.Entry(font, state=tk.DISABLED)
        self.__sentence__panel["font_family"] = tk.Entry(font, state=tk.DISABLED)
        self.__sentence__panel["delete"] = tk.Button(font, state=tk.DISABLED, text="D", command=self.del_text)
        self.__sentence__panel["edit"] = tk.Button(font, state=tk.DISABLED, text="E", command=partial(self.ask_text, edit=True))

        tk.Label(font, text="Font").grid(column=0, columnspan=2, row=0)
        tk.Label(font, text="color:").grid(column=0, row=1)
        self.__sentence__panel["color"].grid(column=1, row=1)
        tk.Label(font, text="size:").grid(column=0, row=2)
        self.__sentence__panel["font_size"].grid(column=1, row=2)
        tk.Label(font, text="family:").grid(column=0, row=3)
        self.__sentence__panel["font_family"].grid(column=1, row=3)
        self.__sentence__panel["delete"].grid(column=0, row=4)
        self.__sentence__panel["edit"].grid(column=1, row=4)

        self.pack_all(label, options, self.__texts_listbox, text_frame, sentence_panel, coords, font)

    def on_change_sentence_selection(self, event):
        select = self.__texts_listbox.curselection()
        if len(select) == 0: return

        for widget in self.__sentence__panel.values():
            widget.config(state=tk.NORMAL)

        sentence = self.variables["sentences"][select[0]]
        self.__sentence__panel["x"].config(textvariable=sentence.x)
        self.__sentence__panel["y"].config(textvariable=sentence.y)
        self.__sentence__panel["color"].config(textvariable=sentence.color)
        self.__sentence__panel["font_size"].config(textvariable=sentence.font_size)
        self.__sentence__panel["font_family"].config(textvariable=sentence.font_family)

        sentence.entry_test(sentence.color, 20, None, None, None, color=True)
        sentence.entry_test(sentence.font_size, 4, None, None, None, only_int=True)
        sentence.entry_test(sentence.font_family, 100, None, None, None, font=True)

    def ask_text(self, edit=False):
        if edit:
            sentence = self.variables["sentences"][self.__texts_listbox.curselection()[0]]
        else:
            sentence = Sentence(self.__sentence__panel)

        popup = tk.Toplevel()
        popup.geometry('300x150')
        popup.resizable(False, True)
        popup.grab_set()

        text = tk.Frame(popup)

        entry = tk.Entry(text, width="280", textvariable=sentence.text)

        btn = tk.Button(popup, text="Confirm", command=partial(self.add_text, sentence, popup=popup, edit=edit))

        self.pack_all(text, entry, btn)

    def del_text(self):
        select = self.__texts_listbox.curselection()
        del self.variables["sentences"][select[0]]

        for widget in self.__sentence__panel.values():
            widget.config(state=tk.DISABLED)

        self.reload_sentences()

    def duplicate_text(self):
        select = self.__texts_listbox.curselection()
        if len(select) == 0: return
        sentence = self.variables["sentences"][select[0]]

        dupe = Sentence(self.__sentence__panel)
        dupe.text.set(sentence.text.get())
        dupe.x.set(sentence.x.get())
        dupe.y.set(sentence.y.get())
        dupe.color.set(sentence.color.get())
        dupe.font_size.set(sentence.font_size.get())
        dupe.font_family.set(sentence.font_family.get())

        self.add_text(dupe)

    def add_text(self, sentence, popup=None, edit=False):
        if not edit:
            self.variables["sentences"].append(sentence)
            self.__texts_listbox.insert(self.variables["sentences"].index(sentence), sentence.text.get())
        else:
            self.reload_sentences()

        if popup is not None:
            popup.destroy()

    def reload_sentences(self):
        self.__texts_listbox.delete(0, tk.END)

        for sentence in self.variables["sentences"]:
            self.__texts_listbox.insert(self.variables["sentences"].index(sentence), sentence.text.get())


class Sentence:
    def __init__(self, panel):
        self.text = tk.StringVar(value="")
        self.panel = panel
        self.x = tk.StringVar(value=0)
        self.y = tk.StringVar(value=0)
        self.color = tk.StringVar(value="white")
        self.font_size = tk.StringVar(value=50)
        self.font_family = tk.StringVar(value="arial")

        self.text.trace("w", partial(self.entry_test, self.text, 20))
        self.x.trace("w", partial(self.entry_test, self.x, 4, only_int=True))
        self.y.trace("w", partial(self.entry_test, self.y, 4, only_int=True))
        self.color.trace("w", partial(self.entry_test, self.color, 20, color=True))
        self.font_size.trace("w", partial(self.entry_test, self.font_size, 4, only_int=True))
        self.font_family.trace("w", partial(self.entry_test, self.font_family, 100, font=True))

    def position(self):
        return int(self.x.get()), int(self.y.get())

    def entry_test(self, text_var: tk.StringVar, limit: int, a, b, c, only_int=False, color=False, font=False):
        if font:
            if is_font_family(self.font_family.get()):
                self.panel["font_family"].config(fg="black")
            else:
                self.panel["font_family"].config(fg="red")
        if color and len(text_var.get()) > 0:
            if is_color(text_var.get()):
                self.panel["color"].config(fg="black")
            else:
                self.panel["color"].config(fg="red")

        if only_int:
            text_var.set(to_only_int(text_var.get()))

        text_var.set(to_max_size(text_var.get(), limit))
