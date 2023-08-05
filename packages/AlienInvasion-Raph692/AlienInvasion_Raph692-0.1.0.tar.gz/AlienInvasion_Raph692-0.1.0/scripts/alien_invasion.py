import pygame
from settings import Settings
from ship import Ship
from button import Button
import game_functions as gf
from game_stats import GameStats
from scoreboard import ScoreBoard
from pygame.sprite import Group


def run_game():
    # Initialize game and create a screen object.
    pygame.init()

    # Create settings instance
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")

    # Create qan instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # # Create stars
    # gf.create_stars(ai_settings, screen, stars)

    # Start the main loop for the game.
    while True:

        # Respond to keyboard and mouse events.
        gf.check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

        if stats.game_active:
            ship.update()
            # Update bullets positions and get rid of old bullets.
            gf.update_bullets(bullets)
            gf.check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens)
            gf.update_aliens(ai_settings, stats, screen, sb, aliens, ship, bullets)
            # gf.update_stars(stars)

        # Update images on the screen and flip to the new screen.
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, stars)


run_game()
