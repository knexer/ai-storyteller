import asyncio
import json
import openai

import os
from dotenv import load_dotenv
from example_app.backend.server import WebSocketServer

from pitching.make_premise import make_premise, function_registry

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create task graphs
overall_graph = make_premise(2)
graph_input = {"conditioning_info": "The client is a dog food company. The story should help sell their dog food by manipulating the readers."}

server = WebSocketServer(overall_graph, function_registry(), graph_input)
print("Created server.")
server.run()
