from scripts.intefaces import IModel, IPresenter

class Model(IModel):
    def __init__(self):
        self.presenter = None

    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter