# cli-converter

🇵🇱 [Polska wersja](README.pl.md)

A command-line tool for converting images, documents and audio files. Supports single file and batch directory processing.

## Requirements

```bash
pip install pillow typer tqdm pypandoc pymupdf pydub ffmpeg-python
```

> `pypandoc` requires [Pandoc](https://pandoc.org/installing.html) to be installed.  
> `pydub` and `ffmpeg-python` require [FFmpeg](https://ffmpeg.org/download.html) to be installed and available in system PATH.  
> HEIC support requires `pip install pillow-heif`.  
> RAW support requires `pip install rawpy`.

## Usage

### Interactive Mode
The tool features an interactive prompt for guided conversions without remembering flags:
```bash
python main.py interactive
```

### Statistics
After a successful conversion, the tool will display the statistics showing space saved or increased during the process with color-coded terminal text.

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
| `--output` | `-o` | Output file | *(optional, prompts if ommited)* |
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
| `--output` | `-o` | Target document path | *(optional, prompts if ommited)* |
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
| `--output` | `-o` | Target audio path | *(optional, prompts if ommited)* |
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

---

### Video

```bash
# Single conversion
python main.py video convert -i movie.mp4 -o movie.avi --resolution 1080p --fps 60

# Batch conversion
python main.py video batch -i ./videos -o ./output --format mkv --codec h265
```

#### Options `video convert`

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--input` | `-i` | Source video path | *(required)* |
| `--output` | `-o` | Target video path | *(optional, prompts if ommited)* |
| `--bitrate` | `-b` | Video bitrate (e.g., 5000k) | `5000k` |
| `--resolution`| `-r` | Target resolution (e.g., 720p, 1080p)| `1080p` |        
| `--fps` | `-f` | Frames per second (24–120) | `30` |
| `--codec` | `-x` | Video codec (h264, h265, vp9, av1) | `h264` |
| `--audio-bitrate`|`-ab`| Audio bitrate (64k–320k) | `192k` |
| `--audio-channels`|`-ac`| Audio channels (1 or 2) | `2` |
| `--overwrite` | `-v` | Overwrite existing file | `False` |

**Supported formats:** `.mp4` `.avi` `.mkv` `.mov`

**Supported conversions:**

| From \ To | MP4 | AVI | MKV | MOV |
|-----------|-----|-----|-----|-----|
| MP4       | ✅  | ✅  | ✅  | ✅   |
| AVI       | ✅  | ✅  | ✅  | ✅   |
| MKV       | ✅  | ✅  | ✅  | ✅   |
| MOV       | ✅  | ✅  | ✅  | ✅   |

**Validation rules:**
- FFmpeg must be installed and available in PATH
- Resolution must be in range `[240, 2160]p`
- FPS must be between `24` and `120`
- Supported codecs: `h264`, `h265`, `vp9`, `av1`
- Audio bitrate must be in range `[64, 320]k`
- Audio channels must be `1` or `2`
- `--trim` must be a non-negative value and cannot exceed the audio duration
- If output file already exists, use `--overwrite` to replace it
- Cross-category conversions (e.g. audio → image) are not allowed

---

## Project Structure

```text
cli-converter/
├── cli/
│   ├── commands.py      # CLI logic and sub-apps
│   ├── display.py       # Terminal UI and progress bars
│   └── __init__.py
├── converter/
│   ├── audio_processor.py # Pydub logic
│   ├── base_processor.py  # Shared media base class
│   ├── docs_processor.py  # Pandoc/Fitz logic
│   ├── image_processor.py # Pillow logic
│   ├── video_processor.py # FFmpeg logic
│   └── __init__.py
├── utils/
│   ├── file_handler.py    # Path and extension validation
│   └── __init__.py
├── main.py                # Entry point
├── README.md              # English documentation
└── README.pl.md           # Polish documentation
```