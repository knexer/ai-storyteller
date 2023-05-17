import { useState } from "react";

import Graph from "../components/graph";
import { TaskDetail } from "../components/task_detail";

export function GraphAndDetail({ serialized_graph }) {
  const [selected_task, update_selected_task] = useState(null);

  return (
    <div className={"graph-and-detail"}>
      <Graph
        serialized_graph={serialized_graph}
        select_task={update_selected_task}
      />
      <TaskDetail serialized_graph={serialized_graph} task={selected_task} />
    </div>
  );
}
