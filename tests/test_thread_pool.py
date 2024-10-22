from time import sleep
from threading import Thread

from project.thread_pool_with_queue import ThreadPool, TaskWrapper


def test_future_result() -> None:
    """Test that Future correctly sets and awaits a result."""

    def set_five() -> int:
        return 5

    task = TaskWrapper(set_five)

    t = Thread(target=task)
    t.start()
    t.join()

    # Await the result
    assert task.get_res() == 5


def test_enqueue_task() -> None:
    """Test that tasks are correctly enqueued and processed."""
    pool = ThreadPool(num_threads=2)

    def sample_task() -> str:
        return "Task completed"

    task = pool.enqueue(sample_task)

    # Await the task completion and check the result
    result = task.get_res()
    assert result == "Task completed"

    # Clean up thread pool
    pool.dispose()


def test_enqueue_multiple_tasks() -> None:
    """Test that multiple tasks are correctly processed by the thread pool."""
    pool = ThreadPool(num_threads=3)

    def task1() -> str:
        return "Task 1 completed"

    def task2() -> str:
        return "Task 2 completed"

    task_1 = pool.enqueue(task1)
    task_2 = pool.enqueue(task2)

    result1 = task_1.get_res()
    result2 = task_2.get_res()

    assert result1 == "Task 1 completed"
    assert result2 == "Task 2 completed"

    # Clean up thread pool
    pool.dispose()


def test_ordered_execution_with_one_threads() -> None:
    """Test that tasks are executed in the order they were enqueued."""
    pool = ThreadPool(num_threads=1)  # Single thread to ensure order

    results = []

    def task1() -> int:
        results.append(1)
        return 1

    def task2() -> int:
        results.append(2)
        return 2

    task_1 = pool.enqueue(task1)
    task_2 = pool.enqueue(task2)

    # Wait for tasks to complete
    task_1.get_res()
    task_2.get_res()

    # Ensure the tasks were executed in order
    assert results == [1, 2]

    # Clean up thread pool
    pool.dispose()


def test_ordered_execution_with_multiple_threads() -> None:
    pool = ThreadPool(num_threads=2)

    results = []

    def task1() -> None:
        results.append(1)

    def task2() -> None:
        sleep(1)
        results.append(2)

    def task3() -> None:
        results.append(3)

    t1 = pool.enqueue(task1)
    t2 = pool.enqueue(task2)
    t3 = pool.enqueue(task3)

    # Wait for tasks to complete
    t1.get_res()
    t2.get_res()
    t3.get_res()

    assert results == [1, 3, 2]

    pool.dispose()


def test_dispose_not_terminate_execution() -> None:
    pool = ThreadPool(num_threads=2)

    tasks = []

    def task1() -> int:
        sleep(1)
        return 1

    def task2() -> int:
        sleep(2)
        return 2

    tasks.append(pool.enqueue(task1))
    tasks.append(pool.enqueue(task2))
    pool.dispose()
    results = list(map(lambda x: x.get_res(), tasks))
    assert results == [1, 2]
