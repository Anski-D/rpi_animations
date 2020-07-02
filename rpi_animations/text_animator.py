import pygame
import sys
from rpi_animations.message import Message


class TextAnimator:
    def __init__(self, message_file: str):
        """Initialise the animation, and create resources."""

        # Store the message file variable
        self._message_file = message_file

        # Initialise pygame
        pygame.init()

        # Set the screen size
        self.screen = pygame.display.set_mode((800, 400))
        # Set the screen title
        pygame.display.set_caption('Text animator')

        # Create the messages group
        self._messages = pygame.sprite.Group()
        # Write the first message and add to group
        self._create_message()

    def run(self):
        """Main loop of the animation."""
        while True:
            # Watch for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Update the message
            self._update_messages()

            # Check the messages for certain criteria
            self._check_messages()

            # Draw the message
            self._update_screen()

    def _set_bg(self):
        """Set the background of the animation."""
        self.screen.fill(self._messages.sprites()[0].bg_colour)

    def _create_message(self):
        # Create a message
        message = Message(self, self._message_file)

        # Add message to message group
        self._messages.add(message)

    def _check_messages(self):
        for message in self._messages.sprites():
            if not message.is_on_screen():
                message.kill()

            if message.is_at_screen_left():
                self._create_message()

    def _update_screen(self):
        # Set the background colour
        self._set_bg()

        # Draw each active message
        for message in self._messages.sprites():
            message.draw_msg()

        # Redraw the screen
        pygame.display.flip()

    def _update_messages(self):
        self._messages.update()
