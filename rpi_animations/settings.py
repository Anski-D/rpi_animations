import pygame
import json
import random
import os


class Settings:
    def __init__(self, resource_loc, settings_file: str) -> None:
        # Set the resources location and settings
        self._resource_loc = resource_loc
        self._settings_file = settings_file

        # Set default colours
        self.bg_colour = (0, 0, 0)
        self.text_colour = (0, 0, 0)
        self.outline_colour = (0, 0, 0)

        # Import the json file
        self._load_settings()

    @property
    def settings(self):
        return self._settings

    def _load_settings(self) -> None:
        # Load the json
        self._settings = self._load_json()

        # Process the settings
        self._process_settings()

    def _process_settings(self):
        # Split the colour list up
        self._settings['colours'] = self._split_colours(self._settings['colours'])
        # Set the message text
        self._settings['messages'] = self._settings['messages'].split(';')
        # Set the typeface, set to None for now
        self._settings['typeface'] = None
        # Set the message scroll speed
        self._settings['text_speed'] = float(self._settings['text_speed'])
        # Set the outline colour
        self._settings['outline_colours'] = self._split_colours(self._settings['outline_colours'])

        # Load resources and set parameters
        self._set_parameters()

    def _set_parameters(self):
        # Randomise the colour allocations
        self.set_colours()
        # Load images
        self._load_images(self._settings['image_sources'])

    def _load_json(self) -> dict:
        # Open the json file safely
        with open(os.path.join(self._resource_loc, self._settings_file)) as settings_file:
            # Load the json
            return json.load(settings_file)

    def set_colours(self) -> None:
        # Allocate colours by random
        self.bg_colour = self._settings['colours'][random.randrange(0, len(self._settings['colours']))]

        # Allocate a different text colour. Need to do this initial one, otherwise it won't change if already
        # different from the background.
        self.text_colour = self._settings['colours'][random.randrange(0, len(self._settings['colours']))]
        # Check if this clashes with the background, if so, allocate again
        while self.text_colour == self.bg_colour:
            self.text_colour = self._settings['colours'][random.randrange(0, len(self._settings['colours']))]

        # Set the outline colour
        self.outline_colour = \
            self._settings['outline_colours'][random.randrange(0, len(self._settings['outline_colours']))]

    @staticmethod
    def _split_colours(colours: str) -> list:
        # Each colours is a string that needs to be split further, turned into an int and then held as a tuple
        return [tuple([int(pigment) for pigment in colour.split(',')]) for colour in colours.split(';')]

    @property
    def text(self) -> str:
        # Set the message text
        return f"{self._settings['messages'][random.randrange(0, len(self._settings['messages']))]}{self._settings['message_sep']}"

    def _load_images(self, images_sources: str) -> None:
        self.images = [
            pygame.image.load(os.path.join(self._resource_loc, image_src))
            for image_src
            in images_sources.split(';')
        ]
