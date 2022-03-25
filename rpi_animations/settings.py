import json
import random
from jsonschema import validate

JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "colours": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 255
                }
            }
        },
        "messages": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "message_sep": {
            "type": "string"
        },
        "typeface": {
            "type": "string"
        },
        "text_size": {
            "type": "integer"
        },
        "bold_text": {
            "type": "integer"
        },
        "italic_text": {
            "type": "integer"
        },
        "text_aa": {
            "type": "integer"
        },
        "text_speed": {
            "type": "number"
        },
        "outline_width": {
            "type": "integer"
        },
        "outline_colours": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 255
                }
            }
        },
        "image_sources": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "num_images": {
            "type": "integer"
        },
        "image_change_time": {
            "type": "integer"
        },
        "colour_change_time": {
            "type": "integer"
        },
        "fps": {
            "type": "integer"
        },
        "reposition_attempts": {
            "type": "integer"
        }
    },
    "required": [
        "colours",
        "messages",
        "message_sep",
        "typeface",
        "text_size",
        "bold_text",
        "italic_text",
        "text_aa",
        "text_speed",
        "outline_width",
        "outline_colours",
        "image_sources",
        "num_images",
        "image_change_time",
        "colour_change_time",
        "fps",
        "reposition_attempts"
    ]
}


class SettingsManager:
    def __init__(self, importer: 'SettingsImporter', settings_loc: str):
        """

        Args:
            importer:
            settings_loc:
        """

        self._importer = importer
        self._settings = self._import_settings(settings_loc)
        self._settings['text'] = self._generate_message
        self._setup_settings()

    @property
    def settings(self):
        return self._settings

    def set_colours(self):
        """

        """
        # Select a random background colour
        self._settings['bg_colour'] = random.choice(self.settings['colours'])

        # Allocate a different text colour. Need to do this initial one, otherwise it won't change if already
        # different from the background.
        self._settings['text_colour'] = random.choice(self.settings['colours'])
        # If there is a clash, keep trying
        while self._settings['text_colour'] == self._settings['bg_colour']:
            self._settings['text_colour'] = random.choice(self.settings['colours'])

        # Set the outline colour
        self._settings['outline_colour'] = random.choice(self.settings['outline_colours'])

    def _import_settings(self, settings_loc: str) -> dict:
        return self._importer.import_settings(settings_loc)

    def _generate_message(self) -> str:
        return f"{random.choice(self.settings['messages'])}{self.settings['message_sep']}"

    def _setup_settings(self):
        self.set_colours()


class SettingsImporter:
    """Imports and validates the user settings.
    """
    def __init__(self):
        """Inits class with settings file string."""
        self._settings = None

    def import_settings(self, settings_loc: str) -> dict:
        """

        Args:
            settings_loc:

        Returns:

        """
        self._read_settings(settings_loc)
        self._validate_settings()
        self._convert_colours()

        return self._settings

    def _read_settings(self, settings_loc: str):
        """

        Args:
            settings_loc:
        """
        with open(settings_loc, encoding='UTF-8') as settings_file:
            self._settings = json.load(settings_file)

    def _validate_settings(self):
        """

        """
        validate(self._settings, JSON_SCHEMA)

    def _convert_colours(self):
        """

        """
        for key, value in self._settings.items():
            if isinstance(value, list):
                for idx, subvalue in enumerate(value):
                    if isinstance(subvalue, list) and all(isinstance(x, int) for x in subvalue):
                        self._settings[key][idx] = tuple(subvalue)
