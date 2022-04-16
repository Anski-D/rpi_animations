from .items import Item
from .settings import SettingsManager
import pygame as pg


class Canvas:
    def __init__(self, settings_manager: SettingsManager):
        self.settings_manager = settings_manager
