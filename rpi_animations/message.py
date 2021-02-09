from .item import Item


class Message(Item):
    def __init__(self, group, screen_animator) -> None:
        super().__init__(group, screen_animator)

        # Store x position as float
        self._x = float(self._rect.x)

        # Set the flag that the message hasn't fully emerged
        self._has_fully_emerged = False

    def _setup_item(self) -> None:
        self._set_text()
        super()._setup_item()

    def _set_text(self) -> None:
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
        # Render text
        self.content = self._font.render(
            self._text,
            self._settings.settings['text_aa'],
            self._settings.text_colour
        )

    def _place_item(self) -> None:
        # Place the rectangle
        self._rect.midleft = self._screen_rect.midright

    def _draw_outline(self) -> None:
        # Repetitively draw the outline
        outline_width = self._settings.settings['outline_width']
        self._screen.blit(self._outline_text, (self._rect.x - outline_width, self._rect.y - outline_width))
        self._screen.blit(self._outline_text, (self._rect.x - outline_width, self._rect.y + outline_width))
        self._screen.blit(self._outline_text, (self._rect.x + outline_width, self._rect.y - outline_width))
        self._screen.blit(self._outline_text, (self._rect.x + outline_width, self._rect.y + outline_width))

    def blit(self) -> None:
        # Draw outline text
        self._draw_outline()

        # Draw the message
        self._set_item_content()
        super().blit()

    def update(self) -> None:
        # Move the message to the right
        self._x -= self._settings.settings['text_speed'] / self._settings.settings['fps']
        self._rect.x = self._x

    def is_on_screen(self) -> bool:
        # Check if this message is still on the screen
        if self._rect.right <= self._screen_rect.left:
            return False

        return True

    def has_just_emerged(self) -> bool:
        # Check if the right of message is now on screen
        if not self._has_fully_emerged and self._rect.right <= self._screen_rect.right:
            self._has_fully_emerged = True
            return True

        return False
