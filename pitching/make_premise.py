from llmtaskgraph.task import TaskGraphTask
from llmtaskgraph.task_graph import GraphContext, TaskGraph
from llmtaskgraph.function_registry import FunctionRegistry, forward_graph_input

from pitching.ideation import (
    make_ideas,
    function_registry as make_ideas_function_registry,
)
from pitching.pick_best_idea import (
    pick_best_idea,
    function_registry as pick_best_idea_function_registry,
)


def init_pick_best(
    context: GraphContext, ideas: list[str]
) -> dict[str, str | list[str]]:
    return {
        "conditioning_info": context.graph_input()["conditioning_info"],
        "ideas": ideas,
    }


registry = FunctionRegistry()
init_pick_best_id = registry.register(init_pick_best)


def function_registry() -> FunctionRegistry:
    return registry.merge(pick_best_idea_function_registry()).merge(
        make_ideas_function_registry()
    )


def make_premise(num_idea_sets: int) -> TaskGraph:
    overall_graph = TaskGraph()
    make_ideas_task = TaskGraphTask(make_ideas(num_idea_sets), forward_graph_input)
    overall_graph.add_task(make_ideas_task)

    overall_graph.add_output_task(
        TaskGraphTask(
            pick_best_idea(),
            init_pick_best_id,
            make_ideas_task,
        )
    )
    return overall_graph
