from scripts.game_configs import ENEMY_1_FOLDER, ENEMY_2_FOLDER, ENEMY_3_FOLDER
from scripts.game_entities.data_models.data_models import PrefabData
from scripts.game_entities.enemies import Enemy,ShooterEnemy
import os

class EnemyType1(Enemy):
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

class EnemyType2(Enemy):
    def __init__(self, prefab_data: PrefabData):
        dirs = {
            "left": os.path.join(ENEMY_2_FOLDER, "left"),
            "right": os.path.join(ENEMY_2_FOLDER, "right")
        }
        super().__init__(prefab_data, dirs)

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

class FinalEnemy(ShooterEnemy):
    def __init__(self, prefab_data: PrefabData):
        dirs = {
            "left": os.path.join(ENEMY_3_FOLDER, "left"),
            "right": os.path.join(ENEMY_3_FOLDER, "right")
        }
        super().__init__(prefab_data, dirs)

    def get_attack_directions(self):
        return {
            "left": os.path.join(ENEMY_3_FOLDER, "shadow_wizard-animation-left_attacking"),#TODO
            "right": os.path.join(ENEMY_3_FOLDER, "shadow_wizard-animation-right_attacking")#TODO
        }