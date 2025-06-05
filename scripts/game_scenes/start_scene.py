import pygame
from scripts.game_scenes.base_scene import BaseScene
from scripts.game_scenes.loading_scene import LoadingScene
from scripts.game_configs import WIDTH, HEIGHT, screen, initial_background_image, HARD_DIFFICULTY, NORMAL_DIFFICULTY, EASY_DIFFICULTY
import sys

class StartScene(BaseScene):
    def __init__(self, load_function):
        super().__init__()
        self.load_function = load_function
        self.next_scene = None
        self.difficulty = "normal"
        self.game_over = False
        self.game_won = False
        self.final_points = 0
        pygame.font.init()
        # Fuentes modernas y legibles sobre fondo oscuro
        self.title_font = pygame.font.SysFont("Segoe UI Black", 60, bold=True)
        self.button_font = pygame.font.SysFont("Segoe UI", 34, bold=True)
        self.text_font = pygame.font.SysFont("Segoe UI", 26)
        self.diff_font = pygame.font.SysFont("Segoe UI", 22, bold=True)
        # Colores adaptados a fondo oscuro
        self.WHITE = (255, 255, 255)
        self.LIGHT = (220, 220, 220)
        self.LIGHTER = (240, 240, 240)
        self.DARK = (30, 30, 30)
        self.BLUE = (70, 130, 255)
        self.LIGHT_BLUE = (120, 200, 255)
        self.GREEN = (60, 200, 120)
        self.YELLOW = (255, 210, 60)
        self.RED = (220, 80, 80)
        self.TRANSPARENT = (0, 0, 0, 120)
        # Botones
        self.start_button = pygame.Rect(WIDTH//2 - 120, HEIGHT - 180, 240, 60)
        btn_width = 170
        btn_height = 60
        btn_margin = 40
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
                    self.difficulty = EASY_DIFFICULTY
                elif self.normal_button.collidepoint(mouse_pos):
                    self.difficulty = NORMAL_DIFFICULTY
                elif self.hard_button.collidepoint(mouse_pos):
                    self.difficulty = HARD_DIFFICULTY
                elif self.start_button.collidepoint(mouse_pos):
                    self.next_scene = LoadingScene(self.difficulty, self.load_function)

    def update(self):
        pass

    def draw_button(self, rect, color, text, hover=False, solid=False, text_color=None):
        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        if solid:
            fondo_color = color  
            alpha = 255
        else:
            fondo_color = (*color, 200 if hover else 140)
            alpha = 200 if hover else 140

        # Fondo y borde
        if solid and hover:
            fondo_color = (0, 0, 0)
            border_color = self.BLUE
            txt_color = self.BLUE if text_color is None else text_color
        elif solid:
            border_color = self.LIGHT
            txt_color = self.LIGHTER if text_color is None else text_color
        else:
            border_color = self.LIGHTER if hover else self.LIGHT
            txt_color = self.LIGHTER if hover else self.LIGHT if text_color is None else text_color

        # Dibuja el fondo
        pygame.draw.rect(button_surface, fondo_color, button_surface.get_rect(), border_radius=18)
        pygame.draw.rect(button_surface, border_color, button_surface.get_rect(), 4, border_radius=18)
        txt = self.button_font.render(text, True, txt_color)
        tx = (rect.width - txt.get_width()) // 2
        ty = (rect.height - txt.get_height()) // 2
        button_surface.blit(txt, (tx, ty))
        screen.blit(button_surface, (rect.x, rect.y))


    def draw(self):
        # Dibuja la imagen de fondo original
        screen.blit(initial_background_image, (0, 0))

        # Mensajes de estado
        if self.game_over:
            LIGHT_RED = (255, 120, 120)
            bold_font = pygame.font.SysFont("Segoe UI", 26, bold=True)
            game_over_text = bold_font.render("¡Has perdido :C! Tu mundo se ha sumido en tinieblas", True, LIGHT_RED)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
        elif self.game_won:
            LIGHT_GREEN = (180, 255, 180)
            bold_font = pygame.font.SysFont("Segoe UI", 26, bold=True)
            game_won_text = bold_font.render("¡Has ganado! Muy bien hecho :DD", True, LIGHT_GREEN)
            screen.blit(game_won_text, (WIDTH//2 - game_won_text.get_width()//2, HEIGHT//2 - 150))
            final_points_text = bold_font.render(f"Puntuación: {self.final_points}", True, LIGHT_GREEN)
            screen.blit(final_points_text, (WIDTH//2 - final_points_text.get_width()//2, HEIGHT//2 - 100))
        # Texto de dificultad 
        diff_text = self.diff_font.render("Selecciona la dificultad:", True, self.LIGHTER)
        diff_y = HEIGHT//2 - 30 
        screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, diff_y))
        # Botones de dificultad con efecto hover
        mouse_pos = pygame.mouse.get_pos()
        easy_hover = self.easy_button.collidepoint(mouse_pos)
        normal_hover = self.normal_button.collidepoint(mouse_pos)
        hard_hover = self.hard_button.collidepoint(mouse_pos)
        
        btn_y = HEIGHT//2 + 30
        self.easy_button.y = btn_y
        self.normal_button.y = btn_y
        self.hard_button.y = btn_y
        
        # Botón de iniciar con efecto hover
        start_hover = self.start_button.collidepoint(mouse_pos)
        
        self.draw_button(self.easy_button, self.GREEN if self.difficulty.lower() == "fácil" else self.DARK, "Fácil", hover=easy_hover)
        self.draw_button(self.normal_button, self.YELLOW if self.difficulty.lower() == "normal" else self.DARK, "Normal", hover=normal_hover)
        self.draw_button(self.hard_button, self.RED if self.difficulty.lower() == "difícil" else self.DARK, "Difícil", hover=hard_hover)
        self.draw_button(self.start_button, self.LIGHT_BLUE if start_hover else self.BLUE, "JUGAR", hover=start_hover, solid=True)
        pygame.display.flip()