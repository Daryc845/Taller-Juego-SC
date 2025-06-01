from scripts.game_configs import ENEMY_1_FOLDER, ENEMY_2_FOLDER, ENEMY_3_FOLDER
from scripts.game_entities.data_models import PrefabData
from scripts.game_entities.enemies import MeleeEnemy,ShooterEnemy
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
        return 7
    
    def get_shoot_type(self):
        return "enemy_3_shoot"

class FinalEnemy(ShooterEnemy, MeleeEnemy):
    def __init__(self, prefab_data: PrefabData):
        dirs = {
            "left": os.path.join(ENEMY_3_FOLDER, "left"),
            "right": os.path.join(ENEMY_3_FOLDER, "right")
        }
        super().__init__(prefab_data, dirs)
        self.current_attack_type = "melee"

    def get_attack_directions(self):
        return {
            "left": os.path.join(ENEMY_3_FOLDER, "shadow_wizard-animation-left_attacking"),#TODO
            "right": os.path.join(ENEMY_3_FOLDER, "shadow_wizard-animation-right_attacking")#TODO
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
            ShooterEnemy.update_animation(self)
    
    def get_shoot_damage(self):
        return 9
    
    def get_shoot_type(self):
        return "final_enemy_shoot"