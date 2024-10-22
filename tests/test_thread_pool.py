from time import sleep
from threading import Thread
from typing import Any
import pytest
from project.thread_pool import ThreadPool, TaskWrapper


def test_task_result() -> None:
    """Test that TaskWrapper correctly sets and awaits a result."""

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


def test_enqueue_for_task_with_parameters() -> None:
    """Test that tasks are correctly enqueued and processed."""
    pool = ThreadPool(num_threads=2)

    def task1(x: str, y: int) -> tuple[str, int]:
        return x, y

    def task2(a: Any) -> Any:
        return a

    task_1 = pool.enqueue(task1, "abc", 123)
    task_2 = pool.enqueue(task2, None)

    # Await the task completion and check the result
    result1 = task_1.get_res()
    assert result1 == ("abc", 123)
    result2 = task_2.get_res()
    assert result2 is None

    # Clean up thread pool
    pool.dispose()


def test_enqueue_for_built_in_functions() -> None:
    """Test that built-in functions are correctly enqueued and processed."""
    pool = ThreadPool(num_threads=2)

    task_1 = pool.enqueue(pow, 2, 10)
    task_2 = pool.enqueue(sum, [1, 2, 3, 4])

    # Await the task completion and check the result
    result1 = task_1.get_res()
    assert result1 == 1024
    result2 = task_2.get_res()
    assert result2 == 10

    # Clean up thread pool
    pool.dispose()


def test_ordered_execution_with_one_threads() -> None:
    """Test that tasks are executed in the order they were enqueued."""
    pool = ThreadPool(num_threads=1)  # Single thread to ensure order

    results = []

    def task1() -> None:
        results.append(1)

    def task2() -> None:
        results.append(2)

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
    """Test that the order is followed to perform tasks on multiple threads."""
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

    # Wait for tasks to complete and check the result
    t1.get_res()
    t2.get_res()
    t3.get_res()
    assert results == [1, 3, 2]

    # Clean up thread pool
    pool.dispose()


def test_dispose_not_terminate_execution() -> None:
    """Test that when you call dispose, tasks from the queue continue to be executed."""
    pool = ThreadPool(num_threads=1)

    def task1() -> int:
        sleep(1)
        return 1

    task = pool.enqueue(task1)

    # Clean up thread pool
    pool.dispose()

    # Wait for task to complete and check the result
    result = task.get_res()
    assert result == 1


def test_that_cannot_add_task_after_dispose() -> None:
    """Test that after dispose a thread cannot add a task."""
    pool = ThreadPool(num_threads=2)

    # Clean up thread pool
    pool.dispose()

    # Attempt to add a task
    with pytest.raises(TypeError):
        pool.enqueue(sum, [1, 2, 3])


def test_for_the_number_of_threads() -> None:
    """Test that cannot create a thread pool with a non-sufficient number of threads."""
    with pytest.raises(ValueError):
        ThreadPool(num_threads=0)
        ThreadPool(num_threads=-1)
