import importlib

from . import default_settings


class Setting:
    def __init__(self):
        self._settings = {}
        self.from_object(default_settings)

        try:
            project_settings = importlib.import_module('settings')
        except ImportError:
            pass
        else:
            self.from_object(project_settings)

    @staticmethod
    def _is_attr(key):
        return str.isupper(key)

    def from_object(self, obj):
        for key, value in vars(obj).items():
            if self._is_attr(key):
                self._settings[key] = value

    def get(self, name, default=None):
        return self._settings.get(name, default)
