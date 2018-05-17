class data_container:
    fitness_data = None
    node_data = None
    edge_data = None
    species_data = None

    def __init__(self, fitness, node, edge, species):
        self.fitness_data = fitness
        self.node_data = node
        self.edge_data = edge
        self.species_data = species