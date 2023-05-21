from collections import defaultdict

from fuzzywuzzy import fuzz

from llmtaskgraph.task_graph import TaskGraph, GraphContext
from llmtaskgraph.task import TaskGraphTask, PythonTask
from pitching.score_ideas import score_ideas, function_registry as score_ideas_function_registry

def function_registry():
    return dict({
        "init_most_creative": init_most_creative,
        "init_best_fit": init_best_fit,
        "init_cutest": init_cutest,
        "weighted_sum": weighted_sum,
    }, **score_ideas_function_registry())

def init_most_creative(context: GraphContext):
    return {
        "criteria": "most creative, surprising, and unexpected ideas that excite the imagination",
        "ideas": context.graph_input()["ideas"],
    }

def init_best_fit(context: GraphContext):
    return {
        "criteria": f"""ideas that best fit the client's constraints:\n{context.graph_input()["conditioning_info"]}""",
        "ideas": context.graph_input()["ideas"],
    }

def init_cutest(context: GraphContext):
    return {
        "criteria": "cutest and most adorable stories",
        "ideas": context.graph_input()["ideas"],
    }


def pick_best_idea():
    task_graph = TaskGraph()
    most_creative = TaskGraphTask(
        score_ideas(4),
        "init_most_creative",
    )
    task_graph.add_task(most_creative)

    best_fit = TaskGraphTask(
        score_ideas(4),
        "init_best_fit",
    )
    task_graph.add_task(best_fit)
    cutest = TaskGraphTask(
        score_ideas(4),
        "init_cutest",
    )
    task_graph.add_task(cutest)
    task_graph.add_output_task(
        PythonTask(
            "weighted_sum",
            most_creative, best_fit, cutest
        )
    )
    return task_graph


def weighted_sum(context: GraphContext, weights, *votes):
    ideas = context.graph_input()["ideas"]
    weights = [0.5, 0.3, 0.2]
    combined_vote_counts = defaultdict(float)
    for weight, vote in zip(weights, votes):
        for idea, count in vote:
            combined_vote_counts[idea] += count * weight

    print_numbered_list("Most creative", votes[0])
    print_numbered_list("Best fit", votes[1])
    print_numbered_list("Cutest", votes[2])

    selected_title = max(combined_vote_counts.items(), key=lambda x: x[1])[0]

    # Find the idea that best matches the selected title
    selected_idea = max(
        [(idea, fuzz.partial_ratio(idea, selected_title)) for idea in ideas],
        key=lambda x: x[1],
    )[0]

    return selected_idea


def print_numbered_list(label, list):
    print(f"\n{label}:\n")
    for i, item in enumerate(list, start=1):
        print(f"{i}. {item}")
