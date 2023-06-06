from llmtaskgraph.task import TaskGraphTask
from llmtaskgraph.task_graph import GraphContext, TaskGraph

from pitching.ideation import (
    make_ideas,
    function_registry as make_ideas_function_registry,
)
from pitching.pick_best_idea import (
    pick_best_idea,
    function_registry as pick_best_idea_function_registry,
)


def function_registry():
    return dict(
        {
            "init_pick_best": init_pick_best,
        },
        **pick_best_idea_function_registry(),
        **make_ideas_function_registry()
    )


def forward_graph_input(context: GraphContext):
    return context.graph_input()


def init_pick_best(context: GraphContext, ideas):
    return {
        "conditioning_info": context.graph_input()["conditioning_info"],
        "ideas": ideas,
    }


def make_premise(num_idea_sets):
    overall_graph = TaskGraph()
    make_ideas_task = TaskGraphTask(make_ideas(num_idea_sets), "forward_graph_input")
    overall_graph.add_task(make_ideas_task)

    overall_graph.add_output_task(
        TaskGraphTask(
            pick_best_idea(),
            "init_pick_best",
            make_ideas_task,
        )
    )
    return overall_graph
