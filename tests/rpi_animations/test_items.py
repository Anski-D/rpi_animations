import pytest
from rpi_animations.items import Message
from pygame import Rect

class TestMessage:
    @pytest.fixture
    def message_setup(self, monkeypatch):
        def mock_init(self):
            self._settings = {'text_speed': 90.0, 'fps': 30}
            self._position = {'x': 100}
            self._rect = Rect(0, 0, 1, 1)

        monkeypatch.setattr(Message, '__init__', mock_init)
        return Message()

    def test_message_update(self, message_setup):
        ppf = message_setup._settings['text_speed'] / message_setup._settings['fps']
        message_setup.update()

        assert message_setup._position['x'] == 100 - ppf
