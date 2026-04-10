from PIL import Image
from base import BaseConverter
class ImageConverter(BaseConverter):
  def __init__(self, input_path, output_path, current_format, new_format, current_resolution, new_resolution, quality):
    super().__init__(input_path, output_path)
    self.quality = quality
    self.current_format = current_format
    self.new_format = new_format
    self.current_resolution = current_resolution
    self.new_resolution = new_resolution

  def convert(self):
    img = Image.open(self.input_path)
    if self.new_format == "JPEG":
      img = img.convert("RGB")
    img.resize(self.new_resolution)
    img.save(self.output_path, self.new_format)
