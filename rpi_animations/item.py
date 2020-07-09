from pygame.sprite import Sprite
from abc import ABC, abstractmethod


class Item(ABC, Sprite):
    def __init__(self, group, text_animator):
        super().__init__(group)

        # Set default values
        self._content = None
        self._rect = None

        # Set the settings
        self._settings = text_animator.settings

        # Save the text animator screen
        self._screen = text_animator.screen
        # Get the size of the text animator screen rectangle
        self._screen_rect = self._screen.get_rect()

        # Setup the item
        self._setup_item()

    @abstractmethod
    def _setup_item(self):
        pass

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def rect(self):
        return self.content.get_rect()

    @rect.setter
    def rect(self, rect):
        self._rect = rect

    @abstractmethod
    def _set_item_content(self):
        pass

    @abstractmethod
    def _place_item(self):
        pass

    def blit(self):
        self._screen.blit(self.content, self.rect)
