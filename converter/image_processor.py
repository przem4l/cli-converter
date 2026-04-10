import os
from PIL import Image
from utils.file_handler import FileHandler


class ImageConverter(FileHandler):
    def __init__(
        self,
        input_path,
        output_path,
        quality,
        resize,
        grayscale,
        keep_aspect_ratio,
        optimize,
        rotate,
        overwrite,
        delete,
    ):
        super().__init__(input_path, output_path)
        self.quality = quality
        self.resize = resize
        self.grayscale = grayscale
        self.keep_aspect_ratio = keep_aspect_ratio
        self.optimize = optimize
        self.rotate = rotate
        self.overwrite = overwrite
        self.delete = delete

    def convert(self):
        if os.path.exists(self.output_path) and not self.overwrite:
            print("Plik istnieje, pomijam...")
            return

        img = Image.open(self.input_path)
        if self.output_ext() in [".jpg", ".jpeg"]:
            img = img.convert("RGB")
        if self.grayscale:
            img = img.convert("L")
        if self.rotate != 0:
            img = img.rotate(self.rotate, expand=True)
        if self.resize and self.keep_aspect_ratio:
            img.thumbnail(self.resize)
        elif self.resize and not self.keep_aspect_ratio:
            img = img.resize(self.resize)
            
        img.save(self.output_path, quality=self.quality, optimize=self.optimize)
        if self.delete:
            os.remove(self.input_path)
