class BaseConverter:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = self.output_path

    def validate(self):
      for field in ["input_path", "output_path"]:
        value = getattr(self, field)
        if isinstance(value, str) != True:
            raise TypeError("Error: entered {key} is not string!")
        if value.strip() != True:
            raise ValueError("Error: {key} is empty string!")
        return True

    def convert(self):
        pass