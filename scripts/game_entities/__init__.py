"""
Este módulo proporciona un punto de entrada central para importar todas las clases del juego.
"""

from scripts.game_entities.prefab import Prefab
from scripts.game_entities.characters import Character
from scripts.game_entities.weapon import Weapon
from scripts.game_entities.bullet import Bullet
from scripts.game_entities.weapon_types import Submachine, Rifle, Shotgun, Raygun
from scripts.game_entities.enemies import Enemy
from scripts.game_entities.enemy_types import EnemyType1, EnemyType2, EnemyType3, FinalEnemy
from scripts.game_entities.static_objects import Chest, Torch, Hearth, Munition
from scripts.game_entities.static_object import StaticObject

__all__ = [
    'Prefab',
    'Character',
    'Weapon',
    'Bullet',
    'Submachine',
    'Rifle',
    'Shotgun',
    'Raygun',
    'Enemy',
    'EnemyType1',
    'EnemyType2',
    'EnemyType3',
    'FinalEnemy',
    'Chest',
    'Torch',
    'Hearth',
    'Munition',
    'StaticObject'
]