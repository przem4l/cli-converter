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
    ):
        super().__init__(input_path, output_path)
        self.quality = quality
        self.resize = resize
        self.grayscale = grayscale
        self.keep_aspect_ratio = keep_aspect_ratio
        self.optimize = optimize
        self.rotate = rotate
        self.overwrite = overwrite

    def convert(self):
        img = Image.open(self.input_path)
        if self.output_ext == "JPEG":
            img = img.convert("RGB")
        img.resize(self.resize)
        img.save(self.output_name, self.input_ext)
