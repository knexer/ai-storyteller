import asyncio
import openai

import os
from dotenv import load_dotenv
from llmtaskgraph.task import TaskGraphTask
from llmtaskgraph.task_graph import TaskGraph

from pitching.ideation import make_ideas
from pitching.pick_best_idea import pick_best_idea
from pitching.make_premise import make_premise

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create task graphs
overall_graph = make_premise(2)

conditioning_info = "The client is a dog food company. The story should help sell their dog food by manipulating the readers."
best_idea = asyncio.run(overall_graph.run({"conditioning_info": conditioning_info}))
print(best_idea)
