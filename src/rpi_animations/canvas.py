from .items import Item, ItemFactory
from .settings import SettingsManager
import pygame as pg


class Canvas:
    def __init__(self, settings_manager: SettingsManager, screen: pg.Surface):
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._screen = screen
        self._perimeter = self._screen.get_rect()
        self._messages = pg.sprite.Group()
        self._message_factory = self._setup_item_factory(self._messages, 'scrolling')
        self._images = pg.sprite.Group()
        self._image_factory = self._setup_item_factory(self._images, 'random')

    def _create_message(self):
        message = self._message_factory(self._settings['message']())
        message.rect.midleft = self._perimeter.midright
        message.movement.speed = self._settings['text_speed'] / self._settings['fps']

    def _create_images(self):
        for _ in range(self._settings['num_images']):
            for image in self._settings['images']:
                self._image_factory(image)

    def _update_messages(self):
        self._messages.update()
        for message in self._messages.sprites():
            if message.rect.right < self._perimeter.left:
                message.kill()
        if all(message.rect.right <= self._perimeter.right for message in self._messages.sprites()):
            self._create_message()

    def _update_images(self):
        group = pg.sprite.Group()
        for image in self._images.sprites():
            self._images.remove(image)
            image.update()
            while pg.sprite.spritecollideany(image, group):
                image.update()
            group.add(image)
        self._images = group

    def _setup_item_factory(self, group: pg.sprite.Group, item_type: str):
        def factory(content: pg.Surface):
            return item_factory.create(group, content, self._perimeter)
        item_factory = ItemFactory(item_type)
        return factory
