from scripts import GameScene, Model, Presenter

if __name__ == "__main__":
    view = GameScene()
    model = Model()
    presenter = Presenter(view, model)
    view.run_game()