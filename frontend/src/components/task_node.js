import { Handle, Position } from "reactflow";
import "reactflow/dist/style.css";

export function LLMTaskNode({ data }) {
  const task = data.task;
  const direction = data.direction;
  const isHorizontal = direction === "LR";
  const handleStyle = isHorizontal ? { top: 10 } : { left: 10 };
  // Show the basic task info. Connectivity info is shown by edges. The details view will show the rest.
  return (
    <>
      <Handle
        type="target"
        position={isHorizontal ? Position.Left : Position.Top}
      />
      <div className="react-flow__node-default custom-node">
        <div>LLM Task</div>
        <div>{task.prompt_formatter_id}</div>
        <div>{task.output_parser_id}</div>
      </div>
      <Handle
        type="source"
        position={isHorizontal ? Position.Right : Position.Bottom}
        id="output"
      />
      <Handle
        type="source"
        position={isHorizontal ? Position.Right : Position.Bottom}
        id="task creation"
        style={handleStyle}
      />
    </>
  );
}

export function PythonTaskNode({ data }) {
  const task = data.task;
  const direction = data.direction;
  const isHorizontal = direction === "LR";
  const handleStyle = isHorizontal ? { top: 10 } : { left: 10 };
  // Show the basic task info. Connectivity info is shown by edges. The details view will show the rest.
  return (
    <>
      <Handle
        type="target"
        position={isHorizontal ? Position.Left : Position.Top}
      />
      <div className="react-flow__node-default custom-node">
        <div>Python Task</div>
        <div>{task.callback_id}</div>
      </div>
      <Handle
        type="source"
        position={isHorizontal ? Position.Right : Position.Bottom}
        id="output"
      />
      <Handle
        type="source"
        position={isHorizontal ? Position.Right : Position.Bottom}
        id="task creation"
        style={handleStyle}
      />
    </>
  );
}
