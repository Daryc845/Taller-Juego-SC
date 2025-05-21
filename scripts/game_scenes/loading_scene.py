import pygame
from scripts.game_scenes.base_scene import BaseScene
from scripts.game_configs import WIDTH, HEIGHT, screen, background_image
import math
import threading
import time


class LoadingSceneBase(BaseScene):
    def __init__(self):
        super().__init__()
        self.rotation_angle = 0
        self.font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 255)
        self.LIGHT_BLUE = (100, 150, 255)
        self.circle_center = (WIDTH // 2, HEIGHT // 2)
        self.circle_radius = 40
        self.dot_radius = 8
        self.num_dots = 12
    
    def update(self):
        self.rotation_angle = (self.rotation_angle + 5) % 360
    
    def draw(self, mid_text:str = ""):
        screen.blit(background_image, (0, 0))
        loading_text = self.font.render("Cargando...", True, self.WHITE)
        screen.blit(loading_text, (WIDTH//2 - loading_text.get_width()//2, HEIGHT//2 - 100))
        diff_text = self.small_font.render(mid_text, True, self.WHITE)
        screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, HEIGHT//2 + 100))
        for i in range(self.num_dots):
            angle = math.radians((i * (360 / self.num_dots) + self.rotation_angle) % 360)
            x = self.circle_center[0] + math.cos(angle) * self.circle_radius
            y = self.circle_center[1] + math.sin(angle) * self.circle_radius
            angle_diff = (i * (360 / self.num_dots)) % 360
            dot_size = self.dot_radius * (0.5 + 0.5 * (1 - angle_diff / 180) if angle_diff <= 180 else 0.5 * angle_diff / 180)
            pygame.draw.circle(screen, self.LIGHT_BLUE if i < 3 else self.BLUE, (int(x), int(y)), int(dot_size))
        pygame.display.flip()

class LoadingScene(LoadingSceneBase):
    """
    Escena de carga que se muestra mientras se generan las configuraciones del juego
    """
    def __init__(self, difficulty, load_function):
        super().__init__()
        self.difficulty = difficulty
        def func():
            time.sleep(2)
            load_function(difficulty)
        threading.Thread(target=func, daemon=True).start()
    
    def draw(self):
        super().draw(mid_text=f"Dificultad: {self.difficulty}")

class NextPhaseLoadingScene(LoadingSceneBase):
    """
    Escena de carga que se muestra mientras se generan las configuraciones del juego
    """
    def __init__(self, thread_function, load_function):
        super().__init__()
        self.thread_function = thread_function
        self.func = load_function

    def draw(self):
        super().draw(mid_text="Preparando la fase 2")

    def start_thread(self):
        threading.Thread(target=self.thread_function, daemon=True).start()
        threading.Thread(target=self.start_load_function, daemon=True).start()

    def start_load_function(self):
        time.sleep(2)
        self.func()