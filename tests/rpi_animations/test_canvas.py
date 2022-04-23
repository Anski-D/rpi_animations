import pytest
import pygame as pg
from rpi_animations.settings import SettingsManager
from rpi_animations.canvas import Canvas
from rpi_animations.items import Item


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

    def test_create_images(self, canvas_setup):
        canvas_setup._create_images()
        assert len(canvas_setup._images) == 3
