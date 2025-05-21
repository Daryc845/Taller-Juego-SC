from scripts.numbs_aux import generate_numbers, test_numbers
import time
import threading

G_VALUE = 20
M_VALUE = 2**G_VALUE

class NumbersModel:
    def __init__(self):
        self.numbers = []
        self.numbers_2 = []
        self.current_number = 0
        self.using_backup = False
        self.terminate = False

    def init_numbers(self):
        if len(self.numbers) > 0 or len(self.numbers_2) > 0:
            return
        self.__generate_numbers()
        self.__generate_numbers(is_backup=True)
    
    def get_next_pseudo_random_number(self):
        if not self.using_backup:
            if self.current_number >= len(self.numbers):
                threading.Thread(target=lambda: self.__generate_numbers(), daemon=True).start()
                self.current_number = 0
                self.using_backup = True
                num = self.numbers_2[self.current_number]
            else:
                num = self.numbers[self.current_number]
        else:
            if self.current_number >= len(self.numbers_2):
                threading.Thread(target=lambda: self.__generate_numbers(is_backup=True), daemon=True).start()
                self.current_number = 0
                self.using_backup = False
                num = self.numbers[self.current_number]
            else:
                num = self.numbers_2[self.current_number]
        self.current_number += 1
        return num

    def __generate_numbers(self, is_backup = False):
        conf = self.__generate_conf()
        if self.terminate:
            return
        numbers = generate_numbers(conf)
        if is_backup:
            self.numbers_2 = numbers
        else:
            self.numbers = numbers
        while not test_numbers(self.numbers) and not self.terminate:
            if self.terminate:
                return
            conf = self.__generate_conf(first=False)
            numbers = generate_numbers(conf)
            if is_backup:
                self.numbers_2 = numbers
            else:
                self.numbers = numbers

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