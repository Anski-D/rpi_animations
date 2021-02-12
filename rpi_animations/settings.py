import importlib.resources
import json
import random
import sys

import pygame

from . import inputs


class Settings:
    def __init__(self, settings_file: str) -> None:
        # Set the resources settings
        self._settings_file = settings_file

        # Set default colours
        self._bg_colour = (0, 0, 0)
        self._text_colour = (0, 0, 0)
        self._outline_colour = (0, 0, 0)

        # Import the json file
        self._setup_settings()

    @property
    def bg_colour(self):
        """
        Return the allocated background colour.

        Returns:
            None
        """

        return self._bg_colour

    @property
    def text_colour(self):
        return self._text_colour

    @property
    def outline_colour(self):
        return self._outline_colour

    @property
    def settings(self):
        return self._settings

    def _setup_settings(self) -> None:
        # Load the json
        self._settings = self._load_json()

        try:
            # Process the settings
            self._process_settings()
        except ValueError as err:
            print(err)
            sys.exit(1)
        except KeyError as err:
            print(f'{err} not found in provided settings')
            sys.exit(1)
        else:
            # Load resources and set parameters
            self._set_parameters()

    def _process_settings(self):
        # Split the colour list up
        self._settings['colours'] = self._split_colours(str(self._settings['colours']))
        # Set the message text
        self._settings['messages'] = str(self._settings['messages']).split(';')
        # Make sure the message separator is a string
        self._settings['message_sep'] = str(self._settings['message_sep'])
        # Make sure the typeface is a string
        self._settings['typeface'] = str(self._settings['typeface'])
        # Make sure the text size is an integer
        self._settings['text_size'] = int(self._settings['text_size'])
        # Get bold boolean
        self._settings['bold_text'] = bool(self._settings['bold_text'])
        # Get italic boolean
        self._settings['italic_text'] = bool(self._settings['italic_text'])
        # Get text anti-aliasing boolean
        self._settings['text_aa'] = bool(self._settings['text_aa'])
        # Make sure the text speed is a float
        self._settings['text_speed'] = float(self._settings['text_speed'])
        # Make sure the outline width is an integer
        self._settings['outline_width'] = int(self._settings['outline_width'])
        # Set the outline colour
        self._settings['outline_colours'] = self._split_colours(str(self._settings['outline_colours']))
        # Make sure the image sources list is initially a string
        self._settings['image_sources'] = str(self._settings['image_sources']).split(';')
        # Make sure number of each image is an integer
        self._settings['num_images'] = int(self._settings['num_images'])
        # Make sure image change time is a float
        self._settings['image_change_time'] = float(self._settings['image_change_time'])
        # Make sure colour change time is a float
        self._settings['colour_change_time'] = float(self._settings['colour_change_time'])
        # Make sure fps is an integer
        self._settings['fps'] = int(self._settings['fps'])
        # Make sure number of reposition attempts is an integer
        self._settings['reposition_attempts'] = int(self._settings['reposition_attempts'])

    def _set_parameters(self):
        # Randomise the colour allocations
        self.set_colours()
        # Load images
        self._load_images()
        # Load the font
        self.font = pygame.font.SysFont(
            self._settings['typeface'],
            self._settings['text_size'],
            bold=self._settings['bold_text'],
            italic=self._settings['italic_text']
        )

    def _load_json(self) -> dict:
        try:
            # Open the json file safely
            with importlib.resources.open_text(inputs, self._settings_file) as settings_file:
                # Load the json
                return json.load(settings_file)
        except FileNotFoundError as err:
            print(f'{err.filename} not found')
            sys.exit(1)
        except json.decoder.JSONDecodeError as err:
            print(f'Issue found when loading {self._settings_file}. {err.args[0]}. You might have used single quotes '
                  f'instead of double quotes.')
            sys.exit(1)

    def set_colours(self) -> None:
        # Allocate colours by random
        self._bg_colour = self._settings['colours'][random.randrange(0, len(self._settings['colours']))]

        # Allocate a different text colour. Need to do this initial one, otherwise it won't change if already
        # different from the background.
        self._text_colour = self._settings['colours'][random.randrange(0, len(self._settings['colours']))]
        # Check if this clashes with the background, if so, allocate again
        while self._text_colour == self._bg_colour:
            self._text_colour = self._settings['colours'][random.randrange(0, len(self._settings['colours']))]

        # Set the outline colour
        self._outline_colour = \
            self._settings['outline_colours'][random.randrange(0, len(self._settings['outline_colours']))]

    @staticmethod
    def _split_colours(colours: str) -> list:
        # Each colours is a string that needs to be split further, turned into an int and then held as a tuple
        return [tuple([int(pigment) for pigment in colour.split(',')]) for colour in colours.split(';')]

    @property
    def text(self) -> str:
        # Set the message text
        return f"{self._settings['messages'][random.randrange(0, len(self._settings['messages']))]}{self._settings['message_sep']}"

    def _load_images(self) -> None:
        self.images = [
            image for image in [
                self._load_single_image(image_src)
                for image_src
                in self._settings['image_sources']
            ]
            if image is not None
        ]

    @staticmethod
    def _load_single_image(image_src):
        try:
            image = pygame.image.load(importlib.resources.open_binary(inputs, image_src))
        except FileNotFoundError as err:
            print(f'{err.filename} not found')
        else:
            return image
