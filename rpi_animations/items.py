from abc import ABC, abstractmethod
from pygame.sprite import Sprite
import random


class Item(ABC, Sprite):
    def __init__(self, group: 'pygame.sprite.Group', content, perimeter: 'pygame.Rect', movement=None) -> None:
        """

        Args:
            group:
            content:
            perimeter:
        """
        super().__init__(group)
        self.content = content
        self._movement = movement

    @property
    def content(self):
        """

        Returns:

        """
        return self._content

    @content.setter
    def content(self, content) -> None:
        """

        Args:
            content:

        Returns:

        """
        self._content = content

        if self._rect is None:
            self._rect = self._content.get_rect()

    def set_position(self, item_ref, target_position):
        self._rect.__setattr__(item_ref, target_position)

    def move(self, *args, **kwargs):
        self._movement.move(*args, **kwargs)


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

    def is_just_within_right(self) -> None:
        """

        Returns:

        """
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
    def __init__(self, group: 'pygame.sprite.Group', settings: dict, perimeter: 'pygame.Rect', image):
        self._image = image

        super().__init__(group, settings, perimeter)

    def update(self):
        """

        Returns:

        """
        self._set_position()

    def _set_content(self):
        self.content = self._image

    def _set_position(self):
        self._rect.left = random.randint(0, self._perimeter.right - self._rect.width)
        self._rect.top = random.randint(0, self._perimeter.bottom - self._rect.height)
