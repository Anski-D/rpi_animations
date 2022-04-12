import pytest
from rpi_animations.items import Item, Movable, RandomMovement, ScrollingMovement
import pygame


class TestMovable:
    @pytest.fixture
    def movable_setup(self):
        Movable.__abstractmethods__ = set()
        return Movable()

    def test_movable_rect_set(self, movable_setup):
        assert movable_setup.rect is None

        movable_setup.rect = 'test'
        assert movable_setup.rect is None

        rect_example = pygame.Rect(0, 0, 20, 10)
        movable_setup.rect = rect_example
        assert isinstance(movable_setup.rect, pygame.Rect)
        assert movable_setup.rect is rect_example

        rect = movable_setup.rect
        rect.x = 5
        assert movable_setup.rect.x == 5

    def test_movable_perimeter_set(self, movable_setup):
        assert movable_setup.perimeter is None

        movable_setup.perimeter = 'test'
        assert movable_setup.perimeter is None

        perimeter_example = pygame.Rect(0, 0, 1000, 500)
        movable_setup.perimeter = perimeter_example
        assert isinstance(movable_setup.perimeter, pygame.Rect)
        assert movable_setup.perimeter is perimeter_example

        perimeter = movable_setup.perimeter
        perimeter.x = 50
        assert movable_setup.perimeter.x == 50


class TestScrollingMovement:
    @pytest.fixture
    def movable_setup(self):
        Movable.__abstractmethods__ = set()
        movable = Movable()
        movable.rect = pygame.Rect(50, 50, 20, 10)
        return movable

    def test_scrolling_movement_speed_set(self):
        scroller = ScrollingMovement(5)
        assert scroller.speed == 5

        scroller.speed = 'test'
        assert scroller.speed == 5

        scroller.speed = 10
        assert scroller.speed == 10

    def test_scrolling_movement_move(self, movable_setup):
        assert movable_setup.rect.x == 50

        scroller = ScrollingMovement(1)
        scroller.move(movable_setup)
        assert movable_setup.rect.x == 49

        scroller.move(movable_setup, 10)
        assert movable_setup.rect.x == 39


class TestRandomMovement:
    @pytest.fixture
    def movable_setup(self):
        Movable.__abstractmethods__ = set()
        movable = Movable()
        movable.rect = pygame.Rect(50, 50, 20, 10)
        movable.perimeter = pygame.Rect(0, 0, 1000, 500)
        return movable

    def test_random_movement_move(self, movable_setup):
        right1 = movable_setup.rect.right
        bottom1 = movable_setup.rect.bottom
        assert right1 == 70 and bottom1 == 60

        random_mover = RandomMovement()

        random_mover.move(movable_setup)
        right2 = movable_setup.rect.right
        bottom2 = movable_setup.rect.bottom
        assert right2 <= movable_setup.perimeter.right and bottom2 <= movable_setup.perimeter.bottom
        assert right2 != right1 and bottom2 != bottom1

        random_mover.move(movable_setup)
        right3 = movable_setup.rect.right
        bottom3 = movable_setup.rect.bottom
        assert right3 <= movable_setup.perimeter.right and bottom3 <= movable_setup.perimeter.bottom
        assert right3 != right2 and bottom3 != bottom2

        random_mover.move(movable_setup)
        right4 = movable_setup.rect.right
        bottom4 = movable_setup.rect.bottom
        assert right4 <= movable_setup.perimeter.right and bottom4 <= movable_setup.perimeter.bottom
        assert right4 != right3 and bottom4 != bottom3


class TestItem:
    @pytest.fixture
    def item_setup(self):
        content = pygame.Surface((20, 10))
        perimeter = pygame.Rect(0, 0, 1000, 500)
        return Item(pygame.sprite.Group(), content, perimeter)

    def test_item_set_content(self, item_setup):
        content1 = item_setup.content
        assert item_setup.rect == pygame.Rect(0, 0, 20, 10)

        content2 = pygame.Surface((40, 20))
        item_setup.content = content2
        assert item_setup.content is not content1
        assert item_setup.rect == pygame.Rect(0, 0, 40, 20)

    def test_item_create_items(self):
        group = pygame.sprite.Group()
        content = pygame.Surface((20, 10))
        perimeter = pygame.Rect(0, 0, 1000, 500)

        scrolling_item = Item.create_scrolling_item(group, content, perimeter)
        assert isinstance(scrolling_item, Item)

        random_item = Item.create_random_item(group, content, perimeter)
        assert isinstance(random_item, Item)


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
