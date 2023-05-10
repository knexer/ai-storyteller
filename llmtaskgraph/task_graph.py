import asyncio
from typing import Any, Optional

from llmtaskgraph.task import Task


class TaskGraph:
    def __init__(self):
        self.tasks = []
        self.started = False
        self.graph_input: Optional[Any] = None
        self.output_task: Optional[Task] = None
        self.function_registry: dict[str, callable] = None

    def add_task(self, task: Task):
        for dependency in task.dependencies:
            if dependency not in self.tasks:
                raise ValueError(f"Dependency {dependency} not found in task graph")

        self.tasks.append(task)
        if self.started:
            asyncio.create_task(task.start(self.graph_input, self.function_registry))

        return task.task_id

    def add_output_task(self, task: Task):
        self.add_task(task)
        self.output_task = task
        return task.task_id

    async def run(
        self, function_registry: dict[str, callable], graph_input: Optional[Any] = None
    ) -> Any:
        self.started = True
        self.graph_input = graph_input
        self.function_registry = function_registry
        # Start all initially available tasks.
        # N.B.: Tasks added during execution will be started by add_task.
        for task in self.tasks:
            asyncio.create_task(task.start(graph_input, function_registry))
        # Let tasks start so we have something to wait for below.
        await asyncio.sleep(0)

        # while any task is not started or not done
        while any(task.output is None or not task.output.done() for task in self.tasks):
            # wait for every started task to be done
            await asyncio.wait(
                [task.output for task in self.tasks if task.output is not None]
            )

        self.function_registry = None
        return await self.output_task.output if self.output_task else None
