import pygame
import os
from scripts.game_configs import SCALE_FACTOR

images = {}
animations_list = {}
idles_list = {}

# --- Load Animations ---
def load_animations(directions: dict[str, str]):
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
    # Verifiar si ya existen las animaciones cargadas
    value = str.join(",",[f"{key}:{value}" for key, value in directions.items()])
    if value in animations_list:
        return animations_list[value]

    animations = {}
    max_dimensions = {}  # Guarda el tamaño maximo de cada direccion para ajustar el tamaño de las imagenes
    for key, folder_path in directions.items():
        frames = []
        max_width, max_height = 0, 0
        for file in sorted(os.listdir(folder_path)):
            if file.endswith(".png") and file != "idle.png":
                image = load_image(os.path.join(folder_path, file))
                print(file)
                frames.append(image)
                width, height = image.get_size()
                max_width = max(max_width, width)
                max_height = max(max_height, height)
        if not frames:
            raise ValueError(f"No images found in: {folder_path}")
        animations[key] = frames
        max_dimensions[key] = (max_width, max_height)

    animations_list[value] = (animations, max_dimensions)
    return animations, max_dimensions


def load_idle_images(directions: dict):
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
    value = str.join(",",[f"{key}:{value}" for key, value in directions.items()])
    if value in idles_list:
        return idles_list[value]
    
    idles = {}
    for key, folder_path in directions.items():
        path = os.path.join(folder_path, "idle.png")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing idle image at: {path}")
        image = load_image(path)
        idles[key] = image

    idles_list[value] = idles
    return idles

def load_image(path: str) -> pygame.Surface:
    if path in images:
        return images[path]
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(
        image,
        (int(image.get_width() * SCALE_FACTOR), int(image.get_height() * SCALE_FACTOR))
    )
    images[path] = image
    return image
