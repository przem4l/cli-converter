# cli-converter

🇵🇱 [Polska wersja](README.pl.md)

A command-line tool for converting images and documents. Supports single file and batch directory processing.

## Requirements

```bash
pip install pillow typer tqdm pypandoc pymupdf
```

> `pypandoc` requires [Pandoc](https://pandoc.org/installing.html) to be installed.

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
| `--rotate` | `-r` | Rotation in degrees | `0` |
| `--overwrite` | `-v` | Overwrite existing file | `False` |
| `--delete` | `-d` | Delete source file after conversion | `False` |

Supported formats: `.png` `.jpg` `.jpeg` `.webp` `.heic` `.raw`

---

### Documents

```bash
# Single conversion
python main.py doc convert -i file.pdf -o file.txt

# Batch conversion
python main.py doc batch -i ./documents -o ./output --format txt
```

Supported formats: `.pdf` `.docx` `.txt` `.odt`

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
│   └── docs_processor.py  # Document conversion (pypandoc, pymupdf)
└── utils/
    ├── __init__.py
    └── file_handler.py    # File validation and path handling
```