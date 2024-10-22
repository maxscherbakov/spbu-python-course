from typing import Callable, Any
from threading import Thread, Condition


class TaskWrapper:
    """
    Wrapper class above the function to store the result and mark the execution.

    Methods:
    -------
    `__call__() -> None`:
        Performs the launch of the function.

    `set_args(*args: Any) -> None`:
        Sets variables for the function.

    `get_res() -> List[List[float]]`:
        Returns a function result.
    """

    args: tuple[Any, ...] = ()

    def __init__(self, func: Callable[..., Any]) -> None:
        """
        Initializes a TaskWrapper object.

        Args:
            func (Callable[..., Any]): the task that needs to be wrapped.
        """
        self._func = func
        self._result = None
        self._done = False

    def set_args(self, *args: Any) -> None:
        """
        Sets the arguments for the function.

        Args:
            args (Any): the arguments with which the function should be started
        """
        self.args = args

    def __call__(self) -> None:
        """Calling a function, saving the result, and marking the execution."""
        if len(self.args) > 0:
            self._result = self._func(*self.args)
        else:
            self._result = self._func()
        self._done = True

    def get_res(self) -> Any:
        """
        Waits for the execution of the function and returns the result.

        Returns:
            result (Any): function result.
        """
        while not self._done:
            pass
        return self._result


class ThreadPool:
    """
    A class for running multiple threads.  Accepts tasks and distributes them across threads.

    Methods:
    -------
    `enqueue(task: Callable[..., Any], *args: Any) -> TaskWrapper`:
        Adds a task to the queue.

    `thread_run(self) -> None`:
        Starts the thread.

    `dispose(self) -> None`:
        Prohibits accepting new tasks, waits for existing ones to be completed, and terminates threads.
    """

    def __init__(self, num_threads: int = 1) -> None:
        """
        Initializes a ThreadPool object.

        Args:
            num_threads (int): number of threads.
        """
        if num_threads <= 0:
            raise ValueError("The number of threads must be greater than 0")
        self.num_threads = num_threads
        self._task_queue: list[TaskWrapper] = []
        self._threads = []
        self._running = True
        self._condition = Condition()

        for _ in range(num_threads):
            thread = Thread(target=self.thread_run)
            thread.start()
            self._threads.append(thread)

    def enqueue(self, task: Callable[..., Any], *args: Any) -> TaskWrapper:
        """
        Wraps the task, sets the arguments, and adds them to the queue.

        Args:
            task (Callable[..., Any]): the task that needs to be added to the queue.
            args (Any):
        """
        with self._condition:
            if not self._running:
                raise TypeError("The thread pool has been dispose")
            task_wrap = TaskWrapper(task)
            task_wrap.set_args(*args)
            self._task_queue.append(task_wrap)
            self._condition.notify()
            return task_wrap

    def thread_run(self) -> None:
        """
        Starts the stream. Waits until the tasks appear.
        If there are no tasks and the dispose method is called,
        it executes tasks from the queue and terminates.
        """
        while True:
            with self._condition:
                self._condition.wait_for(
                    lambda: self._task_queue or not self._running
                )
                if not len(self._task_queue) and self._running:
                    continue
                if not len(self._task_queue) and not self._running:
                    break
                task = self._task_queue.pop(0)
            task()

    def dispose(self) -> None:
        """Finishes accepting tasks and ends threads."""
        with self._condition:
            self._running = False
            self._condition.notify_all()
        for i, thread in enumerate(self._threads):
            thread.join()
