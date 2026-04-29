import os
from pathlib import Path


class FileHandler:
    EXT_DOCS = (".docx", ".pdf", ".txt", ".odt")
    EXT_IMAGE = (".png", ".jpg", ".jpeg", ".webp", ".heic", ".raw")
    EXT_AUDIO = (".mp3", ".wav", ".ogg", ".flac")
    EXT_VIDEO = (".mp4", ".avi", ".mkv", ".mov")

    def __init__(self, input_path, output_path, overwrite=False):
        self.input_path = input_path
        self.output_path = output_path
        self.overwrite = overwrite
        self.ext_docs = self.EXT_DOCS
        self.ext_image = self.EXT_IMAGE
        self.ext_audio = self.EXT_AUDIO
        self.ext_video = self.EXT_VIDEO
        self.validate()

    def validate(self):
        input_abs = os.path.abspath(self.input_path)
        output_abs = os.path.abspath(self.output_path)

        if not os.path.exists(self.input_path):
            raise FileNotFoundError("Input file does not exist!")

        if input_abs == output_abs and not self.overwrite:
            raise FileExistsError(
                "Input and output paths are the exact same! Use --overwrite to attempt in-place modification."
            )

        if (
            os.path.exists(output_abs)
            and input_abs != output_abs
            and not self.overwrite
        ):
            raise FileExistsError(
                f"Output file {self.output_path} already exists! Use --overwrite to modify it."
            )

        groups = [self.EXT_DOCS, self.EXT_IMAGE, self.EXT_AUDIO, self.EXT_VIDEO]
        
        # Determine current group
        input_group = next((g for g in groups if self.input_ext in g), None)
        output_group = next((g for g in groups if self.output_ext in g), None)

        if not input_group:
            raise ValueError(f"Input extension '{self.input_ext}' is not supported.")
        if not output_group:
            raise ValueError(f"Output extension '{self.output_ext}' is not supported.")
        if input_group != output_group:
            raise ValueError(f"Conversion from {self.input_ext} to {self.output_ext} is not allowed (cross-type).")
        
    def get_size(self, path: str):
        return os.path.getsize(path)
    
    def convert_to_megabytes(self, size_bytes: int):
        return round(size_bytes / (1024 * 1024), 2)
    
    def get_savings_percent(self, before: int, after: int):
        if before == 0:
            return 0.0
        return round((1 - (after / before)) * 100, 2)

    @property
    def input_ext(self):
        return Path(self.input_path).suffix.lower()

    @property
    def output_ext(self):
        return Path(self.output_path).suffix.lower()

    @property
    def input_name(self):
        return Path(self.input_path).stem

    @property
    def output_name(self):
        return Path(self.output_path).stem
