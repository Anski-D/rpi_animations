import pygame
import sys
from .message import Message
from .picture import Picture
from .settings import Settings


class TextAnimator:
    def __init__(self, settings_file: str):
        """Initialise the animation, and create resources."""

        # Store the message file variable
        self._message_file = settings_file

        # Create the settings file and hold
        self.settings = Settings(settings_file)

        # Initialise pygame
        pygame.init()

        # Set the screen size
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Set the screen title
        pygame.display.set_caption('Text animator')

        # Create the images group
        self._images = pygame.sprite.Group()
        # Create the images
        self._create_images()
        # Set a counter for when images should be updated
        self._image_update_counter = 0

        # Create the messages group
        self._messages = pygame.sprite.Group()
        # Write the first message and add to group
        self._create_message()
        self._text_colour_swap_count = 0

    def run(self):
        """Main loop of the animation."""
        while True:
            # Check for events
            self._check_events()

            # Update the message
            self._update_items()

            # Check the messages for certain criteria
            self._check_items()

            # Draw the message
            self._update_screen()

    def _check_events(self):
        # Watch for events
        for event in pygame.event.get():
            # Check if should quit
            self._check_quit(event)

    @staticmethod
    def _check_quit(event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()

    def _set_bg(self):
        """Set the background of the animation."""
        self.screen.fill(self.settings.bg_colour)

    def _create_images(self):
        # Create all the required images
        for i in range(self.settings.num_images):
            # Create an image of each type
            for image_src in self.settings.image_src:
                # Create an image
                image = Picture(self, image_src)
                # Add image to images
                self._images.add(image)

    def _create_message(self):
        # Create a message
        message = Message(self)

        # Add message to message group
        self._messages.add(message)

    def _check_items(self):
        # Check whether the message has fully emerged on screen, then create another if so.
        for message in self._messages.sprites():
            if message.has_just_emerged():
                self._create_message()

            # If the message has left the screen, get rid of it.
            if not message.is_on_screen():
                message.kill()

    def _update_items(self):
        # Update images
        self._update_images()

        # Update messages
        self._messages.update()

        # Swap colours every so often
        self._change_colours()

    def _update_images(self):
        # Update images when required
        self._image_update_counter += 1
        if self._image_update_counter == self.settings.image_update_counter_limit:
            self._images.update()

            # Reset the counter
            self._image_update_counter = 0

    def _change_colours(self):
        self._text_colour_swap_count += 1
        if self._text_colour_swap_count == self.settings.colour_change_counter_limit:
            # Use the settings method to randomise colours
            self.settings.set_colours()

            # Reset the counter
            self._text_colour_swap_count = 0

    def _update_screen(self):
        # Set the background colour
        self._set_bg()

        # Draw each image
        for image in self._images.sprites():
            image.blitme()

        # Draw each active message
        for message in self._messages.sprites():
            message.draw_msg()

        # Redraw the screen
        pygame.display.flip()
