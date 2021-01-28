from rpi_animations.settings import Settings
import pytest
import pygame
import os


class TestSettings:
    @pytest.fixture
    def common(self):
        pytest.colours_in = '0,0,0;255,255,255'
        pytest.colours_out = [(0, 0, 0), (255, 255, 255)]

        pytest.messages_in = 'Test1;Test2;Test3'
        pytest.messages_out = ['Test1', 'Test2', 'Test3']

        pytest.message_sep = '   '

        pytest.image_sources_in = 'test1.bmp;test2.bmp;test3.bmp'
        pytest.image_sources_out = [os.path.join('test', file) for file in ['test1.bmp', 'test2.bmp', 'test3.bmp']]

    @pytest.fixture
    def settings_with_dummy_input(self, monkeypatch):
        monkeypatch.setattr(Settings, '_load_settings', lambda x: None)
        class_input_dir = 'test'
        class_input_file = 'test.json'
        return Settings(class_input_dir, class_input_file)

    def test_settings_init_values(self, settings_with_dummy_input):
        assert settings_with_dummy_input._settings_file == 'test.json' \
               and settings_with_dummy_input.bg_colour == (0, 0, 0) \
               and settings_with_dummy_input.text_colour == (0, 0, 0) \
               and settings_with_dummy_input.outline_colour == (0, 0, 0)

    def test_setting_init_types(self, settings_with_dummy_input):
        assert type(settings_with_dummy_input._settings_file) == str \
               and type(settings_with_dummy_input.bg_colour) == tuple \
               and type(settings_with_dummy_input.text_colour) == tuple \
               and type(settings_with_dummy_input.outline_colour) == tuple

    def test_load_settings(self, common, monkeypatch):
        settings_dict = {
            "colours": pytest.colours_in,
            "text": pytest.messages_in,
            "message_sep": pytest.message_sep,
            "typeface": "Serif Regular",
            "text_size": 7,
            "text_speed": 7,
            "outline_width": 7,
            "outline_colours": pytest.colours_in,
            "image_sources": pytest.image_sources_in,
            "num_images": 7,
            "image_change_time": 7,
            "colour_change_time": 7,
            "fps": 7,
            "reposition_attempts": 7
        }
        monkeypatch.setattr(Settings, '_load_json', lambda x: settings_dict)
        monkeypatch.setattr(Settings, '_load_images', lambda x, y: None)
        settings_dummy = Settings('test', 'test.json')

        assert settings_dummy._colours == pytest.colours_out \
               and settings_dummy._messages == pytest.messages_out \
               and settings_dummy._message_sep == pytest.message_sep \
               and settings_dummy.typeface is None \
               and settings_dummy.text_size == 7 \
               and settings_dummy.text_speed == 7 \
               and settings_dummy.outline_width == 7 \
               and settings_dummy._outline_colours == pytest.colours_out \
               and settings_dummy.num_images == 7 \
               and settings_dummy.image_change_time == 7 \
               and settings_dummy.colour_change_time == 7 \
               and settings_dummy.fps == 7 \
               and settings_dummy.reposition_attempts == 7

        # self._colours = self._split_colours(settings['colours'])
        # self._load_images(settings['image_src'])

    def test_load_json_type(self):
        assert type(Settings('inputs', 'settings_example.json')._load_json()) == dict

    @pytest.fixture
    def settings_split_colours(self, common):
        return Settings._split_colours(pytest.colours_in)

    def test_split_colours_return_value(self, common, settings_split_colours):
        assert settings_split_colours == pytest.colours_out

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

    def test_text(self, common, settings_with_dummy_input):
        settings_with_dummy_input._messages = pytest.messages_out
        settings_with_dummy_input._message_sep = pytest.message_sep
        assert settings_with_dummy_input.text in [f'{message}{pytest.message_sep}' for message in pytest.messages_out]

    @pytest.fixture
    def settings_with_colours(self, common, settings_with_dummy_input):
        settings_with_dummy_input._colours = pytest.colours_out
        settings_with_dummy_input._outline_colours = pytest.colours_out
        settings_with_dummy_input.set_colours()
        return settings_with_dummy_input

    def test_set_colours_return_values(self, common, settings_with_colours):
        assert settings_with_colours.bg_colour in pytest.colours_out \
               and settings_with_colours.text_colour in pytest.colours_out \
               and settings_with_colours.outline_colour in pytest.colours_out

    def test_set_colours_return_types(self, settings_with_colours):
        assert type(settings_with_colours.bg_colour) == tuple \
               and type(settings_with_colours.text_colour) == tuple \
               and type(settings_with_colours.outline_colour) == tuple

    @pytest.fixture
    def settings_return_images(self, common, settings_with_dummy_input, monkeypatch):
        monkeypatch.setattr(pygame.image, 'load', lambda x: x)
        settings_with_dummy_input._load_images(pytest.image_sources_in)
        return settings_with_dummy_input

    def test_load_images_return_values(self, common, settings_return_images):
        assert settings_return_images.images == pytest.image_sources_out

    def test_load_images_length(self, common, settings_return_images):
        assert len(settings_return_images.images) == len(pytest.image_sources_out)
