from pawpal_system import Task, Pet

def test_task_completion():
    task = Task(description="Walk dog", time="09:00", frequency="daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True

def test_add_task_increases_task_count():
    pet = Pet(name="Buddy", species="Dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feed", time="08:00", frequency="daily"))
    assert len(pet.tasks) == 1

from pawpal_system import Task, Pet, Owner, Scheduler

def test_sorting_correctness():
    scheduler = Scheduler()
    tasks = [
        Task(description="C", time="14:00", frequency="once", date="2026-02-15"),
        Task(description="A", time="08:00", frequency="once", date="2026-02-15"),
        Task(description="B", time="09:30", frequency="once", date="2026-02-15"),
    ]
    sorted_tasks = scheduler.sort_tasks(tasks)
    assert [t.time for t in sorted_tasks] == ["08:00", "09:30", "14:00"]

def test_conflict_detection_duplicate_times():
    scheduler = Scheduler()
    t1 = Task(description="Walk", time="09:00", frequency="once", date="2026-02-15")
    t2 = Task(description="Feed", time="09:00", frequency="once", date="2026-02-15")
    t3 = Task(description="Vet", time="10:00", frequency="once", date="2026-02-15")

    conflicts = scheduler.detect_conflicts([t1, t2, t3])
    assert any(a.time == "09:00" and b.time == "09:00" for a, b in conflicts)

def test_daily_recurrence_creates_next_day_task():
    scheduler = Scheduler()
    t = Task(description="Daily walk", time="09:00", frequency="daily", date="2026-02-15")
    next_task = scheduler.complete_task(t)

    assert t.completed is True
    assert next_task is not None
    assert next_task.date == "2026-02-16"
    assert next_task.completed is False

def test_owner_filters_tasks_by_completion():
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog", age=2)
    owner.add_pet(pet)

    t1 = Task(description="Walk", time="09:00", frequency="once", date="2026-02-15", completed=False)
    t2 = Task(description="Feed", time="10:00", frequency="once", date="2026-02-15", completed=True)
    pet.add_task(t1)
    pet.add_task(t2)

    incomplete = owner.get_tasks_by_completion(False)
    complete = owner.get_tasks_by_completion(True)

    assert len(incomplete) == 1 and incomplete[0].description == "Walk"
    assert len(complete) == 1 and complete[0].description == "Feed"

def test_owner_with_pet_no_tasks_returns_empty_today_schedule(monkeypatch):
    # This test uses today's date from Scheduler.get_today_tasks, so we just verify empty output.
    owner = Owner("Jordan")
    owner.add_pet(Pet(name="Mochi", species="dog", age=2))

    scheduler = Scheduler()
    assert scheduler.get_today_tasks(owner) == []
