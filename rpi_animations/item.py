from abc import ABC, abstractmethod

from pygame.sprite import Sprite


class Item(ABC, Sprite):
    """
    Item object that holds the content and position for a single feature in the rpi_animation program.
    """

    def __init__(self, group, screen_animator):
        """
        Initialise Item object with sprite group and screen object. Run initial setup methods.

        Args:
            group (Group): Pygame sprite group to which the object will be added.
            screen_animator (ScreenAnimator): Main package object controlling the animation.
        """

        # Run the parent __init__
        super().__init__(group)

        # Set default values
        self._content = None
        self._rect = None

        # Get the settings
        self._settings = screen_animator.settings

        # Save main screen animator
        self._screen = screen_animator.screen
        # Get the size of the text animator screen rectangle
        self._screen_rect = self._screen.get_rect()

        # Setup the item
        self._setup_item()

    def _setup_item(self) -> None:
        """
        Run methods to setup the object.

        Returns:
            None
        """

        self._set_item_content()
        self._place_item()

    @property
    def content(self):
        """
        Return the content of the object.

        Returns:
            The main content of the object.
        """

        return self._content

    @content.setter
    def content(self, content) -> None:
        """
        Set the content of the object. Get the rectangular pygame frame.

        Args:
            content: The content to store in the object.

        Returns:
            None
        """

        self._content = content

        # If the rectangle has not been found, get it.
        if self._rect is None:
            self._rect = self._content.get_rect()

    @property
    def rect(self):
        """
        Return the rectangular pygame frame, once set.

        Returns:
            The rectangular pygame frame of the object content. None, if content not set.
        """

        return self._rect

    @abstractmethod
    def _set_item_content(self):
        """
        Set the object content. To be implemented by child class.

        Returns:
            None
        """

        pass

    @abstractmethod
    def _place_item(self):
        """
        Place the object. To be implemented by child class.

        Returns:
            None
        """

        pass

    def blit(self) -> None:
        """
        Add the object to the pygame screen.

        Returns:
            None
        """

        self._screen.blit(self._content, self._rect)
