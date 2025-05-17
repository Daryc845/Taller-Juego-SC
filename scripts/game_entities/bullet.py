import pygame
from scripts.game_configs import WIDTH, HEIGHT

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
        
    def __init__(self, x, y, direction, damage, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image
        self.alive = True
        self.speed = 10
        self.damage = damage #Usar para el daño
        self.adjust_position()
    
    def adjust_position(self):
        """
        Ajusta la posición de la bala según su dirección.
        Si la dirección es 'up' o 'down', ajusta la posición en el eje x.
        Si la dirección es 'left' o 'right', ajusta la posición en el eje y.
        """
        if self.direction == "up" or self.direction == "down":
            self.x -= 4
        else:
            self.y -= 13

    def move(self):
        """
        Mueve la bala en la dirección especificada. 
        Adicionalmente, verifica si la bala debe ser eliminada y la elimina.
        """
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        #Mata a la bala si sale de la pantalla(TAMBIEN DEBE DESAPARECER SI CHOCA CON UN ENEMIGO U OBJETO)
        self.evaluate_kill_bullet()
    
    
    def evaluate_kill_bullet(self):
        """
        Verifica si la bala ha salido de la pantalla, halla golpeado un objeto o un enemigo. 
        Si es así, marca la bala como no viva. Esto se hace para evitar que la bala siga existiendo indefinidamente.
        """
        if (self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT):
            self.alive = False

    def draw(self, surface: pygame.Surface):
        """
        Dibuja la bala en la superficie proporcionada unicamente si se encuentra viva.
        """
        if self.alive:
            surface.blit(self.image, (self.x, self.y))
            