import json


class Settings:
    def __init__(self, settings_file: str):
        # Set the settings file
        self._settings_file = settings_file

        # Import the json file
        self._load_message()

    def _load_message(self):
        # Load the json
        message = self._load_json()

        # Split the dictionary
        self.bg_colour = tuple(map(int, message['bg_colour'].split(',')))
        self.text_colour = tuple(map(int, message['text_colour'].split(',')))
        self.text = f"  {message['text']}"
        self.text_size = int(message['text_size'])
        self.text_speed = float(message['text_speed'])
        self.image_src = message['image_src']
        self.num_images = int(message['num_images'])

    def _load_json(self):
        # Open the json file safely
        with open(self._settings_file) as msg_file:
            # Load the json
            return json.load(msg_file)
