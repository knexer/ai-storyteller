from ga.category import Category


class Themes(Category):
    def __init__(self, conditioning_info, premise, notes):
        Category.__init__(self, conditioning_info, premise, notes)

    def category_name(self):
        return "themes"

    def best_possible_score(self):
        return 20

    def rubric(self):
        return """Ideal themes are:
- Relevant and engaging for the target audience (see client requirements above)
- Clearly shown by and well-explored in the events of the story
- Positive, empowering, and educational
- Respectful of diversity, avoiding stereotypes and cultural insensitivity"""

    def recommendations_reminder(self):
        return """Remember that combining themes, distilling overly complex themes, and simplifying for the target audience are often important too, not only adding things. Don't be afraid to recommend big changes."""
