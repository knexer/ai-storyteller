from collections import defaultdict
from typing import Any, Iterable

from fuzzywuzzy import fuzz  # type: ignore

from llmtaskgraph.task_graph import TaskGraph, GraphContext
from llmtaskgraph.task import TaskGraphTask, PythonTask
from llmtaskgraph.function_registry import FunctionRegistry
from pitching.score_ideas import (
    score_ideas,
    function_registry as score_ideas_function_registry,
)


def init_most_creative(context: GraphContext) -> dict[str, str | list[str]]:
    return {
        "criteria": "most creative, surprising, and unexpected ideas that excite the imagination",
        "ideas": context.graph_input()["ideas"],
    }


def init_best_fit(context: GraphContext) -> dict[str, str | list[str]]:
    return {
        "criteria": f"""ideas that best fit the client's constraints:\n{context.graph_input()["conditioning_info"]}""",
        "ideas": context.graph_input()["ideas"],
    }


def init_cutest(context: GraphContext) -> dict[str, str | list[str]]:
    return {
        "criteria": "cutest and most adorable stories",
        "ideas": context.graph_input()["ideas"],
    }


def weighted_sum(
    context: GraphContext,
    most_creative: list[tuple[str, int]],
    best_fit: list[tuple[str, int]],
    cutest: list[tuple[str, int]],
) -> str:
    ideas = context.graph_input()["ideas"]
    weights = [0.5, 0.3, 0.2]
    votes = [most_creative, best_fit, cutest]
    combined_vote_counts: dict[str, float] = defaultdict(float)
    for weight, vote in zip(weights, votes):
        for idea, count in vote:
            combined_vote_counts[idea] += count * weight

    print_numbered_list("Most creative", most_creative)
    print_numbered_list("Best fit", best_fit)
    print_numbered_list("Cutest", cutest)

    selected_title = max(combined_vote_counts.items(), key=lambda x: x[1])[0]

    # Find the idea that best matches the selected title
    matches: Iterable[tuple[str, float]] = [
        (idea, fuzz.partial_ratio(idea, selected_title)) for idea in ideas  # type: ignore
    ]
    selected_idea: str = max(
        matches,
        key=lambda x: x[1],
    )[0]

    return selected_idea


registry = FunctionRegistry()
init_most_creative_id = registry.register(init_most_creative)
init_best_fit_id = registry.register(init_best_fit)
init_cutest_id = registry.register(init_cutest)
weighted_sum_id = registry.register(weighted_sum)
registry = registry.merge(score_ideas_function_registry())


def function_registry() -> FunctionRegistry:
    return registry.copy()


def pick_best_idea() -> TaskGraph:
    task_graph = TaskGraph()
    most_creative = TaskGraphTask(
        score_ideas(10),
        init_most_creative_id,
    )
    task_graph.add_task(most_creative)

    best_fit = TaskGraphTask(
        score_ideas(10),
        init_best_fit_id,
    )
    task_graph.add_task(best_fit)
    cutest = TaskGraphTask(
        score_ideas(10),
        init_cutest_id,
    )
    task_graph.add_task(cutest)
    task_graph.add_output_task(
        PythonTask(weighted_sum_id, most_creative, best_fit, cutest)
    )
    return task_graph


def print_numbered_list(label: str, list: list[Any]) -> None:
    print(f"\n{label}:\n")
    for i, item in enumerate(list, start=1):
        print(f"{i}. {item}")
