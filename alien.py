# alien.py

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """The bad guy in the game."""
    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and get its rect.
        self.image = pygame.image.load('images/alien_ship.bmp')
        self.rect = self.image.get_rect()

        # Start the alien near the top left of the screen. There is space above it 
        # equal to its height and space to the left that's equal to its width.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)  # ?Why add a new variable?

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """Move the alien right."""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        

    