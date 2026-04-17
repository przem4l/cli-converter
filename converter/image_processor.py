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
            width, height = self.resize
            if (width is not None and width <= 0) or (height is not None and height <= 0):
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
            w, h = self.resize
            if w is None or h is None:
                orig_w, orig_h = img.size
                if w is None:
                    w = int(orig_w * (h / orig_h))
                else:
                    h = int(orig_h * (w / orig_w))
            img.thumbnail((w, h))
        elif self.resize and not self.keep_aspect_ratio:
            w, h = self.resize
            if w is None or h is None:
                orig_w, orig_h = img.size
                w = w or orig_w
                h = h or orig_h
            img = img.resize((w, h))

        img.save(self.output_path, quality=self.quality, optimize=self.optimize)
        if self.delete:
            os.remove(self.input_path)
