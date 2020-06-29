import pygame
import sys


class TextAnimator:
    def __init__(self):
        """Initialise the animation, and create resources."""

        # Initialise pygame
        pygame.init()

        # Set the screen size
        self._screen = pygame.display.set_mode((800, 400))
        # Set the screen title
        pygame.display.set_caption('Text animator')

    def run(self):
        """Main loop of the animation."""

        while True:
            # Watch for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Redraw the screen
                pygame.display.flip()
