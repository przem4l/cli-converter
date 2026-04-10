import typer
import os
from converter.image_processor import ImageConverter
from cli.display import progress_bar

app = typer.Typer()

def validate_hw(height, width):
    if height <= 0 or width <= 0:
        raise Exception("Resolution must be a positive number!")
    return (height, width)

@app.command()
def convert(
    input_path: str = typer.Option(..., "--input", "-i"),
    output_path: str = typer.Option(..., "--output", "-o"),
    quality: int = typer.Option(95, "--quality", "-q"),
    height: int = typer.Option(..., "--height", "-h"),
    width: int = typer.Option(..., "--width", "-w"),
    grayscale: bool = typer.Option(False, "--grayscale", "-g"),
    keep_aspect_ratio: bool = typer.Option(False, "--keep", "-k"),
    optimize: bool = typer.Option(False, "--optimize", "-o"),
    rotate: int = typer.Option(0, "--rotate", "-r"),
    overwrite: bool = typer.Option(False, "--overwrite", "-v"),
    delete: bool = typer.Option(False, "--delete", "-d"),
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
        converter.process()
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
    typer.echo("The conversion has been completed")


@app.command()
def batch(
    input_dir: str = typer.Option(..., "--input", "-i"),
    output_dir: str = typer.Option(..., "--output", "-o"),
    quality: int = typer.Option(95, "--quality", "-q"),
    height: int = typer.Option(..., "--height", "-h"),
    width: int = typer.Option(..., "--width", "-w"),
    grayscale: bool = typer.Option(False, "--grayscale", "-g"),
    keep_aspect_ratio: bool = typer.Option(False, "--keep", "-k"),
    optimize: bool = typer.Option(False, "--optimize", "-o"),
    rotate: int = typer.Option(0, "--rotate", "-r"),
    overwrite: bool = typer.Option(False, "--overwrite", "-v"),
    delete: bool = typer.Option(False, "--delete", "-d"),
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
        converter.process()
    except Exception as e:
        typer.echo(f"Failed conversion: {file} -> {e}")
    typer.echo("The conversion has been completed")
