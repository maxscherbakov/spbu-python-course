from queue import Queue
from typing import Callable, Any
from threading import Thread, Condition


class TaskWrapper:
    def __init__(self, func: Callable[[], Any]) -> None:
        self._func = func
        self._result = None
        self._done = False

    def __call__(self) -> None:
        self._result = self._func()
        self._done = True

    def get_res(self) -> Any:
        while not self._done:
            pass
        return self._result


class ThreadPool:
    def __init__(self, num_threads: int = 1) -> None:
        if num_threads <= 0:
            raise TypeError("The number of threads must be greater than 0")
        self.num_threads = num_threads
        self._task_queue: Queue[TaskWrapper] = Queue()
        self._threads = []
        self._running = True
        self._cv = Condition()

        for _ in range(num_threads):
            thread = Thread(target=self.thread_run)
            thread.start()
            self._threads.append(thread)

    def enqueue(self, task: Callable[[], Any]) -> TaskWrapper:
        task_wrap = TaskWrapper(task)
        self._task_queue.put(task_wrap)
        return task_wrap

    def thread_run(self) -> None:
        while True:
            with self._cv:
                self._cv.wait_for(
                    lambda: self._task_queue.not_empty or not self._running
                )
                if self._task_queue.empty() and self._running:
                    continue
                elif self._task_queue.empty() and not self._running:
                    break
                elif self._task_queue.not_empty:
                    task = self._task_queue.get()
            task()
            self._task_queue.task_done()

    def dispose(self) -> None:
        self._running = False
        self._task_queue.join()
        for i, thread in enumerate(self._threads):
            thread.join()
