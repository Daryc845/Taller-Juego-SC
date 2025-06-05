from scripts.game_entities.prefab import Prefab
from scripts.game_configs import ENEMY_3_FOLDER
from scripts.game_entities.bullet import Bullet
from scripts.game_entities.data_models import PrefabData, AttackData
from scripts.game_persistence import load_image, load_animations
import os
import pygame
from abc import ABC, abstractmethod

class Enemy(Prefab, ABC):
    def __init__(self, prefab_data: PrefabData, directions, frame_update=4):
        super().__init__(prefab_data, directions, frame_update, has_idles=False)
        self.last_direction = "right"
        self.moving = False
        self.attacking = False
        self.attack_animations, self.attack_max_dimensions = load_animations(self.get_attack_directions())
        self.attack_count_id = 0
        self.width, self.height = self.max_dimensions[self.prefab_data.frame_direction]
        self.blink_counter = 0
        self.blink_interval = 10
        self.blink_visible = True
    
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
        self.prefab_data.frame_direction = direction
        if self.prefab_data.frame_direction != 'right' and self.prefab_data.frame_direction != 'left':
            self.prefab_data.frame_direction = "right" if "right" in self.last_direction else "left"
        self.last_direction = self.prefab_data.frame_direction

    def attack(self):
        """
        Realiza un ataque al objetivo.
        """
        self.attacking = True
        if not self.attacking:
            self.current_frame = 0
    
    def update_animation(self):
        """
        Actualiza el cuadro de animación actual según el estado del enemigo.
        """
        self.cycle_count += 1
        
        if self.attacking:
            if self.cycle_count >= self.frame_update:
                self.cycle_count = 0
                self.current_frame = (self.current_frame + 1) % len(self.attack_animations[self.prefab_data.frame_direction])
                if self.current_frame == 0:
                    self.attacking = False
        elif self.moving:
            if self.cycle_count >= self.frame_update:
                self.cycle_count = 0
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.prefab_data.frame_direction])
        else:
            self.current_frame = 0
    
    def draw(self, surface: pygame.Surface, in_pause=False):
        """
        Dibuja el enemigo en la superficie proporcionada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará el enemigo.
        """
        
        if self.attacking:
            frame = self.attack_animations[self.prefab_data.frame_direction][self.current_frame]
            max_width, max_height = self.attack_max_dimensions[self.prefab_data.frame_direction]
        else:
            self.blink_counter += 1
            if self.blink_counter >= self.blink_interval:
                self.blink_counter = 0
                self.blink_visible = not self.blink_visible
            frame = self.animations[self.prefab_data.frame_direction][self.current_frame]
            max_width, max_height = self.max_dimensions[self.prefab_data.frame_direction]
            if not self.blink_visible:
                frame.set_alpha(130)
            else:
                frame.set_alpha(180)
         
        pos_x = self.prefab_data.x - max_width // 2
        pos_y = self.prefab_data.y - max_height // 2
        surface.blit(frame, (pos_x, pos_y))
        super().draw_life(surface, self.prefab_data.x, self.prefab_data.y, self.prefab_data.life, self.prefab_data.max_life)

class MeleeEnemy(Enemy, ABC):
    def __init__(self, prefab_data: PrefabData, directions):
        super().__init__(prefab_data, directions)

    def update_animation(self):
        super().update_animation()
        middle_animation = len(self.attack_animations[self.prefab_data.frame_direction]) // 2
        if self.attacking and self.current_frame == middle_animation:
            x = self.prefab_data.x + (self.width // 2) if "right" in self.prefab_data.frame_direction else self.prefab_data.x - (self.width // 2)
            data = AttackData(self.attack_count_id, x, self.prefab_data.y, 
                              15, self.prefab_data.direction, "melee")
            self.prefab_data.attacks.append(data)
            self.attack_count_id += 1

    @abstractmethod
    def get_attack_directions(self):
        pass

class ShooterEnemy(Enemy, ABC):
    def __init__(self, prefab_data: PrefabData, directions):
        super().__init__(prefab_data, directions)
        self.attack_delay_counter = 0
        self.attack_cooldown = 30
        bullet_path = os.path.join(ENEMY_3_FOLDER, "ray_shadow.png")
        self.bullet_image = load_image(bullet_path)
        self.bullets_fired : list[Bullet] = []

    @abstractmethod
    def get_attack_directions(self):
        pass

    def update_animation(self):
        super().update_animation()
        if self.attack_delay_counter > 0:
            self.attack_delay_counter -= 1
        # Calcula el frame en el 73% de la animación de ataque
        attack_frames = len(self.attack_animations[self.prefab_data.frame_direction])
        late_frame = int(attack_frames * 0.73)
        if self.attacking and self.current_frame == late_frame and self.attack_delay_counter == 0:
            data = AttackData(
                self.attack_count_id,
                self.prefab_data.x + (40 if "right" in self.prefab_data.frame_direction else -40),
                self.prefab_data.y - 40,
                self.get_shoot_damage(),
                self.prefab_data.direction,
                self.get_shoot_type()
            )
            self.prefab_data.attacks.append(data)
            self.attack_count_id += 1
            bullet = Bullet(data, self.bullet_image)
            self.bullets_fired.append(bullet)
            self.attack_delay_counter = self.attack_cooldown

    def draw(self, surface, in_pause=False):
        super().draw(surface)
        for bullet in self.bullets_fired:
            if bullet.data.alive:
                if not in_pause:
                    bullet.move()
                bullet.draw(surface)
            else:
                self.bullets_fired.remove(bullet)

    @abstractmethod
    def get_shoot_damage(self)->int:
        pass

    @abstractmethod
    def get_shoot_type(self)->str:
        pass