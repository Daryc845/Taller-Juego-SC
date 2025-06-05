from scripts.game_entities.weapon import Weapon
from scripts.game_configs import WEAPONS_FOLDER, WEAPON_SUBMACHINE_FOLDER, WEAPON_RIFLE_FOLDER, WEAPON_SHOTGUN_FOLDER, WEAPON_RAYGUN_FOLDER
import os

class Submachine(Weapon):
    """
    Representa un subfusil(metralleta) con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si el subfusil está disparando.
        max_munition (int): Munición máxima del subfusil.
        remaining_munition (int): Munición restante del subfusil.
    """

    def __init__(self, x, y, direction="down"):
        bullet_folder_url = os.path.join(WEAPONS_FOLDER, "weapon_1-submachine")
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 5, direction=direction)
        self.shooting = False
        self.max_munition = 250
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-backward_shooting"),
        "down": os.path.join(WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-forward_shooting"),
        "left": os.path.join(WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-left_shooting"),
        "right": os.path.join(WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-right_shooting")
        }   
    
    def get_bullet_damage(self):
        return 5
    
    def get_bullet_type(self):
        return "submachine"
    
    def get_name(self):
        return "Submachine"

class Rifle(Weapon):
    """
    Representa un rifle con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si el rifle está disparando.
        max_munition (int): Munición máxima del rifle.
        remaining_munition (int): Munición restante del rifle.
    """

    def __init__(self, x, y, direction="down"):
        bullet_folder_url = os.path.join(WEAPON_RIFLE_FOLDER)
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 10, direction=direction)
        self.shooting = False
        self.max_munition = 175
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-backward_shooting"),
        "down": os.path.join(WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-forward_shooting"),
        "left": os.path.join(WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-left_shooting"),
        "right": os.path.join(WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-right_shooting")
        }
    
    def get_bullet_damage(self):
        return 7
    
    def get_bullet_type(self):
        return "rifle"
    
    def get_name(self):
        return "Rifle"

class Shotgun(Weapon):
    """
    Representa una escopeta con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si la escopeta está disparando.
        max_munition (int): Munición máxima de la escopeta.
        remaining_munition (int): Munición restante de la escopeta.
    """

    def __init__(self, x, y, direction="down"):
        bullet_folder_url = os.path.join(WEAPON_SHOTGUN_FOLDER)
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 60, direction=direction)
        self.shooting = False
        self.max_munition = 90
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-backward_shooting"),
        "down": os.path.join(WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-forward_shooting"),
        "left": os.path.join(WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-left_shooting"),
        "right": os.path.join(WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-right_shooting")
        }

    def get_bullet_damage(self):
        return 30
    
    def get_bullet_type(self):
        return "shotgun"
    
    def get_name(self):
        return "Shotgun"

class Raygun(Weapon):   
    """
    Representa una pistola de rayos con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si la pistola de rayos está disparando.
        max_munition (int): Munición máxima de la pistola de rayos.
        remaining_munition (int): Munición restante de la pistola de rayos.
    """

    def __init__(self, x, y, direction="down"):
        bullet_folder_url = os.path.join(WEAPON_RAYGUN_FOLDER)
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 50, direction=direction)
        self.shooting = False
        self.max_munition = 50
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-backward_shooting"),
        "down": os.path.join(WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-forward_shooting"),
        "left": os.path.join(WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-left_shooting"),
        "right": os.path.join(WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-right_shooting")
        }
    
    def get_bullet_damage(self):
        return 80
    
    def get_bullet_type(self):
        return "raygun"
    
    def get_name(self):
        return "Raygun"
    
    
