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
        if (
            self.output_ext in self.ext_docs and self.input_ext not in self.ext_docs
        ) or (self.input_ext in self.ext_docs and self.output_ext not in self.ext_docs):
            raise ValueError("This type of conversion is not available!")
        if (
            self.output_ext in self.ext_image and self.input_ext not in self.ext_image
        ) or (
            self.input_ext in self.ext_image and self.output_ext not in self.ext_image
        ):
            raise ValueError("This type of conversion is not available!")
        if (
            self.output_ext in self.ext_audio and self.input_ext not in self.ext_audio
        ) or (
            self.input_ext in self.ext_audio and self.output_ext not in self.ext_audio
        ):
            raise ValueError("This type of conversion is not available!")
        if (
            self.output_ext in self.ext_video and self.input_ext not in self.ext_video
        ) or (
            self.input_ext in self.ext_video and self.output_ext not in self.ext_video
        ):
            raise ValueError("This type of conversion is not available!")
        if (
            self.output_ext not in self.ext_docs
            and self.output_ext not in self.ext_image
            and self.output_ext not in self.ext_audio
            and self.output_ext not in self.ext_video
        ):
            raise ValueError("Wrong output file extenstion!")
        if (
            self.input_ext not in self.ext_docs
            and self.input_ext not in self.ext_image
            and self.input_ext not in self.ext_audio
            and self.input_ext not in self.ext_video
        ):
            raise ValueError("Wrong input file extension!")

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
