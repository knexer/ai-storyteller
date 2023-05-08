import asyncio
import random
import re
import os
from dotenv import load_dotenv

import openai

from llmtaskgraph.task import LLMTask, PythonTask
from llmtaskgraph.task_graph import TaskGraph

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def prompt(_):
    return """You are an AI storybook writer. You write engaging, creative, and highly diverse content for illustrated books for children.
The first step in your process is ideation - workshop a bunch of ideas and find the ones with that special spark.

Your client has provided some constraints for you to satisfy, but within those constraints you have total artistic control, so get creative with it!
Client constraints:
target audience is a 5 year old boy.The story should help the reader overcome a fear of butterflies.

Each idea should have a title and a 2-3 sentence premise mentioning the protagonist, the setting, and the conflict, while also highlighting what makes the story interesting.
Here's an example of a successful premise:
“Romeo and Juliet": Two teens, Romeo and Juliet, pursue their forbidden love with each other—to the chagrin of their rival families. When Juliet must choose between her family and her heart, both lovers must find a way to stay united, even if fate won't allow it.


Come up with a numbered list of eight of your best ideas. Focus on variety within the scope of the client's requests.
"""


def parse_ideas(response):
    # The regular expression pattern:
    # It looks for a number followed by a '.', ':', or ')' (with optional spaces)
    # and then captures any text until it finds a newline character or the end of the string
    pattern = re.compile(r"\d[\.\:\)]\s*(.*?)(?=\n\d|$)", re.MULTILINE)

    # Find all matches using the 'findall' method
    matches = pattern.findall(response)

    # Return the matches
    return matches


def join_ideas(ideas):
    # ideas is a map from task id to an array of ideas
    all_ideas = []
    for _, ideas in ideas.items():
        all_ideas = all_ideas + ideas
    return all_ideas


def pick_five_ideas(ideas):
    return random.shuffle(ideas.items()[0])[:5]


task_graph = TaskGraph()
llm_tasks = [
    LLMTask(prompt, {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1}, parse_ideas)
    for _ in range(3)
]
[task_graph.add_task(task) for task in llm_tasks]

join_task = PythonTask(join_ideas, [task.task_id for task in llm_tasks])
task_graph.add_output_task(join_task)

nested_task_ran = False


# create a task that creates other tasks
def add_nested_task(_):
    def nested_task(_):
        global nested_task_ran
        nested_task_ran = True
        print("nested task ran")
        return "nested task ran"

    task_graph.add_task(PythonTask(nested_task))
    print("nested task created")
    return "nested task created"


task_graph.add_task(PythonTask(add_nested_task))


# create a task that throws an exception
def throw_exception(_):
    raise Exception("test exception")


# task_graph.add_task(PythonTask(throw_exception))


asyncio.run(task_graph.run())

print(join_task.output)

assert nested_task_ran
