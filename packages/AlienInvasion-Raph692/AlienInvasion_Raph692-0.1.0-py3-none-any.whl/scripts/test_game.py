import pygame
from settings import Settings
import sys


def run_game():
    # Initialize game and create a screen object.
    pygame.init()

    # Create settings instance
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Test Game")

    # Make a ship
    # ship = Ship(ai_settings, screen)

    # Start the main loop for the game.
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Printing event key will print the keycode of each key in the terminal (SDL)
                # print(event.key)

                # Printing the key name will print the actual key in the terminal
                print(pygame.key.name(event.key))

        # Update images on the screen
        screen.fill(ai_settings.bg_color)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


run_game()

