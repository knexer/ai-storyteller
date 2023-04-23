import openai

import re


def scoring_prompt(conditioning_info, premise, notes):
    return f"""I'm working on an illustrated children's story for a client.
They gave me a premise:
{premise}
They gave me other requirements:
{conditioning_info}

I have elaborated on the premise, producing these notes:
{notes}

Critique this story's cast based on this rubric.

An ideal cast of characters will:
- Be memorable and original
- have distinct characterization and roles, with minimal redundancy
- Be relatable for the target audience
- Have clear motivations, goals, and, for the main characters, growth
- Have age-appropriate complexity and depth

Follow the list structure of the rubric. For each item, discuss things the cast does well and things they do poorly in that dimension, then lastly score that item out of 5. Be as harsh as possible!

End your review with "Overall Score: <score>/<best possible score>"."""


def score(conditioning_info, premise, notes, verbose=False, n=1):
    prompt = scoring_prompt(conditioning_info, premise, notes)
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
        parse_score(prompt, choice.message.content) for choice in response.choices
    ]
    scores = [score for score in scores if score is not None]

    actual = len(scores)
    if actual < n:
        _, replacements = score(conditioning_info, premise, notes, verbose, n - actual)
        scores.extend(replacements)

    average_score = sum([int(score["score"]) for score in scores]) / len(scores)
    return average_score, scores


def parse_score(prompt, response):
    score_regex = re.compile("Overall Score: (\d{1,2})/25")
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
