import json
import random
import importlib.resources
from . import inputs


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
        self._messages = settings['text'].split(';')
        # Set the typeface
        # self.typeface = settings['typeface']
        self.typeface = None
        # Set the message size
        self.text_size = int(settings['text_size'])
        # Set the message scroll speed
        self.text_speed = float(settings['text_speed'])
        # Set the outline width
        self.outline_width = int(settings['outline_width'])
        # Set the outline colour
        self.outline_colour = tuple([int(colour) for colour in settings['outline_colour'].split(',')])
        # Set the list of image sources
        self.image_src = settings['image_src'].split(',')
        # Set how many of each image will be displayed
        self.num_images = int(settings['num_images'])
        # Set the image update counter limit
        self.image_update_counter_limit = int(settings['image_update_counter_limit'])
        # Set the colour change counter limit
        self.colour_change_counter_limit = int(settings['colour_change_counter_limit'])

    def _load_json(self):
        # Open the json file safely
        with importlib.resources.open_text(inputs, self._settings_file) as msg_file:
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
        split_colours = colours.split(';')

        # Each colours is a string that needs to be split further, turned into an int and then held as a tuple
        return [tuple([int(pigment) for pigment in colour.split(',')]) for colour in split_colours]

    @property
    def text(self):
        # Set the message text
        return f"{self._messages[random.randint(0, len(self._messages) - 1)]}  "
