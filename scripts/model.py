from scripts.intefaces import IModel, IPresenter
from scripts.numbs_aux import generate_numbers, test_numbers
from scripts.game_entities.data_models.data_models import PrefabData, EnvironmentData
from scripts.game_configs import WIDTH, HEIGHT
import time

G_VALUE = 20
M_VALUE = 2**G_VALUE

class Model(IModel):
    def __init__(self):
        self.presenter = None
        self.numbers = []
        self.current_number = 0
        self.environment = EnvironmentData(WIDTH, HEIGHT)

    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter

    def generate_game_configs(self, difficulty: str):
        print(f"Dificultad seleccionada: {difficulty}")
        self.environment.reset_environment()
        self.__generate_numbers()
        self.__generate_chests()
        self.presenter.show_character(self.environment.character)
        self.__generate_enemies()

    def __generate_chests(self):
        # TODO: generar cofres, puede ser con montecarlo o markov
        pass

    def __generate_enemies(self):
        # TODO: generar enemigos, con lineas de espera, al escoger el tipo de enemigo puede ser con markov o montecarlo
        enemy1 = PrefabData(WIDTH // 4, HEIGHT // 4, 40, id=1)
        self.environment.add_enemy(enemy1)
        enemy2 = PrefabData(WIDTH // 4 * 3, HEIGHT // 4, 50, id=2)
        self.environment.add_enemy(enemy2)
        enemy3 = PrefabData(WIDTH // 4, HEIGHT // 4 * 3, 70, id=3)
        self.environment.add_enemy(enemy3)
        self.presenter.show_enemy(self.environment.enemies[0], "type1")
        self.presenter.show_enemy(self.environment.enemies[1], "type2")
        self.presenter.show_enemy(self.environment.enemies[2], "type3")
        pass

    a = 0

    def action_on_character_position(self):
        # TODO: calcular disparos, movimientos, y daños al jugador; con agentes
        print(self.environment.get_observation_space())
        for en in self.environment.enemies:
            self.presenter.do_enemy_attack(True, en.id)
            #self.presenter.do_enemy_move("up", en.id)
            #self.presenter.do_enemy_move("down", en.id)
            #self.presenter.do_enemy_move("right", en.id)
            #self.presenter.do_enemy_move("left", en.id)

    def notify_character_shoot(self):
        # TODO: calcular daños a enemigos, con montecarlo
        pass

    def __get_next_pseudo_random_number(self):
        if self.current_number >= len(self.numbers):
            self.__generate_numbers()
        return self.numbers[self.current_number]

    def __generate_numbers(self):
        conf = self.__generate_conf()
        self.numbers = generate_numbers(conf)
        while not test_numbers(self.numbers):
            conf = self.__generate_conf(first=False)
            self.numbers = generate_numbers(conf)
        self.current_number = 0

    def __generate_conf(self, first = True):
        x0= self.__generate_x0(first=first)
        c = 2 * (x0 % (M_VALUE // 2)) + 1
        k = (x0 + 1) % M_VALUE
        return {
            'X0': x0,
            'k': k,
            'c': c,
            'g': G_VALUE
        }
    
    def __generate_x0(self, first = False):
        x0 = int(time.time()) if first else int(time.time() * 1000000)
        if x0 >= M_VALUE:
            m_size = len(str(M_VALUE))
            x0 = int(str(x0)[-(m_size-1):])
        return x0
    