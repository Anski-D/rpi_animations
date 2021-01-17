import pygame
import json
import random
import importlib.resources
from . import inputs, resources


class Settings:
    def __init__(self, settings_file: str) -> None:
        # Set the settings file
        self._settings_file = settings_file

        # Set default colours
        self.bg_colour = (0, 0, 0)
        self.text_colour = (0, 0, 0)
        self.outline_colour = (0, 0, 0)

        # Import the json file
        self._load_settings()

    def _load_settings(self) -> None:
        # Load the json
        settings = self._load_json()

        # Split the dictionary
        # Split the colour list up
        self._colours = self._split_colours(settings['colours'])
        # Set the message text
        self._messages = settings['text'].split(';')
        # Set the message seperator
        self._message_sep = settings['message_sep']
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
        self._outline_colours = self._split_colours(settings['outline_colours'])
        # Randomise the colour allocations
        self.set_colours()
        # Load images
        self._load_images(settings['image_sources'])
        # Set how many of each image will be displayed
        self.num_images = int(settings['num_images'])
        # Set the image update counter limit
        self.image_change_time = int(settings['image_change_time'])
        # Set the colour change counter limit
        self.colour_change_time = int(settings['colour_change_time'])
        # Set the FPS
        self.fps = int(settings['fps'])

    def _load_json(self) -> dict:
        # Open the json file safely
        with importlib.resources.open_text(inputs, self._settings_file) as settings_file:
            # Load the json
            return json.load(settings_file)

    def set_colours(self) -> None:
        # Allocate colours by random
        self.bg_colour = self._colours[random.randrange(0, len(self._colours))]

        # Allocate a different text colour. Need to do this initial one, otherwise it won't change if already
        # different from the background.
        self.text_colour = self._colours[random.randrange(0, len(self._colours))]
        # Check if this clashes with the background, if so, allocate again
        while self.text_colour == self.bg_colour:
            self.text_colour = self._colours[random.randrange(0, len(self._colours))]

        # Set the outline colour
        self.outline_colour = self._outline_colours[random.randrange(0, len(self._outline_colours))]

    @staticmethod
    def _split_colours(colours: str) -> list:
        # Each colours is a string that needs to be split further, turned into an int and then held as a tuple
        return [tuple([int(pigment) for pigment in colour.split(',')]) for colour in colours.split(';')]

    @property
    def text(self) -> str:
        # Set the message text
        return f'{self._messages[random.randrange(0, len(self._messages))]}{self._message_sep}'

    def _load_images(self, images_sources: str) -> None:
        self.images = [
            pygame.image.load(importlib.resources.open_binary(resources, image_src))
            for image_src
            in images_sources.split(';')
        ]
