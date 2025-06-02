from scripts.game_configs import ENEMY_1_FOLDER, ENEMY_2_FOLDER, ENEMY_3_FOLDER, ENEMY_4_FOLDER
from scripts.game_entities.data_models import PrefabData, AttackData
from scripts.game_entities.enemies import MeleeEnemy,ShooterEnemy
from scripts.game_entities.bullet import Bullet
from scripts.game_persistence import load_image
import os
import pygame

class EnemyType1(MeleeEnemy):
    def __init__(self, prefab_data: PrefabData):
        dirs = {
            "left": os.path.join(ENEMY_1_FOLDER, "left"),
            "right": os.path.join(ENEMY_1_FOLDER, "right")
        }
        super().__init__(prefab_data, dirs)

    def get_attack_directions(self):
        return {
            "left": os.path.join(ENEMY_1_FOLDER, "shadow_knight-animation-left_attacking"),
            "right": os.path.join(ENEMY_1_FOLDER, "shadow_knight-animation-right_attacking")
        }

class EnemyType2(MeleeEnemy):
    def __init__(self, prefab_data: PrefabData):
        dirs = {
            "left": os.path.join(ENEMY_2_FOLDER, "left"),
            "right": os.path.join(ENEMY_2_FOLDER, "right")
        }
        super().__init__(prefab_data, dirs)
        self.speed = self.prefab_data.speed

    def get_attack_directions(self):
        return {
            "left": os.path.join(ENEMY_2_FOLDER, "shadow_jester-animation-left_attacking"),
            "right": os.path.join(ENEMY_2_FOLDER, "shadow_jester-animation-right_attacking")
        }

class EnemyType3(ShooterEnemy):
    def __init__(self, prefab_data: PrefabData):
        dirs = {
            "left": os.path.join(ENEMY_3_FOLDER, "left"),
            "right": os.path.join(ENEMY_3_FOLDER, "right")
        }
        super().__init__(prefab_data, dirs)

    def get_attack_directions(self):
        return {
            "left": os.path.join(ENEMY_3_FOLDER, "shadow_wizard-animation-left_attacking"),
            "right": os.path.join(ENEMY_3_FOLDER, "shadow_wizard-animation-right_attacking")
        }
    
    def get_shoot_damage(self):
        return 15
    
    def get_shoot_type(self):
        return "enemy_3_shoot"

class FinalEnemy(ShooterEnemy, MeleeEnemy):
    def __init__(self, prefab_data: PrefabData):
        dirs = {
            "left": os.path.join(ENEMY_4_FOLDER, "left"),
            "right": os.path.join(ENEMY_4_FOLDER, "right")
        }
        super().__init__(prefab_data, dirs)
        bullet_path = os.path.join(ENEMY_4_FOLDER, "ray_light.png")
        self.bullet_image = load_image(bullet_path)
        self.current_attack_type = "melee"

    def get_attack_directions(self):
        return {
            "left": os.path.join(ENEMY_4_FOLDER, "shadow_king-animation-left_attacking"),#TODO
            "right": os.path.join(ENEMY_4_FOLDER, "shadow_king-animation-right_attacking")#TODO
        }
    
    def attack(self, type: str):
        self.current_attack_type = type
        super().attack()

    def draw(self,surface: pygame.Surface, in_pause=False):
        if self.current_attack_type == "melee":
            MeleeEnemy.draw(self, surface, in_pause=in_pause)
        else:
            ShooterEnemy.draw(self, surface, in_pause=in_pause)

    def update_animation(self):
        if self.current_attack_type == "melee":
            MeleeEnemy.update_animation(self)
        else:
            self.update_shooter()
            
    def update_shooter(self):
        super().update_animation()
        if self.attack_delay_counter > 0:
            self.attack_delay_counter -= 1
        # Calcula el frame en el 37% de la animación de ataque
        attack_frames = len(self.attack_animations[self.prefab_data.frame_direction])
        late_frame = int(attack_frames * 0.37)
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
    
    def get_shoot_damage(self):
        return 40
    
    def get_shoot_type(self):
        return "final_enemy_shoot"