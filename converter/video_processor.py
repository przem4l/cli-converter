import shutil
import ffmpeg
from utils.file_handler import FileHandler

class VideoConverter(FileHandler):
    def __init__(
        self,
        input_path,
        output_path,
        bitrate,
        resolution,
        fps,
        codec,
        audio_bitrate,
        audio_channels,
        overwrite=False,
    ):
        super().__init__(input_path, output_path, overwrite=overwrite)
        self.bitrate = bitrate
        self.resolution = resolution
        self.fps = fps
        self.codec = codec
        self.audio_bitrate = audio_bitrate
        self.audio_channels = audio_channels
        self.validate_values()

    def convert(self):
        if not shutil.which("ffmpeg") and not shutil.which("avconv"):
            raise EnvironmentError(
                "FFmpeg is missing! Please install FFmpeg and add it to your system PATH."
            )

        stream = ffmpeg.input(self.input_path)
        scale = f"scale=-2:{self.resolution_value}"
        codec_map = {
            "h264": "libx264",
            "h265": "libx265",
            "vp9": "libvpx-vp9",
            "av1": "libaom-av1"
        }
        stream = ffmpeg.output(
            stream,
            self.output_path,
            vcodec=codec_map[self.codec],
            video_bitrate=self.bitrate,
            vf=scale,
            r=self.fps,
            acodec="aac",
            audio_bitrate=self.audio_bitrate,
            ac=self.audio_channels
        )

        ffmpeg.run(stream, overwrite_output=True)

    def validate_values(self):
        if not self.bitrate.endswith("k"):
            raise ValueError("Bitrate must end with 'k' (e.g. 500k)")
        bitrate_number_part = self.bitrate[:-1]
        if not bitrate_number_part.isdigit():
            raise ValueError("Bitrate must be a number + 'k'")
        bitrate = int(bitrate_number_part)
        if bitrate < 500 or bitrate > 50000:
            raise ValueError("Bitrate must be in range [500, 50000]k")

        if not self.resolution.endswith("p"):
            raise ValueError("Resolution must end with 'p' (e.g. 720p)")
        resolution_number_part = self.resolution[:-1]
        if not resolution_number_part.isdigit():
            raise ValueError("Resolution must be a number + 'p'")
        resolution = int(resolution_number_part)
        if resolution < 240 or resolution > 2160:
            raise ValueError("Resolution must be in range [240, 2160]p")
        self.resolution_value = resolution 

        if self.fps < 24 or self.fps > 120:
            raise ValueError("FPS must be in range [24, 120]")
        
        if self.codec not in ["h264", "h265", "vp9", "av1"]:
            raise ValueError("Unsupported codec")

        if not self.audio_bitrate.endswith("k"):
            raise ValueError("Audio bitrate must end with 'k'")

        audio_bitrate_number = self.audio_bitrate[:-1]

        if not audio_bitrate_number.isdigit():
            raise ValueError("Audio bitrate must be a number + 'k'")
        audio_bitrate = int(audio_bitrate_number)
        if audio_bitrate < 64 or audio_bitrate > 320:
            raise ValueError("Audio bitrate must be in range [64, 320]k")

        if self.audio_channels not in [1, 2]:
            raise ValueError("Audio channels must be 1 or 2")