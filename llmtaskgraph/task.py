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
    from llmtaskgraph.task_graph import TaskGraph


class Task(ABC):
    def __init__(self, *deps: tuple[Task], **kwdeps: dict[str, Task]):
        self.task_id = str(uuid4())
        self.deps = deps
        self.kwdeps = kwdeps
        self.output: Optional[Future] = None

    @property
    def dependencies(self) -> tuple[Task]:
        return self.deps + tuple(self.kwdeps.values())

    async def start(self, graph_input: Any) -> None:
        dep_results = [await dep.output for dep in self.deps]
        kwdep_results = {
            kwdep_name: await kwdep.output for kwdep_name, kwdep in self.kwdeps.items()
        }
        self.output = asyncio.create_task(
            self.execute(graph_input, *dep_results, **kwdep_results)
        )

    @abstractmethod
    async def execute(
        self,
        graph_input: Any,
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        pass


class LLMTask(Task):
    def __init__(
        self,
        prompt_formatter: callable,
        params: Any,
        output_parser: callable[[str], Any],
        *deps: tuple[Task],
        **kwdeps: dict[str, Task],
    ):
        super().__init__(*deps, **kwdeps)
        self.prompt_formatter = prompt_formatter
        self.params = params
        self.output_parser = output_parser

    async def execute(
        self,
        graph_input: Any,
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        formatted_prompt = self.prompt_formatter(
            graph_input, *dep_results, **kwdep_results
        )
        response = await self.api_call(formatted_prompt)
        # Todo: retry api call and parsing if output is None
        return self.output_parser(response)

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
    def __init__(self, callback, *deps: tuple[Task], **kwdeps: dict[str, Task]):
        super().__init__(*deps, **kwdeps)
        self.callback = callback

    async def execute(
        self,
        graph_input: Any,
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        if inspect.iscoroutinefunction(self.callback):
            return await self.callback(graph_input, *dep_results, **kwdep_results)
        else:
            return self.callback(graph_input, *dep_results, **kwdep_results)


class TaskGraphTask(Task):
    def __init__(
        self,
        subgraph: "TaskGraph",
        input_formatter: callable,
        *deps: tuple[Task],
        **kwdeps: dict[str, Task],
    ):
        super().__init__(*deps, **kwdeps)
        self.subgraph = subgraph
        self.input_formatter = input_formatter

    async def execute(
        self,
        graph_input: Any,
        *dep_results: tuple[Any],
        **kwdep_results: dict[str, Any],
    ):
        return await self.subgraph.run(
            self.input_formatter(graph_input, *dep_results, **kwdep_results)
        )
