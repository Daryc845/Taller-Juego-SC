from scripts.intefaces import IModel, IPresenter
from scripts.model_scripts import GameModel

class Model(IModel):
    def __init__(self):
        self.presenter = None
        self.game_model = GameModel()

    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter

    def generate_game_configs(self, difficulty: str):
        self.game_model.reset_game(difficulty)
        self.presenter.show_character(self.game_model.environment.character)
        self.game_model.generate_enemies(difficulty, lambda x, y: self.presenter.show_enemy(x, y))

    def action_on_character_position(self):
        self.game_model.evaluate_character_position_action(
            lambda x, y: self.presenter.do_enemy_attack(x, y),
            lambda x, y: self.presenter.do_enemy_move(x, y),
        )

    def action_on_character_shoot(self):
        self.game_model.evaluate_character_shoot(lambda x: self.presenter.show_chest(x))