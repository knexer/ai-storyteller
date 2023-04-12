import random

# Implements a basic genetic algorithm. Derived classes must implement the various operators.
class GeneticAlgorithmBase:
    def __init__(self, initial_population):
        self.population = initial_population
        self.population_size = len(initial_population)
        self.fitness_cache = {}

    # Memoize fitness calculations
    def fitness(self, individual):
        if individual not in self.fitness_cache:
            self.fitness_cache[individual] = self.compute_fitness(individual)
        return self.fitness_cache[individual]

    def compute_fitness(self, individual):
        raise NotImplementedError("Derived classes must implement the fitness function")

    def mutate(self, individual):
        raise NotImplementedError("Derived classes must implement the mutation operator")

    def crossover(self, parent1, parent2):
        raise NotImplementedError("Derived classes must implement the crossover operator")

    # Select parents randomly, proportional to their fitness
    # todo - tournament selection is probably better. Interpreting the fitness value as ~probability is an unprincipled hack.
    # Or culling to top-k, copying all of those, and then *also* picking some parents from that set?
    def select_parents(self):
        total_fitness = sum(self.fitness(individual) for individual in self.population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual in self.population:
            current += self.fitness(individual)
            if current > pick:
                return individual
        return self.population[-1]

    def evolve(self, crossover_prob, mutation_prob, generations):
        for _ in range(generations):
            new_population = []
            for _ in range(self.population_size):
                parent1 = self.select_parents()
                parent2 = self.select_parents()
                if random.random() < crossover_prob:
                    offspring = self.crossover(parent1, parent2)
                else:
                    offspring = random.choice([parent1, parent2])
                if random.random() < mutation_prob:
                    offspring = self.mutate(offspring)
                new_population.append(offspring)
            self.population = new_population
            # self.fitness_cache = {} # clearing memoization cache probably not needed? We are cloning so keeping it helps

        best_individual = max(self.population, key=self.fitness)
        return best_individual
