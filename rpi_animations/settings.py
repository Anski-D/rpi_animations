import json


class Settings:
    def __init__(self, settings_file: str):
        # Set the settings file
        self._settings_file = settings_file

        # Import the json file
        self._load_message()

    def _load_message(self):
        # Load the json
        settings = self._load_json()

        # Split the dictionary
        self.bg_colour = tuple(map(int, settings['bg_colour'].split(',')))
        self.text_colour = tuple(map(int, settings['text_colour'].split(',')))
        self.text = f"{settings['text']}  "
        self.text_size = int(settings['text_size'])
        self.text_speed = float(settings['text_speed'])
        self.image_src = settings['image_src'].split(',')
        self.num_images = int(settings['num_images'])

    def _load_json(self):
        # Open the json file safely
        with open(self._settings_file) as msg_file:
            # Load the json
            return json.load(msg_file)
