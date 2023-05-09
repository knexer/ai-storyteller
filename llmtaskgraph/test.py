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
    print("ran prompt")
    return "Give a numbered list of five fast food items."


def parse_ideas(response):
    print("ran parse_ideas")
    # The regular expression pattern:
    # It looks for a number followed by a '.', ':', or ')' (with optional spaces)
    # and then captures any text until it finds a newline character or the end of the string
    pattern = re.compile(r"\d[\.\:\)]\s*(.*?)(?=\n\d|$)", re.MULTILINE)

    # Find all matches using the 'findall' method
    matches = pattern.findall(response)

    # Return the matches
    return matches


def join_ideas(_, *ideas):
    print("ran join_ideas")
    # ideas is a map from task id to an array of ideas
    all_ideas = []
    for ideas in ideas:
        all_ideas = all_ideas + ideas
    return all_ideas


task_graph = TaskGraph()
llm_tasks = [
    LLMTask(prompt, {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1}, parse_ideas)
    for _ in range(3)
]

for task in llm_tasks:
    task_graph.add_task(task)

join_task = PythonTask(join_ideas, *llm_tasks)
task_graph.add_output_task(join_task)

nested_task_ran = False


# create a task that creates other tasks
def add_nested_task(_):
    print("ran add_nested_task")

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


task_graph.add_task(PythonTask(throw_exception))

print("running task graph")
output = asyncio.run(task_graph.run())

print(output)

assert nested_task_ran