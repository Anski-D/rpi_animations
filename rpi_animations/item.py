from pygame.sprite import Sprite
from abc import abstractmethod


class Item(Sprite):
    def __init__(self, text_animator):
        super().__init__()

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


if __name__ == '__main__':
    item = Item('test')
