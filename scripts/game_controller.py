from scripts.game_configs import WIDTH, HEIGHT, FPS, screen, background_image, clock
from scripts.game_entities import Character
from scripts.intefaces import IView, IPresenter
from scripts.presenter import Presenter
from scripts.model import Model
import sys
import pygame

"""
Módulo principal del juego. Configura la pantalla, carga los recursos y maneja el bucle principal del juego.
En este módulo deben unirse todos los elementos del juego, como los personajes, enemigos, escenarios, objetos
y ESCENAS.
"""

# --- Crea a Chester ---
character = Character(WIDTH // 2, HEIGHT // 2)

# --- Escena del juego ---
class GameScene(IView):
    """
    Clase que representa una escena del juego. Maneja la lógica de eventos, actualiza el estado del juego y dibuja en pantalla.
    DEBE EDITARSE PARA HACERLA MAS GENERALIZADA Y QUE PUEDA SER REUTILIZADA EN OTRAS ESCENAS.
    Por ejemplo: que pueda especificarse el fondo de la escena, los enemigos y la cantidad de estos, objetos, etc. Para cada escena.
    En este caso, solo se ha implementado la escena del juego, pero en el futuro se pueden agregar más escenas como
    de distintos niveles, menús, etc.
    """
    
    def __init__(self):
        self.presenter = None
        self.character = character
        self.next_scene = None  # Para permitir cambios de escena en el futuro

    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.character.do_action(keys)
        self.character.update_animation()

    def draw(self):
        screen.blit(background_image, (0, 0))
        self.character.draw(screen)
        pygame.display.flip()
    
    def play(self):
        self.handle_events()
        self.update()
        self.draw()

# --- Ciclo principal ---
def main():
    current_scene = GameScene()
    model = Model()
    presenter = Presenter(current_scene, model)

    while True:
        current_scene.play() #Escena de combate
        clock.tick(FPS)