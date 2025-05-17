from scripts.game_configs import FRAME_CHANGE_EVERY
from scripts.game_persistence import load_animations, load_idle_images
import pygame

class Prefab():
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

    def __init__(self, x, y, directions, frame_update=None):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = "down"
        self.current_frame = 0
        self.cycle_count = 0
        self.moving = False
        self.idles = load_idle_images(directions)
        self.animations, self.max_dimensions = load_animations(directions)
        self.frame_update = frame_update if frame_update else FRAME_CHANGE_EVERY

    def do_action(self, keys: pygame.key.ScancodeWrapper):
        """
        Detecta las acciones del prefab según las teclas presionadas, como moverse.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        self.moving = False
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = "up"
            self.moving = True
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = "down"
            self.moving = True
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
            self.moving = True

    def update_animation(self):
        """
        Actualiza el cuadro de animación actual según el estado de movimiento.
        """
        if self.moving:
            self.cycle_count += 1
            if self.cycle_count >= FRAME_CHANGE_EVERY:
                self.cycle_count = 0
                
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.direction])
        else:
            self.current_frame = 0

    def draw(self, surface: pygame.Surface):
        """
        Dibuja el objeto en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el objeto.
        """
        if self.moving and self.current_frame < len(self.animations[self.direction]):
            frame = self.animations[self.direction][self.current_frame]
        else:
            frame = self.idles[self.direction]

        max_width, max_height = self.max_dimensions[self.direction]
        pos_x = self.x - max_width // 2
        pos_y = self.y - max_height // 2
        surface.blit(frame, (pos_x, pos_y))