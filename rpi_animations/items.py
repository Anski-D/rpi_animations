from abc import ABC, abstractmethod
from pygame.sprite import Sprite
from pygame import Vector2


class Item(ABC, Sprite):
    def __init__(self, group: 'pygame.sprite.Group', parent) -> None:
        """

        Args:
            group:
            parent:
        """
        # Run super, add self to group
        super.__init__(group)

        # Get some information about from the parent
        self._settings = parent.settings
        self._perimeter = parent.perimeter

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


class Picture(Item):
    pass
