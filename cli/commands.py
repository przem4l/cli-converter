import typer
import os
from converter.image_processor import ImageConverter
from cli.display import progress_bar

app = typer.Typer()

def validate_hw(height, width):
    if height is None or width is None:
        return None
    if height <= 0 or width <= 0:
        raise Exception("Resolution must be a positive number!")
    return (width, height)

@app.command(help="Converts a single image to the designated format with optional transformations (resizing, rotation, etc.).")
def convert(
    input_path: str = typer.Option(..., "--input", "-i", help="Path to the input file."),
    output_path: str = typer.Option(..., "--output", "-o", help="Path to the output file."),
    quality: int = typer.Option(95, "--quality", "-q", help="Quality of the output image (0-100)."),
    height: int = typer.Option(None, "--height", "-h", help="New height of the image in pixels."),
    width: int = typer.Option(None, "--width", "-w", help="New width of the image in pixels."),
    grayscale: bool = typer.Option(False, "--grayscale", "-g", help="Convert the image to grayscale."),
    keep_aspect_ratio: bool = typer.Option(False, "--keep", "-k", help="Keep the original aspect ratio when resizing."),
    optimize: bool = typer.Option(False, "--optimize", "-O", help="Optimize the output file size."),
    rotate: int = typer.Option(0, "--rotate", "-r", help="Rotate the image by a given degree."),
    overwrite: bool = typer.Option(False, "--overwrite", "-v", help="Overwrite the output file if it already exists."),
    delete: bool = typer.Option(False, "--delete", "-d", help="Delete the input file after successful conversion."),
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
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
    typer.echo("The conversion has been completed")


@app.command(help="Batch conversion of multiple images from the specified directory. Processes formats like PNG, JPG, WEBP with a progress bar.")
def batch(
    input_dir: str = typer.Option(..., "--input", "-i", help="Input directory containing images."),
    output_dir: str = typer.Option(..., "--output", "-o", help="Output directory for the converted images."),
    quality: int = typer.Option(95, "--quality", "-q", help="Quality of the output images (0-100)."),
    height: int = typer.Option(None, "--height", "-h", help="New target height of the images in pixels."),
    width: int = typer.Option(None, "--width", "-w", help="New target width of the images in pixels."),
    grayscale: bool = typer.Option(False, "--grayscale", "-g", help="Apply grayscale filter to each image."),
    keep_aspect_ratio: bool = typer.Option(False, "--keep", "-k", help="Keep the original aspect ratio of the images when resizing."),
    optimize: bool = typer.Option(False, "--optimize", "-O", help="Optimize the output files size."),
    rotate: int = typer.Option(0, "--rotate", "-r", help="Rotate the images by a given degree."),
    overwrite: bool = typer.Option(False, "--overwrite", "-v", help="Overwrite existing output files."),
    delete: bool = typer.Option(False, "--delete", "-d", help="Clean the input directory successively after each conversion."),
):
    resize = validate_hw(height, width)
    files = [
        f
        for f in os.listdir(input_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".heic", ".raw"))
    ]

    for file in progress_bar(files, desc="Converting"):
        in_path = os.path.join(input_dir, file)
        name = file.split(".", 1)[0]
        out_path = os.path.join(output_dir, f"{name}.jpg")

        try:
            converter = ImageConverter(
                input_path=in_path,
                output_path=out_path,
                quality=quality,
                resize=resize,
                grayscale=grayscale,
                keep_aspect_ratio=keep_aspect_ratio,
                optimize=optimize,
                rotate=rotate,
                overwrite=overwrite,
                delete=delete,
            )
            converter.convert()
        except Exception as e:
            typer.echo(f"Failed conversion: {file} -> {e}")
    typer.echo("The conversion has been completed")
