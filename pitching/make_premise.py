from llmtaskgraph.task import TaskGraphTask
from llmtaskgraph.task_graph import TaskGraph

from pitching.ideation import make_ideas
from pitching.pick_best_idea import pick_best_idea


def make_premise(num_idea_sets):
    overall_graph = TaskGraph()
    make_ideas_task_id = overall_graph.add_task(
        TaskGraphTask(make_ideas(num_idea_sets), lambda input: input["global"])
    )
    overall_graph.add_output_task(
        TaskGraphTask(
            pick_best_idea(),
            lambda input: {
                "conditioning_info": input["global"]["conditioning_info"],
                "ideas": input[make_ideas_task_id],
            },
            [make_ideas_task_id],
        )
    )
    return overall_graph
