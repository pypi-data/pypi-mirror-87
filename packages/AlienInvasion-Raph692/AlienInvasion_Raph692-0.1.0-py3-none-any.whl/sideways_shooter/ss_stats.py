class GameStats:
    """Track statistics for sideways shooter."""

    def __init__(self, ss_settings):
        """Initialize statistics."""
        self.ss_settings = ss_settings
        self.reset_stats()

        # Start sideways shooter in an inactive state
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ss_settings.ship_limit
