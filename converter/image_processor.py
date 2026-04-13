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
        super().__init__(input_path, output_path, overwrite=overwrite)
        self.quality = quality
        self.resize = resize
        self.grayscale = grayscale
        self.keep_aspect_ratio = keep_aspect_ratio
        self.optimize = optimize
        self.rotate = rotate
        self.delete = delete

    def convert(self):
        if self.input_ext == ".heic":
            try:
                from pillow_heif import register_heif_opener
                register_heif_opener()
            except ImportError:
                raise ImportError("Install 'pillow-heif' to process HEIC files (pip install pillow-heif).")
                
        if self.input_ext == ".raw":
            try:
                import rawpy
            except ImportError:
                raise ImportError("Install 'rawpy' to process RAW files (pip install rawpy).")
            with rawpy.imread(self.input_path) as raw:
                rgb = raw.postprocess()
                img = Image.fromarray(rgb)
        else:
            img = Image.open(self.input_path)

        if self.output_ext in [".jpg", ".jpeg"]:
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
