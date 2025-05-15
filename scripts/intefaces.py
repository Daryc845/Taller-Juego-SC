from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def set_presenter(self, presenter):
        pass
    
    @abstractmethod
    def start_game(self):
        pass

class IView(ABC):
    @abstractmethod
    def set_presenter(self, presenter):
        pass

class IPresenter(ABC):
    @abstractmethod
    def start_game(self):
        pass