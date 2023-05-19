import React from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from "reactflow";
import dagre from "dagre";

import getObjectsInOrder from "./jsonpickle_helper";
import { LLMTaskNode, PythonTaskNode } from "./task_node";

import "reactflow/dist/style.css";

function makeNode(task, direction) {
  if (task["py/object"] === "llmtaskgraph.task.LLMTask") {
    return {
      id: task.task_id,
      type: "llmtaskgraph.task.LLMTask",
      data: { task: task, direction: direction },
    };
  }

  if (task["py/object"] === "llmtaskgraph.task.PythonTask") {
    return {
      id: task.task_id,
      type: "llmtaskgraph.task.PythonTask",
      data: { task: task, direction: direction },
    };
  }

  return {
    id: task.task_id,
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

function getLayoutedElements(nodes, edges, direction = "TB") {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  // TODO: get node width and height from nodes instead of hardcoding
  const nodeWidth = 172;
  const nodeHeight = 100;

  const isHorizontal = direction === "LR";
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  nodes.forEach((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    node.targetPosition = isHorizontal ? "left" : "top";
    node.sourcePosition = isHorizontal ? "right" : "bottom";

    // We are shifting the dagre node position (anchor=center center) to the top left
    // so it matches the React Flow node anchor point (top left).
    node.position = {
      x: nodeWithPosition.x - nodeWithPosition.width / 2,
      y: nodeWithPosition.y - nodeWithPosition.height / 2,
    };

    return node;
  });

  return { nodes, edges, width: dagreGraph.width, height: dagreGraph.height };
}

export default function Graph({ serialized_graph, select_task }) {
  // Create nodes from serialized graph
  const objects_by_py_id = getObjectsInOrder(serialized_graph);
  const direction = "TB"; // TB or LR

  const initialNodes = serialized_graph.tasks.map((task) =>
    makeNode(task, direction)
  );
  const initialEdges = serialized_graph.tasks.flatMap((task) =>
    makeEdges(task, objects_by_py_id)
  );

  const graph = getLayoutedElements(initialNodes, initialEdges, direction);

  const [nodes, setNodes, onNodesChange] = useNodesState(graph.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(graph.edges);

  const onNodeClick = (event, node) => {
    // Possibly also somehow highlight the selected node?
    // Possibly also highlight related nodes?
    select_task(node.data.task);
  };

  const onPaneClick = (event) => {
    select_task(null);
  };

  return (
    <div className="graph">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        elementsSelectable={true}
        fitView={true}
        fitViewOptions={{ padding: 0.1 }}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
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
// - allow editing of task - change outputs, invalidate the task, etc. - producing an updated serialized graph
// subgraph support for TaskGraphTask
