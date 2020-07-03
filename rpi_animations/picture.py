import pygame
from pygame.sprite import Sprite
import random
import importlib.resources


class Picture(Sprite):
    def __init__(self, text_animator: object, image_src: str):
        super().__init__()

        # Save image src
        self._image_src = image_src

        # Get the settings
        self._settings = text_animator.settings

        # Save the text animator
        self._screen = text_animator.screen
        # Get the size of the text animator rectangle
        self._screen_rect = self._screen.get_rect()

        # Setup the picture
        self._setup_picture()

    def _setup_picture(self):
        self._load_image()
        self.update()

    def _load_image(self):
        # Load the image
        self._image = pygame.image.load(importlib.resources.open_binary('resources', self._image_src))

        # Get the image rect
        self._rect = self._image.get_rect()

    def update(self):
        # Place the image in a random location
        self._rect.x = random.randint(0, self._screen_rect.right)
        self._rect.y = random.randint(0, self._screen_rect.bottom)

        # Check whether the image is on screen
        if self._rect.top < self._screen_rect.top:
            self._rect.top = self._screen_rect.top

        if self._rect.left < self._screen_rect.left:
            self._rect.left = self._screen_rect.left

        if self._rect.bottom > self._screen_rect.bottom:
            self._rect.bottom = self._screen_rect.bottom

        if self._rect.right > self._screen_rect.right:
            self._rect.right = self._screen_rect.right

    def blitme(self):
        self._screen.blit(self._image, self._rect)
