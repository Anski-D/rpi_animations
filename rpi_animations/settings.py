import json
import pathlib


class SettingsImporter:
    """Imports and validates the user settings.
    """
    def __init__(self, settings_loc):
        """Inits class with settings file string."""
        self._settings = None
        self._settings_loc = settings_loc

    def import_settings(self):
        self._read_settings()
        self._convert_colours()

        return self._settings

    def _read_settings(self):
        with open(self._settings_loc) as f:
            self._settings = json.load(f)

    def _convert_colours(self):
        for key, value in self._settings.items():
            if isinstance(value, list):
                for idx, subvalue in enumerate(value):
                    if isinstance(subvalue, list) and all(isinstance(x, int) for x in subvalue):
                        self._settings[key][idx] = tuple(subvalue)


if __name__ == '__main__':
    loc = pathlib.Path('C:\\Users\\david\\PythonProjects\\rpi_animations\\inputs', 'settings.json')
    settings_importer = SettingsImporter(loc)
    settings = settings_importer.import_settings()
    print(settings)
