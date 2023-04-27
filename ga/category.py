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

        average_score = sum([int(score["score"]) for score in scores]) / len(scores)
        return average_score, scores

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
            "best_possible": self.best_possible_score(),
        }
