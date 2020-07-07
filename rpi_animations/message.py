import pygame
from pygame.sprite import Sprite


class Message(Sprite):
    def __init__(self, text_animator):
        super().__init__()

        # Get the settings
        self._settings = text_animator.settings

        # Save the text animator
        self._screen = text_animator.screen
        # Get the size of the text animator rectangle
        self._screen_rect = self._screen.get_rect()

        # Setup the message
        self._setup_message()

        # Store x position as float
        self.x = float(self.rect.x)

        # Set the flag that the message hasn't fully emerged
        self._has_fully_emerged = False

    def _setup_message(self):
        self._set_font()
        self._render_text()
        self._place_msg()

    def _set_font(self):
        # Set font
        self._font = pygame.font.SysFont(self._settings.typeface, self._settings.text_size)

    def _render_text(self):
        # Render text
        self._msg = self._font.render(self._settings.text, True, self._settings.text_colour)

    def _place_msg(self):
        # Get the message rectangle
        self.rect = self._msg.get_rect()

        # Place the rectangle
        self.rect.midleft = self._screen_rect.midright

    def _draw_outline(self):
        # Set the outline text
        outline_text = self._font.render(self._settings.text, True, self._settings.outline_colour)

        # Repetitively draw the outline
        outline_width = self._settings.outline_width
        self._screen.blit(outline_text, (self.rect.x - outline_width, self.rect.y - outline_width))
        self._screen.blit(outline_text, (self.rect.x - outline_width, self.rect.y + outline_width))
        self._screen.blit(outline_text, (self.rect.x + outline_width, self.rect.y - outline_width))
        self._screen.blit(outline_text, (self.rect.x + outline_width, self.rect.y + outline_width))

    def draw_msg(self):
        # Draw outline text
        self._draw_outline()

        # Draw the message
        self._render_text()
        self._screen.blit(self._msg, self.rect)

    def update(self):
        # Move the message to the right
        self.x -= self._settings.text_speed
        self.rect.x = self.x

    def is_on_screen(self):
        # Check if this message is still on the screen
        if self.rect.right <= self._screen_rect.left:
            return False

        return True

    def has_just_emerged(self):
        # Check if the right of message is now on screen
        if not self._has_fully_emerged and self.rect.right <= self._screen_rect.right:
            self._has_fully_emerged = True
            return True

        return False
