import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to represent a star on the screen."""

    def __init__(self, ai_settings, screen):
        """Initialize the star and set its starting position."""
        super(Star, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the star image and set its rect attribute.
        # self.image = pygame.image.load('images/star.bmp')
        self.image = pygame.image.load('../images/raindrop.bmp')
        self.rect = self.image.get_rect()

        # Start each new star near the top left of the screen.
        # (adding space to the left that's equal to the aliens width and
        # a space above it equal to its height)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the stars exact position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the star at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_bottom(self):
        """Move row of stars/raindrops to the top if they disappear off the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.y >= screen_rect.bottom:
            self.rect.y = screen_rect.top

    def update(self):
        """Let the stars/raindrops fall down."""
        self.rect.y += self.ai_settings.fleet_drop_speed

