import pygame
import os
from scripts.game_persistence import load_image
from scripts.game_entities.data_models import PrefabData
from scripts.game_configs import FRAME_CHANGE_EVERY
from scripts.game_entities.weapon_types import Raygun, Submachine, Shotgun, Rifle
from scripts.numbs_aux import generate_numbers
from scripts.game_entities.static_object import StaticObject
import time

class Chest(StaticObject):
    """
    Clase que representa un cofre en el juego.
    Solo se anima cuando el personaje está cerca.
    """
    
    def __init__(self, prefab_data: PrefabData, show_timed_message, draw_character_message):
        animation_path = os.path.join("resources", "objects", "Chest", "Open-chest-animation")
        super().__init__(prefab_data, animation_path, has_eternal_animation=False)
        self.valid_open = False
        self.animating = False
        self.is_open = False
        self.open_delay = 0
        self.last_reward = None
        self.reward = None
        self.show_timed_message = show_timed_message
        self.draw_character_message = draw_character_message
    
    def update(self, character):
        """
        Actualiza el estado del cofre.
        """
        if self.open_delay > 0:
            self.open_delay -= 1
        if not self.is_alive or not self.valid_open:
            return
            
        if self.check_character_nearby(character):
            if not self.animating:
                self.animating = True
        
        if self.animating:
            self.animate()
    
    def animate(self):
        self.cycle_count += 1
        if self.cycle_count >= FRAME_CHANGE_EVERY:
            self.cycle_count = 0
            if(not (self.current_frame >= len(self.animations["default"]) - 1)):
                self.current_frame += 1
            if self.current_frame >= len(self.animations["default"]) - 1:
                self.on_animation_end()
    
    def on_animation_end(self):
        """
        Se llama cuando termina la animación de apertura.
        """
        self.valid_open = False
        self.random_num = self._generate_random_number(0)
        self.reward_config = self._get_reward_config()
        self.reward_type = self._select_reward_type(self.random_num, self.reward_config)
        
        if self.reward_type == 'munition':
            print("VAMOOOOOOOOOOO")
            self.reward = Munition(PrefabData(self.prefab_data.x, self.prefab_data.y - 35, direction="Down", life=1))
        elif self.reward_type == 'health':
            self.reward = Hearth(PrefabData(self.prefab_data.x, self.prefab_data.y - 35, direction="Down", life=1))
        #METODO MONTECARLO PARA SELECCIONAR EL ARMA
        if self.reward_type == 'weapon':
            self.select_weapon()
        
    def show_chest(self, x, y):
        self.prefab_data.x = x
        self.prefab_data.y = y
        self.is_alive = True
    
    def open_chest(self):
        if self.open_delay == 0:
            self.valid_open = True
            self.is_open = True
        
    def select_weapon(self):
        #METODO MONTECARLO PARA SELECCIONAR EL ARMA
        random_num = self._generate_random_number(10)
        if random_num < 0.5:
            self.reward = Submachine(self.prefab_data.x, self.prefab_data.y - 35, self.prefab_data.direction)
        elif random_num < 0.8:
            self.reward = Rifle(self.prefab_data.x, self.prefab_data.y - 35, self.prefab_data.direction)
        elif random_num < 0.95:
            self.reward = Shotgun(self.prefab_data.x, self.prefab_data.y - 35, self.prefab_data.direction)
        else:
            self.reward = Raygun(self.prefab_data.x, self.prefab_data.y - 35, self.prefab_data.direction)
        
    def get_weapon(self, character):
        if not self.valid_open and self.check_character_nearby(character):
            self._reset_chest_state()
            self._apply_reward(self.reward_type, character, self.random_num)
            self.reward = None
            self.is_alive = False

    def _reset_chest_state(self):
        self.animating = False
        self.is_open = False
        self.open_delay = 60
        self.current_frame = 0

    def _generate_random_number(self, number):
        conf = {
            'k': 3,
            'g': 10,
            'c': 1,
            'X0': int(time.time()) % 1000
        }
        return generate_numbers(conf)[number]

    def _get_reward_config(self):
        #CADENAS DE MARKOV PARA SELECCIONAR RECOMPENSAS SEGUN LA ULTIMA RECOMPENSA
        return {
            None: {'munition': 0.33, 'health': 0.33, 'weapon': 0.34},
            'munition': {'munition': 0.3, 'health': 0.3, 'weapon': 0.4},
            'health': {'munition': 0.3, 'health': 0.2, 'weapon': 0.5},
            'weapon': {'munition': 0.35, 'health': 0.55, 'weapon': 0.1}
        }.get(self.last_reward, {'munition': 0.33, 'health': 0.33, 'weapon': 0.34})

    def _select_reward_type(self, random_num, reward_config):
        cumulative_prob = 0
        for reward_type, prob in reward_config.items():
            cumulative_prob += prob
            if random_num < cumulative_prob:
                return reward_type
        return 'munition'  # Por defecto si hay algún error de redondeo

    def do_action(self, keys, character):
        if self.check_character_nearby(character) and not self.is_open and keys[pygame.K_5]:
            self.open_chest()
        elif self.check_character_nearby(character) and self.is_open and keys[pygame.K_5]:
            self.get_weapon(character)
                

    def _apply_reward(self, reward_type, character, random_num):
        reward_actions = {
            'munition': lambda: character.add_munition(60),
            'health': lambda: character.heal(40),
            'weapon': lambda: character.set_weapon(self.reward.set_direction(character.prefab_data.direction))
        }
        
        reward_messages = {
            'munition': f"¡Has obtenido una recompensa: +60 de munición!",
            'health': f"¡Has obtenido una recompensa: +40 de salud!",
            'weapon': f"¡Has obtenido una recompensa: Nueva Arma(" + self.reward.get_name() + ")!"
        }
        
        reward_actions[reward_type]()
        self.last_reward = reward_type
        self.show_timed_message(reward_messages[reward_type])
    
    def draw(self, surface: pygame.Surface, character):
        """
        Dibuja el objeto en la superficie proporcionada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará el objeto
        """
        if not self.is_alive:
            return
            
        if self.current_frame < len(self.animations["default"]):
            frame = self.animations["default"][self.current_frame]
        elif self.idle_image:
            frame = self.idle_image
        else:
            return
            
        max_width, max_height = self.max_dimensions["default"]
        pos_x = self.prefab_data.x - max_width // 2
        pos_y = self.prefab_data.y - max_height // 2
        surface.blit(frame, (pos_x, pos_y))
        
        
        if self.reward is not None:
            self.draw_reward_info(surface, character)
    
    def draw_reward_info(self, surface, character):
        if self.reward_type == "weapon" and self.check_character_nearby(character):
            self.draw_character_message("Pulsa 5 para intercambiar el arma")
        elif self.check_character_nearby(character):
            self.draw_character_message("Pulsa 5 para recoger la recompensa")
        icon = self.reward.get_icon()
        # Escalar el icono a la mitad de su tamaño original
        icon_width, icon_height = icon.get_size()
        scale_factor = 0.7
        small_icon = pygame.transform.scale(icon, (int(icon_width * scale_factor), int(icon_height * scale_factor)))
        # Dibujar el icono centrado
        icon_x = self.prefab_data.x - small_icon.get_width() / 2 
        icon_y = self.prefab_data.y - small_icon.get_height() * 0.2
        surface.blit(small_icon, (icon_x, icon_y))
        
    def get_icon(self):
        """
        Obtiene el icono del cofre.
        
        Returns:
            pygame.Surface: Superficie con el icono del cofre
        """
        return self.idle_image
    
                

        
class Torch(StaticObject):
    """
    Clase que representa una antorcha en el juego.
    Tiene una animación permanente mientras esté viva.
    """
    
    def __init__(self, prefab_data: PrefabData):
        animation_path = os.path.join("resources", "objects", "Torch", "Torch-Light-Animation")
        super().__init__(prefab_data, animation_path, has_eternal_animation=True)
    
    def update(self, character):
        """
        Actualiza la animación de la antorcha.
        """
        self.update_animation()

class Hearth(StaticObject):
    """
    Clase que representa un corazón en el juego.
    No tiene animaciones, desaparece cuando el personaje está cerca.
    """
    
    def __init__(self, prefab_data: PrefabData):
        image_path = os.path.join("resources", "objects", "Hearth", "idle.png")
        super().__init__(prefab_data)
        self.idle_image = load_image(image_path)
        max_width, max_height = self.idle_image.get_size()
        self.max_dimensions = {"default": (max_width, max_height)}
    
    def update(self, character):
        """
        Actualiza el estado del corazón.
        
        Args:
            character (Character): Instancia del personaje del juego
        """
        if self.check_character_nearby(character):
            self.is_alive = False
    
    def get_icon(self):
        """
        Obtiene el icono del corazón.
        
        Returns:
            pygame.Surface: Superficie con el icono del corazón
        """
        return self.idle_image
    
    def get_name(self):
        return "Health"

class Munition(StaticObject):
    """
    Clase que representa un corazón en el juego.
    No tiene animaciones, desaparece cuando el personaje está cerca.
    """
    
    def __init__(self, prefab_data: PrefabData):
        image_path = os.path.join("resources", "objects", "Munition", "idle.png")
        super().__init__(prefab_data)
        self.idle_image = load_image(image_path)
        max_width, max_height = self.idle_image.get_size()
        self.max_dimensions = {"default": (max_width, max_height)}
    
    def update(self, character):
        """
        Actualiza el estado de la munición.
        
        Args:
            character (Character): Instancia del personaje del juego
        """
        if self.check_character_nearby(character):
            self.is_alive = False
    
    def get_icon(self):
        """
        Obtiene el icono de la munición.
        
        Returns:
            pygame.Surface: Superficie con el icono de la munición
        """
        return self.idle_image
    
    def get_name(self):
        return "Munition"