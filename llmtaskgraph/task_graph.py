import asyncio
import traceback


class TaskGraph:
    def __init__(self):
        self.tasks = {}
        self.output_task = None

    def add_task(self, task):
        for dependency in task.dependencies:
            if dependency not in self.tasks:
                raise ValueError(f"Dependency {dependency} not found in task graph")

        self.tasks[task.task_id] = task
        return task.task_id

    def add_output_task(self, task):
        task_id = self.add_task(task)

        self.output_task = task_id

    async def run(self, input=None):
        running_tasks = set()
        task_coros = []
        task_finished = asyncio.Event()

        async def execute_task(task):
            task_input = {dep: self.tasks[dep].output for dep in task.dependencies}
            if input is not None:
                task_input["global"] = input

            try:
                await task.run(task_input)
            except Exception as e:
                # Mark the task as errored so that we can cancel the other tasks in run()
                task.error = e
            finally:
                running_tasks.discard(task)
                task_finished.set()

        try:
            while any([task.output is None for task in self.tasks.values()]) and all(
                [task.error is None for task in self.tasks.values()]
            ):
                new_tasks = [
                    task
                    for task in self.tasks.values()
                    if not task in running_tasks
                    if all(
                        self.tasks[dep].output is not None for dep in task.dependencies
                    )
                ]

                for task in new_tasks:
                    coro = asyncio.create_task(execute_task(task))
                    task_coros.append(coro)
                    running_tasks.add(task)

                await task_finished.wait()
                task_finished.clear()

            errors = [
                task.error for task in self.tasks.values() if task.error is not None
            ]
            if len(errors) > 0:
                # Cancel running coroutines
                for coro in task_coros:
                    coro.cancel()

                # Wait for coroutines to complete cancellation
                await asyncio.gather(*task_coros, return_exceptions=True)

                def format_error(error):
                    return "".join(
                        traceback.format_exception(
                            type(error), error, error.__traceback__
                        )
                    )

                raise Exception(
                    "\n".join(
                        ["Some tasks in the TaskGraph encountered errors: "]
                        + ["".join(format_error(error)) for error in errors],
                    )
                )

            return self.tasks[self.output_task].output

        except asyncio.CancelledError:
            for coro in task_coros:
                coro.cancel()
            raise
