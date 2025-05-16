from scripts.intefaces import IModel, IPresenter
from scripts.numbs_aux import generate_numbers, test_numbers
import time

G_VALUE = 31
M_VALUE = 2**G_VALUE
K_VALUE = (M_VALUE // 4) - 1

class Model(IModel):
    def __init__(self):
        self.presenter = None
        self.numbers = []
        self.current_number = 0

    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter

    def start_game(self):
        self.__generate_numbers()
        # TODO

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
        return {
            'X0': x0,
            'k': K_VALUE,
            'c': c,
            'g': G_VALUE
        }
    
    def __generate_x0(self, first = False):
        x0 = int(time.time()) if first else int(time.time() * 1000)
        if x0 >= M_VALUE:
            dif = x0 - M_VALUE
            x0 -= (dif + 1)
        return x0