import pygame
from scripts.game_scenes.base_scene import BaseScene
from scripts.game_scenes.loading_scene import LoadingScene
from scripts.game_configs import WIDTH, HEIGHT, screen, background_image
import sys

class StartScene(BaseScene):
    """
    Escena de inicio donde se selecciona la dificultad y se inicia el juego
    """
    def __init__(self, load_function):
        super().__init__()
        self.load_function = load_function
        self.next_scene = None
        self.difficulty = "normal"
        pygame.font.init()
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 36)
        self.text_font = pygame.font.SysFont("Arial", 24)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (150, 150, 150)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT - 200, 200, 50)
        btn_width = 150
        btn_height = 40
        btn_margin = 30
        total_width = (btn_width * 3) + (btn_margin * 2)
        start_x = (WIDTH - total_width) // 2
        self.easy_button = pygame.Rect(start_x, HEIGHT//2, btn_width, btn_height)
        self.normal_button = pygame.Rect(start_x + btn_width + btn_margin, HEIGHT//2, btn_width, btn_height)
        self.hard_button = pygame.Rect(start_x + (btn_width + btn_margin) * 2, HEIGHT//2, btn_width, btn_height)
    
    def handle_events(self, other_actions=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if other_actions:
                    other_actions()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.easy_button.collidepoint(mouse_pos):
                    self.difficulty = "fácil"
                elif self.normal_button.collidepoint(mouse_pos):
                    self.difficulty = "normal"
                elif self.hard_button.collidepoint(mouse_pos):
                    self.difficulty = "difícil"
                elif self.start_button.collidepoint(mouse_pos):
                    print(f"Dificultad seleccionada: {self.difficulty}")
                    self.next_scene = LoadingScene(self.difficulty, self.load_function)
    
    def update(self):
        pass
    
    def draw(self):
        screen.blit(background_image, (0, 0))
        title_text = self.title_font.render("Legend of the Shadow Slayer", True, self.WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
        diff_text = self.text_font.render("Selecciona la dificultad:", True, self.WHITE)
        screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, HEIGHT//2 - 50))
        pygame.draw.rect(screen, self.GREEN if self.difficulty == "fácil" else self.GRAY, self.easy_button)
        pygame.draw.rect(screen, self.YELLOW if self.difficulty == "normal" else self.GRAY, self.normal_button)
        pygame.draw.rect(screen, self.RED if self.difficulty == "difícil" else self.GRAY, self.hard_button)
        easy_text = self.button_font.render("Fácil", True, self.BLACK)
        normal_text = self.button_font.render("Normal", True, self.BLACK)
        hard_text = self.button_font.render("Difícil", True, self.BLACK)
        screen.blit(easy_text, (self.easy_button.x + (self.easy_button.width - easy_text.get_width())//2, 
                             self.easy_button.y + (self.easy_button.height - easy_text.get_height())//2))
        screen.blit(normal_text, (self.normal_button.x + (self.normal_button.width - normal_text.get_width())//2, 
                             self.normal_button.y + (self.normal_button.height - normal_text.get_height())//2))
        screen.blit(hard_text, (self.hard_button.x + (self.hard_button.width - hard_text.get_width())//2, 
                             self.hard_button.y + (self.hard_button.height - hard_text.get_height())//2))
        pygame.draw.rect(screen, self.BLUE, self.start_button)
        start_text = self.button_font.render("INICIAR", True, self.WHITE)
        screen.blit(start_text, (self.start_button.x + (self.start_button.width - start_text.get_width())//2, 
                             self.start_button.y + (self.start_button.height - start_text.get_height())//2))
        pygame.display.flip()