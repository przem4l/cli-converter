# cli-converter

🇬🇧 [English version](README.md)

Narzędzie wiersza poleceń do konwersji obrazów, dokumentów i plików audio. Obsługuje pojedyncze pliki oraz przetwarzanie wsadowe całych katalogów.

## Wymagania

```bash
pip install pillow typer tqdm pypandoc pymupdf pydub ffmpeg-python
```

> `pypandoc` wymaga zainstalowanego [Pandoc](https://pandoc.org/installing.html).  
> `pydub` i `ffmpeg-python` wymagają zainstalowanego [FFmpeg](https://ffmpeg.org/download.html) dostępnego w PATH systemowym.  
> Obsługa HEIC wymaga `pip install pillow-heif`.  
> Obsługa RAW wymaga `pip install rawpy`.

## Użycie

### Tryb Interaktywny
Projekt wyposażono w łatwy w obsłudze asystent krok-po-kroku, aby nie pisać poleceń z pamięci:
```bash
python main.py interactive
```

### Podsumowanie i Statystyki
Po każdej udanej konwersji, aplikacja wypisze estetyczne podsumowanie porównujące rozmiary plików (wejściowy vs wyjściowy) wraz z odpowiednio kolorowanym (zielony/czerwony) procentowym zaoszczędzeniem miejsca.

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
| `--output` | `-o` | Plik wyjściowy | *(opcjonalne, zapytanie)* |
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
| `--output` | `-o` | Plik wyjściowy | *(opcjonalne, zapytanie)* |
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
| `--output` | `-o` | Plik wyjściowy | *(opcjonalne, zapytanie)* |
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

---

### Video

```bash
# Pojedyncza konwersja
python main.py video convert -i film.mp4 -o film.avi --resolution 1080p --fps 60

# Wsadowa konwersja katalogu
python main.py video batch -i ./filmy -o ./wyniki --format mkv --codec h265
```

#### Opcje `video convert`

| Flaga | Skrót | Opis | Domyślnie |
|-------|-------|------|-----------|
| `--input` | `-i` | Plik wejściowy | *(wymagane)* |
| `--output` | `-o` | Plik wyjściowy | *(opcjonalne, zapytanie)* |
| `--bitrate` | `-b` | Bitrate wideo (np. 5000k) | `5000k` |
| `--resolution`| `-r` | Rozdzielczość docelowa (np. 720p, 1080p)| `1080p` |   
| `--fps` | `-f` | Klatki na sekundę (24–120) | `30` |
| `--codec` | `-x` | Kodek wideo (h264, h265, vp9, av1) | `h264` |
| `--audio-bitrate`|`-ab`| Bitrate audio (64k–320k) | `192k` |
| `--audio-channels`|`-ac`| Kanały audio (1 lub 2) | `2` |
| `--overwrite` | `-v` | Nadpisanie istniejącego pliku | `False` |

**Obsługiwane formaty:** `.mp4` `.avi` `.mkv` `.mov`

**Obsługiwane konwersje:**

| Z \ Na    | MP4 | AVI | MKV | MOV |
|-----------|-----|-----|-----|-----|
| MP4       | ✅  | ✅  | ✅  | ✅   |
| AVI       | ✅  | ✅  | ✅  | ✅   |
| MKV       | ✅  | ✅  | ✅  | ✅   |
| MOV       | ✅  | ✅  | ✅  | ✅   |

**Walidacja:**
- FFmpeg musi być zainstalowany i dostępny w PATH systemowym
- Rozdzielczość musi być w zakresie `[240, 2160]p`
- FPS musi mieścić się w przedziale od `24` do `120`
- Obsługiwane kodeki: `h264`, `h265`, `vp9`, `av1`
- Bitrate audio musi być w zakresie `[64, 320]k`
- Liczba kanałów audio musi wynosić `1` lub `2`
- `--trim` musi być wartością nieujemną i nie może przekraczać długości pliku audio
- Jeśli plik wyjściowy już istnieje, użyj `--overwrite`, aby go nadpisać
- Konwersje między kategoriami (np. audio → obraz) są niedozwolone

---

## Struktura Projektu

```text
cli-converter/
├── cli/
│   ├── commands.py      # Logika CLI i pod-aplikacje
│   ├── display.py       # UI terminala i paski postępu
│   └── __init__.py
├── converter/
│   ├── audio_processor.py # Logika Pydub
│   ├── base_processor.py  # Bazowa klasa dla multimediów
│   ├── docs_processor.py  # Logika Pandoc/Fitz
│   ├── image_processor.py # Logika Pillow
│   ├── video_processor.py # Logika FFmpeg
│   └── __init__.py
├── utils/
│   ├── file_handler.py    # Walidacja ścieżek i rozszerzeń
│   └── __init__.py
├── main.py                # Punkt wejścia
├── README.md              # Dokumentacja angielska
└── README.pl.md           # Dokumentacja polska
```