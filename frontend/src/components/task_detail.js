export function TaskDetail({ task }) {
  const type = task ? task["py/object"] : null;
  return (
    <div className="task-detail">
      <div>Task Detail</div>
      {type === "llmtaskgraph.task.LLMTask" ? (
        <LLMTaskDetail task={task} />
      ) : null}
      {type === "llmtaskgraph.task.PythonTask" ? (
        <PythonTaskDetail task={task} />
      ) : null}
    </div>
  );
}

export function LLMTaskDetail({ task }) {
  return (
    <>
      <div>LLM Task</div>
      <div>{task.task_id}</div>
      <div>{task.callback_id}</div>
      <div>{JSON.stringify(task.output_data)}</div>
    </>
  );
}

export function PythonTaskDetail({ task }) {
  return (
    <>
      <div>Python Task</div>
      <div>{task.task_id}</div>
      <div>{task.callback_id}</div>
      <div>{JSON.stringify(task.output_data)}</div>
    </>
  );
}
