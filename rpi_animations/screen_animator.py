import sys

import pygame

from .message import Message
from .picture import Picture
from .settings import Settings


class ScreenAnimator:
    """
    ScreenAnimator object that sets up and runs the main animation loop of the rpi_animation program.

    Attributes:
        settings (Settings): A Settings object that loads, stores, and updates settings as the program runs.
        screen (screen): A pygame screen object that holds the pygame animation features.
    """

    def __init__(self, settings_file: str, debug_mode=False, fps_on=False) -> None:
        """
        Initialise ScreenAnimator object with the resource location and settings file. Create initial animation
        features.

        Args:
            settings_file (str): The settings JSON file from where the settings are loaded.
            debug_mode (bool): Boolean switch for activating debug mode which will run the program in windowed mode.
                Defaults to False.
            fps_on (bool): Boolean switch for activating the fps counter as part of the animation.
                Defaults to False.
        """
        # Initialise pygame
        pygame.init()

        # Create the settings file and hold
        self.settings = Settings(settings_file)

        # Set the screen size
        if debug_mode:
            self.screen = pygame.display.set_mode((800, 480))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Determine if fps counter should be shown
        self._fps_on = fps_on

        # Set the screen title
        pygame.display.set_caption('RPi_Animations')

        # Create groups
        self._create_images_group()
        self._create_messages_group()

        # Set initial time variables
        self._image_change_time = pygame.time.get_ticks()
        self._colour_change_time = pygame.time.get_ticks()

        # Add clock
        self._clock = pygame.time.Clock()

    def _create_images_group(self) -> None:
        """
        Create the group of images.

        Returns:
            None
        """
        # Create the images group
        self._images = pygame.sprite.Group()
        # Create the images
        self._create_images()

    def _create_messages_group(self) -> None:
        """
        Create the group of messages.

        Returns:
            None
        """
        # Create the messages group
        self._messages = pygame.sprite.Group()
        # Create a message
        self._create_message()

    def run(self) -> None:
        """
        Run main execution loop of the program. A series of methods check the state of the program nd update as
        required.

        Returns:
            None
        """
        # Run a continuous loop
        while True:
            # Set the FPS
            self._clock.tick(self.settings.settings['fps'])

            # Check for events
            self._check_events()

            # Update the items
            self._update_items()

            # Check the items for certain criteria
            self._check_items()

            # Draw the animations
            self._update_screen()

    def _check_events(self) -> None:
        """
        Check through all the pygame events and then use methods to check if certain criteria are met.

        Returns:
            None
        """
        # Loop through each event
        for event in pygame.event.get():
            # Check if should quit
            self._check_quit(event)

    @staticmethod
    def _check_quit(event: pygame.event) -> None:
        """
        Check whether any of the pygame events meet the criteria for exiting the program, then exit the program if
        there are.

        Args:
            event (event): An event in pygame.

        Returns:
            None
        """
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()

    def _set_bg(self) -> None:
        """
        Set the background colour of the animation.

        Returns:
            None
        """
        self.screen.fill(self.settings.bg_colour)

    def _create_images(self) -> None:
        """
        Create a number of Picture objects, depending on image source and number of each image requested.

        Returns:
            None
        """
        # Create all the required images
        for i in range(self.settings.settings['num_images']):
            # Create an image of each type
            for image in self.settings.images:
                # Create an image
                Picture(self._images, self, image)

    def _create_message(self) -> None:
        """
        Creates a Message object.

        Returns:
            None
        """
        Message(self._messages, self)

    def _check_items(self) -> None:
        """
        Check whether the messages on screen have met certain criteria, then run specific methods depending on
        criteria met.

        Returns:
            None
        """
        # Loop through each message
        for message in self._messages.sprites():
            # Check whether the message has fully emerged on screen, then create another if so
            if message.has_just_emerged():
                self._create_message()

            # If the message has left the screen, get rid of it
            if not message.is_on_screen():
                message.kill()

    def _update_items(self) -> None:
        """
        Run update methods for the different animations features.

        Returns:
            None
        """
        # Update images
        self._update_images()

        # Update messages
        self._messages.update()

        # Swap colours every so often
        self._change_colours()

    def _update_images(self) -> None:
        """
        Check whether enough clock time has passed to update the image positions, run image update method it it has.

        Returns:
            None
        """
        # Get the current clock time
        image_change_time_new = pygame.time.get_ticks()

        # Check whether time passed since last image change update has reached the change limit
        if image_change_time_new - self._image_change_time >= self.settings.settings['image_change_time'] * 1000:
            # Update time measurement with new time
            self._image_change_time = image_change_time_new

            # Create a new group for the images
            image_group_new = pygame.sprite.Group()

            # Move the images
            self._images.update(image_group_new)
            self._images = image_group_new

    def _change_colours(self) -> None:
        """
        Check whether enough clock time has passed to update the colours used, run colour update method it it has.

        Returns:
            None
        """
        # Get the current clock time
        colour_change_time_new = pygame.time.get_ticks()

        # Check whether time passed since last colour change update has reached the change limit
        if colour_change_time_new - self._colour_change_time >= self.settings.settings['colour_change_time'] * 1000:
            # Update time measurement with new time
            self._colour_change_time = colour_change_time_new

            # Use the settings method to randomise colours
            self.settings.set_colours()

    def _update_screen(self) -> None:
        """
        Update all aspects of the animation, and show the new frame.

        Returns:
            None
        """
        # Set the background colour
        self._set_bg()

        # Draw each image
        for image in self._images.sprites():
            image.blit()

        # Draw each active message
        for message in self._messages.sprites():
            message.blit()

        # Draw optional fps counter
        if self._fps_on:
            self._draw_fps()

        # Redraw the screen
        pygame.display.flip()

    def _draw_fps(self):
        """
        Draw the measured frames per second value that the animation is running at on the screen animation.

        Returns:
            None
        """
        fps_font = pygame.font.SysFont(self.settings.settings['typeface'], 36)
        text = f'{self._clock.get_fps():.2f}'
        content = fps_font.render(text, True, (0, 0, 0))
        rect = content.get_rect()
        rect.x = 10
        rect.y = 10
        self.screen.blit(content, rect)
