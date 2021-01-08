import tkinter as tk
from PIL import ImageColor, ImageFont
import re


def is_color(color: str):
    try:
        color = tuple(map(int, color.split()))
        if len(color) < 3 or max(color) > 255:
            return False
    except ValueError:
        try:
            color = ImageColor.getrgb("".join(color.split()))
        except:
            return False
    return color


def is_font_family(font_family: str):
    try:
        font = ImageFont.truetype(font_family + ".ttf", 1)
    except:
        return False
    return True


def to_max_size(text: str, size: int):
    return "".join(text[:size])


def to_only_int(text: str):
    return "".join(re.findall("[0-9]*", text))
