import asyncio
import json
import openai

import os
from dotenv import load_dotenv
from llmtaskgraph.task import TaskGraphTask
from llmtaskgraph.task_graph import TaskGraph

from pitching.make_premise import make_premise, function_registry

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create task graphs
overall_graph = make_premise(2)

conditioning_info = "The client is a dog food company. The story should help sell their dog food by manipulating the readers."
print("Graph constructed:")
print(json.dumps(overall_graph.to_json()))
overall_graph_2 = TaskGraph.from_json(overall_graph.to_json())
best_idea = asyncio.run(overall_graph_2.run(function_registry(), {"conditioning_info": conditioning_info}))
print(best_idea)
print(json.dumps(overall_graph_2.to_json()))
