import typer
import os
from converter.image_processor import ImageConverter
from converter.docs_processor import DocsConverter
from cli.display import progress_bar

app = typer.Typer(help="A versatile File Converter CLI for Images and Documents.")

image_app = typer.Typer(
    help="Commands for image processing (JPG/JPEG, PNG, WEBP, HEIC, RAW)."
)
doc_app = typer.Typer(help="Commands for document processing (PDF, DOCX, TXT, ODT).")

app.add_typer(image_app, name="image")
app.add_typer(doc_app, name="doc")


def validate_hw(height: int, width: int):
    if height is None or width is None:
        return None
    if height <= 0 or width <= 0:
        raise Exception("Resolution must be a positive number!")
    return (width, height)

def prepare_batch(input_dir: str, output_dir: str, valid_ext: tuple):
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_ext)]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return files

def get_output_path(file: str, output_dir: str, target_format: str = None) -> str:
    if target_format:
        filename = os.path.splitext(file)[0] + "." + target_format.strip(".")
    else:
        filename = file
    return os.path.join(output_dir, filename)


@image_app.command(
    "convert", help="Convert a single image with optional filters and transformations."
)
def convert_image(
    input_path: str = typer.Option(
        ..., "--input", "-i", help="Path to the input image file."
    ),
    output_path: str = typer.Option(
        ..., "--output", "-o", help="Path where the output image will be saved."
    ),
    quality: int = typer.Option(
        95, "--quality", "-q", help="Output image quality (0-100)."
    ),
    height: int = typer.Option(None, "--height", "-h", help="Target height in pixels."),
    width: int = typer.Option(None, "--width", "-w", help="Target width in pixels."),
    grayscale: bool = typer.Option(
        False, "--grayscale", "-g", help="Convert image to grayscale."
    ),
    keep_aspect_ratio: bool = typer.Option(
        False, "--keep", "-k", help="Maintain original aspect ratio during resize."
    ),
    optimize: bool = typer.Option(
        False, "--optimize", "-O", help="Optimize output file size."
    ),
    rotate: int = typer.Option(
        0, "--rotate", "-r", help="Degrees to rotate the image."
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite the output file if it exists."
    ),
    delete: bool = typer.Option(
        False, "--delete", "-d", help="Delete the source file after conversion."
    ),
):
    resize = validate_hw(height, width)
    try:
        converter = ImageConverter(
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
        )
        converter.convert()
        typer.echo(f"Success: Image saved to {output_path}")
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@image_app.command("batch", help="Batch convert multiple images within a directory.")
def batch_images(
    input_dir: str = typer.Option(
        ..., "--input", "-i", help="Directory containing source images."
    ),
    output_dir: str = typer.Option(
        ..., "--output", "-o", help="Directory to save converted images."
    ),
    quality: int = typer.Option(
        95, "--quality", "-q", help="Output quality for all images."
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite existing files in output directory."
    ),
    format: str = typer.Option(
        None, "--format", "-f", help="Docelowy format np. png, webp, jpg"
    ),
):
    valid_ext = (".png", ".jpg", ".jpeg", ".webp", ".heic", ".raw")
    files = prepare_batch(input_dir, output_dir, valid_ext)

    for file in progress_bar(files, desc="Converting"):
        in_path = os.path.join(input_dir, file)
        out_path = get_output_path(file, output_dir, format)

        try:
            converter = ImageConverter(
                in_path,
                out_path,
                quality,
                None,
                False,
                False,
                False,
                0,
                overwrite,
                False,
            )
            converter.convert()
        except Exception as e:
            typer.echo(f"Failed to process {file}: {e}")

    typer.echo("Batch conversion completed.")


@doc_app.command(
    "convert", help="Convert document formats (e.g., PDF to TXT, DOCX to PDF)."
)
def convert_document(
    input_path: str = typer.Option(..., "--input", "-i", help="Source document path."),
    output_path: str = typer.Option(
        ..., "--output", "-o", help="Target document path."
    ),
):
    try:
        converter = DocsConverter(input_path, output_path)
        converter.convert()
        typer.echo(f"Success: Document converted to {output_path}")
    except Exception as e:
        typer.echo(f"Document Error: {e}")
        raise typer.Exit(code=1)


@doc_app.command("batch", help="Batch convert multiple documents within a directory.")
def batch_documents(
    input_dir: str = typer.Option(
        ..., "--input", "-i", help="Directory containing source documents."
    ),
    output_dir: str = typer.Option(
        ..., "--output", "-o", help="Directory to save converted documents."
    ),
    format: str = typer.Option(
        None, "--format", "-f", help="Target format e.g. txt, pdf"
    ),
):
    valid_ext = (".pdf", ".docx", ".txt", ".odt")
    files = prepare_batch(input_dir, output_dir, valid_ext)

    for file in progress_bar(files, desc="Converting"):
        in_path = os.path.join(input_dir, file)
        out_path = get_output_path(file, output_dir, format)

        try:
            converter = DocsConverter(in_path, out_path)
            converter.convert()
        except Exception as e:
            typer.echo(f"Failed to process {file}: {e}")
            
    typer.echo("Batch conversion completed.")
