import pygame
from ss_settings import Settings
import ss_game_functions as gf
from ss_ship import Ship
from ss_target import Target
from ss_stats import GameStats
from ss_button import Button
from pygame.sprite import Group


def run_game():
    """Initialize a game and create a screen object."""
    pygame.init()

    # Create settings instance
    ss_settings = Settings()
    screen = pygame.display.set_mode(
        (ss_settings.screen_width, ss_settings.screen_height))
    pygame.display.set_caption("Sideways Shooter")

    # Make the play button
    play_button = Button(ss_settings, screen, "Play")

    # Create an instance to store game statistics.
    stats = GameStats(ss_settings)

    # Create a ship
    ship = Ship(ss_settings, screen)

    # Create the target
    target = Target(ss_settings, screen)

    # Make a group to store bullets in
    bullets = Group()

    # Start the main loop for the game.
    while True:
        # Respond to keyboard and mouse events.
        gf.check_events(ss_settings, screen, stats, ship, bullets, target, play_button)

        if stats.game_active:
            ship.update()

            # Update bullet positions and get rid of old bullets.
            gf.update_bullets(ss_settings, screen, stats, bullets, target)
            gf.update_target(ss_settings, target)

        # Update images on the screen and flip to the new screen.
        gf.update_screen(ss_settings, screen, stats, ship, bullets, target, play_button)


run_game()

