from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List


@dataclass
class Task:
    """Represents a single pet-care activity (walk, feeding, meds, appointment)."""
    description: str
    time: str              # "HH:MM" (zero-padded)
    frequency: str         # "once", "daily", "weekly"
    date: str = date.today().isoformat()  # "YYYY-MM-DD"
    completed: bool = False

    def mark_complete(self) -> None:
        """Marks this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Represents a pet and the tasks associated with that pet."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Returns all tasks for this pet."""
        return self.tasks


class Owner:
    """Represents the pet owner who manages multiple pets."""
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns a flat list of all tasks across all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_tasks_by_pet_name(self, pet_name: str) -> List[Task]:
        """Returns tasks for a specific pet name (empty list if not found)."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def get_tasks_by_completion(self, completed: bool) -> List[Task]:
        """Returns all tasks filtered by completion status."""
        return [t for t in self.get_all_tasks() if t.completed == completed]


class Scheduler:
    """Organizes tasks across pets (today view, sorting, conflicts, recurrence)."""

    def get_today_tasks(self, owner: Owner) -> List[Task]:
        """Returns tasks due today that are not completed."""
        today = date.today().isoformat()
        return [t for t in owner.get_all_tasks() if t.date == today and not t.completed]

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks chronologically by time ("HH:MM")."""
        return sorted(tasks, key=lambda t: t.time)

    def detect_conflicts(self, tasks: List[Task]) -> List[tuple[Task, Task]]:
        """Returns (task1, task2) pairs where both tasks share the same time."""
        conflicts: List[tuple[Task, Task]] = []
        for i, task1 in enumerate(tasks):
            for task2 in tasks[i + 1:]:
                if task1.time == task2.time:
                    conflicts.append((task1, task2))
        return conflicts

    def complete_task(self, task: Task) -> Task | None:
        """
        Marks a task complete and returns the next occurrence if recurring.
        - daily -> next day
        - weekly -> +7 days
        - once (or anything else) -> None
        """
        task.completed = True

        if task.frequency == "daily":
            d = datetime.fromisoformat(task.date).date()
            next_date = (d + timedelta(days=1)).isoformat()
            return Task(
                description=task.description,
                time=task.time,
                frequency=task.frequency,
                date=next_date,
                completed=False,
            )

        if task.frequency == "weekly":
            d = datetime.fromisoformat(task.date).date()
            next_date = (d + timedelta(days=7)).isoformat()
            return Task(
                description=task.description,
                time=task.time,
                frequency=task.frequency,
                date=next_date,
                completed=False,
            )

        return None
