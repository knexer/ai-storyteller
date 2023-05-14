import { Handle, Position } from "reactflow";
import "reactflow/dist/style.css";

const handleStyle = { left: 10 };

export function LLMTaskNode({ data }) {
  console.log(data);
  const task = data.task;
  // Deps, kwdeps, and created_by are all handled by edges. The rest, we should display here.

  // TODO: a separate details view should also show the inputs, the formatted prompt, the unparsed model output, and the final output.
  // TODO: styling (rounded rect around the whole thing, with some padding)
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
