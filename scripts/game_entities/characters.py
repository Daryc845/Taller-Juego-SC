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
            "right": os.path.join(CHARACTER_FOLDER, "Chester-animation-walking_right"),
            "up_beaten": os.path.join(CHARACTER_FOLDER, "Chester-animation-beaten_backward"),
            "down_beaten": os.path.join(CHARACTER_FOLDER, "Chester-animation-beaten_forward"),
            "left_beaten": os.path.join(CHARACTER_FOLDER, "Chester-animation-beaten_left"),
            "right_beaten": os.path.join(CHARACTER_FOLDER, "Chester-animation-beaten_right")
        }
        super().__init__(prefab_data, dirs, frame_update)
        self.is_beaten = False
        self.beaten_frame = 0
        self.beaten_cycle_count = 0
        self.beaten_direction = None
        self.actual_life = prefab_data.life
        self.reset_character()

    def reset_character(self):
        self.weapon_index = 0
        self.weapons : list[Weapon] = [Submachine(self.prefab_data.x, self.prefab_data.y - 35), 
            Rifle(self.prefab_data.x, self.prefab_data.y - 35)]
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
    
    def set_weapon(self, weapon: Weapon):
        """
        Cambia el arma con el indice del inventario de Chester por otra.

        Args:
            weapon (Weapon): El arma puesta en el indice del inventario.

        Raises:
            ValueError: Si ya hay 4 armas en el inventario.
        """
        last_weapon = self.weapons[self.weapon_index]
        self.weapons[self.weapon_index] = weapon.set_position(self.prefab_data.x, self.prefab_data.y - 35)
        return last_weapon
        
    def heal(self, amount):
        """
        Cura a Chester una cantidad especificada de salud.

        Args:
            amount (int): Cantidad de salud a curar.
        """
        self.prefab_data.life += amount
        if self.prefab_data.life > self.prefab_data.max_life:
            self.prefab_data.life = self.prefab_data.max_life
    
    def add_munition(self, amount):
        """
        Agrega munición a la arma equipada de Chester.
        Si el arma equipada es una Raygun, no se puede agregar munición.
        Args:
            amount (_type_): cantidad de munición a agregar.
        """
        if isinstance(self.weapons[self.weapon_index], Raygun):
            return None
        self.weapons[self.weapon_index].add_munition(amount)

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

    def do_action(self, keys, restricted_directions=[False, False, False, False]):
        """
        Realiza acciones de Chester según las teclas presionadas, cosmo moverse
        o cambiar de arma.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        super().do_action(keys, restricted_directions=restricted_directions)
        self.do_action_weapons(keys, restricted_directions=restricted_directions)
    
    def change_weapon(self):
        """
        Cambia el arma equipada de Chester.
        """
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons):
            self.weapon_index = 0

    def do_action_weapons(self, keys, restricted_directions=[False, False, False, False]):
        """
        Realiza acciones específicas de las armas de Chester, en este caso indica que 
        el inventario de armas se mueve junto con Chester.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        for weapon in self.weapons:
            weapon.do_action(keys, restricted_directions=restricted_directions)

    def update_animation(self):
        """
        Actualiza las animaciones del prefab y del arma equipada.
        """
        if self.actual_life > self.prefab_data.life:
            if self.is_beaten:
                self.prefab_data.life = self.actual_life
            else:
                self.is_beaten = True
                self.actual_life = self.prefab_data.life
            self.beaten_direction = self.prefab_data.direction
            self.beaten_frame = 0
            self.beaten_cycle_count = 0
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

    def draw(self, surface, draw_character_message, in_pause=False):
        """
        Dibuja a Chester y su arma equipada en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el prefab.
        """
        
        self.draw_weapons_bullets(surface, in_pause=in_pause)
        self.evaluate_position_and_draw(surface, draw_character_message)
        
        title_surface = self.font.render("ARMAS(Maximo 4)", True, (255, 255, 255))
        surface.blit(title_surface, (10, 40 - 25))
        for i, weapon in enumerate(self.weapons):
            self.draw_munition(surface, weapon, 10, 50 + i * 45, i == self.weapon_index)

    def draw_beaten_animation(self, surface):
        self.beaten_cycle_count += 1
        if self.beaten_cycle_count >= 5:
            self.beaten_cycle_count = 0
            self.beaten_frame += 1
            if self.beaten_frame >= len(self.animations[self.beaten_direction + "_beaten"]):
                self.is_beaten = False
                self.beaten_frame = 0
        frame = self.animations[self.prefab_data.direction + "_beaten"][self.beaten_frame]
        max_width, max_height = self.max_dimensions[self.prefab_data.direction]
        pos_x = self.prefab_data.x - max_width * 0.5
        pos_y = self.prefab_data.y - max_height * 0.5
        surface.blit(frame, (pos_x, pos_y))

    
    def evaluate_position_and_draw(self, surface, draw_character_message=None):
        if self.prefab_data.direction == "up" or self.prefab_data.direction == "down":
            if not self.is_beaten:
                super().draw(surface)
            else:
                self.draw_beaten_animation(surface)
            self.weapons[self.weapon_index].draw(surface, draw_character_message)
        else:
            self.weapons[self.weapon_index].draw(surface, draw_character_message)
            if not self.is_beaten:
                super().draw(surface)
            else:
                self.draw_beaten_animation(surface)
            

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