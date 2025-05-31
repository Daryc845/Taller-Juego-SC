from scripts.intefaces import IPresenter, IView, IModel
from scripts.game_entities.data_models import PrefabData

class Presenter(IPresenter):
    def __init__(self, view: IView, model: IModel):
        self.view = view
        self.model = model
        self.view.set_presenter(self)
        self.model.set_presenter(self)

    def generate_game_configs(self, difficulty: str):
        self.model.generate_game_configs(difficulty)

    def show_character(self, prefab_character: PrefabData):
        self.view.show_character(prefab_character)

    def calculate_actions(self):
        self.model.calculate_actions()

    def show_enemy(self, prefab_enemy: PrefabData, type: str):
        self.view.show_enemy(prefab_enemy, type)

    def do_enemy_attack(self, with_move, enemy_id, attack_type):
        self.view.do_enemy_attack(with_move, enemy_id, attack_type)

    def do_enemy_move(self, direction, enemy_id):
        self.view.do_enemy_move(direction, enemy_id)

    def show_chest(self, type: str):
        self.view.show_chest(type)

    def delete_enemy(self, enemy_id: int):
        self.view.delete_enemy(enemy_id)

    def character_death(self):
        self.view.character_death()

    def to_second_phase(self):
        self.view.to_second_phase()

    def change_in_pause(self):
        self.model.change_in_pause()

    def quit_game(self):
        self.model.quit_game()

    def start_second_phase(self):
        self.model.start_second_phase()

    def game_won(self, obtain_points: int):
        self.view.game_won(obtain_points)

    def get_random_between(self, min, max):
        return self.model.get_random_between(min, max)