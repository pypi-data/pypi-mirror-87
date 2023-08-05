import json


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start alien invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        filename = 'high_score.json'
        with open(filename) as f_obj:
            self.high_score = json.load(f_obj)

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
