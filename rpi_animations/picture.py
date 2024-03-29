import random
from .item import Item
import pygame.sprite


class Picture(Item):
    """
    Picture feature object in the rpi_animations package.
    """

    def __init__(self, group: pygame.sprite.Group, screen_animator, image) -> None:
        """
        Initialise Picture object with sprite group, screen object, and an image. Run setup methods in parent class.

        Args:
            group (Group): Pygame sprite group to which the object will be added.
            screen_animator (ScreenAnimator): Main package object controlling the animation.
            image (image): A loaded pygame image.
        """
        # Store pygame image
        self._image = image

        # Run parent class __init__
        super().__init__(group, screen_animator)

    def _set_item_content(self) -> None:
        """
        Set the content of the object.

        Returns:
            None
        """
        self.content = self._image

    def _place_item(self) -> None:
        """
        Place the object in a random screen location.

        Returns:
            None
        """
        # Place the image in a random location
        self._rect.left = random.randint(0, self._screen_rect.right - self._rect.width)
        self._rect.top = random.randint(0, self._screen_rect.bottom - self._rect.height)

    def update(self, image_group) -> None:
        """
        Place the object in a new position without colliding with other objects in the group.

        Args:
            image_group (Group): New pygame sprite group.

        Returns:
            None
        """
        # Try a few times to place it without collision
        # First remove the sprite from groups it is in
        self.remove()

        # Place the image in a new position
        self._place_item()

        # Keep trying to place the image while there is a collision
        for attempt in range(self._settings.settings['reposition_attempts']):
            # Check if there is not a collision, in which case can stop the loop
            if not pygame.sprite.spritecollideany(self, image_group):
                break

            # Try placing it again
            self._place_item()

        # Add the image to the new group
        image_group.add(self)
