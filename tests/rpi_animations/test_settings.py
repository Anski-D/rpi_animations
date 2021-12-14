import pytest
from rpi_animations.settings import SettingsImporter


class TestSettingsImporters:
    @pytest.fixture
    def imported_json(self):
        pytest.imported_json = {
            "colours": [
                [255, 0, 0],
                [0, 255, 0],
                [0, 0, 255]
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
                [0, 0, 0],
                [255, 255, 255]
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
        pytest.settings_dict = {
            "colours": [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255)
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
                (255, 255, 255)
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

    def test_settings_import_convert_colours(self, imported_json):
        settings_importer = SettingsImporter()
        settings_importer._settings = pytest.imported_json
        settings_importer._convert_colours()
        assert settings_importer._settings == pytest.settings_dict
