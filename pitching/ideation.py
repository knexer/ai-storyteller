from llmtaskgraph.task import LLMTask, PythonTask
from llmtaskgraph.task_graph import TaskGraph

import re


def parse_ideas(response):
    # The regular expression pattern:
    # It looks for a number followed by a '.', ':', or ')' (with optional spaces)
    # and then captures any text until it finds a newline character or the end of the string
    pattern = re.compile(r"\d[\.\:\)]\s*(.*?)(?=\n\d|$)", re.MULTILINE)

    return pattern.findall(response)


def prompt(input):
    return f"""You are an AI storybook writer. You write engaging, creative, and highly diverse content for illustrated books for children.
The first step in your process is ideation - workshop a bunch of ideas and find the ones with that special spark.

Your client has provided some constraints for you to satisfy, but within those constraints you have total artistic control, so get creative with it!
Client constraints:
{input["global"]["conditioning_info"]}

Each idea should have a title and a 2-3 sentence premise mentioning the protagonist, the setting, and the conflict, while also highlighting what makes the story interesting.
Here's an example of a successful premise:
“Romeo and Juliet": Two teens, Romeo and Juliet, pursue their forbidden love with each other—to the chagrin of their rival families. When Juliet must choose between her family and her heart, both lovers must find a way to stay united, even if fate won't allow it.


Come up with a numbered list of eight of your best ideas. Focus on variety within the scope of the client's requests.
"""


def make_ideas(num_idea_sets):
    make_ideas = TaskGraph()
    ideation_task_ids = []
    for _ in range(num_idea_sets):
        ideation_task = LLMTask(
            prompt, {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1}, parse_ideas
        )
        ideation_task_ids.append(ideation_task.task_id)
        make_ideas.add_task(ideation_task)

    make_ideas.add_output_task(PythonTask(join_ideas, ideation_task_ids))
    return make_ideas


def join_ideas(input):
    input.pop("global")
    ideas = []
    for task_output in input.values():
        ideas.extend(task_output)
    return ideas
