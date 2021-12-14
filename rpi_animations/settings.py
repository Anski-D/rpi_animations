import json
import pathlib
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


class SettingsImporter:
    """Imports and validates the user settings.
    """
    def __init__(self):
        """Inits class with settings file string."""
        self._settings = None

    def import_settings(self, settings_loc):
        self._read_settings(settings_loc)
        self._validate_setting()
        self._convert_colours()

        return self._settings

    def _read_settings(self, settings_loc):
        with open(settings_loc, encoding='UTF-8') as settings_file:
            self._settings = json.load(settings_file)

    def _validate_setting(self):
        validate(self._settings, JSON_SCHEMA)

    def _convert_colours(self):
        for key, value in self._settings.items():
            if isinstance(value, list):
                for idx, subvalue in enumerate(value):
                    if isinstance(subvalue, list) and all(isinstance(x, int) for x in subvalue):
                        self._settings[key][idx] = tuple(subvalue)


class SettingsManager:
    def __init__(self, importer, settings_loc):
        self._settings = None
        self._settings_importer = importer
        self._settings_loc = settings_loc

        self._import_settings()

    def _import_settings(self):
        self._settings = self._settings_importer.import_settings(self._settings_loc)


if __name__ == '__main__':
    loc = pathlib.Path('C:\\Users\\david\\PythonProjects\\rpi_animations\\inputs', 'settings.json')
    settings_importer = SettingsImporter(loc)
    settings = settings_importer.import_settings()
    print(settings)
