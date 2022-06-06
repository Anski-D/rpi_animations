import pytest
import pygame as pg
import math
from rpi_animations.settings import SettingsManager
from rpi_animations.model import Model


class TestModel:
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
    def model_setup(self, settings_dict, monkeypatch):
        pg.init()
        monkeypatch.setattr(SettingsManager, '_import_settings', lambda x, y: pytest.settings_dict)
        monkeypatch.setattr(pg.image, 'load', lambda x: pg.Surface((20, 10)))
        return Model(SettingsManager(None, None), pg.Surface((1000, 500)))

    def test_create_message(self, model_setup):
        model_setup._create_message()
        assert len(model_setup._messages) == 1 \
            and model_setup._messages.sprites()[0].rect.left == model_setup._perimeter.right \
            and model_setup._messages.sprites()[0].rect.y == model_setup._perimeter.height / 2 - pytest.settings_dict['text_size'] / 2 \
            and model_setup._messages.sprites()[0].movement.speed == pytest.settings_dict['text_speed'] / pytest.settings_dict['fps']

    def test_create_images(self, model_setup):
        model_setup._create_images()
        assert len(model_setup._images) == len(pytest.settings_dict['image_sources']) * pytest.settings_dict['num_images']

    def test_update_messages(self, model_setup, monkeypatch):
        tests = []
        speed = pytest.settings_dict['text_speed'] / pytest.settings_dict['fps']
        model = model_setup

        model._create_message()
        tests.append(len(model._messages.sprites()) == 1)

        message1_width = model._messages.sprites()[0].rect.width
        for _ in range(math.ceil(message1_width / speed)):
            model._update_messages()
        tests.append(len(model._messages.sprites()) == 2)

        monkeypatch.setattr(Model, '_create_message', lambda x: None)
        message2_width = model._messages.sprites()[-1].rect.width
        for _ in range(math.ceil((model._perimeter.width + message2_width) / speed)):
            model._update_messages()
        tests.append(len(model._messages.sprites()) == 0)

        assert all(tests)

    def test_update_images(self, model_setup):
        model = model_setup
        model._create_images()
        model._update_images()
        xy_orig = [(image.rect.x, image.rect.y) for image in model._images.sprites()]
        model._update_images()
        xy_new = [(image.rect.x, image.rect.y) for image in model._images.sprites()]
        collide_test = []
        for image in model._images.sprites():
            model._images.remove(image)
            collide_test.append(not pg.sprite.spritecollideany(image, model._images))
            model._images.add(image)

        assert xy_new != xy_orig and all(collide_test)
