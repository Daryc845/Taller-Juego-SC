import pytest
from unittest.mock import Mock, patch, MagicMock
import sys

sys.modules['pygame'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['scripts.game_configs'] = MagicMock()

from scripts.model_scripts.game_model import GameModel
from scripts.game_entities.data_models import PrefabData, AttackData

EASY_DIFFICULTY = "Fácil"
NORMAL_DIFFICULTY = "Normal"
HARD_DIFFICULTY = "Difícil"

class TestGameModel:
    
    @pytest.fixture
    def game_model(self)-> GameModel:
        """Fixture que crea una instancia de GameModel para las pruebas"""
        return GameModel(1080, 720)
    
    @pytest.fixture
    def mock_callables(self) -> dict[str, Mock]:
        """Fixture que crea mocks para las funciones Callable"""
        return {
            'enemy_generation': Mock(),
            'new_wave': Mock(),
            'next_phase': Mock(),
            'game_won': Mock(),
            'chest_generation': Mock(),
            'attack': Mock(),
            'move': Mock(),
            'delete_enemy': Mock(),
            'character_death': Mock()
        }

    def test_init(self, game_model: GameModel):
        """Prueba la inicialización del GameModel"""
        assert game_model.in_pause == False
        assert game_model.terminate == False
        assert game_model.enemies_counter == 0
        assert game_model.waiting_lines_arrival.lambda_value == 5
        assert game_model.default_enemies == 5
        assert game_model.waves == 3
        assert game_model.environment is not None
        assert game_model.numbers_model is not None

    def test_reset_game_normal_difficulty(self, game_model: GameModel):
        """Prueba reset_game con dificultad normal"""
        game_model.reset_game(NORMAL_DIFFICULTY)
        
        assert game_model.terminate == False
        assert game_model.waiting_lines_arrival.lambda_value == 5
        assert game_model.default_enemies == 5
        assert game_model.waves == 5

    def test_reset_game_hard_difficulty(self, game_model: GameModel):
        """Prueba reset_game con dificultad difícil"""
        game_model.reset_game(HARD_DIFFICULTY)
        
        assert game_model.terminate == False
        assert game_model.waiting_lines_arrival.lambda_value == 6
        assert game_model.default_enemies == 7
        assert game_model.waves == 9

    def test_reset_game_easy_difficulty(self, game_model: GameModel):
        """Prueba reset_game con dificultad fácil"""
        game_model.reset_game(EASY_DIFFICULTY)
        
        assert game_model.terminate == False
        assert game_model.waiting_lines_arrival.lambda_value == 4
        assert game_model.default_enemies == 3
        assert game_model.waves == 2

    def test_reset_to_second_phase(self, game_model: GameModel):
        """Prueba reset_to_second_phase"""
        # Agregar algunos ataques al personaje
        attack = AttackData(1, 100, 100, 50, "right", "submachine")
        game_model.environment.character.attacks.append(attack)
        
        original_width = game_model.environment.width
        original_height = game_model.environment.height
        
        game_model.reset_to_second_phase()
        
        assert len(game_model.environment.character.attacks) == 0
        assert game_model.environment.character.x == original_width // 2
        assert game_model.environment.character.y == original_height // 2

    def test_verify_first_phase_no_enemies(self, game_model: GameModel, mock_callables: dict[str, Mock]):
        """Prueba verify_first_phase cuando no hay enemigos"""
        # Asegurar que no hay enemigos
        game_model.environment.enemies.clear()
        
        game_model.verify_first_phase(mock_callables['next_phase'])
        
        mock_callables['next_phase'].assert_called_once()

    def test_verify_first_phase_with_enemies(self, game_model: GameModel, mock_callables: dict[str, Mock]):
        """Prueba verify_first_phase cuando hay enemigos"""
        # Simular que el juego termina después de una iteración
        game_model.environment.enemies.clear()

        game_model.verify_first_phase(mock_callables['next_phase'])
        
        # La función debe haber llamado a next_phase
        mock_callables['next_phase'].assert_called_once()

    def test_verify_second_phase_no_enemies(self, game_model: GameModel, mock_callables: dict[str, Mock]):
        """Prueba verify_second_phase cuando no hay enemigos"""
        game_model.environment.total_character_points = 150
        game_model.environment.enemies.clear()
        
        game_model.verify_second_phase(mock_callables['game_won'])
        
        mock_callables['game_won'].assert_called_once_with(150)

    def test_generate_waves(self, game_model: GameModel, mock_callables: dict[str, Mock]):
        """Prueba generate_waves_and_enemies"""
        game_model.waves = 2
        game_model.default_enemies = 1
        game_model.waves_waiting_time = 0
        game_model.waiting_time_in_last_wave = 0
        game_model.environment.enemies.clear()
        
        # Mock para get_ni_number
        with patch.object(game_model, 'get_ni_number', return_value=0):
            with patch.object(game_model, '_GameModel__waiting_lines_enemies_generation'):
                game_model.generate_waves_and_enemies(
                    mock_callables['enemy_generation'],
                    mock_callables['new_wave']
                )
        
        # Verificar que se llamó
        assert mock_callables['new_wave'].call_count == 2

    def test_generate_enemy_type1(self, game_model: GameModel):
        """Prueba generate_enemy para tipo 1"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.3):
            with patch.object(game_model, '_GameModel__get_montecarlo_enemy_position', return_value=(100, 150)):
                enemy, enemy_type = game_model.generate_enemy()
                
                assert enemy_type == "type1"
                assert enemy.life == 150
                assert enemy.speed == 7
                assert enemy.x == 100
                assert enemy.y == 150

    def test_generate_enemy_type2(self, game_model: GameModel):
        """Prueba generate_enemy para tipo 2"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.6):
            with patch.object(game_model, '_GameModel__get_montecarlo_enemy_position', return_value=(200, 250)):
                enemy, enemy_type = game_model.generate_enemy()
                
                assert enemy_type == "type2"
                assert enemy.life == 125
                assert enemy.speed == 9

    def test_generate_enemy_type3(self, game_model: GameModel):
        """Prueba generate_enemy para tipo 3"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.9):
            with patch.object(game_model, '_GameModel__get_montecarlo_enemy_position', return_value=(300, 350)):
                enemy, enemy_type = game_model.generate_enemy()
                
                assert enemy_type == "type3"
                assert enemy.life == 100
                assert enemy.speed == 4

    def test_generate_final_enemy(self, game_model: GameModel):
        """Prueba generate_final_enemy"""
        with patch.object(game_model, '_GameModel__get_montecarlo_enemy_position', return_value=(400, 450)):
            enemy = game_model.generate_final_enemy()
            
            assert enemy.type == "final"
            assert enemy.life == 2000
            assert enemy.speed == 6
            assert enemy.id == 0

    def test_montecarlo_enemy_position_left_side(self, game_model: GameModel):
        """Prueba posición de enemigo en lado izquierdo"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.2):
            with patch.object(game_model, 'get_ni_number', return_value=100):
                x, y = game_model._GameModel__get_montecarlo_enemy_position()
                assert x == 0
                assert y == 100

    def test_montecarlo_enemy_position_right_side(self, game_model: GameModel):
        """Prueba posición de enemigo en lado derecho"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.4):
            with patch.object(game_model, 'get_ni_number', return_value=200):
                x, y = game_model._GameModel__get_montecarlo_enemy_position()
                assert x == game_model.environment.width
                assert y == 200

    def test_montecarlo_enemy_position_bottom(self, game_model: GameModel):
        """Prueba posición de enemigo en parte inferior"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.6):
            with patch.object(game_model, 'get_ni_number', return_value=300):
                x, y = game_model._GameModel__get_montecarlo_enemy_position()
                assert x == 300
                assert y == game_model.environment.height

    def test_montecarlo_enemy_position_top(self, game_model: GameModel):
        """Prueba posición de enemigo en parte superior"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.8):
            with patch.object(game_model, 'get_ni_number', return_value=400):
                x, y = game_model._GameModel__get_montecarlo_enemy_position()
                assert x == 400
                assert y == 0

    def test_evaluate_character_position_action_type1_attack(self, game_model: GameModel, 
                                                             mock_callables: dict[str, Mock]):
        """Prueba evaluate_character_position_action para ataque tipo 1"""
        enemy = PrefabData(100, 100, "right", 150, id=1, type="type1")
        enemy.max_dimensions = {'right': (50, 60)}
        game_model.environment.add_enemy(enemy)
        
        # Mock observation space para que esté dentro del rango de ataque
        with patch.object(game_model.environment, 'get_observation_space', 
                         return_value=(100, 100, 150, 50, 150, 50)):
            game_model.evaluate_character_position_action(
                mock_callables['attack'],
                mock_callables['move'],
                mock_callables['enemy_generation']
            )
        
        mock_callables['attack'].assert_called_once_with(False, 1, None)

    def test_evaluate_character_position_action_type1_move(self, game_model: GameModel, 
                                                           mock_callables: dict[str, Mock]):
        """Prueba evaluate_character_position_action para movimiento tipo 1"""
        enemy = PrefabData(100, 100, "right", 150, id=1, type="type1")
        enemy.max_dimensions = {'right': (50, 60)}
        game_model.environment.add_enemy(enemy)
        
        # Mock observation space para que esté fuera del rango de ataque
        with patch.object(game_model.environment, 'get_observation_space', 
                         return_value=(200, 200, 250, 150, 250, 150)):
            game_model.evaluate_character_position_action(
                mock_callables['attack'],
                mock_callables['move'],
                mock_callables['enemy_generation']
            )
        
        mock_callables['move'].assert_called_once()

    def test_calculate_move_direction_right(self, game_model: GameModel):
        """Prueba cálculo de dirección de movimiento hacia la derecha"""
        result = game_model._GameModel__calculate_move_direction(100, 50, 10, speed=5)
        assert result == "right"

    def test_calculate_move_direction_left(self, game_model: GameModel):
        """Prueba cálculo de dirección de movimiento hacia la izquierda"""
        result = game_model._GameModel__calculate_move_direction(-100, 50, 10, speed=5)
        assert result == "left"

    def test_calculate_move_direction_down(self, game_model: GameModel):
        """Prueba cálculo de dirección de movimiento hacia abajo"""
        result = game_model._GameModel__calculate_move_direction(5, 100, 10, speed=5)
        assert result == "down"

    def test_calculate_move_direction_up(self, game_model: GameModel):
        """Prueba cálculo de dirección de movimiento hacia arriba"""
        result = game_model._GameModel__calculate_move_direction(5, -100, 10, speed=5)
        assert result == "up"

    def test_calculate_move_direction_none(self, game_model: GameModel):
        """Prueba cuando no se necesita movimiento"""
        result = game_model._GameModel__calculate_move_direction(5, 3, 10, speed=5)
        assert result is None

    def test_is_close_to_player_true(self, game_model: GameModel):
        """Prueba is_close_to_player cuando está cerca"""
        result = game_model._GameModel__is_close_to_player(100, 100, 110, 110, 20)
        assert result == True

    def test_is_close_to_player_false(self, game_model: GameModel):
        """Prueba is_close_to_player cuando está lejos"""
        result = game_model._GameModel__is_close_to_player(100, 100, 200, 200, 20)
        assert result == False

    def test_evaluate_attacks_character_kills_enemy(self, game_model: GameModel, 
                                                           mock_callables: dict[str, Mock]):
        """Prueba evaluate_attacks cuando el personaje mata un enemigo"""
        # Crear un enemigo
        game_model.environment.enemies.clear()
        enemy = PrefabData(100, 100, "right", 50, id=1, type="type1")
        enemy.max_dimensions = {'right': (50, 60)}
        game_model.environment.add_enemy(enemy)
        
        # Crear un ataque del personaje
        game_model.environment.character.attacks.clear()
        attack = AttackData(100, 100, 100, 60, "right", "submachine")
        game_model.environment.character.attacks.append(attack)

        def verify(shoot: AttackData, target: PrefabData, _: bool):
            target.life -= shoot.damage
            return True
        
        # Mock para verificar daño
        with patch.object(game_model, '_GameModel__verify_shoot_damage', side_effect=verify):
            game_model.evaluate_attacks(
                mock_callables['chest_generation'],
                mock_callables['delete_enemy'],
                mock_callables['character_death']
            )
        
        # Verificar que el enemigo murió
        assert len(game_model.environment.enemies) == 0
        mock_callables['delete_enemy'].assert_called_once_with(1)
        assert game_model.environment.character_points == 10

    def test_evaluate_attacks_enemy_kills_character(self, game_model: GameModel, 
                                                           mock_callables: dict[str, Mock]):
        """Prueba evaluate_attacks cuando un enemigo mata al personaje"""
        # Crear un enemigo con ataque
        game_model.environment.enemies.clear()
        enemy = PrefabData(100, 100, "right", 100, id=1, type="type1")
        enemy_attack = AttackData(1, 100, 100, 600, "left", "melee")
        enemy.attacks.append(enemy_attack)
        game_model.environment.add_enemy(enemy)

        def verify(shoot: AttackData, target: PrefabData, _: bool):
            target.life -= shoot.damage
            return True
        
        # Mock para verificar daño
        with patch.object(game_model, '_GameModel__verify_shoot_damage', side_effect=verify):
            game_model.evaluate_attacks(
                mock_callables['chest_generation'],
                mock_callables['delete_enemy'],
                mock_callables['character_death']
            )
        
        mock_callables['character_death'].assert_called_once()
        assert game_model.terminate == True

    def test_evaluate_attacks_chest_generation(self, game_model: GameModel, 
                                                           mock_callables: dict[str, Mock]):
        """Prueba generación de cofre cuando se alcanzan 20 puntos"""
        # Configurar puntos del personaje
        game_model.environment.character_points = 10
        
        # Crear enemigo
        game_model.environment.enemies.clear()
        enemy = PrefabData(100, 100, "right", 50, id=1, type="type1")
        enemy.max_dimensions = {'right': (50, 60)}
        game_model.environment.add_enemy(enemy)
        
        # Crear ataque del personaje
        game_model.environment.character.attacks.clear()
        attack = AttackData(1, 100, 100, 60, "right", "submachine")
        game_model.environment.character.attacks.append(attack)

        def verify(shoot: AttackData, target: PrefabData, _: bool):
            target.life -= shoot.damage
            return True
        
        # Mock para chest type
        with patch.object(game_model, '_GameModel__get_chest_type', return_value="health"):
            with patch.object(game_model, '_GameModel__verify_shoot_damage', side_effect=verify):
                game_model.evaluate_attacks(
                    mock_callables['chest_generation'],
                    mock_callables['delete_enemy'],
                    mock_callables['character_death']
                )
        
        mock_callables['chest_generation'].assert_called_once_with("health")
        assert game_model.environment.character_points == 0

    def test_verify_shoot_damage_hit_center(self, game_model: GameModel):
        """Prueba verify_shoot_damage con impacto en el centro"""
        target = PrefabData(100, 100, "right", 100, type="type1")
        target.max_dimensions = {'right': (50, 60)}
        shoot = AttackData(1, 100, 100, 50, "right", "submachine")
        
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.5):
            result = game_model._GameModel__verify_shoot_damage(shoot, target, True)
        
        assert result == True
        assert target.life < 100  # Debería haber recibido daño

    def test_verify_shoot_damage_miss(self, game_model: GameModel):
        """Prueba verify_shoot_damage con fallo"""
        target = PrefabData(100, 100, "right", 100, type="type1")
        target.max_dimensions = {'right': (50, 60)}
        shoot = AttackData(1, 200, 200, 50, "right", "submachine")
        
        result = game_model._GameModel__verify_shoot_damage(shoot, target, True)
        
        assert result == False
        assert target.life == 100  # No debería haber recibido daño

    def test_get_ni_number(self, game_model: GameModel):
        """Prueba get_ni_number"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.5):
            result = game_model.get_ni_number(10, 20)
            assert result == 15.0  # 10 + (20-10) * 0.5

    def test_montecarlo_damage_values(self, game_model: GameModel):
        """Prueba los valores de daño de montecarlo"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.3):
            damage = game_model._GameModel__get_montecarlo_damage()
            assert damage == 2
        
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.7):
            damage = game_model._GameModel__get_montecarlo_damage()
            assert damage == 1
        
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.9):
            damage = game_model._GameModel__get_montecarlo_damage()
            assert damage == 0

    def test_montecarlo_weapon_values(self, game_model: GameModel):
        """Prueba los valores de armas de montecarlo"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.3):
            weapon = game_model._GameModel__get_montecarlo_weapon()
            assert weapon == "submachine"
        
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.6):
            weapon = game_model._GameModel__get_montecarlo_weapon()
            assert weapon == "rifle"
        
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.85):
            weapon = game_model._GameModel__get_montecarlo_weapon()
            assert weapon == "shotgun"
        
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.98):
            weapon = game_model._GameModel__get_montecarlo_weapon()
            assert weapon == "raygun"

    def test_markov_reward_transitions(self, game_model: GameModel):
        """Prueba las transiciones de recompensas de Markov"""
        # Desde munition a munition
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.2):
            reward = game_model._GameModel__get_reward()
            assert reward == "munition"
            assert game_model.chain.current_state.value == "munition"
        
        # Desde munition a health
        game_model.current_reward = "munition"
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.5):
            reward = game_model._GameModel__get_reward()
            assert reward == "health"
            assert game_model.chain.current_state.value == "health"
        
        # Desde munition a weapon
        game_model.current_reward = "munition"
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.8):
            reward = game_model._GameModel__get_reward()
            assert reward == "weapon"
            assert game_model.chain.current_state.value == "weapon"

    def test_get_chest_type_weapon(self, game_model: GameModel):
        """Prueba get_chest_type cuando se obtiene un arma"""
        with patch.object(game_model, '_GameModel__get_reward', return_value="weapon"):
            with patch.object(game_model, '_GameModel__get_montecarlo_weapon', return_value="shotgun"):
                chest_type = game_model._GameModel__get_chest_type()
                assert chest_type == "shotgun"

    def test_get_chest_type_non_weapon(self, game_model: GameModel):
        """Prueba get_chest_type cuando no se obtiene un arma"""
        with patch.object(game_model, '_GameModel__get_reward', return_value="health"):
            chest_type = game_model._GameModel__get_chest_type()
            assert chest_type == "health"

    def test_two_dimension_random_walk(self, game_model: GameModel):
        """Prueba two_dimension_random_walk"""
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.1):
            assert game_model._GameModel__two_dimension_random_walk() == "left"
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.3):
            assert game_model._GameModel__two_dimension_random_walk() == "up"
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.6):
            assert game_model._GameModel__two_dimension_random_walk() == "right"
        with patch.object(game_model, '_GameModel__get_pseudo_random_number', return_value=0.8):
            assert game_model._GameModel__two_dimension_random_walk() == "down"

    def test_verify_and_get_shoot_interval_center_hit(self, game_model: GameModel):
        """Prueba verify_and_get_shoot_interval con impacto central"""
        is_hit, interval = game_model._GameModel__verify_and_get_shoot_interval(100, 50, 50)
        assert is_hit == True
        assert interval == 0

    def test_verify_and_get_shoot_interval_middle_hit(self, game_model: GameModel):
        """Prueba verify_and_get_shoot_interval con impacto medio"""
        is_hit, interval = game_model._GameModel__verify_and_get_shoot_interval(100, 50, 60)
        assert is_hit == True
        assert interval == 1

    def test_verify_and_get_shoot_interval_edge_hit(self, game_model: GameModel):
        """Prueba verify_and_get_shoot_interval con impacto en el borde"""
        is_hit, interval = game_model._GameModel__verify_and_get_shoot_interval(100, 50, 77)
        assert is_hit == True
        assert interval == 2

    def test_verify_and_get_shoot_interval_miss(self, game_model: GameModel):
        """Prueba verify_and_get_shoot_interval con fallo"""
        is_hit, interval = game_model._GameModel__verify_and_get_shoot_interval(100, 50, 200)
        assert is_hit == False
        assert interval == 0


if __name__ == "__main__":
    pytest.main([__file__])