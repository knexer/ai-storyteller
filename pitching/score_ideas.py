from llmtaskgraph.task import PythonTask, LLMTask
from llmtaskgraph.task_graph import GraphContext, TaskGraph
from llmtaskgraph.function_registry import (
    FunctionRegistry,
    openai_chat,
    dont_parse,
    parse_json,
)

import random


def pick_top_five(context: GraphContext) -> str:
    def format_ideas(ideas: list[str]) -> str:
        shuffled_ideas = ideas
        random.shuffle(shuffled_ideas)
        return "\n".join(
            [f"{i}. {idea}" for i, idea in enumerate(shuffled_ideas, start=1)]
        )

    return f"""You are an AI writing assistant helping an author filter through their story concepts to find the ideas with the most potential.
The following is a list of ideas for an illustrated children's book:

{format_ideas(context.graph_input()["ideas"])}

Pick the five {context.graph_input()["criteria"]}."""


def extract_titles(top_five: str) -> str:
    return f"""Extract the titles of the below five story premises into a json list format:
{top_five}

Output json ONLY - your output will be directly parsed so it must have NO other text such as a preamble."""


def tally_votes(*idea_lists: list[str]) -> list[tuple[str, int]]:
    all_ideas: list[str] = []
    for idea_list in idea_lists:
        all_ideas.extend(idea_list)

    counts = [(idea, all_ideas.count(idea)) for idea in set(all_ideas)]
    sorted_by_votes = sorted(counts, key=lambda x: x[1], reverse=True)
    return sorted_by_votes


registry = FunctionRegistry()
pick_top_five_id = registry.register(pick_top_five)
extract_titles_id = registry.register_no_context(extract_titles)
tally_votes_id = registry.register_no_context(tally_votes)


def function_registry() -> FunctionRegistry:
    return registry.copy()


def score_ideas(num_voters: int) -> TaskGraph:
    task_graph = TaskGraph()
    titles_tasks: list[LLMTask] = []
    for _ in range(num_voters):
        # Pick the top five ideas
        top_five = LLMTask(
            pick_top_five_id,
            openai_chat,
            {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1},
            dont_parse,
        )
        task_graph.add_task(top_five)

        # Extract the list of titles
        extract_titles = LLMTask(
            extract_titles_id,
            openai_chat,
            {"model": "gpt-3.5-turbo", "n": 1, "temperature": 0},
            parse_json,
            top_five,
        )
        task_graph.add_task(extract_titles)
        titles_tasks.append(extract_titles)

    task_graph.add_output_task(PythonTask(tally_votes_id, *titles_tasks))
    return task_graph
