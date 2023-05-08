from llmtaskgraph.task import PythonTask, LLMTask
from llmtaskgraph.task_graph import TaskGraph

import json
import random


def score_ideas(num_voters):
    task_graph = TaskGraph()
    titles_task_ids = []
    for _ in range(num_voters):
        # Pick the top five ideas
        top_five = LLMTask(
            top_five_prompt(),
            {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1},
            lambda x: x,
        )
        task_graph.add_task(top_five)

        # Extract the list of titles
        extract_titles = LLMTask(
            extract_titles_prompt(top_five.task_id),
            {"model": "gpt-3.5-turbo", "n": 1, "temperature": 0},
            lambda x: json.loads(x),
            [top_five.task_id],
        )
        task_graph.add_task(extract_titles)
        titles_task_ids.append(extract_titles.task_id)

    task_graph.add_output_task(PythonTask(tally_votes, titles_task_ids))
    return task_graph


def top_five_prompt():
    def format_ideas(ideas):
        shuffled_ideas = ideas
        random.shuffle(shuffled_ideas)
        return "\n".join(
            [f"{i}. {idea}" for i, idea in enumerate(shuffled_ideas, start=1)]
        )

    return lambda input: (
        f"""You are an AI writing assistant helping an author filter through their story concepts to find the ideas with the most potential.
The following is a list of ideas for an illustrated children's book:

{format_ideas(input["global"]["ideas"])}

Pick the five {input["global"]["criteria"]}."""
    )


def extract_titles_prompt(task_id):
    return lambda input: (
        f"""Extract the titles of the below five story premises into a json list format:
{input[task_id]}

Output json ONLY - your output will be directly parsed so it must have NO other text such as a preamble."""
    )


def tally_votes(input):
    task_inputs = [input[task_id] for task_id in input.keys() if task_id != "global"]
    all_ideas = []
    for idea_list in task_inputs:
        all_ideas.extend(idea_list)

    counts = [(idea, all_ideas.count(idea)) for idea in set(all_ideas)]
    sorted_by_votes = sorted(counts, key=lambda x: x[1], reverse=True)
    return sorted_by_votes
