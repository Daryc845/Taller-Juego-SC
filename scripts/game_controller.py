from scripts.game_configs import FPS, screen, background_image, clock, WIDTH, HEIGHT
from scripts.game_entities import Character, EnemyType1, EnemyType2, EnemyType3, FinalEnemy, Enemy, Weapon, Chest, Torch
from scripts.intefaces import IView, IPresenter
from scripts.game_entities.data_models import PrefabData
from scripts.game_scenes import StartScene, BaseScene, NextPhaseLoadingScene
import pygame
import time
import threading

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
        self.leaved_weapons: list[Weapon] = []
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
        self.help_controls_counter = 1000
        self.preparing_time = 0
        self.leaved_weapons_timers = []
        self.leaved_weapon_lifetime = 300
        self.add_chest_generation_points()
        self.torches : list[Torch] = []
        self.add_torch_generation_points()
        self.current_wave = 1
        self.preparing_scene = NextPhaseLoadingScene((lambda: self.presenter.start_second_phase()), 
                                                     (lambda: self.next_phase_load()))
        self.preparing_new_wave = False
        self.show_timed_message(f"OLEADA {self.current_wave}", 200)

    def add_chest_generation_points(self):
        """Añade puntos de generación del cofre en posiciones predefinidas."""
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

    def add_torch_generation_points(self):
        """Añade puntos de generación de antorchas en posiciones predefinidas."""
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

    def add_random_torches(self, num_torches):
        """
        Genera 'num_torches' índices únicos usando generate_numbers(conf), redondea a 1 decimal, 
        multiplica por 10, convierte a entero y crea antorchas en los puntos correspondientes.
        La semilla inicial se basa en el tiempo actual.
        """
        indices = set()
        while len(indices) < num_torches:
            idx = int(self.presenter.get_random_between(0, len(self.torch_generation_points) - 1))
            if idx not in indices:
                indices.add(idx)
        for idx in indices:
            point = self.torch_generation_points[idx]
            self.add_torch(*point)

    def next_phase_load(self):
        self.leaved_weapons.clear()
        self.torches.clear()
        self.add_random_torches(self.current_wave)
        for wp in self.character.weapons:
            wp.direction = self.character.prefab_data.direction
            wp.set_position(self.character.prefab_data.x, self.character.prefab_data.y - 35)
        self.preparing_second_phase = False
        
    def set_presenter(self, presenter: IPresenter):
        self.presenter = presenter
    
    def show_character(self, prefab_character: PrefabData):
        if self.character is None:
            self.character = Character(prefab_character)
            self.add_random_torches(1)
        else:
            self.__reset_all()
        self.is_in_game = True

    def __reset_all(self):
        self.torches.clear()
        self.character.reset_character()
        self.enemies.clear()
        self.leaved_weapons.clear()
        self.add_random_torches(1)
        self.chest = None

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

    def show_chest(self, type: str = None):
        """Muestra el cofre en una posición aleatoria de los puntos de generación predefinidos."""
        """generation_point_index = self.generate_chest_generation_point()
        selected_point = self.chest_generation_points[generation_point_index]
        self.chest.show_chest(*selected_point)"""
        self.generate_chest(type)
        
    def generate_chest(self, type: str):
        """Genera un cofre en una posición aleatoria de los puntos de generación predefinidos"""
        generation_point_index = int(self.presenter.get_random_between(0, len(self.chest_generation_points) - 1))
        selected_point = self.chest_generation_points[generation_point_index]
        chest_data = PrefabData(*selected_point, direction="down", life=1)
        self.chest = Chest(chest_data, self.show_timed_message, self.draw_character_message, type, self.add_leaved_weapon)
        
    def add_torch(self, x: int, y: int):
        """Añade una antorcha en la posición especificada"""
        torch_data = PrefabData(x=x, y=y, direction="down", life=1)
        self.torches.append(Torch(torch_data))

    def delete_enemy(self, enemy_id: int):
        enemy = list(filter(lambda x: x.prefab_data.id == enemy_id, self.enemies))
        if len(enemy) > 0:
            self.enemies.remove(enemy[0])

    def add_leaved_weapon(self, weapon: Weapon):
        self.leaved_weapons.append(weapon)
        self.leaved_weapons_timers.append(self.leaved_weapon_lifetime)

    def on_new_wave(self, wave_number: int):
        self.preparing_new_wave = True
        self.current_wave = wave_number
        def other_actions():
            time.sleep(1)
            self.torches.clear()
            self.add_random_torches(wave_number)
            self.preparing_new_wave = False
        threading.Thread(target=other_actions, daemon=True).start()

    def character_death(self):
        self.start_scene.game_over = True
        self.start_scene.next_scene = None
        self.start_scene.draw()
        self.is_in_game = False
        self.__reset_all()

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
            self.enemies.append(FinalEnemy(prefab_enemy))
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
                self.leaved_weapons_timers.append(self.leaved_weapon_lifetime)
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
                    self.leaved_weapons_timers.pop(weapon_index)
                    
    def update_leaved_weapons(self):
        for i in reversed(range(len(self.leaved_weapons_timers))):
            self.leaved_weapons_timers[i] -= 1
            if i < len(self.leaved_weapons) and self.leaved_weapons_timers[i] <= 0:
                self.leaved_weapons.pop(i)
                self.leaved_weapons_timers.pop(i)

    def update(self):
        if not self.preparing_second_phase:
            self.in_pause_handle()
        if not self.is_in_pause:
            self.update_leaved_weapons()
            
            self.in_weapons_add_remove_handle()
            keys = pygame.key.get_pressed()

            if self.chest:
                self.chest.do_action(keys, self.character)    
                self.chest.update(self.character)
            
            for torch in self.torches:
                torch.update(self.character)
            restricetd_directions = self.restrict_movement_character()
            self.character.do_action(keys, restricted_directions=restricetd_directions)
            self.character.update_animation()
            if self.enemies_counter == 2:
                self.presenter.calculate_actions()
                self.enemies_counter = 0
            self.enemies_counter += 1
            for enemy in self.enemies:
                enemy.update_animation()

    def draw_cannot_leave_weapon(self):
        
        self.message_show_counter += 1
        self.draw_character_message("No puedes soltar mas armas, debes tener al menos una")
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
        if self.preparing_new_wave:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
            font = pygame.font.SysFont("Arial", 30, bold=True)
            if not self.preparing_second_phase:
                text = font.render("¡Nueva oleada!", True, (255, 255, 255))
                self.show_timed_message(f"OLEADA {self.current_wave}", 200)
            else:
                text = font.render("¡Preparate!", True, (255, 255, 255))
                self.show_timed_message(f"¡HAS SIDO CONVOCADO A UNA AUDIENCIA CON EL REY!", 300)
                self.show_chest()
            x = (WIDTH - text.get_width()) // 2
            y = (HEIGHT - text.get_height()) // 2
            screen.blit(text, (x, y))
            pygame.display.flip()
            
            return
        screen.blit(background_image, (0, 0))
        for wp in self.leaved_weapons:
            wp.draw(screen)
        
        for torch in self.torches:
            torch.draw(screen)
        self.character.draw(screen, self.draw_character_message, in_pause=self.is_in_pause)
        
        if self.chest:
            if self.character.prefab_data.y > self.chest.prefab_data.y * 0.99:
                self.chest.draw(screen, self.character)
                self.character.draw(screen, self.draw_character_message, in_pause=self.is_in_pause)
            else:
                self.character.draw(screen, self.draw_character_message, in_pause=self.is_in_pause)
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
            rest = 20 + self.preparing_time - now
            if rest <= 0:
                self.couting_time = False
                self.add_random_torches(self.current_wave)
                self.preparing_scene.start_thread()
            preparing_text = self.text_font.render(f"Tiempo de espera restante: {rest} segundos", True, (255, 0, 0))
            screen.blit(preparing_text, (WIDTH - preparing_text.get_width() - 20, 20))
        for enemy in self.enemies:
            enemy.draw(screen, in_pause=self.is_in_pause)
        self.draw_timed_message()
        self.help_controls_counter -= 1
        if self.help_controls_counter > 0:
            self.draw_controls_help()
        pygame.display.flip()
        pygame.display.update()