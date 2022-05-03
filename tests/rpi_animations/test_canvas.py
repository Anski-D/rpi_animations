import pytest
import pygame as pg
import math
from rpi_animations.settings import SettingsManager
from rpi_animations.canvas import Canvas
from rpi_animations.items import Item, ScrollingMovement


class TestCanvas:
    @pytest.fixture
    def settings_dict(self):
        pytest.settings_dict = {
            "colours": [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
            ],
            "messages": [
                "TEST MESSAGE 1!",
                "TEST MESSAGE 2!",
                "TEST MESSAGE 3!",
                "TEST MESSAGE 4!"
            ],
            "message_sep": "   ",
            "typeface": "freeserif",
            "text_size": 350,
            "bold_text": 1,
            "italic_text": 0,
            "text_aa": 0,
            "text_speed": 240.0,
            "outline_width": 3,
            "outline_colours": [
                (0, 0, 0),
                (255, 255, 255),
            ],
            "image_sources": [
                "pic1.bmp",
                "pic2.bmp",
                "pic3.bmp"],
            "num_images": 10,
            "image_change_time": 2,
            "colour_change_time": 15,
            "fps": 30,
            "reposition_attempts": 50
        }

    @pytest.fixture
    def canvas_setup(self, settings_dict, monkeypatch):
        pg.init()
        monkeypatch.setattr(SettingsManager, '_import_settings', lambda x, y: pytest.settings_dict)
        monkeypatch.setattr(pg.image, 'load', lambda x: pg.Surface((20, 10)))
        return Canvas(SettingsManager(None, None), pg.Surface((1000, 500)))

    def test_create_message(self, canvas_setup):
        canvas_setup._create_message()
        assert len(canvas_setup._messages) == 1 \
            and canvas_setup._messages.sprites()[0].rect.left == canvas_setup._perimeter.right \
            and canvas_setup._messages.sprites()[0].rect.y == canvas_setup._perimeter.height / 2 - pytest.settings_dict['text_size'] / 2 \
            and canvas_setup._messages.sprites()[0].movement.speed == pytest.settings_dict['text_speed'] / pytest.settings_dict['fps']

    def test_create_images(self, canvas_setup):
        canvas_setup._create_images()
        assert len(canvas_setup._images) == len(pytest.settings_dict['image_sources']) * pytest.settings_dict['num_images']

    def test_update_messages(self, canvas_setup, monkeypatch):
        tests = []
        speed = pytest.settings_dict['text_speed'] / pytest.settings_dict['fps']
        canvas = canvas_setup

        canvas._create_message()
        tests.append(len(canvas._messages.sprites()) == 1)

        message1_width = canvas._messages.sprites()[0].rect.width
        for _ in range(math.ceil(message1_width / speed)):
            canvas._update_messages()
        tests.append(len(canvas._messages.sprites()) == 2)

        monkeypatch.setattr(Canvas, '_create_message', lambda x: None)
        message2_width = canvas._messages.sprites()[-1].rect.width
        for _ in range(math.ceil((canvas._perimeter.width + message2_width) / speed)):
            canvas._update_messages()
        tests.append(len(canvas._messages.sprites()) == 0)

        assert all(tests)
