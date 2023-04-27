from ga.category import Category


class Outline(Category):
    def __init__(self, conditioning_info, premise, notes):
        Category.__init__(self, conditioning_info, premise, notes)

    def category_name(self):
        return "outline"

    def best_possible_score(self):
        return 25

    def rubric(self):
        return """An ideal outline:
- Conflict and tension: Has a clear and compelling central conflict that creates tension
- Resolution: Resolves its central conflict in a satisfying and logical manner that does not feel abrupt or unjustified
- Pacing: Is ruthlessly edited and engagingly paced; every event is critical to the story
- Narrative consistency: Follows a logical progression, with no plot holes, non sequitors, or unfulfilled promises
- Character-driven: Drives plot by the actions decisions of characters, not external events or coincidences"""
