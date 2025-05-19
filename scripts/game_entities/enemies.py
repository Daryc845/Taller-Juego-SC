from scripts.game_entities.prefab import Prefab
from scripts.game_configs import WEAPON_RAYGUN_FOLDER
from scripts.game_entities.bullet import Bullet
from scripts.game_entities.data_models import PrefabData
from scripts.game_persistence import load_image, load_animations
import os
import pygame
from abc import ABC, abstractmethod

class Enemy(Prefab, ABC):
    def __init__(self, prefab_data: PrefabData, directions, frame_update=None):
        super().__init__(prefab_data, directions, frame_update, has_idles=False)
        self.direction = "right"
        self.last_direction = "right"
        self.moving = False
        self.attacking = False
        self.attack_animations, self.attack_max_dimensions = load_animations(self.get_attack_directions())
    
    @abstractmethod
    def get_attack_directions(self):
        """
        Método abstracto que devuelve las direcciones de animación de ataque.
        Debe ser implementado por las clases hijas.
        
        Returns:
            dict: Diccionario con las rutas de las animaciones de ataque.
        """
        pass

    def move(self, direction: str):
        super().move(direction)
        if self.direction != 'right' and self.direction != 'left':
            self.direction = "right" if "right" in self.last_direction else "left"
        self.last_direction = self.direction

    def attack(self):
        """
        Realiza un ataque al objetivo.
        """
        self.attacking = True
        if not self.attacking:
            self.current_frame = 0
        self.moving = False
    
    def update_animation(self):
        """
        Actualiza el cuadro de animación actual según el estado del enemigo.
        """
        self.cycle_count += 1
        
        if self.attacking:
            if self.cycle_count >= self.frame_update:
                self.cycle_count = 0
                self.current_frame = (self.current_frame + 1) % len(self.attack_animations[self.direction])
                if self.current_frame == 0:
                    self.attacking = False
        elif self.moving:
            if self.cycle_count >= self.frame_update:
                self.cycle_count = 0
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.direction])
        else:
            self.current_frame = 0
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el enemigo en la superficie proporcionada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará el enemigo.
        """
        if self.attacking:
            frame = self.attack_animations[self.direction][self.current_frame]
            max_width, max_height = self.attack_max_dimensions[self.direction]
        else:
            frame = self.animations[self.direction][self.current_frame]
            max_width, max_height = self.max_dimensions[self.direction]
            
        pos_x = self.prefab_data.x - max_width // 2
        pos_y = self.prefab_data.y - max_height // 2
        surface.blit(frame, (pos_x, pos_y))
        super().draw_life(surface, self.prefab_data.x, self.prefab_data.y, self.prefab_data.life, self.prefab_data.max_life)

class ShooterEnemy(Enemy, ABC):
    def __init__(self, prefab_data: PrefabData, directions):
        super().__init__(prefab_data, directions)
        self.attack_delay_counter = 50
        bullet_path = os.path.join(WEAPON_RAYGUN_FOLDER, "bullet.png")
        self.bullet_image = load_image(bullet_path)
        self.bullets_fired : list[Bullet] = []
        self.max_bullets_per_shot = 5

    @abstractmethod
    def get_attack_directions(self):
        pass

    def attack(self):
        super().attack()
        ca_add_bullet = list(filter(lambda x: x.alive, self.bullets_fired))
        if len(ca_add_bullet) >= self.max_bullets_per_shot:
            return
        bullet = Bullet(self.prefab_data.x + (40 if "right" in self.direction else -40), self.prefab_data.y - 40, self.direction, 100, self.bullet_image)
        self.bullets_fired.append(bullet)

    def draw(self, surface):
        super().draw(surface)
        for bullet in self.bullets_fired:
            if bullet.alive:
                bullet.move()
                bullet.draw(surface)
            else:
                self.bullets_fired.remove(bullet)
