from .item import Item


class Message(Item):
    """
    Message feature object in the rpi_animations package.
    """

    def __init__(self, group, screen_animator) -> None:
        """
        Initialise Message object with sprite group and screen object. Run initial setup methods.

        Args:
            group (Group): Pygame sprite group to which the object will be added.
            screen_animator (ScreenAnimator): Main package object controlling the animation.
        """
        super().__init__(group, screen_animator)

        # Store x position as float
        self._x = float(self._rect.x)

        # Set the flag that the message hasn't fully emerged
        self._has_fully_emerged = False

    def _setup_item(self) -> None:
        """
        Run methods to setup the object.

        Returns:
            None
        """
        self._set_text()

        # Run parent method
        super()._setup_item()

    def _set_text(self) -> None:
        """
        Set font, message text, and outline of text.

        Returns:
            None
        """
        # Set font
        self._font = self._settings.font

        # Set the message text
        self._text = self._settings.text

        # Set the outline text
        self._outline_text = self._font.render(
            self._text,
            self._settings.settings['text_aa'],
            self._settings.outline_colour
        )

    def _set_item_content(self) -> None:
        """
        Render the message text.

        Returns:
            None
        """
        self.content = self._font.render(
            self._text,
            self._settings.settings['text_aa'],
            self._settings.text_colour
        )

    def _place_item(self) -> None:
        """
        Set the initial object position on the screen.

        Returns:
            None
        """
        self._rect.midleft = self._screen_rect.midright

    def _draw_outline(self) -> None:
        """
        Draw the message text outline.

        Returns:
            None
        """
        outline_width = self._settings.settings['outline_width']
        self._screen.blit(self._outline_text, (self._rect.x - outline_width, self._rect.y - outline_width))
        self._screen.blit(self._outline_text, (self._rect.x - outline_width, self._rect.y + outline_width))
        self._screen.blit(self._outline_text, (self._rect.x + outline_width, self._rect.y - outline_width))
        self._screen.blit(self._outline_text, (self._rect.x + outline_width, self._rect.y + outline_width))

    def blit(self) -> None:
        """
        Add the object to the pygame screen.

        Returns:
            None
        """
        # Draw outline text
        self._draw_outline()

        # Draw the message
        self._set_item_content()

        # Run parent method
        super().blit()

    def update(self) -> None:
        """
        Move the object position to the left during a frame update.

        Returns:
            None
        """
        self._x -= self._settings.settings['text_speed'] / self._settings.settings['fps']
        self._rect.x = self._x

    def is_on_screen(self) -> bool:
        """
        Determine whether the object is still on the screen.

        Returns:
            bool: True if still on screen, False otherwise.
        """
        if self._rect.right <= self._screen_rect.left:
            return False

        return True

    def has_just_emerged(self) -> bool:
        """
        Determine whether the right side of the message is now visible on the screen.

        Returns:
            bool: True if right edge is now on screen, False otherwise.
        """
        if not self._has_fully_emerged and self._rect.right <= self._screen_rect.right:
            self._has_fully_emerged = True
            return True

        return False
