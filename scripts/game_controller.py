from scripts.game_configs import FPS, screen, background_image, clock
from scripts.game_entities import Character, EnemyType1, EnemyType2, EnemyType3, Enemy
from scripts.intefaces import IView, IPresenter
from scripts.game_entities.data_models import PrefabData
from scripts.game_scenes import StartScene
import sys
import pygame

"""
Módulo principal del juego. Configura la pantalla, carga los recursos y maneja el bucle principal del juego.
En este módulo deben unirse todos los elementos del juego, como los personajes, enemigos, escenarios, objetos
y ESCENAS.
"""
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
        self.presenter : IPresenter = None
        self.character: Character = None
        self.enemies : list[Enemy] = []
        self.next_scene = None  # Para permitir cambios de escena en el futuro
        self.is_in_game = False
        self.start_scene = StartScene(load_function=lambda x: self.presenter.generate_game_configs(x))

    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter
    
    def show_character(self, prefab_character: PrefabData):
        if self.character is None:
            self.character = Character(prefab_character)
        self.is_in_game = True

    def do_enemy_attack(self, with_move, enemy_id):
        res = list(filter(lambda x: x.prefab_data.id == enemy_id, self.enemies))
        if len(res) > 0:
            res = res[0]
            res.attack()
            if with_move:
                res.move(res.last_direction)
    
    def do_enemy_move(self, direction, enemy_id):
        res = list(filter(lambda x: x.prefab_data.id == enemy_id, self.enemies))
        if len(res) > 0:
            res = res[0]
            res.move(direction)

    def show_chest(self, weapon_type: str):
        pass

    def run_game(self):
        while True:
            if self.is_in_game:
                self.play()
                clock.tick(FPS)
            else:
                if self.start_scene.next_scene is not None:
                    self.start_scene.next_scene.play()
                else:
                    self.start_scene.play()

    def show_enemy(self, prefab_enemy: PrefabData, type: str):
        if type == "type1":
            self.enemies.append(EnemyType1(prefab_enemy))
        elif type == "type2":
            self.enemies.append(EnemyType2(prefab_enemy))
        elif type == "type3":
            self.enemies.append(EnemyType3(prefab_enemy))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.character.do_action(keys)
        self.character.update_animation()
        self.presenter.calculate_actions()
        for enemy in self.enemies:
            enemy.update_animation()

    def draw(self):
        screen.blit(background_image, (0, 0))
        for enemy in self.enemies:
            enemy.draw(screen)
        self.character.draw(screen)
        pygame.display.flip()
    
    def play(self):
        self.handle_events()
        self.update()
        self.draw()

    def init_game(self):
        self.run_game()