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
        self.content = content
        self.perimeter = perimeter
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

    @classmethod
    def create_scrolling_item(cls, group, content, perimeter):
        return Item(group, content, perimeter, movement=ScrollingMovement())

    @classmethod
    def create_random_item(cls, group, content, perimeter):
        return Item(group, content, perimeter, movement=RandomMovement())

    def move(self):
        if self._movement is not None:
            self._movement.move(self)
            
    def update(self):
        self.move()


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
        movable.rect.x -= self._speed # pixel/frame


class RandomMovement(Movement):
    def move(self, movable: Movable):
        movable.rect.left = random.randint(0, movable.perimeter.right - movable.rect.width)
        movable.rect.top = random.randint(0, movable.perimeter.bottom - movable.rect.height)
