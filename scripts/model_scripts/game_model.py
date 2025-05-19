from scripts.game_entities.data_models.data_models import PrefabData, EnvironmentData
from scripts.game_configs import WIDTH, HEIGHT
from scripts.model_scripts.numbers_model import NumbersModel
from typing import Callable

class GameModel:
    def __init__(self):
        self.numbers_model = NumbersModel()
        self.environment = EnvironmentData(WIDTH, HEIGHT)

    def reset_game(self, difficulty: str):
        print(f"Dificultad seleccionada: {difficulty}")
        self.environment.reset_environment()
        self.numbers_model.init_numbers()

    def __generate_chest(self, chest_generation_function: Callable[[str], None]):
        # TODO: generar cofre, puede ser con montecarlo o markov
        chest_generation_function("shotgun")

    def generate_enemies(self, difficulty: str, 
                         enemy_generation_function: Callable[[PrefabData, str], None]):
        # TODO: generar enemigos con dificultad, con lineas de espera, al escoger el tipo de enemigo puede ser con markov o montecarlo
        enemy1 = PrefabData(WIDTH // 4, HEIGHT // 4, 40, id=1)
        self.environment.add_enemy(enemy1)
        enemy2 = PrefabData(WIDTH // 4 * 3, HEIGHT // 4, 50, id=2)
        self.environment.add_enemy(enemy2)
        enemy3 = PrefabData(WIDTH // 4, HEIGHT // 4 * 3, 70, id=3)
        self.environment.add_enemy(enemy3)
        enemy_generation_function(self.environment.enemies[0], "type1")
        enemy_generation_function(self.environment.enemies[1], "type2")
        enemy_generation_function(self.environment.enemies[2], "type3")

    def evaluate_character_position_action(self, attack_function: Callable[[bool, int], None], 
                                           move_function: Callable[[str, int], None]):
        # TODO: calcular disparos, movimientos, y daños al jugador; con agentes
        #print(self.environment.get_observation_space())
        for en in self.environment.enemies:
            attack_function(True, en.id)
            #attack_function(False, en.id)
            #move_function("up", en.id)
            #move_function("down", en.id)
            #move_function("right", en.id)
            #move_function("left", en.id)

    def evaluate_character_shoot(self, chest_generation_function: Callable[[str], None]):
        # TODO: calcular daños a enemigos, con montecarlo, generar cofres
        # direcciones: up, down, left, right
        # tipos: submachine (cada tiro x4 balas), rifle (cada tiro x3 balas), shotgun (cada tiro x1 bala), raygun (cada tiro x1 bala)
        print(self.environment.character.current_bullet_type, 
              self.environment.character.current_shoot_direction,
              self.environment.character.bullets_count)
        self.__generate_chest(chest_generation_function)

    def __get_pseudo_random_number(self):
        return self.numbers_model.get_next_pseudo_random_number()