import pytest
from rpi_animations.items import Item, ItemFactory, Movable, RandomMovement, ScrollingMovement
import pygame as pg


class TestMovable:
    @pytest.fixture
    def movable_setup(self):
        Movable.__abstractmethods__ = set()
        return Movable()

    def test_movable_rect_set(self, movable_setup):
        assert movable_setup.rect is None

        movable_setup.rect = 'test'
        assert movable_setup.rect is None

        rect_example = pg.Rect(0, 0, 20, 10)
        movable_setup.rect = rect_example
        assert isinstance(movable_setup.rect, pg.Rect)
        assert movable_setup.rect is rect_example

        rect = movable_setup.rect
        rect.x = 5
        assert movable_setup.rect.x == 5

    def test_movable_perimeter_set(self, movable_setup):
        assert movable_setup.perimeter is None

        movable_setup.perimeter = 'test'
        assert movable_setup.perimeter is None

        perimeter_example = pg.Rect(0, 0, 1000, 500)
        movable_setup.perimeter = perimeter_example
        assert isinstance(movable_setup.perimeter, pg.Rect)
        assert movable_setup.perimeter is perimeter_example

        perimeter = movable_setup.perimeter
        perimeter.x = 50
        assert movable_setup.perimeter.x == 50


class TestScrollingMovement:
    @pytest.fixture
    def movable_setup(self):
        Movable.__abstractmethods__ = set()
        movable = Movable()
        movable.rect = pg.Rect(50, 50, 20, 10)
        return movable

    def test_speed_set(self):
        scroller = ScrollingMovement(5)
        assert scroller.speed == 5

        scroller.speed = 'test'
        assert scroller.speed == 5

        scroller.speed = 10
        assert scroller.speed == 10

    def test_move(self, movable_setup):
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
        movable.rect = pg.Rect(50, 50, 20, 10)
        movable.perimeter = pg.Rect(0, 0, 1000, 500)
        return movable

    def test_move(self, movable_setup):
        tests = []
        right1 = movable_setup.rect.right
        bottom1 = movable_setup.rect.bottom
        tests.append(right1 == 70 and bottom1 == 60)

        random_mover = RandomMovement()

        random_mover.move(movable_setup)
        right2 = movable_setup.rect.right
        bottom2 = movable_setup.rect.bottom
        tests.append(movable_setup.perimeter.contains(movable_setup.rect))
        tests.append(right2 != right1 and bottom2 != bottom1)

        random_mover.move(movable_setup)
        right3 = movable_setup.rect.right
        bottom3 = movable_setup.rect.bottom
        tests.append(movable_setup.perimeter.contains(movable_setup.rect))
        tests.append(right3 != right2 and bottom3 != bottom2)

        random_mover.move(movable_setup)
        right4 = movable_setup.rect.right
        bottom4 = movable_setup.rect.bottom
        tests.append(movable_setup.perimeter.contains(movable_setup.rect))
        tests.append(right4 != right3 and bottom4 != bottom3)

        assert all(tests)


class TestItem:
    @pytest.fixture
    def item_setup(self):
        content = pg.Surface((20, 10))
        perimeter = pg.Rect(0, 0, 1000, 500)
        return Item(pg.sprite.Group(), content, perimeter)

    def test_set_content(self, item_setup):
        content1 = item_setup.content
        assert item_setup.rect == pg.Rect(0, 0, 20, 10)

        content2 = pg.Surface((40, 20))
        item_setup.content = content2
        assert item_setup.content is not content1
        assert item_setup.rect == pg.Rect(0, 0, 40, 20)

    def test_set_movement(self, item_setup):
        item_setup.movement = ScrollingMovement()
        assert isinstance(item_setup.movement, ScrollingMovement)

        item_setup.movement = RandomMovement()
        assert isinstance(item_setup.movement, RandomMovement)

    def test_create_items(self):
        group = pg.sprite.Group()
        content = pg.Surface((20, 10))
        perimeter = pg.Rect(0, 0, 1000, 500)

        scrolling_item = Item.create_scrolling_item(group, content, perimeter)
        assert isinstance(scrolling_item, Item)

        random_item = Item.create_random_item(group, content, perimeter)
        assert isinstance(random_item, Item)


class TestItemFactory:
    def test_register_type(self):
        ItemFactory.register_type('scrolling', ScrollingMovement)
        assert 'scrolling' in ItemFactory._types \
            and isinstance(ItemFactory._types.get('scrolling')(), ScrollingMovement) \
            and ItemFactory._types.get('test') is None

    def test_create(self):
        tests = []
        group = pg.sprite.Group()
        content = pg.Surface((20, 10))
        perimeter = pg.Rect(0, 0, 1000, 500)

        ItemFactory.register_type('scrolling', ScrollingMovement)
        ItemFactory.register_type('random', RandomMovement)

        scrolling_item_factory = ItemFactory('scrolling')
        scrolling_item1 = scrolling_item_factory.create(group, content, perimeter)
        tests.append(isinstance(scrolling_item1, Item))
        tests.append(isinstance(scrolling_item1.movement, ScrollingMovement))
        scrolling_item2 = scrolling_item_factory.create(group, content, perimeter)
        tests.append(isinstance(scrolling_item2, Item))
        tests.append(isinstance(scrolling_item2.movement, ScrollingMovement))

        random_item_factory = ItemFactory('random')
        random_item1 = random_item_factory.create(group, content, perimeter)
        tests.append(isinstance(random_item1, Item))
        tests.append(isinstance(random_item1.movement, RandomMovement))
        random_item2 = random_item_factory.create(group, content, perimeter)
        tests.append(isinstance(random_item2, Item))
        tests.append(isinstance(random_item2.movement, RandomMovement))

        none_item_factory = ItemFactory()
        none_item1 = none_item_factory.create(group, content, perimeter)
        tests.append(isinstance(none_item1, Item))
        tests.append(none_item1.movement is None)
        none_item2 = none_item_factory.create(group, content, perimeter)
        tests.append(isinstance(none_item2, Item))
        tests.append(none_item2.movement is None)

        assert all(tests)
