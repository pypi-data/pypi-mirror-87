import pygame


class Target:
    """Create a target at the right edge of the screen."""

    def __init__(self, ss_settings, screen):
        """Initialize the target."""
        self.screen = screen
        self.ss_settings = ss_settings
        self.screen_rect = self.screen.get_rect()

        # Create the target rectangle at the right edge of the screen
        self.rect = pygame.Rect(0, 0, ss_settings.target_width, ss_settings.target_height)
        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.right - 10

        # Store the targets position as a decimal value.
        self.centery = float(self.rect.centery)

        self.color = ss_settings.target_color
        self.speed_factor = ss_settings.target_speed_factor

    def update(self):
        """Move the target up and down."""
        self.centery += (self.ss_settings.target_speed_factor *
                   self.ss_settings.target_direction)
        self.rect.y = self.centery

    def check_edges(self):
        """Return true if the target is at the top or bottom of the screen."""
        if self.rect.bottom >= self.screen_rect.bottom:
            return True
        elif self.rect.top <= self.screen_rect.top:
            return True

    def draw_target(self):
        """Draw the target rectangle to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def center_target(self):
        """Center the target on the right side."""
        self.centery = self.screen_rect.centery

