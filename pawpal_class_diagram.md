# PawPal+ Class Diagram

```mermaid
classDiagram
    class Owner {
        -name: string
        -pets: List~Pet~
        +add_pet(pet: Pet) void
        +get_all_tasks() List~Task~
    }
    
    class Pet {
        -name: string
        -species: string
        -age: int
        -tasks: List~Task~
        +add_task(task: Task) void
        +get_tasks() List~Task~
    }
    
    class Task {
        -description: string
        -time: datetime
        -frequency: string
        -completed: boolean
        +mark_complete() void
    }
    
    class Scheduler {
        +get_today_tasks(owner: Owner) List~Task~
        +sort_tasks(tasks: List~Task~) List~Task~
        +detect_conflicts(tasks: List~Task~) List~Conflict~
    }
    
    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Scheduler --> Owner : retrieves from
    Scheduler --> Task : manages
```

## Relationships
- **Owner → Pet**: One owner has many pets (1:*)
- **Pet → Task**: One pet has many tasks (1:*)
- **Scheduler → Owner**: Scheduler retrieves tasks from an owner
- **Scheduler → Task**: Scheduler manages task operations (sorting, conflict detection)

## Class Descriptions

**Owner**: Manages multiple pets and can retrieve all tasks across their pets
- `add_pet()`: Adds a new pet to the owner's collection
- `get_all_tasks()`: Returns all tasks from all pets

**Pet**: Represents a pet with associated tasks
- `add_task()`: Adds a new task for this pet
- `get_tasks()`: Returns all tasks for this pet

**Task**: Represents a single task for a pet
- `mark_complete()`: Marks the task as completed

**Scheduler**: Handles task organization and conflict detection
- `get_today_tasks()`: Retrieves tasks scheduled for today
- `sort_tasks()`: Sorts tasks by time
- `detect_conflicts()`: Identifies overlapping or conflicting tasks
