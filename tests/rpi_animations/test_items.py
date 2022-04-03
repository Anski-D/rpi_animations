import pytest
from rpi_animations.items import Message
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

    def test_message_is_just_within_right_perimeter(self):
        pass
