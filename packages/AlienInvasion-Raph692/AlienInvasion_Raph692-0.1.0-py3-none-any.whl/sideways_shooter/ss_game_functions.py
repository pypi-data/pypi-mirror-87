import sys
import pygame
from ss_bullet import Bullet
from ss_target import Target
from time import sleep


def check_keydown_events(event, ss_settings, screen, stats, ship, bullets, target):
    """Responding to keypresses."""
    # Move the ship to the left or right
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ss_settings, screen, ship, bullets)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ss_settings, stats, ship, bullets, target)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Responding to key releases."""
    # Stop moving the ship when releasing arrow keys.
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ss_settings, screen, stats, ship, bullets, target, play_button):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ss_settings, stats, play_button, ship, bullets, target, mouse_y, mouse_x)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ss_settings, screen, stats, ship, bullets, target)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ss_settings, stats, play_button, ship, bullets, target, mouse_y, mouse_x):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Restart game
        start_game(ss_settings, stats, ship, bullets, target)


def start_game(ss_settings, stats, ship, bullets, target):
    """Start a new game."""
    # Reset the game settings.
    ss_settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Empty the list of bullets
    bullets.empty()

    # Center the ship and target.
    target.center_target()
    ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, bullets, target, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()

    # Redraw target
    target.draw_target()

    # Draw the play button when the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ss_settings, screen, stats, bullets, target):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    screen_rect = screen.get_rect()
    for bullet in bullets.copy():
        if bullet.rect.left >= screen_rect.right:
            check_bullet_edges(stats, bullets)

    # Check for target-bullet collisions
    if pygame.sprite.spritecollideany(target, bullets):
        target_hit(ss_settings, bullets)


def check_bullet_edges(stats, bullets,):
    """Check if a bullet has missed the target."""
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Empty the list of bullets.
        bullets.empty()

        # # Pause.
        # sleep(0.2)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_target_edges(ss_settings, target):
    """Check if the target has reached the top of bottom of the screen."""
    if target.check_edges():
        ss_settings.target_direction *= -1


def target_hit(ss_settings, bullets):
    """Respond to the target being hit by a bullet."""
    # ToDo add scores for hitting target
    # Empty the list of bullets.
    bullets.empty()

    # Increase speed settings.
    ss_settings.increase_speed()


def update_target(ss_settings, target):
    """Check if the target is at an edge and then update its position on the screen."""
    check_target_edges(ss_settings, target)

    target.update()


# def create_target(ss_settings, screen):
#     """Create a target place it on the center right."""
#     target = Target(ss_settings, screen)
#     target.center_target()
#     return target
