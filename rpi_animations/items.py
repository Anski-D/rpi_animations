from abc import ABC, abstractmethod
from pygame import Rect
from pygame.sprite import Group, Sprite
import random


class Item(ABC, Sprite):
    def __init__(self, group: Group, content, perimeter: Rect, movement=None) -> None:
        super().__init__(group)
        self._rect = None
        self._perimeter = None
        self.content = content
        self.perimeter = perimeter
        self.movement = movement(self)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect: Rect):
        if isinstance(rect, Rect):
            self._rect = rect

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content) -> None:
        self._content = content
        self._rect = self._content.get_rect()

    @property
    def perimeter(self):
        return self._perimeter

    @perimeter.setter
    def perimeter(self, perimeter):
        if isinstance(perimeter, Rect):
            self._perimeter = perimeter

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, movement: 'Movement'):
        if isinstance(movement, Movement):
            self._movement = movement

    @classmethod
    def create_scrolling_item(cls, group, content, perimeter):
        return Item(group, content, perimeter, movement=ScrollingMovement)

    @classmethod
    def create_random_item(cls, group, content, perimeter):
        return Item(group, content, perimeter, movement=RandomMovement)

    def set_position(self, item_ref, target_position):
        self._rect.__setattr__(item_ref, target_position)

    def move(self):
        if self._movement is not None:
            self._movement.move()


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


class Movement:
    def __init__(self, item: Item):
        self._item = item

    @abstractmethod
    def move(self):
        pass


class ScrollingMovement(Movement):
    def __init__(self, item: Item, speed=0):
        super().__init__(item)
        self.speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if isinstance(speed, (int, float)):
            self._speed = speed

    def move(self, speed=None):
        self.speed = speed
        self._item.set_position('x', self._item.rect.x - self._speed)  # pixel/frame


class RandomMovement(Movement):
    def move(self):
        self._item.set_position('left', random.randint(0, self._item.perimeter.right - self._item.rect.width))
        self._item.set_position('top', random.randint(0, self._item.perimeter.bottom - self._item.rect.height))
