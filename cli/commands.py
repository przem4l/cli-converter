import typer
import os
from converter.image_processor import ImageConverter
from cli.display import progress_bar

app = typer.Typer()


@app.command()
def convert(
    input_path: str = typer.Option(..., "--input", "-i"),
    output_path: str = typer.Option(..., "--output", "-o"),
    quality: int = typer.Option(..., "--quality", "-q"),
    grayscale: bool = typer.Option(..., "--grayscale", "-g"),
):
    try:
        converter = ImageConverter(input_path, output_path, quality, grayscale)
        converter.process()
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
    typer.echo("The conversion has been completed")


@app.command()
def batch(
    input_dir: str = typer.Option(..., "--input", "-i"),
    output_dir: str = typer.Option(..., "--output", "-o"),
    quality: int = typer.Option(..., "--quality", "-q"),
    grayscale: bool = typer.Option(..., "--grayscale", "-g"),
):
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
            grayscale=grayscale,
        )
        converter.process()
    except Exception as e:
        typer.echo(f"Failed conversion: {file} -> {e}")
    typer.echo("The conversion has been completed")
