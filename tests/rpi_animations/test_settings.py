from rpi_animations.settings import Settings
import pytest


class TestSettings:
    def mock_load_settings(self):
        return None

    def test_settings_init(self, monkeypatch):
        monkeypatch.setattr(Settings, '_load_settings', self.mock_load_settings)

        class_input = 'test.json'

        settings = Settings(class_input)

        assert settings._settings_file == class_input \
               and settings.bg_colour is None \
               and settings.text_colour is None

    def test_load_json_type(self):
        assert type(Settings('settings.json')._load_json()) == dict

    @pytest.fixture
    def settings_split_colours(self):
        colours_in = '0,0,0;255,255,255'
        return Settings._split_colours(colours_in)

    def test_split_colours_return_value(self, settings_split_colours):
        # Expected format of colour
        colours_out = [(0, 0, 0), (255, 255, 255)]

        assert settings_split_colours == colours_out

    def test_split_colours_return_type(self, settings_split_colours):
        # Check expected type of split colours
        assert type(settings_split_colours) == list

    def test_split_colours_return_contents(self, settings_split_colours):
        # Check each item in list is a tuple
        is_tuple = True
        for colour in settings_split_colours:
            if type(colour) is not tuple:
                is_tuple = False
                break

        assert is_tuple
