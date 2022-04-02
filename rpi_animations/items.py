from abc import ABC, abstractmethod
from pygame.sprite import Sprite
from pygame import Vector2


class Item(ABC, Sprite):
    def __init__(self, group: 'pygame.sprite.Group', settings, perimeter) -> None:
        """

        Args:
            group:
            settings:
            perimeter:
        """
        # Run super, add self to group
        super.__init__(group)

        # Set some defaults for the instance
        self._content = None
        self._rect = None

        # Get some information about from the parent
        self._settings = settings
        self._perimeter = perimeter

        # Set up the instance
        self._setup()

    def _setup(self):
        self._set_content()
        self._set_position()

    @abstractmethod
    def _set_content(self):
        pass

    @abstractmethod
    def _set_position(self):
        pass


class Message(Item):
    def __init__(self, group: 'import pygame.sprite', parent):
        pass

    def _set_content(self):
        self._content = self._settings['font'].render(
            self._settings['message'],
            self._settings['text_aa'],
            self._settings['text_colour']
        )

    def _set_position(self):
        self._rect.midleft = self._perimeter.midright


class Picture(Item):
    pass
