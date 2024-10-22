from threading import Thread, Condition
import queue
from time import sleep


class TaskWrapper:
    def __init__(self, func):
        self.func = func
        self.result = None
        self.done = False

    def __call__(self):
        self.result = self.func()
        self.done = True

    def get_res(self):
        while not self.done:
            pass
        return self.result


class ThreadPool:
    def __init__(self, num_threads=1):
        self.num_threads = num_threads
        self.task_queue = queue.Queue()
        self.threads = []
        self.running = True
        self.cv = Condition()

        for _ in range(num_threads):
            thread = Thread(target=self.thread_run)
            thread.start()
            self.threads.append(thread)

    def enqueue(self, task):
        task_wrap = TaskWrapper(task)
        self.task_queue.put(task_wrap)
        return task_wrap

    def thread_run(self):
        while True:
            with self.cv:
                self.cv.wait_for(
                    lambda: self.task_queue.not_empty or not self.running
                )
                if self.task_queue.empty() and self.running:
                    continue
                elif self.task_queue.empty() and not self.running:
                    break
                elif self.task_queue.not_empty:
                    task = self.task_queue.get()
            task()
            self.task_queue.task_done()

    def dispose(self):
        self.running = False
        self.task_queue.join()
        for i, thread in enumerate(self.threads):
            thread.join()
