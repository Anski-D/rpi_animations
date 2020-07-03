import json
import random


class Settings:
    def __init__(self, settings_file: str):
        # Set the settings file
        self._settings_file = settings_file

        # Set default colours
        self.bg_colour = None
        self.text_colour = None

        # Import the json file
        self._load_settings()

    def _load_settings(self):
        # Load the json
        settings = self._load_json()

        # Split the dictionary
        # Split the colour list up
        self._colours = self._split_colours(settings['colours'])
        # Randomise the colour allocations
        self.set_colours()
        # Set the message text
        self.text = f"{settings['text']}  "
        # Set the message size
        self.text_size = int(settings['text_size'])
        # Set the mesage scroll speed
        self.text_speed = float(settings['text_speed'])
        # Set the list of image sources
        self.image_src = settings['image_src'].split(',')
        # Set how many of each image will be displayed
        self.num_images = int(settings['num_images'])

    def _load_json(self):
        # Open the json file safely
        with open(self._settings_file) as msg_file:
            # Load the json
            return json.load(msg_file)

    def set_colours(self):
        # Allocate colours by random
        self.bg_colour = self._colours[random.randint(0, len(self._colours) - 1)]

        # Allocate a different text colour. Need to do this initial one, otherwise it won't change if already
        # different from the background.
        self.text_colour = self._colours[random.randint(0, len(self._colours) - 1)]
        # Check if this clashes with the background, if so, allocate again
        while self.text_colour == self.bg_colour:
            self.text_colour = self._colours[random.randint(0, len(self._colours) - 1)]

    @staticmethod
    def _split_colours(colours):
        # Split the list of colours into distinct colours
        split_colours = colours.split('/')

        # Each colours is a string that needs to be split further, turned into an int and then held as a tuple
        return [tuple([int(pigment) for pigment in colour.split(',')]) for colour in split_colours]
