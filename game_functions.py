# game_functions.py

import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # See if they clicked on the start button
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """See if the mouse has pushed the play button; if so begin a new game."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # If so, begin a new game, but ignore if we're in the middle of a game.
    if button_clicked and not stats.game_active: 
        start_game(ai_settings, screen, stats, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, ship, aliens, bullets):
    # First, hide the mouse cursor during game play.
    pygame.mouse.set_visible(False)
    stats.game_active = True
    stats.reset_stats()
    reset_screen(ai_settings, screen, stats, ship, aliens, bullets)

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update the positions of the bullets and get rid of old bullets."""
    bullets.update()  # Update the positions

    for bullet in bullets.copy():   # Get rid of bullets that have disappeared
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets & aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # If we eliminated the last alien, clear the screen of bullets & make a new
    # alien fleet.
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit is not reached yet."""
    if (len(bullets) < ai_settings.bullets_allowed):
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # First we create a dummy alien just so we can get its width and height
    # but we're not adding it to the fleet.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings,alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            add_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    # Spacing between each alien is equal to one alien width.
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height
                            - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def add_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creat an alien and place it in the row."""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x    # Again, why do we have the .x value?
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge, and then
        update the positions of all the aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions and aliens getting to the bottom of the screen.
    if pygame.sprite.spritecollideany(ship, aliens) or alien_at_bottom(screen, aliens):
        stats.ships_left -= 1
        reset_screen(ai_settings, screen, stats, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def reset_screen(ai_settings, screen, stats, ship, aliens, bullets): # His "ship_hit"
    """
    Reset the screen after the ship has been hit by an alien or an alien 
    reaches the bottom
    """
    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def alien_at_bottom(screen, aliens):
    """
    Check if any aliens have reached the bottomof the screen.  If so, act respond 
    as if the ship has been hit.
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            return True
            


   

 