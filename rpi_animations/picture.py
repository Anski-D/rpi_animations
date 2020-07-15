import pygame
import random
import importlib.resources
from . import resources
from .item import Item


class Picture(Item):
    def __init__(self, group, text_animator, image):
        # Save image src
        self._image = image

        # Run parent class init
        super().__init__(group, text_animator)

    def _set_item_content(self):
        # Load the image
        self.content = self._image

    def _place_item(self):
        # Place the image in a random location
        self._rect.left = random.randint(0, self._screen_rect.right - self._rect.width)
        self._rect.top = random.randint(0, self._screen_rect.bottom - self._rect.height)

    def update(self):
        # Place the image in a new position
        self._place_item()
