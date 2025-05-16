from scripts.intefaces import IPresenter, IView, IModel

class Presenter(IPresenter):
    def __init__(self, view: IView, model: IModel):
        self.view = view
        self.model = model
        self.view.set_presenter(self)
        self.model.set_presenter(self)

    def start_game(self):
        self.model.start_game()