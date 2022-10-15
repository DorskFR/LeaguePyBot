import asyncio
from asyncio import CancelledError, Task
from typing import Any, Coroutine

from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import Runnable

logger = get_logger(__name__)


class Nursery(Runnable):
    def __init__(self, silenced_errors: tuple[Any, ...] | None = None) -> None:
        super().__init__()
        self._tasks: dict[str, Task[None]] = {}
        self._silenced_errors: tuple[Any, ...] = silenced_errors or tuple()

    def create_task(self, coroutine: Coroutine[Any, Any, None], name: str) -> None:
        """
        Start an asyncio Task only if running, otherwise, ignore.
        """
        if name in self._tasks or not self.is_running:
            coroutine.close()
            return
        task = asyncio.create_task(coroutine, name=name)
        task.add_done_callback(self._done_callback)
        self._tasks[name] = task

    def get_task(self, name: str) -> Task[None] | None:
        return self._tasks[name] if name in self._tasks else None

    def get_task_count(self) -> int:
        return len(list(self._tasks))

    def cleanup_tasks(self, names: set[str]) -> None:
        for name in set(self._tasks) - names:
            self._tasks[name].cancel()

    def _done_callback(self, task: Task[None]) -> None:
        """
        Triggered when a task comes to completion.
        Catches common exceptions and then removes the task from the nursery.
        """
        try:
            task.result()
        except CancelledError:
            pass  # silenced as this is expected
        except self._silenced_errors:
            pass  # silenced as requested
        except Exception as error:  # pylint: disable=broad-except
            logger.error(f"{task.get_name()}: {error}")
        finally:
            del self._tasks[task.get_name()]

    def stop(self) -> None:
        for task in self._tasks.values():
            task.cancel()
        super().stop()
