from scripts.model_scripts.montecarlo import montecarlo
import sys
from unittest.mock import MagicMock

sys.modules['pygame'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['scripts.game_configs'] = MagicMock()

def test_sample_returns_expected_value_in_range():
    distribution = [("A", 0.5), ("B", 0.3), ("C", 0.2)]

    assert montecarlo(distribution, 0.1) == "A"
    assert montecarlo(distribution, 0.49) == "A"
    assert montecarlo(distribution, 0.5) == "B"
    assert montecarlo(distribution, 0.79) == "B"
    assert montecarlo(distribution, 0.8) == "C"
    assert montecarlo(distribution, 0.99) == "C"

def test_sample_returns_last_element_on_boundary():
    distribution = [("A", 0.3), ("B", 0.3), ("C", 0.4)]
    assert montecarlo(distribution, 1.0) == "C"

def test_sample_with_exact_probability_match():
    distribution = [("X", 0.4), ("Y", 0.6)]
    assert montecarlo(distribution, 0.4) == "Y"

def test_sample_fallback_when_sum_less_than_1():
    distribution = [("A", 0.3), ("B", 0.3)]
    assert montecarlo(distribution, 0.99) == "B"

def test_sample_with_function_values():
    distribution = [(lambda: "x", 0.5), (lambda: "y", 0.5)]
    selected = montecarlo(distribution, 0.1)
    assert callable(selected)
    assert selected() in ["x", "y"]
