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
    def do_enemy_attack(self, with_move: bool, enemy_id: int):
        pass

    @abstractmethod
    def show_chest(self, weapon_type: str):
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
    def do_enemy_attack(self, with_move: bool, enemy_id: int):
        pass

    @abstractmethod
    def show_chest(self, weapon_type: str):
        pass