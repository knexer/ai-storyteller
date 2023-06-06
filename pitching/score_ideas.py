from llmtaskgraph.task import PythonTask, LLMTask
from llmtaskgraph.task_graph import GraphContext, TaskGraph

import json
import random


def function_registry():
    return {
        "pick_top_five": pick_top_five,
        "extract_titles": extract_titles,
        "tally_votes": tally_votes,
    }


def score_ideas(num_voters):
    task_graph = TaskGraph()
    titles_tasks = []
    for _ in range(num_voters):
        # Pick the top five ideas
        top_five = LLMTask(
            "pick_top_five",
            "openai_chat",
            {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1},
            "identity",
        )
        task_graph.add_task(top_five)

        # Extract the list of titles
        extract_titles = LLMTask(
            "extract_titles",
            "openai_chat",
            {"model": "gpt-3.5-turbo", "n": 1, "temperature": 0},
            "parse_json",
            top_five,
        )
        task_graph.add_task(extract_titles)
        titles_tasks.append(extract_titles)

    task_graph.add_output_task(PythonTask("tally_votes", *titles_tasks))
    return task_graph


def pick_top_five(context):
    def format_ideas(ideas):
        shuffled_ideas = ideas
        random.shuffle(shuffled_ideas)
        return "\n".join(
            [f"{i}. {idea}" for i, idea in enumerate(shuffled_ideas, start=1)]
        )

    return f"""You are an AI writing assistant helping an author filter through their story concepts to find the ideas with the most potential.
The following is a list of ideas for an illustrated children's book:

{format_ideas(context.graph_input()["ideas"])}

Pick the five {context.graph_input()["criteria"]}."""


def extract_titles(context: GraphContext, top_five):
    return f"""Extract the titles of the below five story premises into a json list format:
{top_five}

Output json ONLY - your output will be directly parsed so it must have NO other text such as a preamble."""


def tally_votes(context: GraphContext, *idea_lists):
    all_ideas = []
    for idea_list in idea_lists:
        all_ideas.extend(idea_list)

    counts = [(idea, all_ideas.count(idea)) for idea in set(all_ideas)]
    sorted_by_votes = sorted(counts, key=lambda x: x[1], reverse=True)
    return sorted_by_votes
