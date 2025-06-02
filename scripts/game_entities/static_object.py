import pygame
import os
from scripts.game_persistence import load_animations, load_image
from scripts.game_entities.data_models import PrefabData
from scripts.game_configs import FRAME_CHANGE_EVERY
from abc import ABC

class StaticObject(ABC):
    """
    Clase padre para representar objetos estáticos en el juego.
    Estos objetos tienen una posición fija y pueden tener animaciones.
    
    Attributes:
        prefab_data (PrefabData): Datos del objeto (posición, vida, etc.)
        animations (dict): Diccionario con las animaciones cargadas
        current_frame (int): Índice del cuadro de animación actual
        cycle_count (int): Contador de ciclos para cambiar de cuadro
        max_dimensions (dict): Dimensiones máximas de las imágenes
        frame_update (float): Intervalo para cambiar de cuadro (velocidad animación)
        has_eternal_animation (bool): Si el objeto tiene animación permanente
        is_alive (bool): Si el objeto está activo en pantalla
    """
    
    def __init__(self, prefab_data: PrefabData, animation_path: str = None, frame_update=None, has_eternal_animation=False):
        self.prefab_data = prefab_data
        self.current_frame = 0
        self.cycle_count = 0
        self.frame_update = frame_update if frame_update else FRAME_CHANGE_EVERY
        self.has_eternal_animation = has_eternal_animation
        self.is_alive = True
        
        # Cargar animaciones si se proporciona una ruta
        if animation_path:
            directions = {"default": animation_path}
            self.animations, self.max_dimensions = load_animations(directions)
            self.idle_image = load_image(os.path.join(animation_path, "idle.png"))
        else:
            self.animations = {}
            self.max_dimensions = {"default": (0, 0)}
            self.idle_image = None
    
    def update_animation(self):
        """
        Actualiza la animación del objeto si tiene animación permanente.
        """
        if self.has_eternal_animation and self.is_alive:
            self.cycle_count += 1
            if self.cycle_count >= self.frame_update:
                self.cycle_count = 0
                self.current_frame = (self.current_frame + 1) % len(self.animations["default"])
    
    def play_animation_once(self):
        """
        Reproduce una animación una sola vez.
        """
        if not self.is_alive:
            return
            
        if self.current_frame < len(self.animations["default"]) - 1:
            self.current_frame += 1
        else:
            self.on_animation_end()
    
    def on_animation_end(self):
        """
        Método llamado cuando termina una animación no permanente.
        Puede ser sobrescrito por clases hijas.
        """
        pass
    
    def check_character_nearby(self, character):
        """
        Verifica si el personaje está cerca del objeto.
        
        Args:
            character (Character): Instancia del personaje del juego
            
        Returns:
            bool: True si el personaje está cerca, False en caso contrario
        """
        if not character:
            return False
            
        distance = ((self.prefab_data.x - character.prefab_data.x)**2 + 
                   (self.prefab_data.y - character.prefab_data.y)**2)**0.5
        return distance < 70  # Radio de proximidad
    
    def draw(self, surface: pygame.Surface):
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