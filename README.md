# cli-converter

🇵🇱 [Polska wersja](README.pl.md)

A command-line tool for converting images, documents and audio files. Supports single file and batch directory processing.

## Requirements

```bash
pip install pillow typer tqdm pypandoc pymupdf pydub
```

> `pypandoc` requires [Pandoc](https://pandoc.org/installing.html) to be installed.  
> `pydub` requires [FFmpeg](https://ffmpeg.org/download.html) to be installed and available in system PATH.  
> HEIC support requires `pip install pillow-heif`.  
> RAW support requires `pip install rawpy`.

## Usage

### Images

```bash
# Single conversion
python main.py image convert -i photo.png -o photo.jpg

# Batch conversion
python main.py image batch -i ./photos -o ./output --format webp
```

#### Options `image convert`

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--input` | `-i` | Input file | *(required)* |
| `--output` | `-o` | Output file | *(required)* |
| `--quality` | `-q` | Quality (0–100) | `95` |
| `--height` | `-h` | Height in pixels | `None` |
| `--width` | `-w` | Width in pixels | `None` |
| `--grayscale` | `-g` | Convert to grayscale | `False` |
| `--keep` | `-k` | Keep aspect ratio | `False` |
| `--optimize` | `-O` | Optimize file size | `False` |
| `--rotate` | `-r` | Rotation in degrees (−360–360) | `0` |
| `--overwrite` | `-v` | Overwrite existing file | `False` |
| `--delete` | `-d` | Delete source file after conversion | `False` |

**Supported formats:** `.png` `.jpg` `.jpeg` `.webp` `.heic` `.raw`

**Supported conversions:**

| From \ To | PNG | JPG/JPEG | WEBP | HEIC | RAW |
|-----------|-----|----------|------|------|-----|
| PNG       | ✅  | ✅       | ✅   | ✅   | ✅  |
| JPG/JPEG  | ✅  | ✅       | ✅   | ✅   | ✅  |
| WEBP      | ✅  | ✅       | ✅   | ✅   | ✅  |
| HEIC      | ✅  | ✅       | ✅   | ✅   | ✅  |
| RAW       | ✅  | ✅       | ✅   | ✅   | ✅  |

> Cross-category conversions (e.g. image → document) are not allowed.

**Validation rules:**
- Input file must exist
- Output file extension must be a supported image format
- If output file already exists, use `--overwrite` to replace it
- Input and output paths cannot be the same unless `--overwrite` is used
- Height and width must be positive integers when provided
- HEIC files require the `pillow-heif` package
- RAW files require the `rawpy` package

---

### Documents

```bash
# Single conversion
python main.py doc convert -i file.pdf -o file.txt

# Batch conversion
python main.py doc batch -i ./documents -o ./output --format txt
```

#### Options `doc convert`

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--input` | `-i` | Source document path | *(required)* |
| `--output` | `-o` | Target document path | *(required)* |
| `--overwrite` | `-v` | Overwrite existing file | `False` |

**Supported formats:** `.pdf` `.docx` `.txt` `.odt`

**Supported conversions:**

| From \ To | PDF | DOCX | TXT | ODT |
|-----------|-----|------|-----|-----|
| PDF       | —   | ❌   | ✅  | ❌  |
| DOCX      | ⚠️  | ✅   | ✅  | ✅  |
| TXT       | ⚠️  | ✅   | ✅  | ✅  |
| ODT       | ⚠️  | ✅   | ✅  | ✅  |

> ⚠️ Exporting to PDF requires a PDF engine installed on your system (e.g. MiKTeX, wkhtmltopdf).

**Validation rules:**
- Input file must exist
- PDF input can only be converted to TXT (other targets will raise an error)
- Exporting to PDF requires an external PDF engine; if missing, a descriptive error is shown
- Cross-category conversions (e.g. document → image) are not allowed
- If output file already exists, use `--overwrite` to replace it

---

### Audio

```bash
# Single conversion
python main.py audio convert -i track.mp3 -o track.wav

# Batch conversion
python main.py audio batch -i ./music -o ./output --format flac
```

#### Options `audio convert`

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--input` | `-i` | Source audio path | *(required)* |
| `--output` | `-o` | Target audio path | *(required)* |
| `--bitrate` | `-b` | Output bitrate | `192k` |
| `--channels` | `-c` | Number of channels (1 or 2) | `2` |
| `--samplerate` | `-s` | Sample rate in Hz | `44100` |
| `--gain` | `-g` | Gain adjustment in dB (−30–+30) | `0` |
| `--trim` | `-t` | Trim from start in milliseconds | `0` |
| `--overwrite` | `-v` | Overwrite existing file | `False` |

**Supported formats:** `.mp3` `.wav` `.ogg` `.flac`

**Supported conversions:**

| From \ To | MP3 | WAV | OGG | FLAC |
|-----------|-----|-----|-----|------|
| MP3       | ✅  | ✅  | ✅  | ✅   |
| WAV       | ✅  | ✅  | ✅  | ✅   |
| OGG       | ✅  | ✅  | ✅  | ✅   |
| FLAC      | ✅  | ✅  | ✅  | ✅   |

**Validation rules:**
- FFmpeg must be installed and available in PATH
- `--bitrate` must be one of: `128k`, `192k`, `256k`, `320k`
- `--samplerate` must be one of: `16000`, `22050`, `44100`, `48000`
- `--channels` must be `1` (mono) or `2` (stereo)
- `--gain` must be between `−30` and `+30` dB
- `--trim` must be a non-negative value and cannot exceed the audio duration
- If output file already exists, use `--overwrite` to replace it
- Cross-category conversions (e.g. audio → image) are not allowed

---

## Project Structure

```
├── main.py
├── cli/
│   ├── __init__.py
│   ├── commands.py        # CLI commands (Typer)
│   └── display.py         # Progress bar (tqdm)
├── converter/
│   ├── __init__.py
│   ├── image_processor.py # Image conversion (Pillow)
│   ├── docs_processor.py  # Document conversion (pypandoc, pymupdf)
│   └── audio_processor.py # Audio conversion (pydub)
└── utils/
    ├── __init__.py
    └── file_handler.py    # File validation and path handling
```