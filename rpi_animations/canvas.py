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

    def _create_message(self):
        message = Item.create_scrolling_item(self._messages, self._settings['message'], self._perimeter)
        message.movement.speed = self._settings['text_speed'] / self._settings['fps']

    def _create_images(self):
        for _ in range(self._settings['num_images']):
            for image in self._settings['images']:
                Item.create_random_item(self._images, image, self._perimeter)

    def _is_within_perimeter(self, item: Item):
        if self._perimeter.contains(item.rect):
            return True
        return False

    def _is_within_perimeter_right(self, item: Item):
        if item.rect.right <= self._perimeter.right:
            return True
        return False

    def _update_messages(self):
        self._messages.update()
        for message in self._messages.sprites():
            if not self._is_within_perimeter(message):
                message.kill()
        if all(
            self._is_within_perimeter_right(message) for message in self._messages.sprites()
        ):
            self._create_message()
