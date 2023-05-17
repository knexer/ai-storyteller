import { Handle, Position } from "reactflow";
import "reactflow/dist/style.css";

const handleStyle = { left: 10 };

export function LLMTaskNode({ data }) {
  const task = data.task;
  // Show the basic task info. Connectivity info is shown by edges. The details view will show the rest.
  return (
    <>
      <Handle type="target" position={Position.Top} />
      <div className="react-flow__node-default custom-node">
        <div>LLM Task</div>
        <div>{task.task_id}</div>
        <div>{task.prompt_formatter_id}</div>
        <div>{JSON.stringify(task.params)}</div>
        <div>{task.output_parser_id}</div>
      </div>
      <Handle type="source" position={Position.Bottom} id="output" />
      <Handle
        type="source"
        position={Position.Bottom}
        id="task creation"
        style={handleStyle}
      />
    </>
  );
}

export function PythonTaskNode({ data }) {
  const task = data.task;
  // Show the basic task info. Connectivity info is shown by edges. The details view will show the rest.
  return (
    <>
      <Handle type="target" position={Position.Top} />
      <div className="react-flow__node-default custom-node">
        <div>Python Task</div>
        <div>{task.task_id}</div>
        <div>{task.callback_id}</div>
      </div>
      <Handle type="source" position={Position.Bottom} id="output" />
      <Handle
        type="source"
        position={Position.Bottom}
        id="task creation"
        style={handleStyle}
      />
    </>
  );
}
