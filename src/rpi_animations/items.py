from abc import ABC, abstractmethod
import pygame as pg
import random


class Movable(ABC):
    def __init__(self):
        self._rect = None
        self._perimeter = None

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect: pg.Rect):
        if isinstance(rect, pg.Rect):
            self._rect = rect

    @property
    def perimeter(self):
        return self._perimeter

    @perimeter.setter
    def perimeter(self, perimeter):
        if isinstance(perimeter, pg.Rect):
            self._perimeter = perimeter

    @abstractmethod
    def move(self):
        pass


class Item(pg.sprite.Sprite, Movable):
    def __init__(self, group: pg.sprite.Group, content: pg.Surface, perimeter: pg.Rect, movement=None) -> None:
        super().__init__(group)
        self._content = None
        self.content = content
        self._perimeter = None
        self.perimeter = perimeter
        self._movement = None
        self.movement = movement

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content: pg.Surface) -> None:
        if isinstance(content, pg.Surface):
            self._content = content
            self.rect = self._content.get_rect()

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, movement: 'Movement'):
        if isinstance(movement, Movement):
            self._movement = movement

    def move(self, *args, **kwargs):
        if self._movement is not None:
            self._movement.move(self, *args, **kwargs)

    def update(self, *args, **kwargs):
        self.move(*args, **kwargs)


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

    def move(self, movable: Movable, speed=None, *args, **kwargs):
        self.speed = speed
        movable.rect.x -= self._speed  # pixel/frame


class RandomMovement(Movement):
    def move(self, movable: Movable, *args, **kwargs):
        movable.rect.left = random.randint(0, movable.perimeter.right - movable.rect.width)
        movable.rect.top = random.randint(0, movable.perimeter.bottom - movable.rect.height)


class ItemFactory:
    _types = {}

    def __init__(self, key=None):
        self.key = key

    @property
    def factory_type(self):
        factory_type = self._types.get(self.key)
        if factory_type is None:
            return None
        return factory_type()

    @classmethod
    def register_type(cls, key, handle):
        if key not in cls._types:
            cls._types[key] = handle

    def create(self, group: pg.sprite.Group, content: pg.Surface, perimeter: pg.Rect):
        return Item(group, content, perimeter, movement=self.factory_type)


item_type_dict = {
    'scrolling': ScrollingMovement,
    'random': RandomMovement,
}

for key, value in item_type_dict.items():
    ItemFactory.register_type(key, value)
