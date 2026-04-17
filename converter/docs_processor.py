import os
from utils.file_handler import FileHandler


class DocsConverter(FileHandler):
    def __init__(self, input_path, output_path, overwrite=False, **kwargs):
        super().__init__(input_path, output_path, overwrite=overwrite)

    def convert(self):
        self.validate_libraries()
        if self.input_ext == ".pdf":
            if self.output_ext == ".txt":
                self.pdf_to_txt()
            else:
                raise Exception("PDF input is only supported for conversion to TXT.")
        else:
            self.pandoc_convert()

    def pdf_to_txt(self):
        import fitz

        doc = fitz.open(self.input_path)
        text = ""
        for page in doc:
            text += page.get_text()
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(text)

    def pandoc_convert(self):
        import pypandoc

        out_format = (
            "plain" if self.output_ext == ".txt" else self.output_ext.strip(".")
        )
        in_format = (
            "markdown" if self.input_ext == ".txt" else self.input_ext.strip(".")
        )
        try:
            pypandoc.convert_file(
                self.input_path,
                out_format,
                format=in_format,
                outputfile=self.output_path,
            )
        except RuntimeError as e:
            error_message = str(e).lower()
            if (
                "pdflatex" in error_message
                or "pdf-engine" in error_message
                or "pdf engine" in error_message
            ):
                raise Exception(
                    "PDF export requires a PDF engine (e.g. MiKTeX, wkhtmltopdf) installed on your system."
                )
            raise e

    def validate_libraries(self):
        try:
            import pypandoc
        except ImportError:
            raise ImportError("Install pypandoc to process documents (pip install pypandoc).")

        try:
            import fitz
        except ImportError:
            raise ImportError("Install pymupdf to process PDFs (pip install pymupdf).")
