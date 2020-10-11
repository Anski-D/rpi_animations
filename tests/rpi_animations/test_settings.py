from rpi_animations.settings import Settings
import pytest


class TestSettings:
    @pytest.fixture
    def settings_with_dummy_input(self, monkeypatch):
        monkeypatch.setattr(Settings, '_load_settings', lambda x: None)
        class_input = 'test.json'
        return Settings(class_input)

    def test_settings_init(self, settings_with_dummy_input):
        assert settings_with_dummy_input._settings_file == 'test.json' \
               and settings_with_dummy_input.bg_colour is None \
               and settings_with_dummy_input.text_colour is None

    def test_load_settings(self, monkeypatch):
        settings_dict = {
            "colours": "0,0,0;255,255,255",
            "text": "Test1;Test2;Test3",
            "typeface": "Serif Regular",
            "text_size": 7,
            "text_speed": 7,
            "outline_width": 7,
            "outline_colour": "0,0,0",
            "image_src": "test1.bmp,test2.bmp,test3.bmp",
            "num_images": 7,
            "image_change_time": 7,
            "colour_change_time": 7,
            "fps": 7
        }
        monkeypatch.setattr(Settings, '_load_json', lambda x: settings_dict)
        monkeypatch.setattr(Settings, '_load_images', lambda x, y: None)
        settings_dummy = Settings('test.json')

        assert settings_dummy._colours == [(0, 0, 0), (255, 255, 255)] \
               and settings_dummy._messages == ['Test1', 'Test2', 'Test3'] \
               and settings_dummy.typeface is None \
               and settings_dummy.text_size == 7 \
               and settings_dummy.text_speed == 7 \
               and settings_dummy.outline_width == 7 \
               and settings_dummy.outline_colour == (0, 0, 0) \
               and settings_dummy.num_images == 7 \
               and settings_dummy.image_change_time == 7.0 \
               and settings_dummy.colour_change_time == 7.0 \
               and settings_dummy.fps == 7

        # self._colours = self._split_colours(settings['colours'])
        # self._load_images(settings['image_src'])

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

    def test_text(self, settings_with_dummy_input):
        messages = ['Test1', 'Test2', 'Test3']
        settings_with_dummy_input._messages = messages

        assert settings_with_dummy_input.text[:-3] in messages

    @pytest.fixture
    def settings_with_colours(self, settings_with_dummy_input):
        colours = [(0, 0, 0), (255, 255, 255)]
        settings_with_dummy_input._colours = colours
        settings_with_dummy_input.set_colours()
        return settings_with_dummy_input

    def test_set_colours_return_values(self, settings_with_colours):
        colours = [(0, 0, 0), (255, 255, 255)]

        assert settings_with_colours.bg_colour in colours \
               and settings_with_colours.text_colour in colours

    def test_set_colours_return_types(self, settings_with_colours):
        assert type(settings_with_colours.bg_colour) == tuple \
               and type(settings_with_colours.text_colour) == tuple
