from scripts.game_configs import FPS, screen, background_image, clock, WIDTH, HEIGHT
from scripts.game_entities import Character, EnemyType1, EnemyType2, EnemyType3, Enemy, Weapon, Shotgun
from scripts.game_entities.static_objects import Chest, Torch
from scripts.intefaces import IView, IPresenter
from scripts.game_entities.data_models import PrefabData
from scripts.numbs_aux import generate_numbers
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
        self.chest = None
        self.start_scene = StartScene(load_function=lambda x: self.presenter.generate_game_configs(x))
        self.leaved_weapons: list[Weapon] = [Shotgun(300, 300, direction="left")]
        self.key_pressed = { pygame.K_1: False, pygame.K_2: False, pygame.K_3: False, pygame.K_5: False, pygame.K_p: False }
        self.key_processed = { pygame.K_1: False, pygame.K_2: False, pygame.K_3: False, pygame.K_5: False, pygame.K_p: False }
        self.text_font = pygame.font.SysFont("Arial", 15)
        self.pause_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.cannot_add_weapon = False
        self.cannot_leave_weapon = False
        self.message_show_counter = 0
        self.enemies_counter = 0
        self.preparing_second_phase = False
        self.couting_time = False
        self.preparing_time = 0
        self.chest_generation_points = [
            (WIDTH*0.11, HEIGHT*0.22),
            (WIDTH*0.5, HEIGHT*0.22),
            (WIDTH*0.89, HEIGHT*0.22),
            (WIDTH*0.11, HEIGHT*0.5),
            (WIDTH*0.36, HEIGHT*0.5),
            (WIDTH*0.63, HEIGHT*0.5),
            (WIDTH*0.89, HEIGHT*0.5),
            (WIDTH*0.11, HEIGHT*0.83),
            (WIDTH*0.5, HEIGHT*0.83),
            (WIDTH*0.89, HEIGHT*0.83)
        ]
        self.generate_chest()
        self.torches = []
        self.torch_generation_points = [
            (WIDTH*0.2, HEIGHT*0.07),
            (WIDTH*0.4, HEIGHT*0.07), 
            (WIDTH*0.6, HEIGHT*0.07),
            (WIDTH*0.8, HEIGHT*0.07),
            (WIDTH*0.04, HEIGHT*0.25),
            (WIDTH*0.04, HEIGHT*0.5),
            (WIDTH*0.04, HEIGHT*0.75),
            (WIDTH*0.96, HEIGHT*0.25),
            (WIDTH*0.96, HEIGHT*0.5),
            (WIDTH*0.96, HEIGHT*0.75)
        ]
        self.add_random_torches(5)
        self.help_controls_counter = 200
        self.preparing_scene = NextPhaseLoadingScene((lambda: self.presenter.start_second_phase()), 
                                                     (lambda: self.next_phase_load()))

    def add_random_torches(self, num_torches):
        """
        Genera 'num_torches' índices únicos usando generate_numbers(conf), redondea a 1 decimal, 
        multiplica por 10, convierte a entero y crea antorchas en los puntos correspondientes.
        La semilla inicial se basa en el tiempo actual.
        """
        conf = {
            'k': 3,
            'g': 4,
            'X0': int(time.time()),  # Semilla basada en el tiempo
            'c': 5
        }
        numbers = generate_numbers(conf)
        indices = set()
        i = 0
        while len(indices) < num_torches and i < len(numbers):
            idx = int(round(numbers[i], 1) * 10)
            idx = min(idx, len(self.torch_generation_points) - 1)
            if idx not in indices:
                indices.add(idx)
            i += 1
        for idx in indices:
            point = self.torch_generation_points[idx]
            self.add_torch(*point)
    
    def generate_chest_generation_point(self):
        """
        Genera un índice válido para chest_generation_points usando generate_numbers(conf).
        El índice nunca será igual ni mayor al tamaño del arreglo de puntos.
        """
        conf = {
            'k': 4,
            'g': 5,
            'X0': int(time.time()),
            'c': 5
        }
        points_len = len(self.chest_generation_points)
        while True:
            number = generate_numbers(conf)[0]
            index = int(round(number, 1) * 10)
            if 0 <= index < points_len:
                return index
            conf['X0'] += 1

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

    def show_chest(self, weapon_type: str = None):
        """generation_point_index = self.generate_chest_generation_point()
        selected_point = self.chest_generation_points[generation_point_index]
        self.chest.show_chest(*selected_point)"""
        pass
        
        
    def generate_chest(self, weapon_type: str = None):
        generation_point_index = self.generate_chest_generation_point()
        selected_point = self.chest_generation_points[generation_point_index]
        chest_data = PrefabData(*selected_point, direction="down", life=1)
        self.chest = Chest(chest_data, self.show_timed_message, self.draw_character_message)
        
    def add_torch(self, x: int, y: int):
        """Añade una antorcha en la posición especificada"""
        torch_data = PrefabData(x=x, y=y, direction="down", life=1)
        self.torches.append(Torch(torch_data))

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

            self.chest.do_action(keys, self.character)    
            self.chest.update(self.character)
            
            for torch in self.torches:
                torch.update(self.character)
            restricetd_directions = self.restrict_movement_character()
            self.character.do_action(keys,restricted_directions=restricetd_directions)
            self.character.update_animation()
            if self.enemies_counter == 3:
                self.presenter.calculate_actions()
                self.enemies_counter = 0
            self.enemies_counter += 1
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

    def draw_character_message(self, message):
        x, y = self.character.prefab_data.x - (len(message) * 3), self.character.prefab_data.y - HEIGHT * 0.15
        text = self.text_font.render(message, True, (220, 220, 220))
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
    
    def restrict_movement_character(self):
        ch_x, ch_y = self.character.prefab_data.x, self.character.prefab_data.y
        directions_restricted = [False, False, False, False]
        if(ch_x < int(WIDTH*0.09)):
            directions_restricted[0] = True
        if(ch_x > int(WIDTH*0.91)):
            directions_restricted[1] = True
        if(ch_y < int(HEIGHT*0.2)):
            directions_restricted[2] = True
        if(ch_y > int(HEIGHT*0.88)):
            directions_restricted[3] = True  
        return directions_restricted

    def show_timed_message(self, message, cycles=70):
        """
        Activa un mensaje temporal para mostrar en pantalla.
        El mensaje se mostrará durante 'cycles' ciclos de actualización.
        """
        self._timed_message = message
        self._timed_message_counter = 0
        self._timed_message_cycles = cycles

    def draw_timed_message(self):
        """
        Dibuja el mensaje temporal si está activo, sin fondo y con fuente más grande.
        """
        if hasattr(self, "_timed_message") and self._timed_message and self._timed_message_counter < self._timed_message_cycles:
            big_font = pygame.font.SysFont("Arial", 30, bold=True)
            text = big_font.render(self._timed_message, True, (240, 240, 240))
            x = (WIDTH - text.get_width()) // 2
            y = 20
            screen.blit(text, (x, y))
            self._timed_message_counter += 1
        elif hasattr(self, "_timed_message") and self._timed_message_counter >= self._timed_message_cycles:
            self._timed_message = ""
            self._timed_message_counter = 0
            self._timed_message_cycles = 0
    
    def draw_controls_help(self):
        """
        Dibuja en la esquina superior derecha la lista de controles y sus acciones.
        El texto está alineado a la izquierda.
        """
        controls = [
            ("WASD o flechas", "Mover personaje"),
            ("Espacio", "Disparar arma"),
            ("1", "Cambiar arma"),
            ("2", "Soltar arma"),
            ("3", "Recoger arma"),
            ("5", "Abrir cofre / Tomar recompensa"),
            ("P", "Pausar juego"),
            ("ESC", "Salir"),
        ]
        font = pygame.font.SysFont("Arial", 18)
        line_height = font.get_height() + 2
        x = WIDTH - 220
        y = 10

        for key, action in controls:
            text = font.render(f"{key}: {action}", True, (200, 200, 200))
            screen.blit(text, (x, y))
            y += line_height

    def draw(self):
        screen.blit(background_image, (0, 0))
        for wp in self.leaved_weapons:
            wp.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen, in_pause=self.is_in_pause)
        
        
        for torch in self.torches:
            torch.draw(screen)
        self.character.draw(screen, in_pause=self.is_in_pause)
        
        if self.character.prefab_data.y > self.chest.prefab_data.y * 0.99:
            self.chest.draw(screen, self.character)
            self.character.draw(screen, in_pause=self.is_in_pause)
        else:
            self.character.draw(screen, in_pause=self.is_in_pause)
            self.chest.draw(screen, self.character)
            
        
        if self.cannot_leave_weapon:
            self.draw_cannot_leave_weapon()
        if self.cannot_add_weapon:
            self.draw_character_message("No puedes agregar mas armas, puedes tener maximo 4")
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
        self.draw_timed_message()
        self.help_controls_counter -= 1
        if self.help_controls_counter > 0:
            self.draw_controls_help()
        pygame.display.flip()