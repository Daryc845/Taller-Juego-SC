from abc import ABC, abstractmethod
import scripts.game_config_persistence as gcp
import os

class Prefab():
    """
    Clase base padre para representar un objeto animado en el juego.

    Attributes:
        x (int): Posición en el eje x del objeto.
        y (int): Posición en el eje y del objeto.
        speed (int): Velocidad de movimiento del objeto.
        direction (str): Dirección actual del objeto ('up', 'down', 'left', 'right') en el espacio de 2 dimensiones.
        current_frame (int): Índice del cuadro de animación actual.
        cycle_count (int): Contador de ciclos para cambiar de cuadro.
        moving (bool): Indica si el objeto se está moviendo.
        directions (dict): Diccionario con las rutas de las animaciones.
        idles (dict): Diccionario con las imágenes de estado inactivo.
        animations (dict): Diccionario con las animaciones cargadas.
        max_dimensions (dict): Dimensiones máximas de las imágenes por dirección.
        frame_update (float): Intervalo de tiempo para cambiar de cuadro(velocidad de animación).
    """

    def __init__(self, x, y, directions, frame_update=None):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = "down"
        self.current_frame = 0
        self.cycle_count = 0
        self.moving = False
        self.idles = gcp.load_idle_images(directions)
        self.animations, self.max_dimensions = gcp.load_animations(directions)
        self.frame_update = frame_update if frame_update else gcp.FRAME_CHANGE_EVERY

    def do_action(self, keys):
        """
        Detecta las acciones del prefab según las teclas presionadas, como moverse.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        self.moving = False
        if keys[gcp.pygame.K_UP]:
            self.y -= self.speed
            self.direction = "up"
            self.moving = True
        elif keys[gcp.pygame.K_DOWN]:
            self.y += self.speed
            self.direction = "down"
            self.moving = True
        elif keys[gcp.pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
            self.moving = True
        elif keys[gcp.pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
            self.moving = True

    def update_animation(self):
        """
        Actualiza el cuadro de animación actual según el estado de movimiento.
        """
        if self.moving:
            self.cycle_count += 1
            if self.cycle_count >= gcp.FRAME_CHANGE_EVERY:
                self.cycle_count = 0
                
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.direction])
        else:
            self.current_frame = 0

    def draw(self, surface):
        """
        Dibuja el objeto en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el objeto.
        """
        if self.moving and self.current_frame < len(self.animations[self.direction]):
            frame = self.animations[self.direction][self.current_frame]
        else:
            frame = self.idles[self.direction]

        max_width, max_height = self.max_dimensions[self.direction]
        pos_x = self.x - max_width // 2
        pos_y = self.y - max_height // 2
        surface.blit(frame, (pos_x, pos_y))

class Character(Prefab):
    """
    Representa un prefab jugable con animaciones y armas, en este caso Chester el gato.
    ACCIONES QUE PUEDE REALIZAR:
    - Se mueve con las teclas de flecha(arriba, abajo, izquierda y derecha) en la
    respectiva direccion.
    - Dispara con la barra espaciadora.
    - Cambia de arma con la tecla 1.

    Attributes:
        weapons (list): Lista de armas disponibles para el prefab.
        weapon_index (int): Índice del arma actualmente equipada.
        change_weapon_delay_counter (int): Contador para evitar cambios rápidos de arma.
    """

    def __init__(self, x, y, directions, frame_update=None):
        super().__init__(x, y, directions, frame_update)
        self.weapon_index = 0
        self.weapons = (Submachine(x, y - 35), Rifle(x, y - 35), Shotgun(x, y - 35), Raygun(x, y - 35))
        self.weapons[self.weapon_index].x = x
        self.weapons[self.weapon_index].y = y - 35
        self.change_weapon_delay_counter = 50

    def add_weapon(self, weapon):
        """
        Agrega un arma al inventario de Chester con un maximo de 4 armas.

        Args:
            weapon (Weapon): El arma a agregar.

        Raises:
            ValueError: Si ya hay 4 armas en el inventario.
        """
        if len(self.weapons) < 4:
            self.weapons.append(weapon.set_position(self.x, self.y - 35))
        else:
            print("Cannot add more weapons. Maximum of 4 reached.")
            #Debe remplazarse a un mensaje en pantalla que indique que no se pueden agregar más armas.

    def do_action(self, keys):
        """
        Realiza acciones de Chester según las teclas presionadas, como moverse
        o cambiar de arma.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        super().do_action(keys)
        self.change_weapon_delay_counter -= 1
        if keys[gcp.pygame.K_1] and self.change_weapon_delay_counter <= 0:
            self.change_weapon()
        self.do_action_weapons(keys)
    
    def change_weapon(self):
        """
        Cambia el arma equipada de Chester.
        """
        self.change_weapon_delay_counter = 50
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons):
            self.weapon_index = 0

    def do_action_weapons(self, keys):
        """
        Realiza acciones específicas de las armas de Chester, en este caso indica que 
        el inventario de armas se mueve junto con Chester.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        for weapon in self.weapons:
            weapon.do_action(keys)

    def update_animation(self):
        """
        Actualiza las animaciones del prefab y del arma equipada.
        """
        super().update_animation()
        self.weapons[self.weapon_index].update_animation()
        
    def draw_weapons_bullets(self, surface):
        """
        Dibuja las balas disparadas por las armas de Chester(incluso si el arma de donde provino la bala no esta seleccionada).

        Args:
            surface (pygame.Surface): Superficie donde se dibujarán las balas.
        """
        for weapon in self.weapons:
            weapon.draw_bullets(surface)

    def draw(self, surface):
        """
        Dibuja a Chester y su arma equipada en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el prefab.
        """
        if self.direction == "up" or self.direction == "down":
            super().draw(surface)
            self.draw_weapons_bullets(surface)
            self.weapons[self.weapon_index].draw(surface)
            
        else:
            self.draw_weapons_bullets(surface)
            self.weapons[self.weapon_index].draw(surface)
            super().draw(surface)
            


class Weapon(Prefab, ABC):
    """
    Representa un arma con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si el arma está disparando.
        max_munition (int): Munición máxima del arma.
        remaining_munition (int): Munición restante del arma.
        bullets_fired (list): Lista de balas disparadas por el arma.
        bullet_image (pygame.Surface): Imagen de la bala disparada por el arma.
    """

    def __init__(self, x, y, directions, bullet_folder_url, frameUpdate=None):
        super().__init__(x, y, directions, frameUpdate)
        self.bullet_image = gcp.pygame.image.load(os.path.join(bullet_folder_url, "bullet.png")).convert_alpha()
        self.adjust_image_size()
        self.shooting = False
        self.max_munition = 100
        self.remaining_munition = self.max_munition
        self.bullets_fired = []
        
    def adjust_image_size(self):
        """
        Ajusta el tamaño de la imagen de la bala a un 20% de su tamaño original.
        """
        self.bullet_image = gcp.pygame.transform.scale(
            self.bullet_image,
            (int(self.bullet_image.get_width() * gcp.SCALE_FACTOR),
            int(self.bullet_image.get_height() * gcp.SCALE_FACTOR))
        )

    def set_position(self, x, y):
        """
        Establece la posición del arma.

        Args:
            x (int): Nueva posición en el eje x.
            y (int): Nueva posición en el eje y.

        Returns:
            Weapon: La instancia actual del arma en la posición indicada.
        """
        self.x = x
        self.y = y
        return self

    def do_action(self, keys):
        """
        Realiza acciones del arma según las teclas presionadas, como disparar.

        Args:
            keys (pygame.key.ScancodeWrapper): Estado de las teclas presionadas.
        """
        super().do_action(keys)
        self.shooting = False
        if keys[gcp.pygame.K_SPACE]:
            self.shooting = True

    def shoot(self):
        """
        Dispara el arma, reduciendo la munición restante.
        Adicionalmente, crea una nueva bala y la agrega a la lista de balas disparadas.
        Esto es con el fin de tener control e información de las balas disparadas.
        """
        self.remaining_munition -= 1
        self.bullets_fired.append(Bullet(self.x, self.y, self.direction, 100,self.bullet_image))
            

    def update_animation(self):
        """
        Actualiza las animaciones del arma según su estado (disparando o inactiva).
        """
        self.cycle_count += 1
        if self.shooting:
            if self.cycle_count >= self.frame_update:
                self.evaluate_bullets_and_shoot()
        else:
            self.current_frame = 0
        
    def evaluate_bullets_and_shoot(self):
        """
        Verifica si el arma tiene munición restante y actualiza el cuadro de animación.
        Si no hay munición, muestra un mensaje indicando que no se puede disparar.
        """
        if self.remaining_munition > 0:
            self.cycle_count = self.cycle_count / 2
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.direction])
        else:
            self.current_frame = 0
            print("No munition left")
            #Debe remplazarse a un mensaje en pantalla que indique que no hay munición.
        if self.current_frame == 1:
            self.shoot()
    
    def draw_bullets(self, surface):
        """
        Dibuja las balas disparadas por el arma en la superficie proporcionada.
        """
        for bullet in self.bullets_fired:
            if bullet.alive:
                bullet.move()
                bullet.draw(surface)
            else:
                self.bullets_fired.remove(bullet)

    def draw(self, surface):
        """
        Dibuja el arma en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el arma.
        """
        if self.shooting and self.current_frame < len(self.animations[self.direction]):
            frame = self.animations[self.direction][self.current_frame]
        else:
            frame = self.idles[self.direction]
        adjust_positions = self.adjust_position()
        surface.blit(frame, adjust_positions)

    def adjust_position(self):
        """
        Ajusta la posición del arma según su dirección y la posición de Chester.
        
        Returns:
            tuple: Posición ajustada (x, y) del arma.
        """
        max_width, max_height = self.max_dimensions[self.direction]
        pos_x = (self.x - max_width // 2)
        pos_y = (self.y - max_height // 2)
        if(self.direction == "up"):
            pos_y = (self.y - max_height // 2) - 5
        elif(self.direction == "down"):
            pos_y = (self.y - max_height // 2) +25
        elif(self.direction == "left"):
            pos_x = (self.x - max_height // 2) - 50
        else:
            pos_x = (self.x - max_height // 2) - 21
        return pos_x, pos_y
    
    @abstractmethod
    def get_directions(self):
        """
        Devuelve un diccionario con las rutas de las animaciones del subfusil.

        Returns:
            dictionary: diccionario que relaciona las animaciones de una ruta con una dirección particular.
        """
        pass


class Submachine(Weapon):
    """
    Representa un subfusil(metralleta) con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si el subfusil está disparando.
        max_munition (int): Munición máxima del subfusil.
        remaining_munition (int): Munición restante del subfusil.
    """

    def __init__(self, x, y):
        bullet_folder_url = os.path.join(gcp.WEAPONS_FOLDER, "weapon_1-submachine")
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 5)
        self.shooting = False
        self.max_munition = 150
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(gcp.WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-backward_shooting"),
        "down": os.path.join(gcp.WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-forward_shooting"),
        "left": os.path.join(gcp.WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-left_shooting"),
        "right": os.path.join(gcp.WEAPON_SUBMACHINE_FOLDER, "weapon_1-submachine-animation-right_shooting")
        }   

class Rifle(Weapon):
    """
    Representa un rifle con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si el rifle está disparando.
        max_munition (int): Munición máxima del rifle.
        remaining_munition (int): Munición restante del rifle.
    """

    def __init__(self, x, y):
        bullet_folder_url = os.path.join(gcp.WEAPON_RIFLE_FOLDER)
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 10)
        self.shooting = False
        self.max_munition = 100
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(gcp.WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-backward_shooting"),
        "down": os.path.join(gcp.WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-forward_shooting"),
        "left": os.path.join(gcp.WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-left_shooting"),
        "right": os.path.join(gcp.WEAPON_RIFLE_FOLDER, "weapon_2-rifle-animation-right_shooting")
        }

class Shotgun(Weapon):
    """
    Representa una escopeta con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si la escopeta está disparando.
        max_munition (int): Munición máxima de la escopeta.
        remaining_munition (int): Munición restante de la escopeta.
    """

    def __init__(self, x, y):
        bullet_folder_url = os.path.join(gcp.WEAPON_SHOTGUN_FOLDER)
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 60)
        self.shooting = False
        self.max_munition = 70
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(gcp.WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-backward_shooting"),
        "down": os.path.join(gcp.WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-forward_shooting"),
        "left": os.path.join(gcp.WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-left_shooting"),
        "right": os.path.join(gcp.WEAPON_SHOTGUN_FOLDER, "weapon_3-shotgun-animation-right_shooting")
        }   

class Raygun(Weapon):   
    """
    Representa una pistola de rayos con animaciones y funcionalidad de disparo.

    Attributes:
        shooting (bool): Indica si la pistola de rayos está disparando.
        max_munition (int): Munición máxima de la pistola de rayos.
        remaining_munition (int): Munición restante de la pistola de rayos.
    """

    def __init__(self, x, y):
        bullet_folder_url = os.path.join(gcp.WEAPON_RAYGUN_FOLDER)
        super().__init__(x, y, self.get_directions(), bullet_folder_url, 50)
        self.shooting = False
        self.max_munition = 100
        self.remaining_munition = self.max_munition
    
    def get_directions(self):
        return {
        "up": os.path.join(gcp.WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-backward_shooting"),
        "down": os.path.join(gcp.WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-forward_shooting"),
        "left": os.path.join(gcp.WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-left_shooting"),
        "right": os.path.join(gcp.WEAPON_RAYGUN_FOLDER, "weapon_4-raygun-animation-right_shooting")
        }

class Bullet:
    """
    Representa una bala disparada por un arma.
    
    Atributes:
        x (int): Posición en el eje x de la bala.
        y (int): Posición en el eje y de la bala.
        direction (str): Dirección en la que se mueve la bala ('up', 'down', 'left', 'right').
        alive (bool): Indica si la bala está viva o no.
        speed (int): Velocidad de movimiento de la bala.
        damage (int): Daño que causa la bala al impactar.
        image (pygame.Surface): Imagen de la bala.
    """
        
    def __init__(self, x, y, direction, damage, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image
        self.alive = True
        self.speed = 10
        self.damage = damage #Usar para el daño
        self.adjust_position()
    
    def adjust_position(self):
        """
        Ajusta la posición de la bala según su dirección.
        Si la dirección es 'up' o 'down', ajusta la posición en el eje x.
        Si la dirección es 'left' o 'right', ajusta la posición en el eje y.
        """
        if self.direction == "up" or self.direction == "down":
            self.x -= 4
        else:
            self.y -= 13

    def move(self):
        """
        Mueve la bala en la dirección especificada. 
        Adicionalmente, verifica si la bala debe ser eliminada y la elimina.
        """
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        #Mata a la bala si sale de la pantalla(TAMBIEN DEBE DESAPARECER SI CHOCA CON UN ENEMIGO U OBJETO)
        self.evaluate_kill_bullet()
    
    
    def evaluate_kill_bullet(self):
        """
        Verifica si la bala ha salido de la pantalla, halla golpeado un objeto o un enemigo. 
        Si es así, marca la bala como no viva. Esto se hace para evitar que la bala siga existiendo indefinidamente.
        """
        if (self.x < 0 or self.x > gcp.WIDTH or self.y < 0 or self.y > gcp.HEIGHT):
            self.alive = False

    def draw(self, surface):
        """
        Dibuja la bala en la superficie proporcionada unicamente si se encuentra viva.
        """
        if self.alive:
            surface.blit(self.image, (self.x, self.y))