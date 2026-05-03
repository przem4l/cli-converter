import shutil
from rich.console import Console

def check_external_dependencies():
    console = Console()
    if not shutil.which("ffmpeg") and not shutil.which("avconv"):
        console.print("[bold yellow]Warning: FFmpeg is missing! Audio and video conversions will fail. Please install FFmpeg and add it to your system PATH.[/bold yellow]")

check_external_dependencies()
