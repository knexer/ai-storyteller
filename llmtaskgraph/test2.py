import asyncio
import json
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


def parse_ideas(_, response):
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


function_registry = {}
function_registry["prompt"] = prompt
function_registry["parse_ideas"] = parse_ideas
function_registry["join_ideas"] = join_ideas

nested_task_ran = False


def nested_task(_):
    global nested_task_ran
    nested_task_ran = True
    print("nested task ran")
    return "nested task ran"


# create a task that creates other tasks
def add_nested_task(context):
    print("ran add_nested_task")

    context.add_task(PythonTask("nested_task"))
    print("nested task created")
    return "nested task created"


function_registry["nested_task"] = nested_task
function_registry["add_nested_task"] = add_nested_task


# create a task that throws an exception
def throw_exception(_):
    raise Exception("test exception")


function_registry["throw_exception"] = throw_exception

serialized_graph = """{"tasks":[{"type":"LLMTask","task_id":"3769a085-1687-4b88-87b8-9683da6816c5","deps":[],"kwdeps":{},"created_by":null,"output_data":["Cheeseburgerzzz!!1!1","Chicken nuggets","French fries","Soft drink","Hot dog"],"prompt_formatter_id":"prompt","params":{"model":"gpt-3.5-turbo","n":1,"temperature":1},"output_parser_id":"parse_ideas"},{"type":"LLMTask","task_id":"27f6f4df-1c4e-4c50-adfb-0a95081ba565","deps":[],"kwdeps":{},"created_by":null,"output_data":["Big Mac burger from McDonald's ","Whopper sandwich from Burger King ","Chicken sandwich from Chick-fil-A ","Crunchy Taco from Taco Bell ","Classic Roast Beef sandwich from Arby's"],"prompt_formatter_id":"prompt","params":{"model":"gpt-3.5-turbo","n":1,"temperature":1},"output_parser_id":"parse_ideas"},{"type":"LLMTask","task_id":"59067c3b-3473-478b-9d3b-0e8c5f88f77f","deps":[],"kwdeps":{},"created_by":null,"output_data":["Hamburger","Chicken Nuggets","French Fries","Pizza","Tacos"],"prompt_formatter_id":"prompt","params":{"model":"gpt-3.5-turbo","n":1,"temperature":1},"output_parser_id":"parse_ideas"},{"type":"PythonTask","task_id":"95c0370b-2488-4882-99a5-61fdc0dda382","deps":["3769a085-1687-4b88-87b8-9683da6816c5","27f6f4df-1c4e-4c50-adfb-0a95081ba565","59067c3b-3473-478b-9d3b-0e8c5f88f77f"],"kwdeps":{},"created_by":null,"output_data":null,"callback_id":"join_ideas"},{"type":"PythonTask","task_id":"862e65ca-390b-4e37-8ad9-fad69de0ab59","deps":[],"kwdeps":{},"created_by":null,"output_data":"nested task created","callback_id":"add_nested_task"},{"type":"PythonTask","task_id":"4f08b363-65ab-4e4f-948a-31df70c0820b","deps":[],"kwdeps":{},"created_by":null,"output_data":null,"callback_id":"throw_exception"},{"type":"PythonTask","task_id":"28ac8033-f97f-4ae5-885d-ebe8044f2382","deps":[],"kwdeps":{},"created_by":"862e65ca-390b-4e37-8ad9-fad69de0ab59","output_data":"nested task ran","callback_id":"nested_task"}],"graph_input":null,"output_task":"95c0370b-2488-4882-99a5-61fdc0dda382"}"""
task_graph = TaskGraph.from_json(json.loads(serialized_graph))
output = asyncio.run(task_graph.run(function_registry))

print(output)
assert not nested_task_ran

serialized_2 = json.dumps(task_graph.to_json())
print(serialized_2)