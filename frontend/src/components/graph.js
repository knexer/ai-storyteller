import React from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from "reactflow";
import dagre from "dagre";

import { TaskNode } from "./task_node";

import "reactflow/dist/style.css";

function makeNode(task, direction) {
  return {
    id: task.task_id,
    type: "Task",
    data: { task: task, direction: direction },
  };
}

function makeEdge(task, dep_task_id, tasks, sourceHandle = "output") {
  const dep_task = tasks.find((t) => t.task_id === dep_task_id);
  const edge = {
    id: `${task.task_id}-${dep_task.task_id}`,
    source: dep_task.task_id,
    target: task.task_id,
    sourceHandle: sourceHandle,
  };
  return edge;
}

function makeEdges(task, tasks) {
  const deps = task.deps.map((dep) =>
    makeEdge(task, dep, tasks)
  );
  const kwdeps = Object.values(task.kwdeps).map((dep) =>
    makeEdge(task, dep, tasks)
  );
  const created_by = task.created_by
    ? [makeEdge(task, task.created_by, tasks, "task creation")]
    : [];
  return deps.concat(kwdeps).concat(created_by);
}

const nodeTypes = {
  "Task": TaskNode,
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
  const direction = "TB"; // TB or LR

  const initialNodes = serialized_graph.tasks.map((task) =>
    makeNode(task, direction)
  );
  const initialEdges = serialized_graph.tasks.flatMap((task) =>
    makeEdges(task, serialized_graph.tasks)
  );

  const graph = getLayoutedElements(initialNodes, initialEdges, direction);

  const [nodes] = useNodesState(graph.nodes);
  const [edges] = useEdgesState(graph.edges);

  const onNodeClick = (_, node) => {
    // Possibly also somehow highlight the selected node?
    // Possibly also highlight related nodes?
    select_task(node.data.task);
  };

  const onPaneClick = (_) => {
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
