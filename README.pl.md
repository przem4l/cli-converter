# cli-converter

🇬🇧 [English version](README.md)

Narzędzie wiersza poleceń do konwersji obrazów i dokumentów. Obsługuje pojedyncze pliki oraz przetwarzanie wsadowe całych katalogów.

## Wymagania

```bash
pip install pillow typer tqdm pypandoc pymupdf
```

> `pypandoc` wymaga zainstalowanego [Pandoc](https://pandoc.org/installing.html).

## Użycie

### Obrazy

```bash
# Pojedyncza konwersja
python main.py image convert -i foto.png -o foto.jpg

# Wsadowa konwersja katalogu
python main.py image batch -i ./zdjecia -o ./wyniki --format webp
```

#### Opcje `image convert`

| Flaga | Skrót | Opis | Domyślnie |
|-------|-------|------|-----------|
| `--input` | `-i` | Plik wejściowy | *(wymagane)* |
| `--output` | `-o` | Plik wyjściowy | *(wymagane)* |
| `--quality` | `-q` | Jakość (0–100) | `95` |
| `--height` | `-h` | Wysokość w pikselach | `None` |
| `--width` | `-w` | Szerokość w pikselach | `None` |
| `--grayscale` | `-g` | Skala szarości | `False` |
| `--keep` | `-k` | Zachowanie proporcji | `False` |
| `--optimize` | `-O` | Optymalizacja rozmiaru | `False` |
| `--rotate` | `-r` | Obrót w stopniach | `0` |
| `--overwrite` | `-v` | Nadpisanie istniejącego pliku | `False` |
| `--delete` | `-d` | Usunięcie pliku źródłowego | `False` |

Obsługiwane formaty: `.png` `.jpg` `.jpeg` `.webp` `.heic` `.raw`

---

### Dokumenty

```bash
# Pojedyncza konwersja
python main.py doc convert -i plik.pdf -o plik.txt

# Wsadowa konwersja katalogu
python main.py doc batch -i ./dokumenty -o ./wyniki --format txt
```

Obsługiwane formaty: `.pdf` `.docx` `.txt` `.odt`

---

## Struktura projektu

```
├── main.py
├── cli/
│   ├── __init__.py
│   ├── commands.py        # Komendy CLI (Typer)
│   └── display.py         # Pasek postępu (tqdm)
├── converter/
│   ├── __init__.py
│   ├── image_processor.py # Konwersja obrazów (Pillow)
│   └── docs_processor.py  # Konwersja dokumentów (pypandoc, pymupdf)
└── utils/
    ├── __init__.py
    └── file_handler.py    # Walidacja plików i ścieżek
```