import pytest
from rpi_animations.items import Movable, Item
import pygame


class TestMovable:
    @pytest.fixture
    def movable_setup(self, monkeypatch):
        Movable.__abstractmethods__ = set()
        return Movable()

    def test_movable_rect_set(self, movable_setup):
        assert movable_setup.rect is None

        movable_setup.rect = 'test'
        assert movable_setup.rect is None

        rect_example = pygame.Rect(0, 0, 10, 10)
        movable_setup.rect = rect_example
        assert isinstance(movable_setup.rect, pygame.Rect)
        assert movable_setup.rect is rect_example

    def test_movable_perimeter_set(self, movable_setup):
        assert movable_setup.perimeter is None

        movable_setup.perimeter = 'test'
        assert movable_setup.perimeter is None

        perimeter_example = pygame.Rect(0, 0, 100, 100)
        movable_setup.perimeter = perimeter_example
        assert isinstance(movable_setup.perimeter, pygame.Rect)
        assert movable_setup.perimeter is perimeter_example

    def test_movable_set_position(self, movable_setup):
        movable_setup.rect = pygame.Rect(0, 0, 100, 50)

        movable_setup.set_position('left', 50)
        assert movable_setup.rect.left == 50

        movable_setup.set_position('height', 25)
        assert movable_setup.rect.height == 25


# class TestMessage:
#     @pytest.fixture
#     def message_setup(self, monkeypatch):
#         def mock_init(mock_self):
#             mock_self._rect = Rect(0, 0, 10, 10)
#             mock_self._position = {'x': 100}
#             mock_self._settings = {'text_speed': 90.0, 'fps': 30}
#             mock_self._perimeter = Rect(0, 0, 1000, 1000)
#
#         monkeypatch.setattr(Message, '__init__', mock_init)
#         return Message()
#
#     def test_message_update(self, message_setup):
#         ppf = message_setup._settings['text_speed'] / message_setup._settings['fps']
#         message_setup.update()
#
#         assert message_setup._position['x'] == 100 - ppf
#
#     def test_message_is_within_left(self, message_setup):
#         message_setup._rect.right = message_setup._perimeter.left - 1
#         assert not message_setup.is_within_left()
#
#         message_setup._rect.right = message_setup._perimeter.left
#         assert message_setup.is_within_left()
#
#         message_setup._rect.right = message_setup._perimeter.left + 1
#         assert message_setup.is_within_left()
#
#     def test_message_is_just_within_right(self, message_setup):
#         message_setup._is_within_right = True
#         message_setup._rect.right = message_setup._perimeter.right - 1
#         assert not message_setup.is_just_within_right() and message_setup._is_within_right
#
#         message_setup._is_within_right = True
#         message_setup._rect.right = message_setup._perimeter.right
#         assert not message_setup.is_just_within_right() and message_setup._is_within_right
#
#         message_setup._is_within_right = True
#         message_setup._rect.right = message_setup._perimeter.right + 1
#         assert not message_setup.is_just_within_right() and message_setup._is_within_right
#
#         message_setup._is_within_right = False
#         message_setup._rect.right = message_setup._perimeter.right - 1
#         assert message_setup.is_just_within_right() and message_setup._is_within_right
#
#         message_setup._is_within_right = False
#         message_setup._rect.right = message_setup._perimeter.right
#         assert message_setup.is_just_within_right() and message_setup._is_within_right
#
#         message_setup._is_within_right = False
#         message_setup._rect.right = message_setup._perimeter.right + 1
#         assert not message_setup.is_just_within_right() and not message_setup._is_within_right


# class TestPicture:
#     @pytest.fixture
#     def common(self):
#         pytest._perimeter_width = 1000
#         pytest._perimeter_height = 1000
#
#     @pytest.fixture
#     def picture_setup(self, common, monkeypatch):
#         def mock_init(mock_self):
#             mock_self._rect = Rect(0, 0, 10, 10)
#             mock_self._perimeter = Rect(0, 0, pytest._perimeter_width, pytest._perimeter_height)
#
#         monkeypatch.setattr(Picture, '__init__', mock_init)
#         return Picture()
#
#     def test_picture_set_position(self, common, picture_setup):
#         picture_setup._set_position()
#         assert picture_setup._rect.top >= 0 \
#             and picture_setup._rect.left >= 0 \
#             and picture_setup._rect.bottom <= pytest._perimeter_height \
#             and picture_setup._rect.right <= pytest._perimeter_width
