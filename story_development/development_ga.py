import openai

from ga.ga import GeneticAlgorithmBase
from outline_story import Outliner

# Overall approach:
# One method, feedback(idea), that emits written feedback
# Branch off from that one to implement the other methods
# feedback should be memoized, naturally.
class DevelopmentGA(GeneticAlgorithmBase):
    def __init__(self, conditioning_info, premise, population_size):
        self.conditioning_info = conditioning_info
        self.premise = premise
        self.feedback_cache = {}
        self.role_setting = """I am an experienced author and editor of children's books. I like helping new authors develop their ideas for children's stories.
The best stories:
- have memorable and relatable characters
- have positive and empowering themes
- are age appropriate
- educate
- have imaginative and creative story telling
- encourage interactive reading
- tell a focused story without getting distracted by extra fluff

I'm a ruthless critic, because tough love helps new authors learn.
My feedback is always specific and actionable."""
        GeneticAlgorithmBase.__init__(self, self.initialize_ideas(population_size))

    def initialize_ideas(self, population_size):
        outliner = Outliner(self.conditioning_info, self.premise)
        population = outliner.outline(population_size)
        print("\n\nNotes:\n\n")
        print(population[0])
        return population

    def feedback(self, individual):
        if individual not in self.feedback_cache:
            self.feedback_cache[individual] = self.get_feedback(individual)
        return self.feedback_cache[individual]
    
    def call_api(self, prompt, n=1):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": self.role_setting},
                {"role": "user", "content": prompt},
            ],
            n=n,
            temperature=1,
        )
        
        return [choice.message.content for choice in response.choices]
    
    def get_feedback(self, individual):
        # Give the LLM the overall goal, the individual
        # Ask for overall feedback, specific positive points, specific negative points... give specific evaluation criteria?
        # Rephrase it to be more concise and structured in some specific way
        feedback = self.call_api(f"""I'm writing a story for a client who gave me a premise and some requirements:
{self.premise}
{self.conditioning_info}

Here are the notes I have so far:
{individual}

My client was underwhelmed, but they couldn't articulate why.
You're an expert, and your cutting advice came highly recommended.
Please tell me what I'm doing well and what I could do better. I need to improve this story to impress my client.""")[0]
        print("\n\nFeedback:\n\n")
        print(feedback)
        return feedback
    
    def compute_fitness(self, individual):
        # Given the individual plus concise feedback, score on 2-3 specific metrics
        # Synthesize those scores into an overall score
        score = self.call_api(f"""I'm writing a story for a client who gave me a premise and some requirements:
{self.premise}
{self.conditioning_info}

Here are the notes I have so far:
{individual}

I asked an expert about my notes and got this feedback:
{self.feedback(individual)}

Rate how extensive of changes this feedback asks for between 1 and 10, where:
1 means "back to the drawing board"
10 means "some details could be improved"
Return only the number and no other text.
""")[0]
        print("\n\nScore:\n\n")
        print(score)
        return int(score)

    def mutate(self, individual):
        mutated = self.call_api(f"""I'm writing a story for a client who gave me a premise and some requirements:
{self.premise}
{self.conditioning_info}

Here are the story notes I have so far:
======== Story Notes Begin ========

{individual}

======== Story Notes End ========

I asked an expert about my notes and got this feedback:
{self.feedback(individual)})

Please rewrite my story notes to fix the issues identified in the feedback. Add new details if you need to.
""")[0]
        print("\n\nRevised:\n\n")
        print(mutated)
        return mutated

    def crossover(self, parent1, parent2):
        # Given two individuals, parent1 as the primary and parent2 as the secondary
        # Identify the best things about parent2, based on the feedback
        # Update parent1 to incorporate those best things
        raise NotImplementedError("Derived classes must implement the crossover operator")
