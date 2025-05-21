from scripts.game_configs import FPS, screen, background_image, clock, WIDTH, HEIGHT
from scripts.game_entities import Character, EnemyType1, EnemyType2, EnemyType3, Enemy, Weapon, Shotgun
from scripts.intefaces import IView, IPresenter
from scripts.game_entities.data_models import PrefabData
from scripts.game_scenes import StartScene, BaseScene, NextPhaseLoadingScene
import pygame
import time

"""
Módulo principal del juego. Configura la pantalla, carga los recursos y maneja el bucle principal del juego.
En este módulo deben unirse todos los elementos del juego, como los personajes, enemigos, escenarios, objetos
y ESCENAS.
"""
# --- Escena del juego ---
class GameScene(IView, BaseScene):
    """
    Clase que representa una escena del juego. Maneja la lógica de eventos, actualiza el estado del juego y dibuja en pantalla.
    DEBE EDITARSE PARA HACERLA MAS GENERALIZADA Y QUE PUEDA SER REUTILIZADA EN OTRAS ESCENAS.
    Por ejemplo: que pueda especificarse el fondo de la escena, los enemigos y la cantidad de estos, objetos, etc. Para cada escena.
    En este caso, solo se ha implementado la escena del juego, pero en el futuro se pueden agregar más escenas como
    de distintos niveles, menús, etc.
    """
    def __init__(self):
        super().__init__()
        self.presenter : IPresenter = None
        self.character: Character = None
        self.enemies : list[Enemy] = []
        self.is_in_game = False
        self.is_in_pause = False
        self.start_scene = StartScene(load_function=lambda x: self.presenter.generate_game_configs(x))
        self.leaved_weapons: list[Weapon] = [Shotgun(300, 300, direction="left")]
        self.key_pressed = { pygame.K_1: False, pygame.K_2: False, pygame.K_3: False, pygame.K_p: False }
        self.key_processed = { pygame.K_1: False, pygame.K_2: False, pygame.K_3: False, pygame.K_p: False }
        self.text_font = pygame.font.SysFont("Arial", 15)
        self.pause_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.cannot_add_weapon = False
        self.cannot_leave_weapon = False
        self.message_show_counter = 0
        self.preparing_second_phase = False
        self.couting_time = False
        self.preparing_time = 0
        self.preparing_scene = NextPhaseLoadingScene((lambda: self.presenter.start_second_phase()), 
                                                     (lambda: self.next_phase_load()))

    def next_phase_load(self):
        self.leaved_weapons.clear()
        for wp in self.character.weapons:
            wp.direction = self.character.prefab_data.direction
            wp.set_position(self.character.prefab_data.x, self.character.prefab_data.y - 35)
        self.preparing_second_phase = False

    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter
    
    def show_character(self, prefab_character: PrefabData):
        if self.character is None:
            self.character = Character(prefab_character)
        else:
            self.__reset_all()
        self.is_in_game = True

    def __reset_all(self):
        self.character.reset_character()
        self.enemies.clear()
        self.leaved_weapons.clear()
        self.leaved_weapons.append(Shotgun(300, 300, direction="left"))

    def do_enemy_attack(self, with_move, enemy_id, attack_type):
        res = list(filter(lambda x: x.prefab_data.id == enemy_id, self.enemies))
        if len(res) > 0:
            res = res[0]
            if attack_type:
                res.attack(attack_type)
            else:
                res.attack()
            if with_move:
                res.move(res.last_direction)
    
    def do_enemy_move(self, direction, enemy_id):
        res = list(filter(lambda x: x.prefab_data.id == enemy_id, self.enemies))
        if len(res) > 0:
            res = res[0]
            res.move(direction)

    def show_chest(self, weapon_type: str):
        # TODO: mostrar el cofre
        pass

    def delete_enemy(self, enemy_id: int):
        enemy = list(filter(lambda x: x.prefab_data.id == enemy_id, self.enemies))
        if len(enemy) > 0:
            self.enemies.remove(enemy[0])

    def character_death(self):
        self.start_scene.game_over = True
        self.start_scene.next_scene = None
        self.start_scene.draw()
        self.is_in_game = False

    def to_second_phase(self):
        self.preparing_second_phase = True
        self.couting_time = True
        self.preparing_time = int(time.time())

    def run_game(self):
        while True:
            if not self.couting_time and self.preparing_second_phase:
                self.preparing_scene.play(other_actions=lambda: self.presenter.quit_game())
            elif self.is_in_game:
                self.play(other_actions=lambda: self.presenter.quit_game())
                clock.tick(FPS)
            elif not self.is_in_game:
                if self.start_scene.next_scene is not None:
                    self.start_scene.next_scene.play(other_actions=lambda: self.presenter.quit_game())
                else:
                    self.start_scene.play(other_actions=lambda: self.presenter.quit_game())

    def in_pause_handle(self):
        p_pressed = False
        if self.key_pressed[pygame.K_p] and not self.key_processed[pygame.K_p]:
            p_pressed = True
            self.key_processed[pygame.K_p] = True
        if p_pressed:
            self.presenter.change_in_pause()
            self.is_in_pause = not self.is_in_pause

    def show_enemy(self, prefab_enemy: PrefabData, type: str):
        if type == "type1":
            self.enemies.append(EnemyType1(prefab_enemy))
        elif type == "type2":
            self.enemies.append(EnemyType2(prefab_enemy))
        elif type == "type3":
            self.enemies.append(EnemyType3(prefab_enemy))
        elif type == "final":
            # TODO: generar enemigo final
            pass

    def game_won(self, obtain_points):
        self.is_in_game = False
        self.start_scene.next_scene = None
        self.start_scene.game_over = False
        self.start_scene.game_won = True
        self.start_scene.final_points = obtain_points

    def handle_events(self, other_actions=None):
        super().handle_events(other_actions=other_actions)
        keys_state = pygame.key.get_pressed()
        for key in self.key_pressed:
            if keys_state[key] and not self.key_pressed[key]:
                self.key_pressed[key] = True
                self.key_processed[key] = False
            elif not keys_state[key]:
                self.key_pressed[key] = False
                self.key_processed[key] = False

    def in_weapons_add_remove_handle(self):
        k1_pressed = False
        k2_pressed = False
        k3_pressed = False
        if self.key_pressed[pygame.K_1] and not self.key_processed[pygame.K_1]:
            k1_pressed = True
            self.key_processed[pygame.K_1] = True
        if k1_pressed:
            self.character.change_weapon()
        if self.key_pressed[pygame.K_2] and not self.key_processed[pygame.K_2]:
            k2_pressed = True
            self.key_processed[pygame.K_2] = True
        if k2_pressed:
            wp = self.character.leave_weapon()
            if wp is None:
                self.cannot_leave_weapon = True
            else:
                wp.direction = "left"
                self.leaved_weapons.append(wp)
        if self.key_pressed[pygame.K_3] and not self.key_processed[pygame.K_3]:
            k3_pressed = True
            self.key_processed[pygame.K_3] = True
        if k3_pressed:
            weapon_index = self.verify_and_get_weapon_index()
            if weapon_index != -1:
                success = self.character.add_weapon(self.leaved_weapons[weapon_index])
                if not success:
                    self.cannot_add_weapon = True
                else:
                    self.leaved_weapons.pop(weapon_index)

    def update(self):
        if not self.preparing_second_phase:
            self.in_pause_handle()
        if not self.is_in_pause:
            self.in_weapons_add_remove_handle()
            keys = pygame.key.get_pressed()
            self.character.do_action(keys)
            self.character.update_animation()
            self.presenter.calculate_actions()
            for enemy in self.enemies:
                enemy.update_animation()

    def draw_cannot_leave_weapon(self):
        x, y = self.character.prefab_data.x, self.character.prefab_data.y
        text = self.text_font.render("No puedes soltar mas armas, debes tener al menos una", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, text.get_width() + 10, text.get_height()))
        screen.blit(text, (x + 5, y))
        self.message_show_counter += 1
        if self.message_show_counter > 70:
            self.message_show_counter = 0
            self.cannot_leave_weapon = False

    def draw_cannot_add_weapon(self):
        x, y = self.character.prefab_data.x, self.character.prefab_data.y
        text = self.text_font.render("No puedes agregar mas armas, puedes tener maximo 4", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, text.get_width() + 10, text.get_height()))
        screen.blit(text, (x + 5, y))
        self.message_show_counter += 1
        if self.message_show_counter > 70:
            self.message_show_counter = 0
            self.cannot_add_weapon = False

    def verify_and_get_weapon_index(self):
        ch_x, ch_y = self.character.prefab_data.x, self.character.prefab_data.y
        for i, wp in enumerate(self.leaved_weapons):
            wp_x, wp_y = wp.adjust_position()
            wp_width, wp_height = wp.max_dimensions[wp.direction]
            if ch_x >= wp_x and ch_x <= wp_x + wp_width and ch_y >= wp_y and ch_y <= wp_y + wp_height:
                return i
        return -1

    def draw(self):
        screen.blit(background_image, (0, 0))
        for wp in self.leaved_weapons:
            wp.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen, in_pause=self.is_in_pause)
        self.character.draw(screen, in_pause=self.is_in_pause)
        if self.cannot_leave_weapon:
            self.draw_cannot_leave_weapon()
        if self.cannot_add_weapon:
            self.draw_cannot_add_weapon()
        if self.is_in_pause:
            pause_text = self.pause_font.render("Juego en pausa", True, (255, 0, 0))
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - pause_text.get_height()//2))
        if self.preparing_second_phase:
            now = int(time.time())
            rest = 60 + self.preparing_time - now
            if rest <= 0:
                self.couting_time = False
                self.preparing_scene.start_thread()
            preparing_text = self.text_font.render(f"Tiempo de abastecimiento restante: {rest} segundos", True, (255, 0, 0))
            screen.blit(preparing_text, (WIDTH - preparing_text.get_width() - 20, 20))
        pygame.display.flip()