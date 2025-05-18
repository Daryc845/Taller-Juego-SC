
class PrefabData:
    def __init__(self, x: int, y: int, life: int, id: int = None):
        self.id = id
        self.x = x
        self.y = y
        self.life = life
        self.max_life = life
        self.current_shoot_direction: str = None
        self.current_bullet_type: str = None

class EnvironmentData:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.character: PrefabData = PrefabData(width // 2, height // 2, 100)
        self.enemies: list[PrefabData] = []
        self.character_points = 0

    def get_observation_space(self):
        """
        Devuelve la observacion del espacio de observacion del agente

        Returns:
            list: [x, y]
        """
        return [self.character.x, self.character.y]
    
    def add_enemy(self, enemy: PrefabData):
        self.enemies.append(enemy)

    def reset_environment(self):
        self.character.x = self.width // 2
        self.character.y = self.height // 2
        self.character.life = 100
        self.enemies.clear()