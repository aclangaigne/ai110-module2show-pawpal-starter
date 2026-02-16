from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def get_today_tasks(self, owner: Owner) -> List[Task]:
        return owner.get_all_tasks()

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.time)

    def detect_conflicts(self, tasks: List[Task]) -> List[tuple[Task, Task]]:
        """Returns list of (task1, task2) pairs that conflict/overlap"""
        conflicts = []
        for i, task1 in enumerate(tasks):
            for task2 in tasks[i + 1:]:
                if task1.time == task2.time:
                    conflicts.append((task1, task2))
        return conflicts
