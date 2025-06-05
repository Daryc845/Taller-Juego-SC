import pygame
from scripts.game_configs import WIDTH, HEIGHT
from scripts.game_entities.data_models import AttackData

class Bullet:
    """
    Representa una bala disparada por un arma.
    
    Atributes:
        x (int): Posición en el eje x de la bala.
        y (int): Posición en el eje y de la bala.
        direction (str): Dirección en la que se mueve la bala ('up', 'down', 'left', 'right').
        alive (bool): Indica si la bala está viva o no.
        speed (int): Velocidad de movimiento de la bala.
        damage (int): Daño que causa la bala al impactar.
        image (pygame.Surface): Imagen de la bala.
    """
        
    def __init__(self, data: AttackData, image):
        self.data = data
        self.image = image
        self.speed = 10
        self.adjust_position()
    
    def adjust_position(self):
        """
        Ajusta la posición de la bala según su dirección.
        Si la dirección es 'up' o 'down', ajusta la posición en el eje x.
        Si la dirección es 'left' o 'right', ajusta la posición en el eje y.
        """
        if self.data.direction == "up" or self.data.direction == "down":
            self.data.x -= 4
        else:
            self.data.y -= 13

    def move(self):
        """
        Mueve la bala en la dirección especificada. 
        Adicionalmente, verifica si la bala debe ser eliminada y la elimina.
        """
        if self.data.direction == "up":
            self.data.y -= self.speed
        elif self.data.direction == "down":
            self.data.y += self.speed
        elif self.data.direction == "left":
            self.data.x -= self.speed
        elif self.data.direction == "right":
            self.data.x += self.speed
        self.evaluate_kill_bullet()
    
    
    def evaluate_kill_bullet(self):
        """
        Verifica si la bala ha salido de la pantalla, halla golpeado un objeto o un enemigo. 
        Si es así, marca la bala como no viva. Esto se hace para evitar que la bala siga existiendo indefinidamente.
        """
        if (self.data.x < 0 or self.data.x > WIDTH or self.data.y < 0 or self.data.y > HEIGHT):
            self.data.alive = False

    def draw(self, surface: pygame.Surface):
        """
        Dibuja la bala en la superficie proporcionada unicamente si se encuentra viva.
        """
        if self.data.alive:
            surface.blit(self.image, (self.data.x, self.data.y))
            