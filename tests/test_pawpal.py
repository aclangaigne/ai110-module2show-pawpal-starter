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
