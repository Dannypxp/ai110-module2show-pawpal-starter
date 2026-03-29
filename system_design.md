# PawPal+ System Design

## Class Diagram

```mermaid
classDiagram
    class Owner {
        -name: str
        -age: int
        -address: str
        +enter_info()
        +edit_info()
        +delete_info()
    }

    class Pet {
        -name: str
        -breed: str
        -age: int
        -gender: str
        +enter_info()
        +edit_info()
        +delete_info()
    }

    class Schedule {
        -tasks: List[Task]
        +add_task(task)
        +modify_task(task_id, new_task)
        +remove_task(task_id)
        +add_priority(task_id, priority)
    }

    class Task {
        -title: str
        -duration_minutes: int
        -priority: str
    }

    class Plan {
        -plan: List[Task]
        +create_plan(schedule)
    }

    Schedule --> Task
    Plan --> Schedule
    Owner "1" -- "*" Pet
    Owner "1" -- "*" Plan
```

## System Overview

- **Owner**: Manages owner information (name, age, address) with abilities to create, edit, and delete their profile
- **Pet**: Represents a pet with attributes (name, breed, age, gender) and similar CRUD operations as Owner
- **Schedule**: Manages a collection of tasks for a pet, allowing you to add, modify, remove tasks and adjust their priorities
- **Task**: Individual pet care tasks with a title, duration, and priority level
- **Plan**: Creates an optimized schedule by taking tasks from the Schedule and organizing them based on constraints
