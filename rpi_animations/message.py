import pygame
from pygame.sprite import Sprite


class Message(Sprite):
    def __init__(self, text_animator: object):
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
        self.x = float(self._msg_rect.x)

        # Set the flag that the message hasn't fully emerged
        self._has_fully_emerged = False

    def _setup_message(self):
        self._set_font()
        self._place_msg()

    def _set_font(self):
        # Set font
        font = pygame.font.SysFont(None, self._settings.text_size)

        # Render text
        self._msg = font.render(self._settings.text, True, self._settings.text_colour)

    def _place_msg(self):
        # Get the message rectangle
        self._msg_rect = self._msg.get_rect()

        # Place the rectangle
        self._msg_rect.midright = self._screen_rect.midleft

    def draw_msg(self):
        # Draw the message
        self._screen.blit(self._msg, self._msg_rect)

    def update(self):
        # Move the message to the right
        self.x += self._settings.text_speed
        self._msg_rect.x = self.x

    def is_on_screen(self):
        # Check if this message is still on the screen
        if self._msg_rect.left >= self._screen_rect.right:
            return False

        return True

    def has_just_emerged(self):
        # Check if the left of message is now on screen
        if not self._has_fully_emerged and self._msg_rect.left >= self._screen_rect.left:
            self._has_fully_emerged = True
            return True

        return False
