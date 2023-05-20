export function TaskDetail({ task }) {
  if (task === null) {
    return (<div className="task-detail">
      <div>Task Detail</div>
      No task selected
    </div>);
  }
  const type = task.type;
  return (
    <div className="task-detail">
      <div>Task Detail</div>
      <div>{type}</div>
      <div>State: {task.output_data === null ? "Incomplete" : "Complete"}</div>
      <div>{task.task_id}</div>
      {type === "LLMTask" ? (
        <LLMTaskDetail task={task} />
      ) : null}
      {type === "PythonTask" ? (
        <PythonTaskDetail task={task} />
      ) : null}
      <div>{JSON.stringify(task.output_data)}</div>
    </div>
  );
}

export function LLMTaskDetail({ task }) {
  return (
    <>
      <div>{task.prompt_formatter_id}</div>
      <div>{JSON.stringify(task.params)}</div>
      <div>{task.output_parser_id}</div>
    </>
  );
}

export function PythonTaskDetail({ task }) {
  return (
    <>
      <div>{task.callback_id}</div>
    </>
  );
}
