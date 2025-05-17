"""
Este módulo proporciona un punto de entrada central para importar todas las clases del juego.
"""

from scripts.game_entities.prefab import Prefab
from scripts.game_entities.characters import Character
from scripts.game_entities.weapon import Weapon
from scripts.game_entities.bullet import Bullet
from scripts.game_entities.weapon_types import Submachine, Rifle, Shotgun, Raygun

__all__ = [
    'Prefab',
    'Character',
    'Weapon',
    'Bullet',
    'Submachine',
    'Rifle',
    'Shotgun',
    'Raygun'
]