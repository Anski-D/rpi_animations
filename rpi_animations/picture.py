import random
from .item import Item
import pygame.sprite


class Picture(Item):
    def __init__(self, group, screen_animator, image):
        # Save image src
        self._image = image

        # Run parent class init
        super().__init__(group, screen_animator)

    def _set_item_content(self):
        # Load the image
        self.content = self._image

    def _place_item(self):
        # Place the image in a random location
        self._rect.left = random.randint(0, self._screen_rect.right - self._rect.width)
        self._rect.top = random.randint(0, self._screen_rect.bottom - self._rect.height)

    def update(self, image_group):
        # Try a few times to place it without collision
        # First remove the sprite from groups it is in
        self.remove()

        # Place the image in a new position
        self._place_item()

        # Keep trying to place the image while there is a collision
        for attempt in range(self._settings.reposition_attempts):
            # Check if there is not a collision, in which case can stop the loop
            if not pygame.sprite.spritecollideany(self, image_group):
                break

            # Try placing it again
            self._place_item()

        # Add the image to the new group
        image_group.add(self)
