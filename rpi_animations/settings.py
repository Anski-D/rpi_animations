import pygame
import json
import random
import importlib.resources
from . import inputs, resources


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
        # Load images
        self._load_images(settings['image_src'])
        # Set how many of each image will be displayed
        self.num_images = int(settings['num_images'])
        # Set the image update counter limit
        self.image_change_time = int(settings['image_change_time'])
        # Set the colour change counter limit
        self.colour_change_time = int(settings['colour_change_time'])
        # Set the FPS
        self.fps = int(settings['fps'])

    def _load_json(self):
        # Open the json file safely
        with importlib.resources.open_text(inputs, self._settings_file) as settings_file:
            # Load the json
            return json.load(settings_file)

    def set_colours(self):
        # Allocate colours by random
        self.bg_colour = self._colours[random.randrange(0, len(self._colours))]

        # Allocate a different text colour. Need to do this initial one, otherwise it won't change if already
        # different from the background.
        self.text_colour = self._colours[random.randrange(0, len(self._colours))]
        # Check if this clashes with the background, if so, allocate again
        while self.text_colour == self.bg_colour:
            self.text_colour = self._colours[random.randrange(0, len(self._colours))]

    @staticmethod
    def _split_colours(colours):
        # Each colours is a string that needs to be split further, turned into an int and then held as a tuple
        return [tuple([int(pigment) for pigment in colour.split(',')]) for colour in colours.split(';')]

    @property
    def text(self):
        # Set the message text
        return f"{self._messages[random.randrange(0, len(self._messages))]}   "

    def _load_images(self, image_srcs):
        self.images = [
            pygame.image.load(importlib.resources.open_binary(resources, image_src))
            for image_src
            in image_srcs.split(',')
        ]
