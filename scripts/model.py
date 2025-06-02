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
        self.game_model.generate_enemies(lambda x, y: self.presenter.show_enemy(x, y),
                                         lambda x: self.presenter.on_new_wave(x))
        self.game_model.verify_first_phase(next_phase_function=lambda: self.presenter.to_second_phase())

    def start_second_phase(self):
        self.game_model.reset_to_second_phase()
        enemy = self.game_model.generate_final_enemy()
        self.presenter.show_enemy(enemy, "final")
        self.game_model.verify_second_phase(game_won_function=lambda x: self.presenter.game_won(x))

    def calculate_actions(self):
        self.game_model.evaluate_attacks(
            lambda x: self.presenter.show_chest(x),
            lambda x: self.presenter.delete_enemy(x),
            lambda: self.presenter.character_death()
        )
        self.game_model.evaluate_character_position_action(
            lambda x, y, z: self.presenter.do_enemy_attack(x, y, z),
            lambda x, y: self.presenter.do_enemy_move(x, y),
            lambda x, y: self.presenter.show_enemy(x, y)
        )

    def change_in_pause(self):
        self.game_model.in_pause = not self.game_model.in_pause

    def quit_game(self):
        self.game_model.terminate = True
        self.game_model.numbers_model.terminate = True

    def get_random_between(self, min, max):
        return self.game_model.get_ni_number(min, max)