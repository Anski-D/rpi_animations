import pygame
import sys
from rpi_animations.message import Message


class TextAnimator:
    def __init__(self, message_file: str):
        """Initialise the animation, and create resources."""

        # Initialise pygame
        pygame.init()

        # Set the screen size
        self._screen = pygame.display.set_mode((800, 400))
        # Set the screen title
        pygame.display.set_caption('Text animator')

        # Create the message
        self._message = Message(self, message_file)

    def run(self):
        """Main loop of the animation."""
        while True:
            # Watch for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Set the background colour
            self._set_bg()

            # Redraw the screen
            pygame.display.flip()

    def _set_bg(self):
        """Set the background of the animation."""
        self._screen.fill(self._message.bg_colour)
