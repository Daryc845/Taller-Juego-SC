import pygame
import os

# --- Initial Setup ---
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character with Animations")
clock = pygame.time.Clock()

# --- Parametros de animación ---
RESOURCES_FOLDER = "resources" # Carpeta donde se encuentran los recursos graficos
WEAPONS_FOLDER = os.path.join(RESOURCES_FOLDER, "weapons") # Carpeta donde se encuentran los recursos graficos de las armas
WEAPON_SUBMACHINE_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_1-submachine") # Carpeta donde se encuentran los recursos graficos de la metralleta
WEAPON_RIFLE_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_2-rifle") # Carpeta donde se encuentran los recursos graficos del rifle
WEAPON_SHOTGUN_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_3-shotgun") # Carpeta donde se encuentran los recursos graficos de la escopeta
WEAPON_RAYGUN_FOLDER = os.path.join(WEAPONS_FOLDER, "weapon_4-raygun") # Carpeta donde se encuentran los recursos graficos de la pistola de rayos
CHARACTER_FOLDER = os.path.join(RESOURCES_FOLDER, "character - Chester") # Carpeta donde se encuentran los recursos graficos del personaje Chester
FRAME_CHANGE_EVERY = 1.117    # Cambia los frames cada 1.025 segundos
SCALE_FACTOR = 0.2  # Ajusta el tamaño de las imágenes a un 20% de su tamaño original (USAR PARA AJUSTAR EL TAMAÑO DE LAS IMÁGENES)
background_image = pygame.image.load(os.path.join(RESOURCES_FOLDER, "backgrounds", "bg.png"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Ajustar al tamaño de la pantalla

# --- Load Animations ---
def load_animations(directions):
    """
    Carga las animaciones de un prefab desde las carpetas especificadas.

    Args:
        directions (dict): Un diccionario donde las claves son las direcciones
            ('up', 'down', 'left', 'right') y los valores son las rutas a las carpetas
            que contienen las imágenes de las animaciones.

    Returns:
        tuple: Un diccionario con las animaciones cargadas y otro con las dimensiones máximas
        de las imágenes por dirección.

    Raises:
        ValueError: Si no se encuentran imágenes en alguna de las carpetas.
    """
    animations = {}
    max_dimensions = {}  # Guarda el tamaño maximo de cada direccion para ajustar el tamaño de las imagenes
    for key, folder_path in directions.items():
        frames = []
        max_width, max_height = 0, 0
        for file in sorted(os.listdir(folder_path)):
            if file.endswith(".png") and file != "idle.png":
                image = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
                image = pygame.transform.scale(
                    image,
                    (int(image.get_width() * SCALE_FACTOR), int(image.get_height() * SCALE_FACTOR))
                )
                frames.append(image)
                width, height = image.get_size()
                max_width = max(max_width, width)
                max_height = max(max_height, height)
        if not frames:
            raise ValueError(f"No images found in: {folder_path}")
        animations[key] = frames
        max_dimensions[key] = (max_width, max_height)
    return animations, max_dimensions


def load_idle_images(directions):
    """
    Carga las imágenes de estado inactivo (idle) de un prefab, es decir, cuando no se mueve.

    Args:
        directions (dict): Un diccionario donde las claves son las direcciones
            ('up', 'down', 'left', 'right') y los valores son las rutas a las carpetas
            que contienen las imágenes de estado inactivo.

    Returns:
        dict: Un diccionario con las imágenes de estado inactivo por dirección.

    Raises:
        FileNotFoundError: Si no se encuentra la imagen de estado inactivo en alguna de las rutas.
    """
    idles = {}
    for key, folder_path in directions.items():
        path = os.path.join(folder_path, "idle.png")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing idle image at: {path}")
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(
            image,
            (int(image.get_width() * SCALE_FACTOR), int(image.get_height() * SCALE_FACTOR))
        )
        idles[key] = image
    return idles