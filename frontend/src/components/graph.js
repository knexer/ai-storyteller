import React from "react";
import ReactFlow, { MiniMap, Controls, Background } from "reactflow";

import getObjectsInOrder from "./jsonpickle_helper";
import { LLMTaskNode, PythonTaskNode } from "./task_node";

import "reactflow/dist/style.css";

function makeNode(task, y) {
  const random_x = Math.random() * 1000;
  if (task["py/object"] === "llmtaskgraph.task.LLMTask") {
    return {
      id: task.task_id,
      type: "llmtaskgraph.task.LLMTask",
      position: { x: random_x, y: y * 100 },
      data: { task: task },
    };
  }

  if (task["py/object"] === "llmtaskgraph.task.PythonTask") {
    return {
      id: task.task_id,
      type: "llmtaskgraph.task.PythonTask",
      position: { x: random_x, y: y * 100 },
      data: { task: task },
    };
  }

  return {
    id: task.task_id,
    position: { x: random_x, y: y * 100 },
    data: { label: task["py/object"] },
  };
}

function makeEdge(task, dep, objects_by_py_id, sourceHandle = "output") {
  const dep_task = objects_by_py_id[dep["py/id"]];
  const edge = {
    id: `${task.task_id}-${dep_task.task_id}`,
    source: dep_task.task_id,
    target: task.task_id,
    sourceHandle: sourceHandle,
  };
  return edge;
}

function makeEdges(task, objects_by_py_id) {
  const deps = task.deps["py/tuple"].map((dep) =>
    makeEdge(task, dep, objects_by_py_id)
  );
  const kwdeps = Object.values(task.kwdeps).map((dep) =>
    makeEdge(task, dep, objects_by_py_id)
  );
  const created_by = task.created_by
    ? [makeEdge(task, task.created_by, objects_by_py_id, "task creation")]
    : [];
  return deps.concat(kwdeps).concat(created_by);
}

const nodeTypes = {
  "llmtaskgraph.task.LLMTask": LLMTaskNode,
  "llmtaskgraph.task.PythonTask": PythonTaskNode,
};

export default function Graph({ serialized_graph }) {
  const objects_by_py_id = getObjectsInOrder(serialized_graph);

  let starting_y = 0;
  // Create nodes from serialized graph
  const initialNodes = serialized_graph.tasks.map((task) =>
    makeNode(task, starting_y++)
  );

  const initialEdges = serialized_graph.tasks.flatMap((task) =>
    makeEdges(task, objects_by_py_id)
  );

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
        nodeTypes={nodeTypes}
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}

// TODO:
// styling: show task state visually - with color?
// add node selection:
// - refocus the graph around the selected node?
// - show the task details in a panel
// - allow editing of task - change outputs, invalidate the task, etc. - producing an updated serialized graph
// custom class for node?
// subgraph support for TaskGraphTask
