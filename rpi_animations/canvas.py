from .items import Item
from .settings import SettingsManager
import pygame as pg


class Canvas:
    def __init__(self, settings_manager: SettingsManager, screen: pg.Surface):
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._screen = screen
        self._perimeter = self._screen.get_rect()
        self._messages = pg.sprite.Group()
        self._images = pg.sprite.Group()

    def _create_images(self):
        for _ in range(self._settings['num_images']):
            for image in self._settings['images']:
                Item.create_random_item(self._images, image, self._perimeter)

    def _create_message(self):
        Item.create_scrolling_item(self._messages, self._settings['message'], self._perimeter)
