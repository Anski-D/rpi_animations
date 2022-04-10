from abc import ABC, abstractmethod
from pygame import Rect
from pygame.sprite import Group, Sprite
import random


class Item(Sprite):
    def __init__(self, group: Group, content, perimeter: Rect, movement=None) -> None:
        super().__init__(group)
        self._rect = None
        self._perimeter = None
        self.content = content
        self.perimeter = perimeter
        self.movement = movement

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
        return Item(group, content, perimeter, movement=ScrollingMovement())

    @classmethod
    def create_random_item(cls, group, content, perimeter):
        return Item(group, content, perimeter, movement=RandomMovement())

    def set_position(self, item_ref, target_position):
        self._rect.__setattr__(item_ref, target_position)

    def move(self):
        if self._movement is not None:
            self._movement.move(self)


class Movement:
    @abstractmethod
    def move(self, item: Item):
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

    def move(self, item: Item, speed=None):
        self.speed = speed
        item.set_position('x', item.rect.x - self._speed)  # pixel/frame


class RandomMovement(Movement):
    def move(self, item: Item):
        item.set_position('left', random.randint(0, item.perimeter.right - item.rect.width))
        item.set_position('top', random.randint(0, item.perimeter.bottom - item.rect.height))
