import random


class Individual:
    def __init__(self, categories):
        self.categories = categories

    def score(self, verbose=False, n=3):
        for category in self.categories:
            category.score(verbose=verbose, n=n)

    def total_score(self):
        return sum(category.average_score() for category in self.categories)

    def normalized_score(self):
        return sum(category.normalized_score() for category in self.categories) / len(
            self.categories
        )

    def best_possible_score(self):
        return sum(category.best_possible_score() for category in self.categories)

    def make_recommendations(self, verbose=False, num_recommendations=3):
        num_missing_points = self.best_possible_score() - self.total_score()

        # Pick some categories to improve on, weighted by how many points they're missing
        # Categories with worse scores (more missing points) are probably easier to improve
        recommendations_per_category = {category: 0 for category in self.categories}
        for _ in range(num_recommendations):
            missing_point = random.uniform(0, num_missing_points)
            current = 0
            for category in self.categories:
                current += category.best_possible_score() - category.average_score()
                if current > missing_point:
                    recommendations_per_category[category] += 1

        # Make recommendations for each category
        recommendations = []
        for category, category_recs in recommendations_per_category.items():
            recommendations.append(
                category.make_recommendations(category_recs, verbose)
            )

        return recommendations

    # def apply_recommendation(self, recommendation, verbose=False):
