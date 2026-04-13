# cli-converter

🇬🇧 [English version](README.md)

Narzędzie wiersza poleceń do konwersji obrazów, dokumentów i plików audio. Obsługuje pojedyncze pliki oraz przetwarzanie wsadowe całych katalogów.

## Wymagania

```bash
pip install pillow typer tqdm pypandoc pymupdf pydub
```

> `pypandoc` wymaga zainstalowanego [Pandoc](https://pandoc.org/installing.html).  
> `pydub` wymaga zainstalowanego [FFmpeg](https://ffmpeg.org/download.html) dostępnego w PATH systemowym.  
> Obsługa HEIC wymaga `pip install pillow-heif`.  
> Obsługa RAW wymaga `pip install rawpy`.

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
| `--rotate` | `-r` | Obrót w stopniach (−360–360) | `0` |
| `--overwrite` | `-v` | Nadpisanie istniejącego pliku | `False` |
| `--delete` | `-d` | Usunięcie pliku źródłowego po konwersji | `False` |

**Obsługiwane formaty:** `.png` `.jpg` `.jpeg` `.webp` `.heic` `.raw`

**Obsługiwane konwersje:**

| Z \ Na    | PNG | JPG/JPEG | WEBP | HEIC | RAW |
|-----------|-----|----------|------|------|-----|
| PNG       | ✅  | ✅       | ✅   | ✅   | ✅  |
| JPG/JPEG  | ✅  | ✅       | ✅   | ✅   | ✅  |
| WEBP      | ✅  | ✅       | ✅   | ✅   | ✅  |
| HEIC      | ✅  | ✅       | ✅   | ✅   | ✅  |
| RAW       | ✅  | ✅       | ✅   | ✅   | ✅  |

> Konwersje między kategoriami (np. obraz → dokument) są niedozwolone.

**Walidacja:**
- Plik wejściowy musi istnieć
- Rozszerzenie pliku wyjściowego musi być obsługiwanym formatem obrazu
- Jeśli plik wyjściowy już istnieje, użyj `--overwrite`, aby go nadpisać
- Ścieżki wejściowa i wyjściowa nie mogą być takie same, chyba że użyto `--overwrite`
- Wysokość i szerokość muszą być liczbami całkowitymi większymi od zera, jeśli zostały podane
- Pliki HEIC wymagają pakietu `pillow-heif`
- Pliki RAW wymagają pakietu `rawpy`

---

### Dokumenty

```bash
# Pojedyncza konwersja
python main.py doc convert -i plik.pdf -o plik.txt

# Wsadowa konwersja katalogu
python main.py doc batch -i ./dokumenty -o ./wyniki --format txt
```

#### Opcje `doc convert`

| Flaga | Skrót | Opis | Domyślnie |
|-------|-------|------|-----------|
| `--input` | `-i` | Plik wejściowy | *(wymagane)* |
| `--output` | `-o` | Plik wyjściowy | *(wymagane)* |
| `--overwrite` | `-v` | Nadpisanie istniejącego pliku | `False` |

**Obsługiwane formaty:** `.pdf` `.docx` `.txt` `.odt`

**Obsługiwane konwersje:**

| Z \ Na | PDF | DOCX | TXT | ODT |
|--------|-----|------|-----|-----|
| PDF    | —   | ❌   | ✅  | ❌  |
| DOCX   | ⚠️  | ✅   | ✅  | ✅  |
| TXT    | ⚠️  | ✅   | ✅  | ✅  |
| ODT    | ⚠️  | ✅   | ✅  | ✅  |

> ⚠️ Eksport do PDF wymaga silnika PDF zainstalowanego w systemie (np. MiKTeX, wkhtmltopdf).

**Walidacja:**
- Plik wejściowy musi istnieć
- PDF można konwertować wyłącznie do formatu TXT (inne cele zwrócą błąd)
- Eksport do PDF wymaga zewnętrznego silnika PDF; jego brak skutkuje czytelnym komunikatem o błędzie
- Konwersje między kategoriami (np. dokument → obraz) są niedozwolone
- Jeśli plik wyjściowy już istnieje, użyj `--overwrite`, aby go nadpisać

---

### Audio

```bash
# Pojedyncza konwersja
python main.py audio convert -i sciezka.mp3 -o sciezka.wav

# Wsadowa konwersja katalogu
python main.py audio batch -i ./muzyka -o ./wyniki --format flac
```

#### Opcje `audio convert`

| Flaga | Skrót | Opis | Domyślnie |
|-------|-------|------|-----------|
| `--input` | `-i` | Plik wejściowy | *(wymagane)* |
| `--output` | `-o` | Plik wyjściowy | *(wymagane)* |
| `--bitrate` | `-b` | Bitrate wyjściowy | `192k` |
| `--channels` | `-c` | Liczba kanałów (1 lub 2) | `2` |
| `--samplerate` | `-s` | Częstotliwość próbkowania w Hz | `44100` |
| `--gain` | `-g` | Zmiana głośności w dB (−30–+30) | `0` |
| `--trim` | `-t` | Przycięcie od początku w milisekundach | `0` |
| `--overwrite` | `-v` | Nadpisanie istniejącego pliku | `False` |

**Obsługiwane formaty:** `.mp3` `.wav` `.ogg` `.flac`

**Obsługiwane konwersje:**

| Z \ Na | MP3 | WAV | OGG | FLAC |
|--------|-----|-----|-----|------|
| MP3    | ✅  | ✅  | ✅  | ✅   |
| WAV    | ✅  | ✅  | ✅  | ✅   |
| OGG    | ✅  | ✅  | ✅  | ✅   |
| FLAC   | ✅  | ✅  | ✅  | ✅   |

**Walidacja:**
- FFmpeg musi być zainstalowany i dostępny w PATH systemowym
- `--bitrate` musi być jedną z wartości: `128k`, `192k`, `256k`, `320k`
- `--samplerate` musi być jedną z wartości: `16000`, `22050`, `44100`, `48000`
- `--channels` musi wynosić `1` (mono) lub `2` (stereo)
- `--gain` musi mieścić się w przedziale od `−30` do `+30` dB
- `--trim` musi być wartością nieujemną i nie może przekraczać długości pliku audio
- Jeśli plik wyjściowy już istnieje, użyj `--overwrite`, aby go nadpisać
- Konwersje między kategoriami (np. audio → obraz) są niedozwolone

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
│   ├── docs_processor.py  # Konwersja dokumentów (pypandoc, pymupdf)
│   └── audio_processor.py # Konwersja audio (pydub)
└── utils/
    ├── __init__.py
    └── file_handler.py    # Walidacja plików i ścieżek
```