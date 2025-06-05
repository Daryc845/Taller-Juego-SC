from scripts.model_scripts.markov import MarkovNode, MarkovChain
import sys
from unittest.mock import MagicMock

sys.modules['pygame'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['scripts.game_configs'] = MagicMock()

def test_markov_node_probability_range():
    node = MarkovNode(value="test1", state=1, probability=0.4)
    node.calculate_probability_range(previous_probability=0.3)
    assert node.probability_range == [0.3, 0.7]

def test_markov_chain_valid_row_sum():
    row = [
        MarkovNode(value="test1", state=1, probability=0.5),
        MarkovNode(value="test2", state=2, probability=0.5)
    ]
    chain = MarkovChain(markov_nodes=[row], initial_state=row[0])
    assert chain.validate_row_sums() == True

def test_markov_chain_is_square_matrix():
    row1 = [MarkovNode("test1", 1, 0.5), MarkovNode("test2", 2, 0.5)]
    row2 = [MarkovNode("test1", 1, 0.5), MarkovNode("test2", 2, 0.5)]
    chain = MarkovChain(markov_nodes=[row1, row2], initial_state=row1[0])
    assert chain.is_square_matrix() == True

def test_markov_chain_state_transition():
    node11 = MarkovNode("test1", 1, 0.6)
    node12 = MarkovNode("test2", 2, 0.4)
    node21 = MarkovNode("test1", 1, 0.3)
    node22 = MarkovNode("test2", 2, 0.7)

    matrix = [
        [node11, node12],
        [node21, node22]  
    ]

    chain = MarkovChain(markov_nodes=matrix, initial_state=node11)

    chain.set_state(0.35)
    assert chain.current_state.state == 1

    chain.set_state(0.75)
    assert chain.current_state.state == 2

test_markov_chain_is_square_matrix()
test_markov_chain_valid_row_sum()
test_markov_node_probability_range()
test_markov_chain_state_transition()