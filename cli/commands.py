import typer
from utils.file_handler import FileHandler

app = typer.Typer()

@app.command()
def convert(
    input_path: str = typer.Option(..., "--input", "-i"),
    output_path: str = typer.Option(..., "--output", "-o"),
):
  if not input_path.endswith((".jpg", ".png", ".webp")):
    raise typer.BadParameter("Unsupported input format")
  
  handler = FileHandler(input_path, output_path)