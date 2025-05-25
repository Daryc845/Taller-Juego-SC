from scripts.game_entities.data_models import PrefabData, EnvironmentData, AttackData
from scripts.game_configs import WIDTH, HEIGHT
from scripts.model_scripts.numbers_model import NumbersModel
from typing import Callable
import math

class GameModel:
    def __init__(self):
        self.numbers_model = NumbersModel()
        self.environment = EnvironmentData(WIDTH, HEIGHT)
        self.in_pause = False # TODO: pausa para generar enemigos
        self.terminate = False # TODO: para terminar ejecucion hilo de generacion de enemigos

    def reset_game(self, difficulty: str):
        print(f"Dificultad seleccionada: {difficulty}")
        self.environment.reset_environment()
        self.numbers_model.init_numbers()

    def reset_to_second_phase(self):
        width, height = self.environment.width, self.environment.height
        self.environment.character.attacks.clear()
        self.environment.character.x = width // 2
        self.environment.character.y = height // 2

    def verify_first_phase(self, next_phase_function: Callable[[], None]):
        while not self.terminate:
            if len(self.environment.enemies) == 0:
                next_phase_function()
                break

    def verify_second_phase(self, game_won_function: Callable[[int], None]):
        #TODO: verificar que se venza el enemigo final, llamar a la funcion si se vence
        import time
        time.sleep(7)
        game_won_function(self.environment.character_points)
        pass

    def __generate_chest(self, chest_generation_function: Callable[[str], None]):
        # TODO: generar cofre, puede ser con montecarlo o markov
        chest_generation_function("shotgun")

    def generate_enemies(self, difficulty: str, 
                         enemy_generation_function: Callable[[PrefabData, str], None]):
        # TODO: generar enemigos con dificultad, con lineas de espera
        enemy1 = PrefabData(WIDTH // 4, HEIGHT // 4, 'right', 100, id=1, type="type1")
        self.environment.add_enemy(enemy1)
        enemy2 = PrefabData(WIDTH // 4 * 3, HEIGHT // 4, 'left', 125, id=2, type="type2", speed=20) # se puede cambiar la velocidad dependiendo de la dificultad
        self.environment.add_enemy(enemy2)
        enemy3 = PrefabData(WIDTH // 4, HEIGHT // 4 * 3, 'right', 150, id=3, type="type3")
        self.environment.add_enemy(enemy3)
        enemy_generation_function(self.environment.enemies[0], "type1")
        enemy_generation_function(self.environment.enemies[1], "type2")
        enemy_generation_function(self.environment.enemies[2], "type3")

    def generate_enemy(self):
        # TODO: generar enemigo, escoger el tipo de enemigo puede ser con markov o montecarlo
        pass

    def generate_final_enemy(self):
        # TODO: generar enemigo final
        pass

    def evaluate_character_position_action(self, attack_function: Callable[[bool, int, str | None], None], 
                                           move_function: Callable[[str, int], None]):
        ob_sp = self.environment.get_observation_space()
        for en in self.environment.enemies:
            type = en.type
            if type == "type1":
                action, type_action = self.do_enemy_type1_action_policy(en, ob_sp)
            elif type == "type2":
                action, type_action = self.do_enemy_type2_action_policy(en, ob_sp)
            elif type == "type3":
                action, type_action = self.do_enemy_type3_action_policy(en, ob_sp)
            elif type == "final":
                action, type_action = self.do_final_enemy_action_policy(en, ob_sp)
            if action == "attack":
                attack_function(type == "final", en.id, type_action)
            else:
                move_function(type_action, en.id)

    def do_enemy_type1_action_policy(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        action, ob_x, ob_y, x, x_width = self.__calculate_melee_attack(enemy, observation_space)
        if action == "attack":
            return action, None
        x_diff = ob_x - x
        y_diff = ob_y - enemy.y
        move = self.__calculate_move_direction(x_diff, y_diff, x_width)
        return "move", move if move else enemy.frame_direction

    def do_enemy_type2_action_policy(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        action, ob_x, ob_y, x, x_width = self.__calculate_melee_attack(enemy, observation_space)
        if action == "attack":
            return action, None
        if enemy.action_counter == 150:
            enemy.action_counter = 0
        if enemy.action_counter == 0:
            prob = (self.__get_pseudo_random_number() + (1 - (enemy.life / enemy.max_life))) / 2
            enemy.in_strategy = prob <= 0.5
        if enemy.in_strategy:
            num = self.__get_pseudo_random_number()
            enemy.action_counter += 1
            return "move", self.__two_dimension_random_walk(num)
        else:
            x_diff = ob_x - x
            y_diff = ob_y - enemy.y
            enemy.action_counter += 1
            move = self.__calculate_move_direction(x_diff, y_diff, x_width)
            return "move", move if move else enemy.frame_direction

    def do_enemy_type3_action_policy(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        action, ob_x, ob_y, x, x_width = self.__calculate_shoot_attack(enemy, observation_space)
        if action == "attack":
            return action, None
        x_diff = ob_x - x
        y_diff = ob_y - enemy.y + 40
        move = self.__calculate_move_direction(x_diff, y_diff, x_width)
        return "move", move if move else enemy.frame_direction

    def do_final_enemy_action_policy(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        action, ob_x, ob_y, x_melee, x_width = self.__calculate_melee_attack(enemy, observation_space)
        if action == "attack":
            return action, "melee"
        action, ob_x, ob_y, _, _ = self.__calculate_shoot_attack(enemy, observation_space)
        if action == "attack":
            return action, "shoot"
        if enemy.action_counter == 150:
            enemy.action_counter = 0
        if enemy.action_counter == 0:
            prob = (self.__get_pseudo_random_number() + (1 - (enemy.life / enemy.max_life))) / 2
            enemy.in_strategy = prob <= 0.5
        if enemy.in_strategy:
            num = self.__get_pseudo_random_number()
            enemy.action_counter += 1
            return "move", self.__two_dimension_random_walk(num)
        else:
            x_diff = ob_x - x_melee
            y_diff = ob_y - enemy.y
            enemy.action_counter += 1
            move = self.__calculate_move_direction(x_diff, y_diff, x_width)
            return "move", move if move else enemy.frame_direction

    def __two_dimension_random_walk(self, num):
        if num <= 0.25:
            return "left"
        elif num > 0.25 and num <= 0.5:
            return "up"
        elif num > 0.5 and num <= 0.75:
            return "right"
        return "down"

    def __calculate_melee_attack(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        ob_x, ob_y, ob_max_x, ob_min_x, ob_max_y, ob_min_y = observation_space
        x_width, _ = enemy.max_dimensions[enemy.frame_direction] if enemy.max_dimensions else (0, 0)
        x = enemy.x - (x_width // 2) if enemy.frame_direction == "left" else enemy.x + (x_width // 2)
        if x >= ob_min_x and x <= ob_max_x and enemy.y >= ob_min_y and enemy.y <= ob_max_y:
            return "attack", ob_x, ob_y, x, x_width
        return "move", ob_x, ob_y, x, x_width
    
    def __calculate_shoot_attack(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        ob_x, ob_y, ob_max_x, ob_min_x, ob_max_y, ob_min_y = observation_space
        x_width, _ = enemy.max_dimensions[enemy.frame_direction] if enemy.max_dimensions else (0, 0)
        x, y = enemy.x + 40 if enemy.frame_direction == "right" else enemy.x - 40, enemy.y - 40
        direction = enemy.direction
        lim = enemy.speed * 2
        on_x = x >= ob_min_x + lim and x <= ob_max_x - lim
        on_y = y >= ob_min_y + lim and y <= ob_max_y - lim
        if (direction == "right" and x <= ob_min_x + lim and on_y) or \
            (direction == "left" and x >= ob_max_x - lim and on_y) or \
            (direction == "up" and y >= ob_max_y - lim and on_x) or \
            (direction == "down" and y <= ob_min_y + lim and on_x):
            return "attack", ob_x, ob_y, x, x_width
        return "move", ob_x, ob_y, x, x_width

    def __calculate_move_direction(self, x_diff, y_diff, value, speed=5):
        abs_x_diff = abs(x_diff)
        abs_y_diff = abs(y_diff)
        if abs_x_diff > abs_y_diff and abs_x_diff > value:
            if x_diff > 0:
                return "right"
            else:
                return "left"
        else:
            if abs_y_diff <= speed:
                return None
            if y_diff > 0:
                return "down"
            else:
                return "up"

    def evaluate_attacks(self, chest_generation_function: Callable[[str], None], 
                         delete_enemy_function: Callable[[int], None], 
                         character_death_function: Callable[[], None]):
        character_shoots = list(filter(lambda x: x.alive, self.environment.character.attacks))
        enemies_death: list[PrefabData] = []
        for shoot in character_shoots:
            for en in self.environment.enemies:
                if self.__verify_shoot_damage(shoot, en, True):
                    shoot.alive = False
                    if en.life <= 0:
                        enemies_death.append(en)
                        self.environment.character_points += 10
                    break
        for en in self.environment.enemies:
            en_shoots = list(filter(lambda x: x.alive, en.attacks))
            for shoot in en_shoots:
                if self.__verify_shoot_damage(shoot, self.environment.character, False):
                    shoot.alive = False
                    if self.environment.character.life <= 0:
                        character_death_function()
                elif shoot.type == "melee":
                    shoot.alive = False
        for en in enemies_death:
            if en in self.environment.enemies: 
                self.environment.enemies.remove(en)
            delete_enemy_function(en.id)
        # TODO: generar cofre si el jugador consigue X puntaje
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
            value = to.life - (shoot.damage - interval - self.__get_montecarlo_damage())
            to.life = value if value >= 0 else 0
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
    
    def __get_montecarlo_damage(self):
        num = self.__get_pseudo_random_number()
        if num <= 0.5:
            return 2
        elif num <= 0.85:
            return 1
        else:
            return 0
