from ga.ga import GeneticAlgorithmBase
from outline_story import Outliner

# Overall approach:
# One method, feedback(idea), that emits written feedback
# Branch off from that one to implement the other methods
# feedback should be memoized, naturally.
class DevelopmentGA(GeneticAlgorithmBase):
    def __init__(self, conditioning_info, idea, population_size):
        self.conditioning_info = conditioning_info
        self.idea = idea
        self.feedback_cache = {}
        GeneticAlgorithmBase.__init__(self.initialize_ideas(population_size))

    def initialize_ideas(self, population_size):
        outliner = Outliner(self.conditioning_info, self.premise)
        ideas = outliner.outline(population_size)
        return ideas

    def feedback(self, individual):
        if individual not in self.feedback_cache:
            self.feedback_cache[individual] = self.get_feedback(individual)
        return self.feedback_cache[individual]
    
    def get_feedback(self, individual):
        # Give the LLM the overall goal, the individual
        # Ask for overall feedback, specific positive points, specific negative points... give specific evaluation criteria?
        # Rephrase it to be more concise and structured in some specific way
        raise NotImplementedError("get some feedback")
    
    def compute_fitness(self, individual):
        # Given the individual plus concise feedback, score on 2-3 specific metrics
        # Synthesize those scores into an overall score
        raise NotImplementedError("Derived classes must implement the fitness function")

    def mutate(self, individual):
        # Given the individual plus feedback, rewrite with the feedback incorporated
        raise NotImplementedError("Derived classes must implement the mutation operator")

    def crossover(self, parent1, parent2):
        # Given two individuals, parent1 as the primary and parent2 as the secondary
        # Identify the best things about parent2, based on the feedback
        # Update parent1 to incorporate those best things
        raise NotImplementedError("Derived classes must implement the crossover operator")
