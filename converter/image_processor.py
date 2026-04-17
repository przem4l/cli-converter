import os
from utils.file_handler import FileHandler


class ImageConverter(FileHandler):
    def __init__(
        self,
        input_path,
        output_path,
        quality=95,
        resize=None,
        grayscale=False,
        keep_aspect_ratio=False,
        optimize=False,
        rotate=0,
        overwrite=False,
        delete=False,
        **kwargs,
    ):
        super().__init__(input_path, output_path, overwrite=overwrite)
        self.quality = quality
        self.resize = resize
        self.grayscale = grayscale
        self.keep_aspect_ratio = keep_aspect_ratio
        self.optimize = optimize
        self.rotate = rotate
        self.delete = delete
        self.validate_values()

    def validate_values(self):
        if self.quality < 0 or self.quality > 100:
            raise ValueError("Quality must be in range [0, 100]")
        if self.rotate < -360 or self.rotate > 360:
            raise ValueError("Rotate must be in range [-360, 360]")
        if self.resize is not None:
            if not isinstance(self.resize, tuple) or len(self.resize) != 2:
                raise ValueError("Resize must be a tuple of (width, height)")
            if self.resize[0] <= 0 or self.resize[1] <= 0:
                raise ValueError("Resize dimensions must be positive integers")

    def convert(self):
        try:
            from PIL import Image
        except ImportError:
            raise ImportError("Install Pillow to process image files (pip install Pillow).")

        if self.input_ext == ".heic":
            try:
                from pillow_heif import register_heif_opener

                register_heif_opener()
            except ImportError:
                raise ImportError(
                    "Install 'pillow-heif' to process HEIC files (pip install pillow-heif)."
                )

        if self.input_ext == ".raw":
            try:
                import rawpy
            except ImportError:
                raise ImportError(
                    "Install 'rawpy' to process RAW files (pip install rawpy)."
                )
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
