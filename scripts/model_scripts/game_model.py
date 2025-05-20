from scripts.game_entities.data_models import PrefabData, EnvironmentData, AttackData
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
        enemy1 = PrefabData(WIDTH // 4, HEIGHT // 4, 'right', 40, id=1)
        self.environment.add_enemy(enemy1)
        enemy2 = PrefabData(WIDTH // 4 * 3, HEIGHT // 4, 'left', 50, id=2)
        self.environment.add_enemy(enemy2)
        enemy3 = PrefabData(WIDTH // 4, HEIGHT // 4 * 3, 'right', 70, id=3)
        self.environment.add_enemy(enemy3)
        enemy_generation_function(self.environment.enemies[0], "type1")
        enemy_generation_function(self.environment.enemies[1], "type2")
        enemy_generation_function(self.environment.enemies[2], "type3")

    def evaluate_character_position_action(self, attack_function: Callable[[bool, int], None], 
                                           move_function: Callable[[str, int], None]):
        # TODO: calcular movimientos, y ataques al jugador, segun el tipo de enemigo; con agentes
        #print(self.environment.get_observation_space())
        for en in self.environment.enemies:
            attack_function(True, en.id)
            #attack_function(False, en.id)
            #move_function("up", en.id)
            #move_function("down", en.id)
            #move_function("right", en.id)
            #move_function("left", en.id)

    def evaluate_attacks(self, chest_generation_function: Callable[[str], None]):
        # TODO: calcular daños a enemigos y al jugador, con montecarlo, generar cofres
        character_shoots = list(filter(lambda x: x.alive, self.environment.character.attacks))
        enemies_death: list[PrefabData] = []
        for shoot in character_shoots:
            for en in self.environment.enemies:
                if self.__verify_shoot_damage(shoot, en, True):
                    shoot.alive = False
                    if en.life <= 0:
                        enemies_death.append(en)
                        #TODO: aumentar puntaje de jugador
                    break
        for en in self.environment.enemies:
            en_shoots = list(filter(lambda x: x.alive, en.attacks))
            for shoot in en_shoots:
                if self.__verify_shoot_damage(shoot, self.environment.character, False):
                    shoot.alive = False
                    if self.environment.character.life <= 0:
                        #TODO: notificar muerte de jugador
                        pass
                elif shoot.type == "melee":
                    shoot.alive = False
        for en in enemies_death:
            self.environment.enemies.remove(en)
            #TODO: notificar muerte de enemigo
        # generar cofre si el jugador consigue X puntaje
        self.__generate_chest(chest_generation_function)

    def __get_pseudo_random_number(self):
        return self.numbers_model.get_next_pseudo_random_number()
    
    def __verify_shoot_damage(self, shoot: AttackData, to: PrefabData, is_enemy: bool)-> bool:
        direction_to = to.direction
        if is_enemy:
            direction_to = "left"
        X, Y = to.max_dimensions[direction_to]
        if shoot.direction == "left" or shoot.direction == "right":
            if to.x - (X * 0.5) <= shoot.x and to.x + (X * 0.5) >= shoot.x:
                is_hit, interval = self.__verify_and_get_shoot_interval(Y, to.y, shoot.y)
            else:
                return False
        else:
            if to.y - (Y * 0.5) <= shoot.y and to.y + (Y * 0.5) >= shoot.y:
                is_hit, interval = self.__verify_and_get_shoot_interval(X, to.x, shoot.x)
            else:
                return False
        if is_hit:
            to.life -= (shoot.damage - interval) #TODO: usar montecarlo para aleatorizar daño
            return True
        return False

    def __verify_and_get_shoot_interval(self, dim: int, pos: int, shoot_pos: int)-> tuple[bool, int]:
        a_min, a_max = pos - (dim * 0.05), pos + (dim * 0.05)
        b_min, b_max = pos - (dim * 0.25), pos + (dim * 0.25)
        c_min, c_max = pos - (dim * 0.5), pos + (dim * 0.5)
        if shoot_pos >= a_min and shoot_pos <= a_max:
            return True, 0
        elif shoot_pos >= b_min and shoot_pos <= b_max:
            return True, 1
        elif shoot_pos >= c_min and shoot_pos <= c_max:
            return True, 2
        return False, 0
