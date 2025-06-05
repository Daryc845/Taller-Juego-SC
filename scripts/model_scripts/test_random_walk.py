# scripts/model_scripts/test_random_walk.py

import pytest
from scripts.model_scripts.random_walk import random_choice

def test_random_choice_uniform():
    states = ["a", "b", "c", "d"]
    assert random_choice(states, rand_num=0.1) == "a"
    assert random_choice(states, rand_num=0.3) == "b"
    assert random_choice(states, rand_num=0.6) == "c"
    assert random_choice(states, rand_num=0.9) == "d"

def test_random_choice_with_probabilities():
    states = ["left", "up", "right", "down"]
    probs = [0.25, 0.25, 0.25, 0.25]
    assert random_choice(states, probs, rand_num=0.1) == "left"
    assert random_choice(states, probs, rand_num=0.3) == "up"
    assert random_choice(states, probs, rand_num=0.6) == "right"
    assert random_choice(states, probs, rand_num=0.9) == "down"

def test_random_choice_fallback():
    # Catches rounding errors
    states = ["one", "two", "three"]
    probs = [0.1, 0.2, 0.7]
    assert random_choice(states, probs, rand_num=0.9999999) == "three"

def test_random_choice_invalid():
    with pytest.raises(ValueError):
        random_choice([])
    with pytest.raises(ValueError):
        random_choice(["a", "b"], [0.5])
    with pytest.raises(ValueError):
        random_choice(["a", "b"], [0.5, 0.6])  # sum > 1
