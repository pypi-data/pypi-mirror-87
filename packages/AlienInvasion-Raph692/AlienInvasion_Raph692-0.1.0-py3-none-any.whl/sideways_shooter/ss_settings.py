class Settings:
    """A class to store all settings for Sideways Shooter."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # Target settings
        self.target_width = 6
        self.target_height = 200
        self.target_color = (0, 200, 0)

        # Define how quickly the game speeds up.
        self.speedup_scale = 1.2

        # Initialize the game's dynamic settings.
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the game's dynamic settings."""
        self.ship_speed_factor = 5
        self.target_speed_factor = 3
        self.bullet_speed_factor = 30

        self.target_direction = 1  # fleet direction of 1 represents right, -1 represents left

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.target_speed_factor *= self.speedup_scale

