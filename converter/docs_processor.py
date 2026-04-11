import os, pypandoc, fitz
from utils.file_handler import FileHandler


class DocsConverter(FileHandler):
    def __init__(self, input_path, output_path):
        super().__init__(input_path, output_path)

    def convert(self):
        if self.input_ext == ".pdf" and self.output_ext == ".txt":
            self.pdf_to_txt()
        else:
            self.pandoc_convert()

    def pdf_to_txt(self):
        doc = fitz.open(self.input_path)
        text = ""
        for page in doc:
            text += page.get_text()
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(text)

    def pandoc_convert(self):
        pypandoc.convert_file(
            self.input_path, self.output_ext.strip("."), outputfile=self.output_path
        )

    def validate_libraries(self):
        try:
            import pypandoc
        except ImportError:
            print("Install pypandoc")

        try:
            import fitz
        except ImportError:
            print("Install pymupdf")
