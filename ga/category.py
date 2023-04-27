import openai

import re


class Category:
    def __init__(self, conditioning_info, premise, notes):
        self.conditioning_info = conditioning_info
        self.premise = premise
        self.notes = notes

    def category_name(self):
        raise NotImplementedError("Derived classes must define a category name")

    def best_possible_score(self):
        raise NotImplementedError("Derived classes must define the best possible score")

    def rubric(self):
        raise NotImplementedError("Derived classes must define the rubric")

    def recommendations_reminder(self):
        raise NotImplementedError(
            "Derived classes must define the recommendations reminder"
        )

    def scoring_prompt(self):
        return f"""I'm working on an illustrated children's story for a client.
They gave me a premise:
{self.premise}
They gave me other requirements:
{self.conditioning_info}

I have elaborated on the premise, producing these notes:
{self.notes}

Critique this story's {self.category_name()} based on this rubric.

{self.rubric()}

Follow the list structure of the rubric. For each item, discuss things the story's {self.category_name()} do well and things they do poorly in that dimension, then lastly score that item out of 5. Be as harsh as possible!

End your review with "Overall Score: <sum of item scores>/{self.best_possible_score()}"."""

    def score(self, verbose=False, n=1):
        prompt = self.scoring_prompt()
        if verbose:
            print(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            n=n,
            temperature=1,
        )

        if verbose:
            [print(choice.message.content) for choice in response.choices]

        scores = [
            self.parse_score(prompt, choice.message.content)
            for choice in response.choices
        ]
        scores = [score for score in scores if score is not None]

        actual = len(scores)
        if actual < n:
            print(
                f"WARNING: Only {actual} scores could be parsed of the {n} responses."
            )
            _, replacements = self.score(verbose, n - actual)
            scores.extend(replacements)

        self.scores = scores

    def average_score(self):
        return sum([int(score["score"]) for score in self.scores]) / len(self.scores)

    def normalized_score(self):
        return self.average_score() / self.best_possible_score()

    def parse_score(self, prompt, response):
        score_regex = re.compile(
            "Overall Score: (\d{1,2})/" + f"{self.best_possible_score()}"
        )
        match = score_regex.search(response)

        if not match:
            print(f"WARNING: Could not parse score from response: {response}")
            return None

        overall_score = match.group(1)

        return {
            "conversation": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response},
            ],
            "score": overall_score,
        }

    def recommendations_prompt(self):
        return f"""Based on your feedback, give three detailed recommendations for how to improve the outline.
Each recommendation should solve a problem highlighted above and specify every detail on what should be changed and how. DO NOT list multiple alternative, options, or examples; give one detailed, concrete solution.
Multiple recommendations can target one problem.

{self.recommendations_reminder()}

Give your recommendations in a numbered list format. Omit preface, omit a summary, and omit other notes; include only the list itself."""

    def make_recommendations(self, num_recommendations, verbose=False):
        # Pick the num_recommendations worst scores to improve on
        worst_scores = sorted(self.scores, key=lambda score: score["score"])[
            :num_recommendations
        ]

        # Make recommendations for each score
        recommendations = []
        for score in worst_scores:
            recommendations += self.make_recommendations_from_score(score, verbose)

        self.recommendations = recommendations
        return recommendations

    def make_recommendations_from_score(self, score, verbose=False):
        prompt = self.recommendations_prompt()
        if verbose:
            print(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=score["conversation"] + [{"role": "user", "content": prompt}],
            n=1,
            temperature=1,
        )
        if verbose:
            print(response.choices[0].message.content)
        recommendations = self.parse_recommendations(
            response.choices[0].message.content
        )
        if len(recommendations) != 3:
            print(
                f"WARNING: Could not parse recommendations from response:\n{response.choices[0].message.content}\nRetrying..."
            )
            recommendations = self.make_recommendations_from_score(score)

        return recommendations

    def parse_recommendations(self, response):
        # Response is a string with a numbered list of recommendations

        # Match the start of each list element
        # Regex explanation:
        # ^(\d+) - Match a number at the start of a line
        # [^\w\n] - Match a non-word character (e.g. a period, colon, or close parenthesis)
        matches = re.finditer(r"^(\d+)[^\w\n]", response, re.MULTILINE)

        # Extract indices and sort them
        indices = [match.start() for match in matches]
        indices.append(len(response))
        indices.sort()

        # Extract items using indices
        items = [
            response[indices[i] : indices[i + 1]].strip()
            for i in range(len(indices) - 1)
        ]

        # Remove the number, punctuation, and leading whitespace from each item
        items = [
            re.sub(r"^\d+[^\w\n]\s*", "", item, flags=re.MULTILINE) for item in items
        ]

        if len(items) != 3:
            return []

        return items
