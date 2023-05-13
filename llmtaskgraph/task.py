from __future__ import annotations
from abc import ABC, abstractmethod
from asyncio import Future
import asyncio
import inspect
from typing import Any, Optional
from uuid import uuid4
import openai

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llmtaskgraph.task_graph import GraphContext
    from llmtaskgraph.task_graph import TaskGraph


class Task(ABC):
    def __init__(self, *deps: tuple[Task | str], **kwdeps: dict[str, Task | str]):
        self.task_id = str(uuid4())
        self.deps = deps
        self.kwdeps = kwdeps
        self.output: Optional[Future] = None
        self.created_by: Optional[Task] = None

    @property
    def dependencies(self) -> tuple[Task | str]:
        declared_deps = self.deps + tuple(self.kwdeps.values())
        if self.created_by:
            return declared_deps + (self.created_by,)
        else:
            return declared_deps

    def hydrate_deps(self, tasks_by_id: dict[str, Task], created_by: Task):
        self.deps = tuple(tasks_by_id[dep_id] for dep_id in self.deps)
        self.kwdeps = {
            kwdep_name: tasks_by_id[kwdep_id]
            for kwdep_name, kwdep_id in self.kwdeps.items()
        }
        self.created_by = created_by

    async def start(
        self, graph: TaskGraph, function_registry: dict[str, callable]
    ) -> None:
        dep_results = [await dep.output for dep in self.deps]
        kwdep_results = {
            kwdep_name: await kwdep.output for kwdep_name, kwdep in self.kwdeps.items()
        }
        context: GraphContext = graph.make_context_for(self)
        self.output = asyncio.create_task(
            self.execute(context, function_registry, *dep_results, **kwdep_results)
        )

    @abstractmethod
    async def execute(
        self,
        context: GraphContext,
        function_registry: dict[str, callable],
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        pass


class LLMTask(Task):
    def __init__(
        self,
        prompt_formatter_id: str,
        params: Any,
        output_parser_id: str,
        *deps: tuple[Task | str],
        **kwdeps: dict[str, Task | str],
    ):
        super().__init__(*deps, **kwdeps)
        self.prompt_formatter_id = prompt_formatter_id
        self.params = params
        self.output_parser_id = output_parser_id

    async def execute(
        self,
        context: GraphContext,
        function_registry: dict[str, callable],
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        formatted_prompt = function_registry[self.prompt_formatter_id](
            context, *dep_results, **kwdep_results
        )
        response = await self.api_call(formatted_prompt)
        # Todo: retry api call and parsing if output is None
        return function_registry[self.output_parser_id](context, response)

    async def api_call(self, messages):
        # make sure messages is a list of objects with role and content keys
        if not isinstance(messages, list):
            if isinstance(messages, str):
                messages = {"role": "user", "content": messages}
            messages = [messages]

        # Todo: handle api calls elsewhere for request batching and retries
        response = await openai.ChatCompletion.acreate(
            messages=messages,
            **self.params,
        )
        # Todo: handle n > 1
        return response.choices[0].message.content


class PythonTask(Task):
    def __init__(
        self, callback_id, *deps: tuple[Task | str], **kwdeps: dict[str, Task | str]
    ):
        super().__init__(*deps, **kwdeps)
        self.callback_id = callback_id

    async def execute(
        self,
        context: GraphContext,
        function_registry: dict[str, callable],
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        callback = function_registry[self.callback_id]
        if inspect.iscoroutinefunction(callback):
            return await callback(context, *dep_results, **kwdep_results)
        else:
            return callback(context, *dep_results, **kwdep_results)


class TaskGraphTask(Task):
    def __init__(
        self,
        subgraph: "TaskGraph",
        input_formatter_id: str,
        *deps: tuple[Task | str],
        **kwdeps: dict[str, Task | str],
    ):
        super().__init__(*deps, **kwdeps)
        self.subgraph = subgraph
        self.input_formatter_id = input_formatter_id

    async def execute(
        self,
        context: GraphContext,
        function_registry: dict[str, callable],
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        return await self.subgraph.run(
            function_registry,
            function_registry[self.input_formatter_id](
                context, *dep_results, **kwdep_results
            ),
        )
