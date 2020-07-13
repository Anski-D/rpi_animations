import pygame
import sys
from time import time
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
        # self.screen = pygame.display.set_mode((800, 600))  # Test screen size

        # Set the screen title
        pygame.display.set_caption('Text animator')

        # Create groups
        self._create_images_group()
        self._create_messages_group()

        # Set initial time variables
        self._image_change_time = time()
        self._colour_change_time = time()

    def _create_images_group(self):
        # Create the images group
        self._images = pygame.sprite.Group()
        # Create the images
        self._create_images()

    def _create_messages_group(self):
        # Create the messages group
        self._messages = pygame.sprite.Group()
        # Write the first message and add to group
        self._create_message()

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
                Picture(self._images, self, image_src)

    def _create_message(self):
        # Create a message
        Message(self._messages, self)

    def _check_items(self):
        # Check whether the message has fully emerged on screen, then create another if so.
        for message in self._messages.sprites():
            if message.has_just_emerged():
                # Create a new message
                self._create_message()
                # Check if the number of messages is more than required, delete if so.
                if len(self._messages.sprites()) > self._reqd_num_of_messages():
                    # Check which message is now off screen
                    for sprite in self._messages.sprites():
                        # Get rid of the message if of screen
                        if not sprite.is_on_screen():
                            sprite.kill()

    def _reqd_num_of_messages(self):
        # Work out how many rectangles fit on the screen, pad by 2 because that is the minimum required if the
        # message is wider than the screen.
        return int(self.screen.get_rect().width / min(message.rect.width for message in self._messages.sprites())) + 2

    def _update_items(self):
        # Update images
        self._update_images()

        # Update messages
        self._messages.update()

        # Swap colours every so often
        self._change_colours()

    def _update_images(self):
        # Update images when required
        image_change_time_new = time()
        if image_change_time_new - self._image_change_time >= self.settings.image_change_time:
            # Move the images
            self._images.update()
            self._image_change_time = image_change_time_new

    def _change_colours(self):
        # Update colours when required
        colour_change_time_new = time()
        if colour_change_time_new - self._colour_change_time >= self.settings.colour_change_time:
            # Use the settings method to randomise colours
            self.settings.set_colours()
            self._colour_change_time = colour_change_time_new

    def _update_screen(self):
        # Set the background colour
        self._set_bg()

        # Draw each image
        for image in self._images.sprites():
            image.blit()

        # Draw each active message
        for message in self._messages.sprites():
            message.blit()

        # Redraw the screen
        pygame.display.flip()
