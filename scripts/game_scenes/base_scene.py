import pygame
import sys
from abc import ABC, abstractmethod

class BaseScene(ABC):
    """
    Clase base para todas las escenas del juego
    """
    def __init__(self):
        self.next_scene = None
    
    def handle_events(self, other_actions=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if other_actions:
                    other_actions()
                pygame.quit()
                sys.exit()
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    def play(self):
        self.handle_events()
        self.update()
        self.draw()