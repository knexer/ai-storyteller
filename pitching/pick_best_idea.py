from collections import defaultdict

from fuzzywuzzy import fuzz

from llmtaskgraph.task_graph import TaskGraph
from llmtaskgraph.task import TaskGraphTask, PythonTask
from pitching.score_ideas import score_ideas


def pick_best_idea():
    task_graph = TaskGraph()
    most_creative = task_graph.add_task(
        TaskGraphTask(
            score_ideas(4),
            lambda input: {
                "criteria": "most creative, surprising, and unexpected ideas that excite the imagination",
                "ideas": input["global"]["ideas"],
            },
        )
    )
    best_fit = task_graph.add_task(
        TaskGraphTask(
            score_ideas(4),
            lambda input: {
                "criteria": f"""ideas that best fit the client's constraints:\n{input["global"]["conditioning_info"]}""",
                "ideas": input["global"]["ideas"],
            },
        )
    )
    cutest = task_graph.add_task(
        TaskGraphTask(
            score_ideas(4),
            lambda input: {
                "criteria": "cutest and most adorable stories",
                "ideas": input["global"]["ideas"],
            },
        )
    )
    task_graph.add_output_task(
        weighted_sum_task([0.5, 0.3, 0.2], [most_creative, best_fit, cutest])
    )
    return task_graph


def weighted_sum_task(weights, votes_tasks):
    return PythonTask(
        lambda input: weighted_sum(
            weights, [input[id] for id in votes_tasks], input["global"]["ideas"]
        ),
        votes_tasks,
    )


def weighted_sum(weights, votes, ideas):
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
