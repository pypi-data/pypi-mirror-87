import sys
import pygame
import json
from bullet import Bullet
from alien import Alien
from time import sleep
from star import Star
from random import randint


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
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
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_q:
        write_high_score(stats)
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


def check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            write_high_score(stats)
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_y, mouse_x)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def write_high_score(stats):
    """Writing the high score to a file."""
    if stats.score >= stats.high_score:
        filename = 'high_score.json'
        with open(filename, 'w') as f_obj:
            json.dump(stats.high_score, f_obj)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_y, mouse_x):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Restart game.
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Start a new game."""
    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Empty the list of bullets and aliens.
    bullets.empty()
    aliens.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Reset the score board images.
    sb.prep_images(ai_settings, screen)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, stars):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        # bullet.blitme() # change bullets to drops

    # Redraw ship
    ship.blitme()

    # Redraw fleet of aliens
    aliens.draw(screen)

    # Redraw group of stars
    stars.draw(screen)

    # Show the score
    sb.show_score()

    # Draw the play button when the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_score()


def update_bullets(bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Responding to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    # Python returns a collisions dictionary when bullet hits alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # loop through dict to award points for each alien hit.
        # each value is a list of aliens hit by a single bullet (key).
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # Repopulate the alien fleet if it has been shot down.
    if len(aliens) < 1:
        # If the entire fleet is destroyed, start a new level.
        start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)

   
def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Start a new level when the entire alien fleet is destroyed."""
    bullets.empty()
    ai_settings.increase_speed()

    # Increase level
    stats.level += 1
    sb.prep_level()

    create_fleet(ai_settings, screen, ship, aliens)


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by an alien."""
    if stats.ships_left > 0:
        # Decrement ships left.
        stats.ships_left -= 1
        sb.prep_ships(ai_settings, screen)

        # Empty the list of bullets and aliens.
        bullets.empty()
        aliens.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.2)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, aliens, ship, bullets):
    """
    Check if the fleet is at an edge,
     and then update the position of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)

    # Check if any aliens have reached the bottom
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


# def check_stars_edges(stars):
#     """Respond appropriately when stars/raindrops disappear off the bottom of the screen."""
#     for star in stars.sprites():
#         star.check_bottom()
#
#
# def update_stars(stars):
#     """Update the position of all stars/raindrops."""
#     check_stars_edges(stars)
#     stars.update()


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - alien_width * 2
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


# def get_number_stars_x(ai_settings, star_width):
#     """Determine the number of stars that fit in a row."""
#     available_space_x = ai_settings.screen_width - 2 * star_width
#     number_stars_x = int(available_space_x / (2 * star_width))
#     return number_stars_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


# def get_number_rows_star(ai_settings, star_height):
#     """Determine the number of rows of stars that fit on the screen."""
#     number_rows = int(ai_settings.screen_height / (2 * star_height))
#     return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + alien_width * 2 * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


# def create_star(ai_settings, screen, stars, row_number):
#     """Create a star and place it in a row."""
#     star = Star(ai_settings, screen)
#     star_width = star.rect.width
#
#     # Introduce randomness when placing stars
#     random_number = randint(-10, 10) # (-30, 30) for stars and *4 in row below
#     star.x = star_width + star_width * 2 * random_number
#     star.rect.x = star.x
#     star.rect.y = star.rect.height + 2 * star.rect.height * row_number
#     stars.add(star)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    num_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    num_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(num_rows):
        for alien_number in range(num_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


# def create_stars(ai_settings, screen, stars):
#     """Create a group of stars."""
#     star = Star(ai_settings, screen)
#     num_stars_x = get_number_stars_x(ai_settings, star.rect.width)
#     num_rows = get_number_rows_star(ai_settings, star.rect.height)
#
#     # Create stars
#     for row_number in range(num_rows):
#         for star_number in range(num_stars_x):
#             create_star(ai_settings, screen, stars, row_number)
