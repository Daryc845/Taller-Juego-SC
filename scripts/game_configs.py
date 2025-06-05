import pygame
import os

# --- Initial Setup ---
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("Legend of the Shadow Slayer")
clock = pygame.time.Clock()

EASY_DIFFICULTY = "Fácil"
NORMAL_DIFFICULTY = "Normal"
HARD_DIFFICULTY = "Difícil"

# --- Parametros de animación ---
RESOURCES_FOLDER = "resources" # Carpeta donde se encuentran los recursos graficos
WEAPONS_FOLDER = os.path.join(RESOURCES_FOLDER, "weapons") # Carpeta donde se encuentran los recursos graficos de las armas
WEAPON_SUBMACHINE_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_1-submachine") # Carpeta donde se encuentran los recursos graficos de la metralleta
WEAPON_RIFLE_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_2-rifle") # Carpeta donde se encuentran los recursos graficos del rifle
WEAPON_SHOTGUN_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_3-shotgun") # Carpeta donde se encuentran los recursos graficos de la escopeta
WEAPON_RAYGUN_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_4-raygun") # Carpeta donde se encuentran los recursos graficos de la pistola de rayos
ENEMY_1_FOLDER = os.path.join(RESOURCES_FOLDER, "enemies", "enemy_type_1") # Carpeta donde se encuentran los recursos graficos del enemigo 1
ENEMY_2_FOLDER = os.path.join(RESOURCES_FOLDER, "enemies", "enemy_type_2") # Carpeta donde se encuentran los recursos graficos del enemigo 2
ENEMY_3_FOLDER = os.path.join(RESOURCES_FOLDER, "enemies", "enemy_type_3") # Carpeta donde se encuentran los recursos graficos del enemigo 3
ENEMY_4_FOLDER = os.path.join(RESOURCES_FOLDER, "enemies", "enemy_type_4") # Carpeta donde se encuentran los recursos graficos del enemigo 4
CHARACTER_FOLDER = os.path.join(RESOURCES_FOLDER, "character - Chester") # Carpeta donde se encuentran los recursos graficos del personaje Chester
FRAME_CHANGE_EVERY = 1.117    # Cambia los frames cada 1.025 segundos
SCALE_FACTOR = 0.2  # Ajusta el tamaño de las imágenes a un 20% de su tamaño original (USAR PARA AJUSTAR EL TAMAÑO DE LAS IMÁGENES)
background_image = pygame.image.load(os.path.join(RESOURCES_FOLDER, "backgrounds", "bg.png"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Ajustar al tamaño de la pantalla
initial_background_image = pygame.image.load(os.path.join(RESOURCES_FOLDER, "backgrounds", "presentation_bg.png"))
initial_background_image = pygame.transform.scale(initial_background_image, (WIDTH, HEIGHT))  # Ajustar al tamaño de la pantalla
pygame.mixer.music.load(os.path.join(RESOURCES_FOLDER, "sounds", "intro.mp3"))
pygame.mixer.music.play(-1)
is_intro_playing = True

def stop_intro():
    global is_intro_playing
    if is_intro_playing:
        pygame.mixer.music.fadeout(2000)
        is_intro_playing = False

def reset_intro():
    global is_intro_playing
    if not is_intro_playing:
        pygame.mixer.music.play(-1)
        is_intro_playing = True