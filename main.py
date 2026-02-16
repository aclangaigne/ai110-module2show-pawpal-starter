from pawpal_system import Task, Pet, Owner, Scheduler

def main():
    owner = Owner("Abigail")

    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(description="Morning walk", time="09:00", frequency="daily"))
    cat.add_task(Task(description="Feed breakfast", time="08:00", frequency="daily"))
    dog.add_task(Task(description="Vet appointment", time="14:00", frequency="once"))

    scheduler = Scheduler()
    tasks = scheduler.get_today_tasks(owner)
    tasks_sorted = scheduler.sort_tasks(tasks)
    conflicts = scheduler.detect_conflicts(tasks_sorted)

    print("\nToday's Schedule:")
    for task in tasks_sorted:
        status = "✅" if task.completed else "⬜"
        print(f"{task.time} - {task.description} [{task.frequency}] {status}")

    if conflicts:
        print("\nConflicts Detected:")
        for t1, t2 in conflicts:
            print(f"- {t1.time}: '{t1.description}' conflicts with '{t2.description}'")
    else:
        print("\nNo conflicts detected.")

if __name__ == "__main__":
    main()
