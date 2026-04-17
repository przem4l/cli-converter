import typer
import os
from converter.image_processor import ImageConverter
from converter.docs_processor import DocsConverter
from converter.audio_processor import AudioConverter
from converter.video_processor import VideoConverter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from utils.file_handler import FileHandler
from cli.display import progress_bar

console = Console()

app = typer.Typer(
    help="A versatile File Converter CLI for Images, Documents and Audio."
)

image_app = typer.Typer(
    help="Commands for image processing (JPG/JPEG, PNG, WEBP, HEIC, RAW)."
)
doc_app = typer.Typer(help="Commands for document processing (PDF, DOCX, TXT, ODT).")
audio_app = typer.Typer(help="Commands for audio processing (MP3, WAV, OGG, FLAC)")
video_app = typer.Typer(help="Commands for video processing (MP4, AVI, MKV, MOV).")

app.add_typer(image_app, name="image")
app.add_typer(doc_app, name="doc")
app.add_typer(audio_app, name="audio")
app.add_typer(video_app, name="video")


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


def run_batch_conversion(
    input_dir, output_dir, valid_ext, converter_class, format, overwrite, **kwargs
):
    files = prepare_batch(input_dir, output_dir, valid_ext)

    for file in progress_bar(files, desc="Converting"):
        in_path = os.path.join(input_dir, file)
        out_path = get_output_path(file, output_dir, format)

        try:
            converter = converter_class(
                in_path, out_path, overwrite=overwrite, **kwargs
            )
            converter.convert()
        except Exception as e:
            typer.echo(f"Failed to process {file}: {e}")

    typer.echo("Batch conversion completed.")


@app.command("interactive", help="Enter interactive mode.")
def interactive_mode():
    console.print(
        Panel("[bold cyan]CLI Converter - Interactive Mode[/bold cyan]", expand=False)
    )

    table = Table(show_header=False, box=None)
    table.add_row("[1]", "Image Conversion")
    table.add_row("[2]", "Document Conversion")
    table.add_row("[3]", "Audio Conversion")
    table.add_row("[4]", "Video Conversion")
    table.add_row("[q]", "Quit")
    console.print(table)

    choice = typer.prompt("Choose an option", default="1")

    if choice == "q":
        raise typer.Exit()

    if choice not in ["1", "2", "3", "4"]:
        console.print("[bold red]Invalid option![/bold red]")
        return

    input_path = typer.prompt("Enter input file or directory path", default=".")

    if not os.path.exists(input_path):
        console.print(
            f"[bold red]Error: Path '{input_path}' does not exist![/bold red]"
        )
        return

    output_path = typer.prompt("Enter output path", default="output")
    target_format = (
        typer.prompt("Enter target format (e.g., png, pdf, mp3, mp4)").strip().lower()
    )

    if not target_format:
        console.print("[bold red]Error: Target format cannot be empty![/bold red]")
        return

    overwrite = typer.confirm("Overwrite existing files?", default=False)

    try:
        if choice == "1":
            quality = typer.prompt("Quality (0-100)", type=int, default=95)
            if not (0 <= quality <= 100):
                console.print("[bold red]Quality must be between 0 and 100![/bold red]")
                return

            grayscale = typer.confirm("Convert to grayscale?", default=False)

            if os.path.isdir(input_path):
                run_batch_conversion(
                    input_path,
                    output_path,
                    (".jpg", ".jpeg", ".png", ".webp", ".heic"),
                    ImageConverter,
                    target_format,
                    overwrite,
                    quality=quality,
                    grayscale=grayscale,
                )
            else:
                out_path = get_output_path(os.path.basename(input_path), output_path, target_format)
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                converter = ImageConverter(
                    input_path,
                    out_path,
                    overwrite=overwrite,
                    quality=quality,
                    grayscale=grayscale,
                )
                converter.convert()

        elif choice == "2":
            if os.path.isdir(input_path):
                run_batch_conversion(
                    input_path,
                    output_path,
                    (".pdf", ".docx", ".txt", ".odt"),
                    DocsConverter,
                    target_format,
                    overwrite,
                )
            else:
                out_path = get_output_path(os.path.basename(input_path), output_path, target_format)
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                converter = DocsConverter(
                    input_path, out_path, overwrite=overwrite
                )
                converter.convert()

        elif choice == "3":
            bitrate = typer.prompt("Audio bitrate (e.g., 192k)", default="192k")
            if os.path.isdir(input_path):
                run_batch_conversion(
                    input_path,
                    output_path,
                    (".mp3", ".wav", ".ogg", ".flac"),
                    AudioConverter,
                    target_format,
                    overwrite,
                    bitrate=bitrate,
                )
            else:
                out_path = get_output_path(os.path.basename(input_path), output_path, target_format)
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                converter = AudioConverter(
                    input_path,
                    out_path,
                    overwrite=overwrite,
                    bitrate=bitrate,
                )
                converter.convert()

        elif choice == "4":
            if os.path.isdir(input_path):
                run_batch_conversion(
                    input_path,
                    output_path,
                    (".mp4", ".avi", ".mkv", ".mov"),
                    VideoConverter,
                    target_format,
                    overwrite,
                )
            else:
                out_path = get_output_path(os.path.basename(input_path), output_path, target_format)
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                converter = VideoConverter(
                    input_path, out_path, overwrite=overwrite
                )
                converter.convert()

        console.print("[bold green]Operation finished successfully![/bold green]")

    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")


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
        95, "--quality", "-q", help="Output image quality. [0, 100]"
    ),
    height: int = typer.Option(
        None, "--height", "-h", help="Target height in pixels. (0, ∞)"
    ),
    width: int = typer.Option(
        None, "--width", "-w", help="Target width in pixels. (0, ∞)"
    ),
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
        0, "--rotate", "-r", help="Degrees to rotate the image. [-360, 360]"
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
        95, "--quality", "-q", help="Output quality for all images. [0, 100]"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite existing files in output directory."
    ),
    format: str = typer.Option(
        None,
        "--format",
        "-f",
        help="Target image format. {png, jpg, jpeg, webp, heic, raw}",
    ),
):
    run_batch_conversion(
        input_dir,
        output_dir,
        FileHandler.EXT_IMAGE,
        ImageConverter,
        format,
        overwrite,
        quality=quality,
        resize=None,
        grayscale=False,
        keep_aspect_ratio=False,
        optimize=False,
        rotate=0,
        delete=False,
    )


@doc_app.command(
    "convert", help="Convert document formats (e.g., PDF to TXT, DOCX to PDF)."
)
def convert_document(
    input_path: str = typer.Option(..., "--input", "-i", help="Source document path."),
    output_path: str = typer.Option(
        ..., "--output", "-o", help="Target document path."
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite the output file if it exists."
    ),
):
    try:
        converter = DocsConverter(input_path, output_path, overwrite)
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
        None, "--format", "-f", help="Target document format. {pdf, docx, txt, odt}"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite existing files in output directory."
    ),
):
    run_batch_conversion(
        input_dir, output_dir, FileHandler.EXT_DOCS, DocsConverter, format, overwrite
    )


@audio_app.command(
    "convert", help="Convert audio formats (e.g., MP3 to WAV, OGG to FLAC)."
)
def convert_audio(
    input_path: str = typer.Option(..., "--input", "-i", help="Source audio path."),
    output_path: str = typer.Option(..., "--output", "-o", help="Target audio path."),
    bitrate: str = typer.Option(
        "192k",
        "--bitrate",
        "-b",
        help="Target audio bitrate for all files. {128k, 192k, 256k, 320k}",
    ),
    channels: int = typer.Option(
        2, "--channels", "-c", help="Number of audio channels. {1, 2}"
    ),
    sample_rate: int = typer.Option(
        44100,
        "--samplerate",
        "-s",
        help="Audio sample rate in Hz. {16000, 22050, 44100, 48000}",
    ),
    gain: int = typer.Option(
        0, "--gain", "-g", help="Change audio gain in dB. [-30db, +30db]"
    ),
    trim: int = typer.Option(
        0,
        "--trim",
        "-t",
        help="Trim audio from the start in miliseconds. (0, audio lenght in ms]",
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite the output file if it exists."
    ),
):

    try:
        converter = AudioConverter(
            input_path,
            output_path,
            bitrate,
            channels,
            sample_rate,
            gain,
            trim,
            overwrite,
        )
        converter.convert()
        typer.echo(f"Success: Audio converted to {output_path}")
    except Exception as e:
        typer.echo(f"Audio Error: {e}")
        raise typer.Exit(code=1)


@audio_app.command("batch", help="Batch convert multiple audio within a directory.")
def batch_audio(
    input_dir: str = typer.Option(
        ..., "--input", "-i", help="Directory containing source audio."
    ),
    output_dir: str = typer.Option(
        ..., "--output", "-o", help="Directory to save converted audio."
    ),
    format: str = typer.Option(
        None, "--format", "-f", help="Target audio format (e.g., mp3, wav, ogg, flac)."
    ),
    bitrate: str = typer.Option(
        "192k",
        "--bitrate",
        "-b",
        help="Target audio bitrate for all files. {128k, 192k, 256k, 320k}",
    ),
    channels: int = typer.Option(
        2, "--channels", "-c", help="Number of audio channels. {1, 2}"
    ),
    sample_rate: int = typer.Option(
        44100,
        "--samplerate",
        "-s",
        help="Audio sample rate in Hz. {16000, 22050, 44100, 48000}",
    ),
    gain: int = typer.Option(
        0, "--gain", "-g", help="Change audio gain in dB. [-30db, +30db]"
    ),
    trim: int = typer.Option(
        0,
        "--trim",
        "-t",
        help="Trim audio from the start in miliseconds. (0, audio lenght in ms]",
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite existing files in output directory."
    ),
):
    run_batch_conversion(
        input_dir,
        output_dir,
        FileHandler.EXT_AUDIO,
        AudioConverter,
        format,
        overwrite,
        bitrate=bitrate,
        channels=channels,
        sample_rate=sample_rate,
        gain=gain,
        trim=trim,
    )


@video_app.command(
    "convert", help="Convert video formats (e.g., MP4 to AVI, MKV to MOV)."
)
def convert_video(
    input_path: str = typer.Option(..., "--input", "-i", help="Source video path."),
    output_path: str = typer.Option(..., "--output", "-o", help="Target video path."),
    bitrate: str = typer.Option(
        "2000k",
        "--bitrate",
        "-b",
        help="Target video bitrate (e.g., 1000k, 5000k).",
    ),
    resolution: str = typer.Option(
        "720p",
        "--resolution",
        "-r",
        help="Target resolution (e.g., 480p, 720p, 1080p).",
    ),
    fps: int = typer.Option(
        30,
        "--fps",
        "-f",
        help="Target frames per second. [24, 120]",
    ),
    codec: str = typer.Option(
        "h264",
        "--codec",
        "-x",
        help="Video codec. {h264, h265, vp9, av1}",
    ),
    audio_bitrate: str = typer.Option(
        "128k",
        "--audio-bitrate",
        "-ab",
        help="Target audio bitrate. {64k to 320k}",
    ),
    audio_channels: int = typer.Option(
        2,
        "--audio-channels",
        "-ac",
        help="Number of audio channels. {1, 2}",
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite the output file if it exists."
    ),
):
    try:
        converter = VideoConverter(
            input_path,
            output_path,
            bitrate,
            resolution,
            fps,
            codec,
            audio_bitrate,
            audio_channels,
            overwrite,
        )
        converter.convert()
        typer.echo(f"Success: Video converted to {output_path}")
    except Exception as e:
        typer.echo(f"Video Error: {e}")
        raise typer.Exit(code=1)


@video_app.command("batch", help="Batch convert multiple videos within a directory.")
def batch_video(
    input_dir: str = typer.Option(
        ..., "--input", "-i", help="Directory containing source videos."
    ),
    output_dir: str = typer.Option(
        ..., "--output", "-o", help="Directory to save converted videos."
    ),
    format: str = typer.Option(
        None, "--format", "-f", help="Target video format (e.g., mp4, avi, mkv, mov)."
    ),
    bitrate: str = typer.Option(
        "2000k",
        "--bitrate",
        "-b",
        help="Target video bitrate for all files.",
    ),
    resolution: str = typer.Option(
        "720p",
        "--resolution",
        "-r",
        help="Target resolution for all files.",
    ),
    fps: int = typer.Option(
        30,
        "--fps",
        "-f",
        help="Target frames per second. [24, 120]",
    ),
    codec: str = typer.Option(
        "h264",
        "--codec",
        "-x",
        help="Video codec. {h264, h265, vp9, av1}",
    ),
    audio_bitrate: str = typer.Option(
        "128k",
        "--audio-bitrate",
        "-ab",
        help="Target audio bitrate.",
    ),
    audio_channels: int = typer.Option(
        2,
        "--audio-channels",
        "-ac",
        help="Number of audio channels. {1, 2}",
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-v", help="Overwrite existing files in output directory."
    ),
):
    run_batch_conversion(
        input_dir,
        output_dir,
        FileHandler.EXT_VIDEO,
        VideoConverter,
        format,
        overwrite,
        bitrate=bitrate,
        resolution=resolution,
        fps=fps,
        codec=codec,
        audio_bitrate=audio_bitrate,
        audio_channels=audio_channels,
    )
