from abc import ABC, abstractmethod
import inspect
from uuid import uuid4
import openai


class Task(ABC):
    def __init__(self, dependencies=None):
        self.task_id = str(uuid4())
        self.dependencies = dependencies or []
        self.output = None
        self.error = None

    async def run(self, dependency_results):
        if self.output is None:
            self.output = await self.execute(dependency_results)
        if self.output is None:
            raise ValueError(f"Task {self.task_id} did not produce an output.")
        return self.output

    @abstractmethod
    async def execute(self, dependency_results):
        pass


class LLMTask(Task):
    def __init__(self, prompt_formatter, params, output_parser, dependencies=None):
        super().__init__(dependencies)
        self.prompt_formatter = prompt_formatter
        self.params = params
        self.output_parser = output_parser

    async def execute(self, dependency_results):
        formatted_prompt = self.prompt_formatter(dependency_results)
        response = await self.api_call(formatted_prompt)
        # Todo: retry api call and parsing if output is None
        return self.output_parser(response)

    async def api_call(self, messages):
        # Todo: handle api calls elsewhere for request batching and retries
        response = await openai.ChatCompletion.acreate(
            messages=messages,
            **self.params,
        )
        return response.choices[0].message.content


class PythonTask(Task):
    def __init__(self, callback, dependencies=None):
        super().__init__(dependencies)
        self.callback = callback

    async def execute(self, dependency_results):
        if inspect.iscoroutinefunction(self.callback):
            return await self.callback(dependency_results)
        else:
            return self.callback(dependency_results)


class TaskGraphTask(Task):
    def __init__(self, subgraph, dependencies=None):
        super().__init__(dependencies)
        self.subgraph = subgraph

    async def execute(self, dependency_results):
        return await self.subgraph.run(dependency_results)
