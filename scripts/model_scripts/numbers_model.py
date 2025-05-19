from scripts.numbs_aux import generate_numbers, test_numbers
import time

G_VALUE = 20
M_VALUE = 2**G_VALUE

class NumbersModel:
    def __init__(self):
        self.numbers = []
        self.current_number = 0

    def init_numbers(self):
        self.__generate_numbers()
    
    def get_next_pseudo_random_number(self):
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