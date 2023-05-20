import React from "react";

import { GraphAndDetail } from "./app/graph_and_detail";

const serialized_graph = {
  "tasks": [
    {
      "type": "LLMTask",
      "task_id": "3769a085-1687-4b88-87b8-9683da6816c5",
      "deps": [],
      "kwdeps": {},
      "created_by": null,
      "output_data": [
        "Cheeseburger",
        "Chicken nuggets",
        "French fries",
        "Soft drink",
        "Hot dog"
      ],
      "prompt_formatter_id": "prompt",
      "params": {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1},
      "output_parser_id": "parse_ideas"
    },
    {
      "type": "LLMTask",
      "task_id": "27f6f4df-1c4e-4c50-adfb-0a95081ba565",
      "deps": [],
      "kwdeps": {},
      "created_by": null,
      "output_data": [
        "Big Mac burger from McDonald's ",
        "Whopper sandwich from Burger King ",
        "Chicken sandwich from Chick-fil-A ",
        "Crunchy Taco from Taco Bell ",
        "Classic Roast Beef sandwich from Arby's"
      ],
      "prompt_formatter_id": "prompt",
      "params": {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1},
      "output_parser_id": "parse_ideas"
    },
    {
      "type": "LLMTask",
      "task_id": "59067c3b-3473-478b-9d3b-0e8c5f88f77f",
      "deps": [],
      "kwdeps": {},
      "created_by": null,
      "output_data": ["Hamburger", "Chicken Nuggets", "French Fries", "Pizza", "Tacos"],
      "prompt_formatter_id": "prompt",
      "params": {"model": "gpt-3.5-turbo", "n": 1, "temperature": 1},
      "output_parser_id": "parse_ideas"
    },
    {
      "type": "PythonTask",
      "task_id": "95c0370b-2488-4882-99a5-61fdc0dda382",
      "deps": ["3769a085-1687-4b88-87b8-9683da6816c5", "27f6f4df-1c4e-4c50-adfb-0a95081ba565", "59067c3b-3473-478b-9d3b-0e8c5f88f77f"],
      "kwdeps": {},
      "created_by": null,
      "output_data": [
        "Cheeseburger",
        "Chicken nuggets",
        "French fries",
        "Soft drink",
        "Hot dog",
        "Big Mac burger from McDonald's ",
        "Whopper sandwich from Burger King ",
        "Chicken sandwich from Chick-fil-A ",
        "Crunchy Taco from Taco Bell ",
        "Classic Roast Beef sandwich from Arby's",
        "Hamburger",
        "Chicken Nuggets",
        "French Fries",
        "Pizza",
        "Tacos"
      ],
      "callback_id": "join_ideas"
    },
    {
      "type": "PythonTask",
      "task_id": "862e65ca-390b-4e37-8ad9-fad69de0ab59",
      "deps": [],
      "kwdeps": {},
      "created_by": null,
      "output_data": "nested task created",
      "callback_id": "add_nested_task"
    },
    {
      "type": "PythonTask",
      "task_id": "4f08b363-65ab-4e4f-948a-31df70c0820b",
      "deps": [],
      "kwdeps": {},
      "created_by": null,
      "output_data": null,
      "callback_id": "throw_exception"
    },
    {
      "type": "PythonTask",
      "task_id": "28ac8033-f97f-4ae5-885d-ebe8044f2382",
      "deps": [],
      "kwdeps": {},
      "created_by": "862e65ca-390b-4e37-8ad9-fad69de0ab59",
      "output_data": "nested task ran",
      "callback_id": "nested_task"
    }
  ],
  "graph_input": null,
  "output_task": "95c0370b-2488-4882-99a5-61fdc0dda382"
};

export default function App() {
  return <GraphAndDetail serialized_graph={serialized_graph} />;
}
