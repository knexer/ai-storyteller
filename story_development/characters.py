from ga.category import Category


class Characters(Category):
    def __init__(self, conditioning_info, premise, notes):
        Category.__init__(self, conditioning_info, premise, notes)

    def category_name(self):
        return "characters"

    def best_possible_score(self):
        return 25

    def rubric(self):
        return """An ideal cast of characters will:
- Be memorable and original
- Have distinct characterization and roles, with minimal redundancy
- Be relatable for the target audience
- Have clear motivations, goals, and, for the main characters, growth
- Have age-appropriate complexity and depth"""
