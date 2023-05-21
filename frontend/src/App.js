import React, { useState } from "react";

import { GraphAndDetail } from "./app/graph_and_detail";

const original_graph = {
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

const original_graph2 = {
  "tasks": [
    {
      "type": "TaskGraphTask",
      "task_id": "b55bccc7-a1de-41fa-bb99-7e0b7079569d",
      "deps": [],
      "kwdeps": {},
      "created_by": null,
      "output_data": null,
      "subgraph": {
        "tasks": [
          {
            "type": "LLMTask",
            "task_id": "ea6e3bba-4fde-43f4-8856-10ff8bebac3a",
            "deps": [],
            "kwdeps": {},
            "created_by": null,
            "output_data": null,
            "prompt_formatter_id": "make_eight_ideas",
            "params": {
              "model": "gpt-3.5-turbo",
              "n": 1,
              "temperature": 1
            },
            "output_parser_id": "parse_ideas"
          },
          {
            "type": "LLMTask",
            "task_id": "8b522d8d-12a8-47dd-9475-6ac56cd7ece1",
            "deps": [],
            "kwdeps": {},
            "created_by": null,
            "output_data": null,
            "prompt_formatter_id": "make_eight_ideas",
            "params": {
              "model": "gpt-3.5-turbo",
              "n": 1,
              "temperature": 1
            },
            "output_parser_id": "parse_ideas"
          },
          {
            "type": "PythonTask",
            "task_id": "f8d5e7cd-7387-4add-9d3b-e95eb9ec9ba0",
            "deps": [
              "ea6e3bba-4fde-43f4-8856-10ff8bebac3a",
              "8b522d8d-12a8-47dd-9475-6ac56cd7ece1"
            ],
            "kwdeps": {},
            "created_by": null,
            "output_data": null,
            "callback_id": "join_ideas"
          }
        ],
        "graph_input": null,
        "output_task": "f8d5e7cd-7387-4add-9d3b-e95eb9ec9ba0"
      },
      "input_formatter_id": "forward_graph_input"
    },
    {
      "type": "TaskGraphTask",
      "task_id": "d216a6a1-a864-4102-9fe6-492b6b310330",
      "deps": [
        "b55bccc7-a1de-41fa-bb99-7e0b7079569d"
      ],
      "kwdeps": {},
      "created_by": null,
      "output_data": null,
      "subgraph": {
        "tasks": [
          {
            "type": "TaskGraphTask",
            "task_id": "d414edd0-9f6e-4c59-87fe-f8feb1b3d660",
            "deps": [],
            "kwdeps": {},
            "created_by": null,
            "output_data": null,
            "subgraph": {
              "tasks": [
                {
                  "type": "LLMTask",
                  "task_id": "bd92c7b0-dc62-43c5-8b15-84037ee5ae9e",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "a4b59326-c08f-44ae-854f-09571f573556",
                  "deps": [
                    "bd92c7b0-dc62-43c5-8b15-84037ee5ae9e"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "90ac5d9c-53a2-413e-8e55-768c4aba9dbd",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "3396f601-f7f5-49a8-990b-3873b2fd60d1",
                  "deps": [
                    "90ac5d9c-53a2-413e-8e55-768c4aba9dbd"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "eb1be7cc-811d-4982-8813-2cad77e54994",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "6d3b8fb4-9e23-4bcd-994e-f0b8079f7076",
                  "deps": [
                    "eb1be7cc-811d-4982-8813-2cad77e54994"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "37ec4c58-6abf-4603-87dc-14acfec32c77",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "c6d0db42-849d-46d1-bc97-ca3b3a789fd2",
                  "deps": [
                    "37ec4c58-6abf-4603-87dc-14acfec32c77"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "PythonTask",
                  "task_id": "cc69160f-2a55-4bc1-8e5c-3224dacb37d3",
                  "deps": [
                    "a4b59326-c08f-44ae-854f-09571f573556",
                    "3396f601-f7f5-49a8-990b-3873b2fd60d1",
                    "6d3b8fb4-9e23-4bcd-994e-f0b8079f7076",
                    "c6d0db42-849d-46d1-bc97-ca3b3a789fd2"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "callback_id": "tally_votes"
                }
              ],
              "graph_input": null,
              "output_task": "cc69160f-2a55-4bc1-8e5c-3224dacb37d3"
            },
            "input_formatter_id": "init_most_creative"
          },
          {
            "type": "TaskGraphTask",
            "task_id": "24b0428e-ec7c-45d1-ade9-a4be170cd459",
            "deps": [],
            "kwdeps": {},
            "created_by": null,
            "output_data": null,
            "subgraph": {
              "tasks": [
                {
                  "type": "LLMTask",
                  "task_id": "a8fdb25c-dcbc-490f-be62-fcd44f63b66c",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "c6d727f1-107d-40b4-89ff-376aa47b67c6",
                  "deps": [
                    "a8fdb25c-dcbc-490f-be62-fcd44f63b66c"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "9e1d684a-3330-465b-aaa2-b2afcf373157",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "a1c37400-54b5-499a-b1a8-0320f3dd06c7",
                  "deps": [
                    "9e1d684a-3330-465b-aaa2-b2afcf373157"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "29f259f9-2d98-4343-b128-a6e9672ac582",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "1cbe2daa-d270-4432-ae26-0695e894bf6b",
                  "deps": [
                    "29f259f9-2d98-4343-b128-a6e9672ac582"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "5fc65d0f-2a0f-4f28-ab93-35b2bbf7a18f",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "568ef6ff-29c1-4d20-8781-f8e11298f233",
                  "deps": [
                    "5fc65d0f-2a0f-4f28-ab93-35b2bbf7a18f"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "PythonTask",
                  "task_id": "d3fe7c8c-734e-40be-9c73-a895296706e7",
                  "deps": [
                    "c6d727f1-107d-40b4-89ff-376aa47b67c6",
                    "a1c37400-54b5-499a-b1a8-0320f3dd06c7",
                    "1cbe2daa-d270-4432-ae26-0695e894bf6b",
                    "568ef6ff-29c1-4d20-8781-f8e11298f233"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "callback_id": "tally_votes"
                }
              ],
              "graph_input": null,
              "output_task": "d3fe7c8c-734e-40be-9c73-a895296706e7"
            },
            "input_formatter_id": "init_best_fit"
          },
          {
            "type": "TaskGraphTask",
            "task_id": "49b801ec-0107-4459-98e5-8609f97847c4",
            "deps": [],
            "kwdeps": {},
            "created_by": null,
            "output_data": null,
            "subgraph": {
              "tasks": [
                {
                  "type": "LLMTask",
                  "task_id": "89f8b087-0e80-4ee8-aeb8-d4f9df570506",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "9dd3687a-1a9c-4e49-a589-99661cf27c2a",
                  "deps": [
                    "89f8b087-0e80-4ee8-aeb8-d4f9df570506"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "3393ea9a-892e-44ea-9e3f-c86ac4ae7f4c",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "0f6a014d-d351-412f-8161-025d237f1717",
                  "deps": [
                    "3393ea9a-892e-44ea-9e3f-c86ac4ae7f4c"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "a7ee9a1e-b276-4b3a-ac73-b1d5ce89f900",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "b489181e-22de-4c7f-88c7-dfe2f83d626f",
                  "deps": [
                    "a7ee9a1e-b276-4b3a-ac73-b1d5ce89f900"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "LLMTask",
                  "task_id": "d82e50cd-e68c-42bd-88a0-616d6d5d1abd",
                  "deps": [],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "pick_top_five",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 1
                  },
                  "output_parser_id": "identity"
                },
                {
                  "type": "LLMTask",
                  "task_id": "d120e020-65db-4d6a-aac7-da728086231c",
                  "deps": [
                    "d82e50cd-e68c-42bd-88a0-616d6d5d1abd"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "prompt_formatter_id": "extract_titles",
                  "params": {
                    "model": "gpt-3.5-turbo",
                    "n": 1,
                    "temperature": 0
                  },
                  "output_parser_id": "parse_json"
                },
                {
                  "type": "PythonTask",
                  "task_id": "049023cf-8792-41ec-b50e-3a8e84452882",
                  "deps": [
                    "9dd3687a-1a9c-4e49-a589-99661cf27c2a",
                    "0f6a014d-d351-412f-8161-025d237f1717",
                    "b489181e-22de-4c7f-88c7-dfe2f83d626f",
                    "d120e020-65db-4d6a-aac7-da728086231c"
                  ],
                  "kwdeps": {},
                  "created_by": null,
                  "output_data": null,
                  "callback_id": "tally_votes"
                }
              ],
              "graph_input": null,
              "output_task": "049023cf-8792-41ec-b50e-3a8e84452882"
            },
            "input_formatter_id": "init_cutest"
          },
          {
            "type": "PythonTask",
            "task_id": "215d4fcd-3d0f-4bb8-b83a-2e62f504a3eb",
            "deps": [
              "d414edd0-9f6e-4c59-87fe-f8feb1b3d660",
              "24b0428e-ec7c-45d1-ade9-a4be170cd459",
              "49b801ec-0107-4459-98e5-8609f97847c4"
            ],
            "kwdeps": {},
            "created_by": null,
            "output_data": null,
            "callback_id": "weighted_sum"
          }
        ],
        "graph_input": null,
        "output_task": "215d4fcd-3d0f-4bb8-b83a-2e62f504a3eb"
      },
      "input_formatter_id": "init_pick_best"
    }
  ],
  "graph_input": null,
  "output_task": "d216a6a1-a864-4102-9fe6-492b6b310330"
};

export default function App() {
  const [serialized_graph, setSerializedGraph] = useState(original_graph2);

  const handleEdit = (task_id, output_data) => {
    // Deep copy the serialized graph
    const new_graph = JSON.parse(JSON.stringify(serialized_graph));

    // Find the task
    const task = new_graph.tasks.find((task) => task.task_id === task_id);
    if (!task) return;

    // Update the output_data
    task.output_data = output_data;

    // Update the state
    setSerializedGraph(new_graph);
  };

  return (
    <div className="app">
      <button onClick={() => setSerializedGraph(original_graph2)}>Reset</button>
      <button onClick={() => navigator.clipboard.writeText(JSON.stringify(serialized_graph))}>Copy to clipboard</button>
      <GraphAndDetail serialized_graph={serialized_graph} onEdit={handleEdit} />
    </div>
  );
}
