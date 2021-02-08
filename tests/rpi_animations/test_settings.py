from rpi_animations.settings import Settings
import pytest
import pygame
import importlib.resources


class TestSettings:
    @pytest.fixture
    def common(self):
        pytest.colours_in = '0,0,0;255,255,255'
        pytest.colours_out = [(0, 0, 0), (255, 255, 255)]

        pytest.messages_in = 'Test1;Test2;Test3'
        pytest.messages_out = ['Test1', 'Test2', 'Test3']

        pytest.message_sep = '   '
        pytest.typeface = 'freeserif'

        pytest.image_sources_in = 'test1.bmp;test2.bmp;test3.bmp'
        pytest.image_sources_out = ['test1.bmp', 'test2.bmp', 'test3.bmp']

        pytest.settings_dict = {
            'colours': pytest.colours_in,
            'messages': pytest.messages_in,
            'message_sep': pytest.message_sep,
            'typeface': 'freeserif',
            'text_size': 7,
            'bold_text': 1,
            'italic_text': 1,
            'text_aa': 1,
            'text_speed': 7.0,
            'outline_width': 7,
            'outline_colours': pytest.colours_in,
            'image_sources': pytest.image_sources_in,
            'num_images': 7,
            'image_change_time': 7,
            'colour_change_time': 7,
            'fps': 7,
            'reposition_attempts': 7
        }

    @pytest.fixture
    def settings_with_dummy_input(self, monkeypatch):
        monkeypatch.setattr(Settings, '_load_settings', lambda x: None)
        class_input_file = 'test.json'
        return Settings(class_input_file)

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
        monkeypatch.setattr(Settings, '_load_json', lambda x: pytest.settings_dict)
        monkeypatch.setattr(Settings, '_process_settings', lambda x: None)
        settings_dummy = Settings('test.json')

        assert settings_dummy.settings['colours'] == pytest.colours_in \
               and settings_dummy.settings['messages'] == pytest.messages_in \
               and settings_dummy.settings['message_sep'] == pytest.message_sep \
               and settings_dummy.settings['typeface'] == pytest.typeface \
               and settings_dummy.settings['text_size'] == 7 \
               and settings_dummy.settings['bold_text'] == 1 \
               and settings_dummy.settings['italic_text'] == 1 \
               and settings_dummy.settings['text_aa'] == 1 \
               and settings_dummy.settings['text_speed'] == 7 \
               and settings_dummy.settings['outline_width'] == 7 \
               and settings_dummy.settings['outline_colours'] == pytest.colours_in \
               and settings_dummy.settings['image_sources'] == pytest.image_sources_in \
               and settings_dummy.settings['num_images'] == 7 \
               and settings_dummy.settings['image_change_time'] == 7 \
               and settings_dummy.settings['colour_change_time'] == 7 \
               and settings_dummy.settings['fps'] == 7 \
               and settings_dummy.settings['reposition_attempts'] == 7

        # self._colours = self._split_colours(settings['colours'])
        # self._load_images(settings['image_src'])

    def test_process_settings_values(self, common, monkeypatch):
        monkeypatch.setattr(Settings, '_load_json', lambda x: pytest.settings_dict)
        monkeypatch.setattr(Settings, '_set_parameters', lambda x: None)
        settings_dummy = Settings('test.json')

        assert settings_dummy.settings['colours'] == pytest.colours_out \
               and settings_dummy.settings['messages'] == pytest.messages_out \
               and settings_dummy.settings['bold_text'] is True \
               and settings_dummy.settings['italic_text'] is True \
               and settings_dummy.settings['text_aa'] is True \
               and settings_dummy.settings['outline_colours'] == pytest.colours_out \
               and settings_dummy.settings['image_sources'] == pytest.image_sources_out

    def test_process_settings_types(self, common, monkeypatch):
        monkeypatch.setattr(Settings, '_load_json', lambda x: pytest.settings_dict)
        monkeypatch.setattr(Settings, '_set_parameters', lambda x: None)
        settings_dummy = Settings('test.json')

        assert type(settings_dummy.settings['colours']) is list \
               and type(settings_dummy.settings['messages']) is list \
               and type(settings_dummy.settings['message_sep']) is str \
               and type(settings_dummy.settings['typeface']) is str \
               and type(settings_dummy.settings['text_size']) is int \
               and type(settings_dummy.settings['bold_text']) is bool \
               and type(settings_dummy.settings['italic_text']) is bool \
               and type(settings_dummy.settings['text_aa']) is bool \
               and type(settings_dummy.settings['text_speed']) is float \
               and type(settings_dummy.settings['outline_width']) is int \
               and type(settings_dummy.settings['outline_colours']) is list \
               and type(settings_dummy.settings['image_sources']) is list \
               and type(settings_dummy.settings['num_images']) is int \
               and type(settings_dummy.settings['image_change_time']) is float \
               and type(settings_dummy.settings['colour_change_time']) is float \
               and type(settings_dummy.settings['fps']) is int \
               and type(settings_dummy.settings['reposition_attempts']) is int

    def test_load_json_type(self, monkeypatch):
        monkeypatch.setattr(Settings, '_load_settings', lambda x: None)
        assert type(Settings('settings_example.json')._load_json()) is dict

    @pytest.fixture
    def settings_split_colours(self, common):
        return Settings._split_colours(pytest.colours_in)

    def test_split_colours_return_value(self, common, settings_split_colours):
        assert settings_split_colours == pytest.colours_out

    def test_split_colours_return_type(self, settings_split_colours):
        # Check expected type of split colours
        assert type(settings_split_colours) is list

    def test_split_colours_return_contents(self, settings_split_colours):
        # Check each item in list is a tuple
        is_tuple = [type(colour) is tuple for colour in settings_split_colours]

        assert all(is_tuple)

    def test_text(self, common, settings_with_dummy_input):
        settings_with_dummy_input._settings = {'messages': pytest.messages_out, 'message_sep': pytest.message_sep}
        assert settings_with_dummy_input.text in [f'{message}{pytest.message_sep}' for message in pytest.messages_out]

    @pytest.fixture
    def settings_with_colours(self, common, settings_with_dummy_input):
        settings_with_dummy_input._settings = {'colours': pytest.colours_out, 'outline_colours': pytest.colours_out}
        settings_with_dummy_input.set_colours()
        return settings_with_dummy_input

    def test_set_colours_return_values(self, common, settings_with_colours):
        assert settings_with_colours.bg_colour in pytest.colours_out \
               and settings_with_colours.text_colour in pytest.colours_out \
               and settings_with_colours.outline_colour in pytest.colours_out

    def test_set_colours_return_types(self, settings_with_colours):
        assert type(settings_with_colours.bg_colour) is tuple \
               and type(settings_with_colours.text_colour) is tuple \
               and type(settings_with_colours.outline_colour) is tuple

    @pytest.fixture
    def settings_return_images(self, common, settings_with_dummy_input, monkeypatch):
        monkeypatch.setattr(importlib.resources, 'open_binary', lambda x, y: y)
        monkeypatch.setattr(pygame.image, 'load', lambda x: x)
        settings_with_dummy_input._settings = {'image_sources': pytest.image_sources_out}
        settings_with_dummy_input._load_images()
        return settings_with_dummy_input

    def test_load_images_return_values(self, common, settings_return_images):
        assert settings_return_images.images == pytest.image_sources_out

    def test_load_images_length(self, common, settings_return_images):
        assert len(settings_return_images.images) == len(pytest.image_sources_out)

    def test_load_single_image_return(self, settings_with_dummy_input):
        # Check what happens if non existent file
        assert settings_with_dummy_input._load_single_image('random.bmp') is None
