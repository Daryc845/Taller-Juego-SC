from scripts.intefaces import IPresenter, IView, IModel
from scripts.game_entities.data_models.data_models import PrefabData

class Presenter(IPresenter):
    def __init__(self, view: IView, model: IModel):
        self.view = view
        self.model = model
        self.view.set_presenter(self)
        self.model.set_presenter(self)

    def generate_game_configs(self):
        self.model.generate_game_configs()

    def show_character(self, prefab_character: PrefabData):
        self.view.show_character(prefab_character)

    def notify_character_moved(self):
        self.model.notify_character_moved()

    def notify_character_shoot(self):
        self.model.notify_character_shoot()

    def show_enemy(self, prefab_enemy: PrefabData, type: str):
        self.view.show_enemy(prefab_enemy, type)

    def do_enemy_attack(self, with_move, enemy_id):
        self.view.do_enemy_attack(with_move, enemy_id)

    def do_enemy_move(self, direction, enemy_id):
        self.view.do_enemy_move(direction, enemy_id)