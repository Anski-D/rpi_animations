import pytest
from rpi_animations.items import Message, Picture
from pygame import Rect


class TestMessage:
    @pytest.fixture
    def message_setup(self, monkeypatch):
        def mock_init(mock_self):
            mock_self._rect = Rect(0, 0, 10, 10)
            mock_self._position = {'x': 100}
            mock_self._settings = {'text_speed': 90.0, 'fps': 30}
            mock_self._perimeter = Rect(0, 0, 1000, 1000)

        monkeypatch.setattr(Message, '__init__', mock_init)
        return Message()

    def test_message_update(self, message_setup):
        ppf = message_setup._settings['text_speed'] / message_setup._settings['fps']
        message_setup.update()

        assert message_setup._position['x'] == 100 - ppf

    def test_message_is_within_left(self, message_setup):
        message_setup._rect.right = message_setup._perimeter.left - 1
        assert not message_setup.is_within_left()

        message_setup._rect.right = message_setup._perimeter.left
        assert message_setup.is_within_left()

        message_setup._rect.right = message_setup._perimeter.left + 1
        assert message_setup.is_within_left()

    def test_message_is_just_within_right(self, message_setup):
        message_setup._is_within_right = True
        message_setup._rect.right = message_setup._perimeter.right - 1
        assert not message_setup.is_just_within_right() and message_setup._is_within_right

        message_setup._is_within_right = True
        message_setup._rect.right = message_setup._perimeter.right
        assert not message_setup.is_just_within_right() and message_setup._is_within_right

        message_setup._is_within_right = True
        message_setup._rect.right = message_setup._perimeter.right + 1
        assert not message_setup.is_just_within_right() and message_setup._is_within_right

        message_setup._is_within_right = False
        message_setup._rect.right = message_setup._perimeter.right - 1
        assert message_setup.is_just_within_right() and message_setup._is_within_right

        message_setup._is_within_right = False
        message_setup._rect.right = message_setup._perimeter.right
        assert message_setup.is_just_within_right() and message_setup._is_within_right

        message_setup._is_within_right = False
        message_setup._rect.right = message_setup._perimeter.right + 1
        assert not message_setup.is_just_within_right() and not message_setup._is_within_right


class TestPicture:
    @pytest.fixture
    def common(self):
        pytest._perimeter_width = 1000
        pytest._perimeter_height = 1000

    @pytest.fixture
    def picture_setup(self, common, monkeypatch):
        def mock_init(mock_self):
            mock_self._rect = Rect(0, 0, 10, 10)
            mock_self._perimeter = Rect(0, 0, pytest._perimeter_width, pytest._perimeter_height)

        monkeypatch.setattr(Picture, '__init__', mock_init)
        return Picture()

    def test_picture_set_position(self, common, picture_setup):
        picture_setup._set_position()
        assert picture_setup._rect.top >= 0 \
            and picture_setup._rect.left >= 0 \
            and picture_setup._rect.bottom <= pytest._perimeter_height \
            and picture_setup._rect.right <= pytest._perimeter_width
