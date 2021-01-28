import pygame
import sys
from .message import Message
from .picture import Picture
from .settings import Settings


class TextAnimator:
    def __init__(self, resource_loc: str, settings_file: str) -> None:
        """Initialise the animation, and create resources."""

        # Create the settings file and hold
        self.settings = Settings(resource_loc, settings_file)

        # Initialise pygame
        pygame.init()

        # Set the screen size
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((800, 480))  # Test screen size

        # Set the screen title
        pygame.display.set_caption('Text animator')

        # Create groups
        self._create_images_group()
        self._create_messages_group()

        # Set initial time variables
        self._image_change_time = pygame.time.get_ticks()
        self._colour_change_time = pygame.time.get_ticks()

        # Add clock
        self._clock = pygame.time.Clock()

    def _create_images_group(self) -> None:
        # Create the images group
        self._images = pygame.sprite.Group()
        # Create the images
        self._create_images()

    def _create_messages_group(self) -> None:
        # Create the messages group
        self._messages = pygame.sprite.Group()
        # Write the first message and add to group
        self._create_message()

    def run(self) -> None:
        """Main loop of the animation."""
        while True:
            # Set the FPS
            self._clock.tick(self.settings.fps)

            # Check for events
            self._check_events()

            # Update the message
            self._update_items()

            # Check the messages for certain criteria
            self._check_items()

            # Draw the message
            self._update_screen()

    def _check_events(self) -> None:
        # Watch for events
        for event in pygame.event.get():
            # Check if should quit
            self._check_quit(event)

    @staticmethod
    def _check_quit(event) -> None:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()

    def _set_bg(self) -> None:
        """Set the background of the animation."""
        self.screen.fill(self.settings.bg_colour)

    def _create_images(self) -> None:
        # Create all the required images
        for i in range(self.settings.num_images):
            # Create an image of each type
            for image in self.settings.images:
                # Create an image
                Picture(self._images, self, image)

    def _create_message(self) -> None:
        # Create a message
        Message(self._messages, self)

    def _check_items(self) -> None:
        # Check whether the message has fully emerged on screen, then create another if so.
        for message in self._messages.sprites():
            if message.has_just_emerged():
                self._create_message()

            # If the message has left the screen, get rid of it.
            if not message.is_on_screen():
                message.kill()
    #
    # def _reqd_num_of_messages(self) -> int:
    #     # Work out how many rectangles fit on the screen, pad by 2 because that is the minimum required if the
    #     # message is wider than the screen.
    #     return int(self.screen.get_rect().width / min(message.rect.width for message in self._messages.sprites())) + 2

    def _update_items(self) -> None:
        # Update images
        self._update_images()

        # Update messages
        self._messages.update()

        # Swap colours every so often
        self._change_colours()

    def _update_images(self) -> None:
        # Update images when required
        image_change_time_new = pygame.time.get_ticks()
        if image_change_time_new - self._image_change_time >= self.settings.image_change_time * 1000:
            # Create a new group for the images
            image_group_new = pygame.sprite.Group()

            # Move the images
            self._images.update(image_group_new)
            self._images = image_group_new
            self._image_change_time = image_change_time_new

    def _change_colours(self) -> None:
        # Update colours when required
        colour_change_time_new = pygame.time.get_ticks()
        if colour_change_time_new - self._colour_change_time >= self.settings.colour_change_time * 1000:
            # Use the settings method to randomise colours
            self.settings.set_colours()
            self._colour_change_time = colour_change_time_new

    def _update_screen(self) -> None:
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
    #
    # def _draw_fps(self):
    #     fps_font = pygame.font.SysFont(self.settings.typeface, 36)
    #     text = f'{self._clock.get_fps():.2f}'
    #     content = fps_font.render(text, True, (0, 0, 0))
    #     rect = content.get_rect()
    #     screen_rect = self.screen.get_rect()
    #     rect.x = 10
    #     rect.y = 10
    #     self.screen.blit(content, rect)
