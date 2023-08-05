from CacheCoherence import protocols, simulation_parameters, Ops
from random import randint
import numpy as np
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, title, graphs):
        self.title, self.bar_width = "Number of {}".format(title), 0.25
        self.n_experiments, self.protocols = len(graphs), list(protocols.keys())
        self.colors = [Graph.color() for _ in range(len(protocols))]  # TODO randomize colors
        self.set_bars(graphs)
        self.plot()

    @staticmethod
    def color():
        return f'#{randint(0, 255):02X}{randint(0, 255):02X}{randint(0, 255):02X}'

    def set_bars(self, graphs):
        positions = [np.arange(self.n_experiments)]
        for i in range(1, len(protocols)):
            positions.append([x + self.bar_width for x in positions[-1]])

        for i, protocol in enumerate(protocols):
            bars = [_[protocol] for _ in graphs]
            plt.bar(positions[i], bars, color=self.colors[i], width=self.bar_width, edgecolor='white', label=protocol)

    def plot(self):
        plt.xlabel('# Experiments', fontweight='bold')
        plt.xticks([r + self.bar_width for r in range(self.n_experiments)], [str(i) for i in range(1, self.n_experiments + 1)])
        plt.legend()
        plt.title(self.title, y=1.08, fontsize=20)
        plt.show()


class Simulation:
    def __init__(self, instruction_sizes, n_processors, memory_content):
        Simulation.plot(Simulation.simulate(instruction_sizes, n_processors, memory_content))

    @staticmethod
    def generate_random_instructions(n_instructions, n_processors):
        """
        Generate a set of random instructions given the size of the instructions and number of processors
        """
        random_instructions = []
        inst, use_op, ops = (Ops.PrRd, Ops.PrWr, Ops.PrInv), (True, False), ("+", "-")
        randomized = lambda array: array[randint(0, len(array) - 1)]
        for _ in range(n_instructions):
            random_processor, random_op = randint(1, n_processors), randomized(inst)
            if random_op == Ops.PrWr:
                if randomized(use_op):
                    func = "lambda x: x" + randomized(ops) + str(randint(1, 100))
                else:
                    func = "lambda x: " + str(randint(1, 100))
                random_instructions.append((random_processor, random_op, eval(func)))
            else:
                random_instructions.append((random_processor, random_op))
        return random_instructions

    @staticmethod
    def generate_single_stats(instructions, n_processors, memory_content):
        """
        Runs a Single Experiment for each Protocols
        """
        statistics = {}
        for key in protocols.keys():
            protocol = protocols[key](n_processors=n_processors, memory_content=memory_content)
            protocol.perform_instructions(instructions, display=False)
            statistics[key] = protocol.statistics()
        return statistics

    @staticmethod
    def simulate(instruction_size, n_processors, memory_content):
        """
        Performs the simulations for 5 different sizes of instructions
        """
        return [Simulation.generate_single_stats(Simulation.generate_random_instructions(sample, n_processors), n_processors, memory_content) for sample in instruction_size]

    @staticmethod
    def graph_selector(parameter, simulations_array):
        """
        Selects the graph data based on the simulation parameter
        """
        return [{key: simulations[key][parameter] for key in protocols.keys()} for simulations in simulations_array]

    @staticmethod
    def plot(simulations_array):
        """
        Creates a single simulation session and then plot the graphs for each simulation parameters
        """
        [Graph(title=parameter, graphs=Simulation.graph_selector(parameter, simulations_array)) for parameter in simulation_parameters]


Simulation(instruction_sizes=[1000, 1000, 1000, 1000, 1000], n_processors=5, memory_content=2)
