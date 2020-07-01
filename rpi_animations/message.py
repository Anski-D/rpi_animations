import pygame
from pygame.sprite import Sprite
import json


class Message(Sprite):
    def __init__(self, text_animator: object, message_file: str):
        super().__init__()

        # Save the text animator
        self._screen = text_animator.screen
        # Get the size of the text animator rectangle
        self._screen_rect = self._screen.get_rect()

        # Load the message from the json file
        self._load_message(message_file)

        # Setup the message
        self._setup_message()

        # Store x position as float
        self.x = float(self._msg_rect.x)

    def _load_message(self, message_file: str):
        message = self._load_json(message_file)

        # Split the dictionary
        self.bg_colour = tuple(map(int, message['bg_colour'].split(',')))
        self.text_colour = tuple(map(int, message['text_colour'].split(',')))
        self.text = message['text']
        self.text_size = int(message['text_size'])
        self.text_speed = float(message['text_speed'])

    @staticmethod
    def _load_json(message_file: str):
        # Open the json file safely
        with open(message_file) as msg_file:
            # Load the json
            return json.load(msg_file)

    def _setup_message(self):
        self._set_font()
        self._place_msg()

    def _set_font(self):
        # Set font
        font = pygame.font.SysFont(None, self.text_size)

        # Render text
        self._msg = font.render(self.text, True, self.text_colour)

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
        self.x += self.text_speed
        self._msg_rect.x = self.x

    def is_on_screen(self):
        # Check if this message is still on the screen
        if self._msg_rect.left >= self._screen_rect.right:
            return False

        return True

    def is_at_screen_left(self):
        # Check if the left of message is now on screen
        if self._msg_rect.left == self._screen_rect.left:
            return True

        return False
