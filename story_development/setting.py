from ga.category import Category


class Setting(Category):
    def __init__(self, conditioning_info, premise, notes):
        Category.__init__(self, conditioning_info, premise, notes)

    def category_name(self):
        return "setting"

    def best_possible_score(self):
        return 25

    def rubric(self):
        return """An ideal setting:
- excites the imagination with originality and depth
- has excellent potential for illustration
- is relatable and appropriate for the target audience
- demonstrates themes or conflict with illustrative or contrasting setting elements
- has well-differentiated locations with distinct story roles and contrasting characteristics (give a 5/5 if it has only one location)"""

    def recommendations_reminder(self):
        return """Prefer to keep things simple - replacing, simplifying, or deleting a location, or combining two redundant locations - instead of adding more stuff. Don't be afraid to recommend big changes. Remember, these are early story notes, so focus on the core elements. Descriptive language and non-story-relevant details will happen later."""
