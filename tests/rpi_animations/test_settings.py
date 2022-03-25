import pytest
from rpi_animations.settings import SettingsImporter, SettingsManager


class TestSettingsManager:
    @pytest.fixture
    def settings_dict(self):
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

    @pytest.fixture
    def settings_manager_setup(self, settings_dict, monkeypatch):
        monkeypatch.setattr(SettingsManager, '_import_settings', lambda x, y: pytest.settings_dict)
        return SettingsManager(None, None)

    def test_settings_manager_set_colours(self, settings_manager_setup):
        settings_manager_setup.set_colours()

        assert settings_manager_setup.settings['bg_colour'] in pytest.settings_dict['colours'] \
               and settings_manager_setup.settings['text_colour'] in pytest.settings_dict['colours'] \
               and settings_manager_setup.settings['outline_colour'] in pytest.settings_dict['outline_colours']

    def test_settings_manager_text(self, settings_manager_setup, settings_dict):
        assert settings_manager_setup.settings['text'] \
               in [f"{message}{pytest.settings_dict['message_sep']}" for message in pytest.settings_dict['messages']]


class TestSettingsImporter:
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

    def test_settings_importer_convert_colours(self, imported_json):
        settings_importer = SettingsImporter()
        settings_importer._settings = pytest.imported_json
        settings_importer._convert_colours()
        assert settings_importer._settings == pytest.settings_dict
