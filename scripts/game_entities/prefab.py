from scripts.game_entities.data_models import PrefabData
from scripts.game_configs import FRAME_CHANGE_EVERY, WIDTH, HEIGHT
from scripts.game_persistence import load_animations, load_idle_images
from abc import ABC
import pygame

class Prefab(ABC):
    """
    Clase base padre para representar un objeto animado en el juego.

    Attributes:
        x (int): Posición en el eje x del objeto.
        y (int): Posición en el eje y del objeto.
        speed (int): Velocidad de movimiento del objeto.
        direction (str): Dirección actual del objeto ('up', 'down', 'left', 'right') en el espacio de 2 dimensiones.
        current_frame (int): Índice del cuadro de animación actual.
        cycle_count (int): Contador de ciclos para cambiar de cuadro.
        moving (bool): Indica si el objeto se está moviendo.
        directions (dict): Diccionario con las rutas de las animaciones.
        idles (dict): Diccionario con las imágenes de estado inactivo.
        animations (dict): Diccionario con las animaciones cargadas.
        max_dimensions (dict): Dimensiones máximas de las imágenes por dirección.
        frame_update (float): Intervalo de tiempo para cambiar de cuadro(velocidad de animación).
    """

    def __init__(self, prefab_data: PrefabData, directions, frame_update=None, has_idles=True):
        self.prefab_data = prefab_data
        self.speed = 5
        self.current_frame = 0
        self.cycle_count = 0
        self.moving = False
        self.idles = load_idle_images(directions) if has_idles else {}
        self.animations, self.max_dimensions = load_animations(directions)
        self.prefab_data.max_dimensions = self.max_dimensions
        self.frame_update = frame_update if frame_update else FRAME_CHANGE_EVERY
        self.font = pygame.font.SysFont('Arial', 18, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 14)

    def do_action(self, keys: pygame.key.ScancodeWrapper, restricted_directions=[False, False, False, False]):
        
        """
        Detecta las acciones del prefab según las teclas presionadas, como moverse.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        self.moving = False
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (not restricted_directions[2]):
            self.move("up")
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (not restricted_directions[3]):
            self.move("down")
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not restricted_directions[0]):
            self.move("left")
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not restricted_directions[1]):
            self.move("right")

    def move(self, direction: str):
        """
        Mueve el objeto en la dirección actual.

        Args:
            direction (str): Dirección en la que se mueve el objeto ('up', 'down', 'left', 'right').
        """
        self.prefab_data.direction = direction
        if self.prefab_data.direction == "up" and self.prefab_data.y >= self.speed:
            self.prefab_data.y -= self.speed
        elif self.prefab_data.direction == "down" and self.prefab_data.y <= HEIGHT - self.speed:
            self.prefab_data.y += self.speed
        elif self.prefab_data.direction == "left" and self.prefab_data.x >= self.speed:
            self.prefab_data.x -= self.speed
        elif self.prefab_data.direction == "right" and self.prefab_data.x <= WIDTH - self.speed:
            self.prefab_data.x += self.speed
        self.moving = True

    def update_animation(self):
        """
        Actualiza el cuadro de animación actual según el estado de movimiento.
        """
        if self.moving:
            self.cycle_count += 1
            if self.cycle_count >= FRAME_CHANGE_EVERY:
                self.cycle_count = 0
                
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.prefab_data.direction])
        else:
            self.current_frame = 0
            
            

    def draw(self, surface: pygame.Surface):
        """
        Dibuja el objeto en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el objeto.
        """
        if self.moving and self.current_frame < len(self.animations[self.prefab_data.direction]):
            frame = self.animations[self.prefab_data.direction][self.current_frame]
        else:
            frame = self.idles[self.prefab_data.direction]

        max_width, max_height = self.max_dimensions[self.prefab_data.direction]
        pos_x = self.prefab_data.x - max_width // 2
        pos_y = self.prefab_data.y - max_height // 2
        surface.blit(frame, (pos_x, pos_y))
        self.draw_life(surface, self.prefab_data.x, self.prefab_data.y, self.prefab_data.life, self.prefab_data.max_life)

    def draw_life(self, surface: pygame.Surface, x, y, current_health:int, max_health:int, width=50, height=8, offset_y=-70):
        bar_x = x - width // 2
        bar_y = y + offset_y
        pygame.draw.rect(surface, (70, 70, 70), (bar_x, bar_y, width, height))
        health_width = int((current_health / max_health) * width)
        if current_health / max_health > 0.7:
            color = (0, 255, 0)
        elif current_health / max_health > 0.3:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(surface, color, (bar_x, bar_y, health_width, height))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, width, height), 1)
        health_text = f"{current_health}/{max_health}"
        text_surface = self.small_font.render(health_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(bar_x + width // 2, bar_y - height - 2))
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(6, 4)
        pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)
        surface.blit(text_surface, text_rect)