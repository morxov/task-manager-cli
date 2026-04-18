"""Pytest tests for CLI Task Manager."""

import json
import os
import pytest
from pathlib import Path
from task_manager import load_tasks, save_tasks, add_task, list_tasks, done_task

TEST_FILE = Path("/tmp/test_tasks.json")


@pytest.fixture(autouse=True)
def use_test_file(monkeypatch, tmp_path):
    test_file = tmp_path / "test_tasks.json"
    import task_manager
    monkeypatch.setattr(task_manager, "TASKS_FILE", test_file)


def test_add_task(tmp_path):
    import task_manager
    task_manager.TASKS_FILE = tmp_path / "tasks.json"
    task_manager.add_task("Write tests", "high")
    tasks = task_manager.load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Write tests"
    assert tasks[0]["priority"] == "high"
    assert tasks[0]["done"] is False


def test_add_multiple_tasks(tmp_path):
    import task_manager
    task_manager.TASKS_FILE = tmp_path / "tasks.json"
    task_manager.add_task("Task 1", "low")
    task_manager.add_task("Task 2", "medium")
    tasks = task_manager.load_tasks()
    assert len(tasks) == 2
    assert tasks[1]["id"] == 2


def test_done_task(tmp_path):
    import task_manager
    task_manager.TASKS_FILE = tmp_path / "tasks.json"
    task_manager.add_task("Test me", "high")
    task_manager.done_task(1)
    tasks = task_manager.load_tasks()
    assert tasks[0]["done"] is True


def test_done_nonexistent(tmp_path, capsys):
    import task_manager
    task_manager.TASKS_FILE = tmp_path / "tasks.json"
    task_manager.done_task(999)
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_priority_normalization(tmp_path):
    import task_manager
    task_manager.TASKS_FILE = tmp_path / "tasks.json"
    task_manager.add_task("Normalize me", "HIGH")
    tasks = task_manager.load_tasks()
    assert tasks[0]["priority"] == "high"
