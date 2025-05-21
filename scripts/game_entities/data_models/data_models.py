
class AttackData:
    def __init__(self, id: int, x: int, y: int, damage: int, direction: str, type: str):
        self.id = id
        self.x = x
        self.y = y
        self.damage = damage
        self.direction = direction
        self.type = type # melee, enemy_3_shoot, final_enemy_shoot, submachine, rifle, shotgun, raygun
        self.alive = True

class PrefabData:
    def __init__(self, x: int, y: int, direction: str, life: int, id: int = None):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.life = life
        self.max_life = life
        self.max_dimensions = {}
        self.attacks: list[AttackData] = []

class EnvironmentData:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.character: PrefabData = PrefabData(width // 2, height // 2, "down", 500)
        self.enemies: list[PrefabData] = []
        self.character_points = 0

    def get_observation_space(self):
        """
        Devuelve el espacio de observación, para los agentes, que es la posición del personaje.

        Returns:
            list: [x, y]
        """
        return [self.character.x, self.character.y]
    
    def add_enemy(self, enemy: PrefabData):
        self.enemies.append(enemy)

    def reset_environment(self):
        self.character.x = self.width // 2
        self.character.y = self.height // 2
        self.character_points = 0
        self.character.direction = "down"
        self.character.life = 500
        self.character.attacks.clear()
        self.enemies.clear()