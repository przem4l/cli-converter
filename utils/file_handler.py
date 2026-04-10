import os
from pathlib import Path

class FileHandler:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.validate()

    def validate(self):
        for field in ["input_path", "output_path"]:
            value = getattr(self, field)
            if not isinstance(value, str):
                raise TypeError(f"{field} must be a string!")
            if not value.strip():
                raise ValueError(f"{field} must be a non-empty string!")
        if not os.path.exists(self.input_path):
            raise FileNotFoundError("Input file does not exist!")

    def mkdir(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def input_ext(self):
        return Path(self.input_path).suffix.lower()

    def output_ext(self):
        return Path(self.output_path).suffix.lower()

    def input_name(self):
        return Path(self.input_path).stem