import os
from pathlib import Path


class FileHandler:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.ext_docs = [".docx", ".pdf", ".txt", ".odt"]
        self.ext_image = [".png", ".jpg", ".jpeg", ".webp", ".heic", ".raw"]
        self.validate()

    def validate(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError("Input file does not exist!")
        if (self.output_ext in self.ext_docs and self.input_ext not in self.ext_docs) or (self.input_ext in self.ext_docs and self.output_ext not in self.ext_docs):
            raise Exception("This type of conversion is not avaliable!")
        if (self.output_ext in self.ext_image and self.input_ext not in self.ext_image) or (self.input_ext in self.ext_image and self.output_ext not in self.ext_image):
            raise Exception("This type of conversion is not avaliable!")
        if self.output_ext not in self.ext_docs or self.output_ext not in self.ext_image:
            raise Exception("Wrong output file extenstion!")
        if self.input_ext not in self.ext_docs or self.output_ext not in self.ext_image:
            raise Exception("Wrong input file extension!")
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
