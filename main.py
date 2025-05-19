from scripts.game_controller import GameScene
from scripts.model import Model
from scripts.presenter import Presenter

if __name__ == "__main__":
    view = GameScene()
    model = Model()
    presenter = Presenter(view, model)
    view.init_game()