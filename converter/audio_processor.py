import shutil
from utils.file_handler import FileHandler
from converter.base_processor import MediaConverterBase


class AudioConverter(FileHandler, MediaConverterBase):
    def __init__(
        self,
        input_path,
        output_path,
        bitrate,
        channels,
        sample_rate,
        gain,
        trim,
        overwrite=False,
    ):
        super().__init__(input_path, output_path, overwrite=overwrite)
        self.bitrate = bitrate
        self.channels = channels
        self.sample_rate = sample_rate
        self.gain = gain
        self.trim = trim
        self.validate_values()

    def convert(self):
        try:
            from pydub import AudioSegment
        except ImportError:
            raise ImportError("Install pydub to process audio files (pip install pydub).")

        self.check_ffmpeg()

        audio = AudioSegment.from_file(self.input_path)

        if self.trim > 0:
            if self.trim > len(audio):
                raise ValueError("Trim duration is larger than audio duration")
            audio = audio[self.trim :]

        if self.gain != 0:
            audio = audio + self.gain

        if self.channels:
            audio = audio.set_channels(self.channels)

        if self.sample_rate:
            audio = audio.set_frame_rate(self.sample_rate)

        out_format = self.output_ext.replace(".", "")
        audio.export(self.output_path, format=out_format, bitrate=self.bitrate)

    def validate_values(self):
        if self.bitrate not in ["128k", "192k", "256k", "320k"]:
            raise ValueError("Invalid bitrate")
        if self.sample_rate not in [16000, 22050, 44100, 48000]:
            raise ValueError("Invalid sample rate")
        if self.channels not in [1, 2]:
            raise ValueError("Invalid channels")
        if self.trim < 0:
            raise ValueError("Invalid trim")
        if self.gain > 30 or self.gain < -30:
            raise ValueError("Invalid gain")
