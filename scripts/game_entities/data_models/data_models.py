
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
    def __init__(self, x: int, y: int, direction: str, life: int, id: int = None, 
                 frame_direction: str = "right", type: str = None, speed: int = 5):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.life = life
        self.max_life = life
        self.max_dimensions = {}
        self.attacks: list[AttackData] = []
        self.frame_direction = frame_direction
        self.type = type # tipos: type1, type2, type3, final, (None en caso del jugador)
        self.action_counter = 0
        self.in_strategy = False
        self.speed = speed

class EnvironmentData:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.character: PrefabData = PrefabData(width // 2, height // 2, "down", 500)
        self.enemies: list[PrefabData] = []
        self.character_points = 0

    def get_observation_space(self):
        """
        Devuelve el espacio de observación, para los agentes, que es la posición del personaje, 
        y sus limites.

        Returns:
            x, y, max_x, min_x, max_y, min_y
        """
        x, y = self.character.x, self.character.y
        width, height = self.character.max_dimensions[self.character.direction]
        max_x, min_x = x + (width//2), x - (width//2)
        max_y, min_y = y + (height//2), y - (height//2)
        return x, y, max_x, min_x, max_y, min_y
    
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