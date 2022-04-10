from abc import ABC, abstractmethod
from pygame import Rect
from pygame.sprite import Group, Sprite
import random


class Movable(ABC):
    def __init__(self):
        self._rect = None
        self._perimeter = None

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect: Rect):
        if isinstance(rect, Rect):
            self._rect = rect

    @property
    def perimeter(self):
        return self._perimeter

    @perimeter.setter
    def perimeter(self, perimeter):
        if isinstance(perimeter, Rect):
            self._perimeter = perimeter

    def set_position(self, item_ref, target_position):
        if self._rect is not None:
            self._rect.__setattr__(item_ref, target_position)

    @abstractmethod
    def move(self):
        pass


class Item(Sprite, Movable):
    def __init__(self, group: Group, content, perimeter: Rect, movement=None) -> None:
        super().__init__(group)
        self.content = content
        self.perimeter = perimeter
        self.movement = movement

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content) -> None:
        self._content = content
        self._rect = self._content.get_rect()

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, movement: 'Movement'):
        if isinstance(movement, Movement):
            self._movement = movement

    @classmethod
    def create_scrolling_item(cls, group, content, perimeter):
        return Item(group, content, perimeter, movement=ScrollingMovement())

    @classmethod
    def create_random_item(cls, group, content, perimeter):
        return Item(group, content, perimeter, movement=RandomMovement())

    def move(self):
        if self._movement is not None:
            self._movement.move(self)


class Movement:
    @abstractmethod
    def move(self, movable: Movable):
        pass


class ScrollingMovement(Movement):
    def __init__(self, speed=0):
        self.speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if isinstance(speed, (int, float)):
            self._speed = speed

    def move(self, movable: Movable, speed=None):
        self.speed = speed
        movable.set_position('x', movable.rect.x - self._speed)  # pixel/frame


class RandomMovement(Movement):
    def move(self, movable: Movable):
        movable.set_position('left', random.randint(0, movable.perimeter.right - movable.rect.width))
        movable.set_position('top', random.randint(0, movable.perimeter.bottom - movable.rect.height))
