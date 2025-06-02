from scripts.game_entities.data_models import PrefabData, EnvironmentData, AttackData
from scripts.game_configs import WIDTH, HEIGHT, NORMAL_DIFFICULTY, HARD_DIFFICULTY
from scripts.model_scripts.numbers_model import NumbersModel
from typing import Callable
import math
import time

class GameModel:
    def __init__(self):
        self.numbers_model = NumbersModel()
        self.environment = EnvironmentData(WIDTH, HEIGHT)
        self.in_pause = False
        self.terminate = False
        self.enemies_counter = 0
        self.lambda_value = 5 # valor de lamda en llegadas/minuto
        self.default_enemies = 5
        self.waves = 3

    def reset_game(self, difficulty: str):
        print(f"Dificultad seleccionada: {difficulty}")
        self.terminate = False
        self.environment.reset_environment()
        self.numbers_model.init_numbers()
        self.lambda_value = 6 if difficulty == HARD_DIFFICULTY else 5 if difficulty == NORMAL_DIFFICULTY else 4
        self.default_enemies = 7 if difficulty == HARD_DIFFICULTY else 5 if difficulty == NORMAL_DIFFICULTY else 3
        self.waves = 9 if difficulty == HARD_DIFFICULTY else 5 if difficulty == NORMAL_DIFFICULTY else 2

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
        while not self.terminate:
            if len(self.environment.enemies) == 0:
                game_won_function(self.environment.total_character_points)
                break

    def __generate_chest(self, chest_generation_function: Callable[[str], None]):
        type = self.__get_chest_type()
        chest_generation_function(type)

    def generate_enemies(self, enemy_generation_function: Callable[[PrefabData, str], None],
                          new_wave_function: Callable[[int], None]):
        for i in range(1, self.waves + 1):
            time.sleep(3)
            #at = 0
            iat = 0
            enemy_counter = 0
            enemies_amount = self.default_enemies
            enemies_amount += int(self.get_ni_number(i, i*3))
            while enemy_counter < enemies_amount:
                if self.terminate:
                    return
                if self.in_pause:
                    continue
                en, type = self.generate_enemy()
                enemy_generation_function(en, type)
                enemy_counter += 1
                ri = self.__get_pseudo_random_number()
                iat = - math.log(1 - ri, math.e) / self.lambda_value
                segs = iat * 60
                #at += iat
                time.sleep(segs)
            while len(self.environment.enemies) > 0:
                if self.terminate:
                    return
            else:
                new_wave_function(i + 1)
            if i != self.waves:
                time.sleep(2)

    def generate_enemy(self):
        type, life, speed = self.__get_montecarlo_enemy()
        self.enemies_counter += 1
        id = self.enemies_counter
        x, y = self.__get_montecarlo_enemy_position()
        enemy = PrefabData(x, y, 'right', life, type=type, speed=speed, id=id)
        self.environment.add_enemy(enemy)
        return enemy, type

    def __get_montecarlo_enemy_position(self):
        num1 = self.__get_pseudo_random_number()
        if num1 <= 0.25:
            return 0, int(self.get_ni_number(0, HEIGHT))
        elif num1 <= 0.5:
            return WIDTH, int(self.get_ni_number(0, HEIGHT))
        elif num1 <= 0.75:
            return int(self.get_ni_number(0, WIDTH)), HEIGHT
        else:
            return int(self.get_ni_number(0, WIDTH)), 0

    def __get_montecarlo_enemy(self):
        num = self.__get_pseudo_random_number()
        if num <= 0.45:
            return "type1", 150, 7
        elif num <= 0.8:
            return "type2", 125, 9
        else:
            return "type3", 100, 4

    def generate_final_enemy(self):
        life = 2000
        speed = 6
        id = 0
        x, y = self.__get_montecarlo_enemy_position()
        enemy = PrefabData(x, y, 'right', life, type="final", speed=speed, id=id)
        self.environment.add_enemy(enemy)
        return enemy

    def evaluate_character_position_action(self, attack_function: Callable[[bool, int, str | None], None], 
                                           move_function: Callable[[str, int], None],
                                           enemy_generation_function: Callable[[PrefabData, str], None]):
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
                action, type_action = self.do_final_enemy_action_policy(en, ob_sp, enemy_generation_function)
                if action is None:
                    continue
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
        move = self.__calculate_move_direction(x_diff, y_diff, x_width, speed=enemy.speed)
        return "move", move if move else enemy.frame_direction

    def do_enemy_type2_action_policy(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        action, ob_x, ob_y, x, x_width = self.__calculate_melee_attack(enemy, observation_space)
        if action == "attack":
            return action, None
        enemy.in_strategy = (enemy.life / enemy.max_life) > 0.7 and not self.__is_close_to_player(ob_x, ob_y, x, enemy.y, x_width)
        if enemy.in_strategy:
            num = self.__get_pseudo_random_number()
            return "move", self.__two_dimension_random_walk(num)
        else:
            x_diff = ob_x - x
            y_diff = ob_y - enemy.y
            move = self.__calculate_move_direction(x_diff, y_diff, x_width, speed=enemy.speed)
            return "move", move if move else enemy.frame_direction

    def do_enemy_type3_action_policy(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int]):
        action, ob_x, ob_y, x, x_width = self.__calculate_shoot_attack(enemy, observation_space)
        if action == "attack":
            return action, None
        x_diff = ob_x - x
        y_diff = ob_y - enemy.y + 40
        move = self.__calculate_move_direction(x_diff, y_diff, x_width, speed=enemy.speed)
        return "move", move if move else enemy.frame_direction

    def do_final_enemy_action_policy(self, enemy: PrefabData, observation_space: tuple[int, int, int, int, int, int],
                                     enemy_generation_function: Callable[[PrefabData, str], None]):
        action, ob_x, ob_y, x_melee, x_width = self.__calculate_melee_attack(enemy, observation_space)
        if action == "attack":
            return action, "melee"
        action, ob_x, ob_y, _, _ = self.__calculate_shoot_attack(enemy, observation_space)
        if action == "attack":
            return action, "shoot"
        if enemy.genration_enemies_counter == 200:
            en, type = self.generate_enemy()
            enemy_generation_function(en, type)
            enemy.genration_enemies_counter = 0
            return None, None
        enemy.genration_enemies_counter += 1
        enemy.in_strategy = (enemy.life / enemy.max_life) > 0.7 and not self.__is_close_to_player(ob_x, ob_y, x_melee, enemy.y, x_width)
        if enemy.in_strategy:
            num = self.__get_pseudo_random_number()
            return "move", self.__two_dimension_random_walk(num)
        else:
            x_diff = ob_x - x_melee
            y_diff = ob_y - enemy.y
            move = self.__calculate_move_direction(x_diff, y_diff, x_width, speed=enemy.speed)
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
        
    def __is_close_to_player(self, ob_x: int, ob_y: int, x: int, y: int, x_width: int):
        euclidean_distance = math.sqrt((ob_x - x) ** 2 + (ob_y - y) ** 2)
        return euclidean_distance <= x_width * 1.5

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
                        self.environment.total_character_points += 10                
                        if self.environment.character_points == 20:
                            self.__generate_chest(chest_generation_function)
                            self.environment.character_points = 0
                    break
        for en in self.environment.enemies:
            en_shoots = list(filter(lambda x: x.alive, en.attacks))
            for shoot in en_shoots:
                if self.__verify_shoot_damage(shoot, self.environment.character, False):
                    shoot.alive = False
                    if self.environment.character.life <= 0:
                        character_death_function()
                        self.terminate = True
                elif shoot.type == "melee":
                    shoot.alive = False
        for en in enemies_death:
            if en in self.environment.enemies: 
                self.environment.enemies.remove(en)
            delete_enemy_function(en.id)

    def __get_pseudo_random_number(self):
        return self.numbers_model.get_next_pseudo_random_number()
    
    def get_ni_number(self, a, b):
        ri = self.__get_pseudo_random_number()
        return a + (b - a) * ri
    
    def __verify_shoot_damage(self, shoot: AttackData, to: PrefabData, is_enemy: bool)-> bool:
        if is_enemy:
            direction_to = to.frame_direction
        else:
            direction_to = to.direction
        if not to.max_dimensions:
            if to.type == "type1":
                to.max_dimensions = {'left': (178, 202), 'right': (178, 202)}
            elif to.type == "type2":
                to.max_dimensions = {'left': (141, 160), 'right': (141, 160)}
            elif to.type == "type3":
                to.max_dimensions = {'left': (165, 196), 'right': (165, 196)}
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
        
    def __get_montecarlo_weapon(self):
        num = self.__get_pseudo_random_number()
        if num < 0.5:
            return "submachine"
        elif num < 0.8:
            return "rifle"
        elif num < 0.95:
            return "shotgun"
        else:
            return "raygun"
        
    markov_reward = {
        "munition":{'munition': 0.3, 'health': 0.3, 'weapon': 0.4},
        "health":{'munition': 0.3, 'health': 0.2, 'weapon': 0.5},
        "weapon":{'munition': 0.35, 'health': 0.55, 'weapon': 0.1}
    }

    current_reward = "munition" # estado inicial en munition

    def __get_reward(self):
        num = self.__get_pseudo_random_number()
        if num <= self.markov_reward[self.current_reward]["munition"]:
            self.current_reward = "munition"
            return "munition"
        elif num <= self.markov_reward[self.current_reward]["munition"] + self.markov_reward[self.current_reward]["health"]:
            self.current_reward = "health"
            return "health"
        else:
            self.current_reward = "weapon"
            return "weapon"
        
    def __get_chest_type(self):
        type = self.__get_reward()
        if type == "weapon":
            type = self.__get_montecarlo_weapon()
        return type