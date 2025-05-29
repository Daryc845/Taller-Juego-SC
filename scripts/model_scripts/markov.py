
# nodo de markov que contiene estado actual, probabilidad y rangos de probabilidad de cambio de estado
class MarkovNode():
    def __init__(self, state, probability):
        self.state = state
        self.probability = probability
        self.probability_range = []
    # calcula los rangos de probabilidad para el nodo de markov
    def calculate_probability_range(self, previous_probability=0):
       self.probability_range = [previous_probability, previous_probability + self.probability]
    
# cadena de markov que contiene los nodos de markov y el estado actual
class MarkovChain():
    def __init__(self, markov_nodes : list[list], initial_state):
        self.markov_nodes = markov_nodes
        self.current_state = initial_state
        self.previous_state = initial_state
        self.init_probability_ranges()

    # Inicializa los rangos de probabilidad para cada nodo de markov
    def init_probability_ranges(self):
         for row in self.markov_nodes:
            previous_probability = 0
            for node in row:
                node.calculate_probability_range(previous_probability)
                previous_probability += node.probability
                if(previous_probability>= 1.0):
                    previous_probability = 0
    
    # Establece el estado actual de la cadena de markov basado en una probabilidad nueva
    def set_state(self, prob_new_state):
        for node_markov in self.markov_nodes[self.current_state.state -1]:
            if prob_new_state >= node_markov.probability_range[0] and prob_new_state <= node_markov.probability_range[1]:
                self.previous_state = self.current_state
                self.current_state = node_markov
                break
    # Valida que la suma de las probabilidades de cada fila sea igual a 1 
    def validate_row_sums(self):
        for row in self.markov_nodes:
            total = sum(node.probability for node in row)
            if abs(total - 1.0) > 1e-6:
                return False
        return True
    # Verifica si la matriz de markov es cuadrada, es decir, tiene el mismo número de filas y columnas
    def is_square_matrix(self):
        num_rows = len(self.markov_nodes)
        for row in self.markov_nodes:
            if len(row) != num_rows:
                return False
        return True