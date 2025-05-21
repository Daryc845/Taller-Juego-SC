from abc import ABC, abstractmethod
from scripts.game_configs import FRAME_CHANGE_EVERY
from scripts.game_entities.bullet import Bullet
from scripts.game_persistence import load_image, load_animations, load_idle_images
import os
import pygame

class Weapon(ABC):
    """
    Representa un arma con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si el arma está disparando.
        max_munition (int): Munición máxima del arma.
        remaining_munition (int): Munición restante del arma.
        bullets_fired (list): Lista de balas disparadas por el arma.
        bullet_image (pygame.Surface): Imagen de la bala disparada por el arma.
    """

    def __init__(self, x, y, directions, bullet_folder_url, frame_update=None, direction="down"):
        self.x = x
        self.y = y
        self.direction = direction
        self.moving = False
        self.speed = 5
        self.cycle_count = 0
        self.idles = load_idle_images(directions)
        self.animations, self.max_dimensions = load_animations(directions)
        self.frame_update = frame_update if frame_update else FRAME_CHANGE_EVERY
        self.bullet_image = load_image(os.path.join(bullet_folder_url, "bullet.png"))
        self.shooting = False
        self.max_munition = 100
        self.remaining_munition = self.max_munition
        self.bullets_fired: list[Bullet] = []

    def set_position(self, x, y):
        """
        Establece la posición del arma.

        Args:
            x (int): Nueva posición en el eje x.
            y (int): Nueva posición en el eje y.

        Returns:
            Weapon: La instancia actual del arma en la posición indicada.
        """
        self.x = x
        self.y = y
        return self

    def do_action(self, keys):
        """
        Realiza acciones del arma según las teclas presionadas, como disparar.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        self.shooting = False
        self.moving = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = "up"
            self.y -= self.speed
            self.moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = "down"
            self.y += self.speed
            self.moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = "left"
            self.x -= self.speed
            self.moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = "right"
            self.x += self.speed
            self.moving = True
        if keys[pygame.K_SPACE]:
            self.shooting = True

    def shoot(self, bullet_data_creation):
        """
        Dispara el arma, reduciendo la munición restante.
        Adicionalmente, crea una nueva bala y la agrega a la lista de balas disparadas.
        Esto es con el fin de tener control e información de las balas disparadas.
        """
        data = bullet_data_creation(self.x, self.y, self.direction, self.get_bullet_damage(), self.get_bullet_type())
        self.remaining_munition -= 1
        self.bullets_fired.append(Bullet(data, self.bullet_image))

    def update_animation(self, bullet_data_creation):
        """
        Actualiza las animaciones del arma según su estado (disparando o inactiva).
        """
        self.cycle_count += 1
        if self.shooting:
            if self.cycle_count >= self.frame_update:
                self.evaluate_bullets_and_shoot(bullet_data_creation)
        else:
            self.current_frame = 0
        
    def evaluate_bullets_and_shoot(self, bullet_data_creation):
        """
        Verifica si el arma tiene munición restante y actualiza el cuadro de animación.
        Si no hay munición, muestra un mensaje indicando que no se puede disparar.
        """
        if self.remaining_munition > 0:
            self.cycle_count = self.cycle_count / 2
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.direction])
        else:
            self.current_frame = 0
        if self.current_frame == 1:
            self.shoot(bullet_data_creation)
    
    def draw_bullets(self, surface: pygame.Surface, in_pause=False):
        """
        Dibuja las balas disparadas por el arma en la superficie proporcionada.
        """
        for bullet in self.bullets_fired:
            if bullet.data.alive:
                if not in_pause:
                    bullet.move()
                bullet.draw(surface)
            else:
                self.bullets_fired.remove(bullet)

    def draw(self, surface: pygame.Surface):
        """
        Dibuja el arma en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el arma.
        """
        if self.shooting and self.current_frame < len(self.animations[self.direction]):
            frame = self.animations[self.direction][self.current_frame]
        else:
            frame = self.idles[self.direction]
        adjust_positions = self.adjust_position()
        surface.blit(frame, adjust_positions)

    def adjust_position(self):
        """
        Ajusta la posición del arma según su dirección y la posición de Chester.
        
        Returns:
            tuple: Posición ajustada (x, y) del arma.
        """
        max_width, max_height = self.max_dimensions[self.direction]
        pos_x = (self.x - max_width // 2)
        pos_y = (self.y - max_height // 2)
        if(self.direction == "up"):
            pos_y = (self.y - max_height // 2) - 5
        elif(self.direction == "down"):
            pos_y = (self.y - max_height // 2) +25
        elif(self.direction == "left"):
            pos_x = (self.x - max_height // 2) - 50
        else:
            pos_x = (self.x - max_height // 2) - 21
        return pos_x, pos_y
    
    @abstractmethod
    def get_directions(self):
        """
        Devuelve un diccionario con las rutas de las animaciones del subfusil.

        Returns:
            dictionary: diccionario que relaciona las animaciones de una ruta con una dirección particular.
        """
        pass

    @abstractmethod
    def get_bullet_type(self)->str:
        """
        Devuelve el tipo de bala que el arma dispara.
        """
        pass

    @abstractmethod
    def get_bullet_damage(self)->int:
        """
        Devuelve el daño de la bala que el arma dispara.
        """
        pass