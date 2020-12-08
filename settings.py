# settings.py

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""

        # Screen settings
        self.screen_width = 1200  # Constant    
        self.screen_height = 800  # Constant    
        self.bg_color = (200, 200, 255)  # Constant    

        # Ship settings
        self.ship_speed_factor = 3.0
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 30  # Constant    
        self.bullet_height = 15  # Constant    
        self.bullet_color = (60, 60, 60)  # Constant    
        self.bullets_allowed = 3  # Constant    

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1   # 1 for right, -1 for left

        
