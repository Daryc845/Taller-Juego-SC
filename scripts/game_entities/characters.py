from scripts.game_entities.prefab import Prefab
from scripts.game_entities.weapon import Weapon
from scripts.game_entities.weapon_types import Submachine, Rifle, Shotgun, Raygun
from scripts.game_entities.data_models import PrefabData, AttackData
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

    def __init__(self, prefab_data: PrefabData, frame_update=None):
        dirs = {
            "up": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_backward"),
            "down": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_forward"),
            "left": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_left"),
            "right": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_right")
        }
        super().__init__(prefab_data, dirs, frame_update)
        self.reset_character()

    def reset_character(self):
        self.weapon_index = 0
        self.weapons : list[Weapon] = [Submachine(self.prefab_data.x, self.prefab_data.y - 35), 
            Rifle(self.prefab_data.x, self.prefab_data.y - 35), 
            Shotgun(self.prefab_data.x, self.prefab_data.y - 35), 
            Raygun(self.prefab_data.x, self.prefab_data.y - 35)]
        self.weapons[self.weapon_index].x = self.prefab_data.x
        self.weapons[self.weapon_index].y = self.prefab_data.y - 35
        self.bullets_count_id = 0

    def add_weapon(self, weapon: Weapon):
        """
        Agrega un arma al inventario de Chester con un maximo de 4 armas.

        Args:
            weapon (Weapon): El arma a agregar.

        Raises:
            ValueError: Si ya hay 4 armas en el inventario.
        """
        if weapon in self.weapons:
            return True
        elif len(self.weapons) < 4:
            weapon.direction = self.prefab_data.direction
            self.weapons.append(weapon.set_position(self.prefab_data.x, self.prefab_data.y - 35))
            return True
        return False

    def leave_weapon(self):
        """
        Elimina un arma del inventario de Chester.

        Args:
            weapon (Weapon): El arma a eliminar.
        """
        if len(self.weapons) == 1:
            return None
        wp = self.weapons.pop(self.weapon_index)
        if self.weapon_index >= len(self.weapons):
            self.weapon_index = len(self.weapons) - 1
        return wp

    def do_action(self, keys):
        """
        Realiza acciones de Chester según las teclas presionadas, como moverse
        o cambiar de arma.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        super().do_action(keys)
        self.do_action_weapons(keys)
    
    def change_weapon(self):
        """
        Cambia el arma equipada de Chester.
        """
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
        def bullet_data_creation(x: int, y: int, direction: str, damage: int, type: str) -> AttackData:
            data = AttackData(self.bullets_count_id, x, y, damage, direction, type)
            self.prefab_data.attacks.append(data)
            self.bullets_count_id += 1
            return data
        super().update_animation()
        self.weapons[self.weapon_index].update_animation(bullet_data_creation)
        
    def draw_weapons_bullets(self, surface, in_pause=False):
        """
        Dibuja las balas disparadas por las armas de Chester(incluso si el arma de donde provino la bala no esta seleccionada).

        Args:
            surface (pygame.Surface): Superficie donde se dibujarán las balas.
        """
        for weapon in self.weapons:
            weapon.draw_bullets(surface, in_pause=in_pause)

    def draw(self, surface, in_pause=False):
        """
        Dibuja a Chester y su arma equipada en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el prefab.
        """
        super().draw(surface)
        self.draw_weapons_bullets(surface, in_pause=in_pause)
        self.weapons[self.weapon_index].draw(surface)
        title_surface = self.font.render("ARMAS", True, (255, 255, 255))
        surface.blit(title_surface, (10, 40 - 25))
        for i, weapon in enumerate(self.weapons):
            self.draw_munition(surface, weapon, 10, 50 + i * 45, i == self.weapon_index)

    def draw_munition(self, surface: pygame.Surface, weapon: Weapon, x, y, selected=False):
        background_color = (60, 60, 60, 200) if selected else (40, 40, 40, 150)
        border_color = (255, 255, 255) if selected else (100, 100, 100)
        bg_surface = pygame.Surface((120, 40), pygame.SRCALPHA)
        bg_surface.fill(background_color)
        pygame.draw.rect(bg_surface, border_color, bg_surface.get_rect(), 1)
        surface.blit(bg_surface, (x, y))
        weapon_name = weapon.__class__.__name__
        text_surface = self.small_font.render(weapon_name, True, (255, 255, 255))
        surface.blit(text_surface, (x + 5, y + 2))
        ammo_text = f"{weapon.remaining_munition}/{weapon.max_munition}"
        ammo_surface = self.small_font.render(ammo_text, True, (255, 255, 255))
        surface.blit(ammo_surface, (x + 5, y + 16))