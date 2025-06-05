from abc import ABC, abstractmethod
from scripts.game_entities.data_models import PrefabData

class IModel(ABC):
    @abstractmethod
    def set_presenter(self, presenter):
        pass
    
    @abstractmethod
    def generate_game_configs(self, difficulty: str):
        pass

    @abstractmethod
    def calculate_actions(self):
        pass

    @abstractmethod
    def change_in_pause(self):
        pass

    @abstractmethod
    def quit_game(self):
        pass

    @abstractmethod
    def start_second_phase(self):
        pass

    @abstractmethod
    def get_random_between(self, min, max):
        pass

class IView(ABC):
    @abstractmethod
    def set_presenter(self, presenter):
        pass

    @abstractmethod
    def show_character(self, prefab_character: PrefabData):
        pass

    @abstractmethod
    def show_enemy(self, prefab_enemy: PrefabData, type: str):
        pass

    @abstractmethod
    def do_enemy_move(self, direction: str, enemy_id: int):
        pass

    @abstractmethod
    def do_enemy_attack(self, with_move: bool, enemy_id: int, attack_type: str | None):
        pass

    @abstractmethod
    def show_chest(self, type: str):
        pass

    @abstractmethod
    def delete_enemy(self, enemy_id: int):
        pass

    @abstractmethod
    def character_death(self):
        pass

    @abstractmethod
    def to_second_phase(self):
        pass

    @abstractmethod
    def game_won(self, obtain_points: int):
        pass

    @abstractmethod
    def on_new_wave(self, wave_number):
        pass

class IPresenter(ABC):
    @abstractmethod
    def generate_game_configs(self, difficulty: str):
        pass

    @abstractmethod
    def show_character(self, prefab_character: PrefabData):
        pass

    @abstractmethod
    def calculate_actions(self):
        pass

    @abstractmethod
    def show_enemy(self, prefab_enemy: PrefabData, type: str):
        pass

    @abstractmethod
    def do_enemy_move(self, direction: str, enemy_id: int):
        pass

    @abstractmethod
    def do_enemy_attack(self, with_move: bool, enemy_id: int, attack_type: str | None):
        pass

    @abstractmethod
    def show_chest(self, type: str):
        pass

    @abstractmethod
    def delete_enemy(self, enemy_id: int):
        pass

    @abstractmethod
    def character_death(self):
        pass

    @abstractmethod
    def to_second_phase(self):
        pass

    @abstractmethod
    def change_in_pause(self):
        pass

    @abstractmethod
    def quit_game(self):
        pass

    @abstractmethod
    def start_second_phase(self):
        pass

    @abstractmethod
    def game_won(self, obtain_points: int):
        pass

    @abstractmethod
    def get_random_between(self, min, max):
        pass

    @abstractmethod
    def on_new_wave(self, wave_number):
        pass