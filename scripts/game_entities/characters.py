from scripts.game_entities.prefab import Prefab
from scripts.game_entities.weapon import Weapon
from scripts.game_entities.weapon_types import Submachine, Rifle, Shotgun, Raygun
import pygame
import os
from scripts.game_configs import CHARACTER_FOLDER

class Character(Prefab):
    """
    Representa un prefab jugable con animaciones y armas, en este caso Chester el gato.
    ACCIONES QUE PUEDE REALIZAR:
    - Se mueve con las teclas de flecha(arriba, abajo, izquierda y derecha) en la
    respectiva direccion.
    - Dispara con la barra espaciadora.
    - Cambia de arma con la tecla 1.

    Attributes:
        weapons (list): Lista de armas disponibles para el prefab.
        weapon_index (int): Índice del arma actualmente equipada.
        change_weapon_delay_counter (int): Contador para evitar cambios rápidos de arma.
    """

    def __init__(self, x, y, frame_update=None):
        dirs = {
            "up": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_backward"),
            "down": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_forward"),
            "left": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_left"),
            "right": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_right")
        }
        super().__init__(x, y, dirs, frame_update)
        self.weapon_index = 0
        self.weapons : list[Weapon] = [Submachine(x, y - 35), Rifle(x, y - 35), Shotgun(x, y - 35), Raygun(x, y - 35)]
        self.weapons[self.weapon_index].x = x
        self.weapons[self.weapon_index].y = y - 35
        self.change_weapon_delay_counter = 50

    def add_weapon(self, weapon: Weapon):
        """
        Agrega un arma al inventario de Chester con un maximo de 4 armas.

        Args:
            weapon (Weapon): El arma a agregar.

        Raises:
            ValueError: Si ya hay 4 armas en el inventario.
        """
        if len(self.weapons) < 4:
            self.weapons.append(weapon.set_position(self.x, self.y - 35))
        else:
            print("Cannot add more weapons. Maximum of 4 reached.")
            #Debe remplazarse a un mensaje en pantalla que indique que no se pueden agregar más armas.

    def do_action(self, keys):
        """
        Realiza acciones de Chester según las teclas presionadas, como moverse
        o cambiar de arma.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        super().do_action(keys)
        self.change_weapon_delay_counter -= 1
        if keys[pygame.K_1] and self.change_weapon_delay_counter <= 0:
            self.change_weapon()
        self.do_action_weapons(keys)
    
    def change_weapon(self):
        """
        Cambia el arma equipada de Chester.
        """
        self.change_weapon_delay_counter = 50
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons):
            self.weapon_index = 0

    def do_action_weapons(self, keys):
        """
        Realiza acciones específicas de las armas de Chester, en este caso indica que 
        el inventario de armas se mueve junto con Chester.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        for weapon in self.weapons:
            weapon.do_action(keys)

    def update_animation(self):
        """
        Actualiza las animaciones del prefab y del arma equipada.
        """
        super().update_animation()
        self.weapons[self.weapon_index].update_animation()
        
    def draw_weapons_bullets(self, surface):
        """
        Dibuja las balas disparadas por las armas de Chester(incluso si el arma de donde provino la bala no esta seleccionada).

        Args:
            surface (pygame.Surface): Superficie donde se dibujarán las balas.
        """
        for weapon in self.weapons:
            weapon.draw_bullets(surface)

    def draw(self, surface):
        """
        Dibuja a Chester y su arma equipada en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el prefab.
        """
        if self.direction == "up" or self.direction == "down":
            super().draw(surface)
            self.draw_weapons_bullets(surface)
            self.weapons[self.weapon_index].draw(surface)
            
        else:
            self.draw_weapons_bullets(surface)
            self.weapons[self.weapon_index].draw(surface)
            super().draw(surface)