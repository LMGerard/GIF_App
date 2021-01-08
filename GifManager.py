from PIL import Image, ImageColor, ImageDraw, ImageFont
import tempfile
import os


class GifManager:
    def __init__(self, variables):
        self.variables = variables
        self.tempImages = []

    def create_gif(self):
        background_color = self.to_color(self.variables["background_color"].get(), (0, 0, 0))

        image = Image.new(size=(500, 500), mode="RGB", color=background_color)

        # Creating the images
        self.images = [image]
        lengths = list(map(lambda x: len(x.text.get()), self.variables["sentences"]))

        for i in range(max([0] + lengths)):
            image = image.copy()
            draw = ImageDraw.Draw(image)
            for sentence in self.variables["sentences"]:
                if len(sentence.text.get()) <= i:
                    continue
                font_color = self.to_color(sentence.color.get(), (255, 255, 255))

                font = self.to_font(sentence.font_family.get(), sentence.font_size.get())

                draw.text((int(sentence.x.get()), int(sentence.y.get())),
                          sentence.text.get()[: i + 1],
                          font_color, font=font)
            self.images.append(image)

    def save_gif(self, temp=False):
        loop = self.variables["infinite_loop"].get()
        directory = self.variables["dir_path"].get() if len(
            self.variables["dir_path"].get()) > 0 else os.path.expanduser("~\\Desktop")
        file_name = self.variables["file_name"].get() if len(self.variables["file_name"].get()) > 0 else "output_gif"

        file_path = ""
        if temp:
            self.tempImages = []
            for image in self.images:
                tempImage = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
                file_path = tempImage.name
                image.save(file_path)
                self.tempImages.append(tempImage)
        else:
            file_path = os.path.join(directory, file_name + ".gif")

            # Saving the GIF
            if len(self.variables["duration"].get()) > 0:
                duration = int(self.variables["duration"].get())
            else:
                duration = 100
            try:
                self.images[0].save(file_path, save_all=True, append_images=self.images[1:],
                                    loop=(loop != 1), duration=duration)
            except PermissionError:
                pass

    @staticmethod
    def to_color(color: str, default: tuple):
        if len(color) == 0:
            return default

        try:
            color = tuple(map(int, color.split()))
            if len(color) < 3 or max(color) > 255:
                return default
        except ValueError:
            try:
                color = ImageColor.getrgb("".join(color.split()))
            except:
                return default
        return color

    @staticmethod
    def to_font(font: str, size: str):
        if len(size) == 0:
            size = 50
        else:
            size = int(size)

        try:
            return ImageFont.truetype(font + ".ttf", size)
        except OSError:
            return ImageFont.truetype("arial.ttf", size)
