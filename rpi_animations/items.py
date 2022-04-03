from abc import ABC, abstractmethod
from pygame.sprite import Sprite


class Item(ABC, Sprite):
    def __init__(self, group: 'pygame.sprite.Group', settings: dict, perimeter: 'pygame.Rect') -> None:
        """

        Args:
            group:
            settings:
            perimeter:
        """
        # Run super, add self to group
        super().__init__(group)

        # Set some defaults for the instance
        self._content = None
        self._rect = None
        self._position = None

        # Get some information about from the parent
        self._settings = settings
        self._perimeter = perimeter

        # Set up the instance
        self._setup()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content) -> None:
        self._content = content

        if self._rect is None:
            self._rect = self._content.get_rect()

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
    def __init__(self, group: 'pygame.sprite.Group', settings: dict, perimeter: 'pygame.Rect'):
        super().__init__(group, settings, perimeter)

        # Keep accurate track of position
        self._position['x'] = self._rect.x

        # Keep track of whether fully within the right perimeter
        self._is_within_right = False

    def update(self) -> None:
        """

        Returns:

        """
        self._position['x'] -= self._settings['text_speed'] / self._settings['fps']  # px/s / frame/s = px/frame
        self._rect.x = self._position['x']

    def is_within_left(self) -> None:
        """

        Returns:

        """
        if self._rect.right < self._perimeter.left:
            return False

        return True

    def is_just_within_right(self):
        if not self._is_within_right and self._rect.right <= self._perimeter.right:
            self._is_within_right = True
            return True

        return False

    def _set_content(self) -> None:
        self.content = self._settings['font'].render(
            self._settings['message'],
            self._settings['text_aa'],
            self._settings['text_colour'],
        )

    def _set_position(self) -> None:
        self._rect.midleft = self._perimeter.midright


class Picture(Item):
    pass
