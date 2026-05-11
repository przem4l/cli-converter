FROM python:3.12-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ffmpeg pandoc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir pillow typer tqdm pypandoc pymupdf pydub ffmpeg-python pillow-heif rawpy

COPY main.py main.py
COPY cli/ cli/
COPY converter/ converter/
COPY utils/ utils/

ENV IS_DOCKER=1

ENTRYPOINT ["python", "main.py"]