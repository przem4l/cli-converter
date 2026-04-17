import shutil


class MediaConverterBase:
    def check_ffmpeg(self):
        if not shutil.which("ffmpeg") and not shutil.which("avconv"):
            raise EnvironmentError(
                "FFmpeg is missing! Please install FFmpeg and add it to your system PATH."
            )
