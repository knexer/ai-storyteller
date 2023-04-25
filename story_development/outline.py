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

Critique this story's outline based on this rubric describing an ideal outline:

- Conflict and tension: Has a clear and compelling central conflict that creates tension
- Resolution: Resolves its central conflict in a satisfying and logical manner that does not feel abrupt or unjustified
- Pacing: Is ruthlessly edited and engagingly paced; every event is critical to the story
- Narrative consistency: Follows a logical progression, with no plot holes, non sequitors, or unfulfilled promises
- Character-driven: Drives plot by the actions decisions of characters, not external events or coincidences

Follow the list structure of the rubric. For each item, discuss how well the outline does, identify specific ways the outline falls short of the ideal, and finally score that item out of 5. Be as harsh as possible!

End your review with "Overall Score: <sum of item scores>/<best possible score>"."""


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
