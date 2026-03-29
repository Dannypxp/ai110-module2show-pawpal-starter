

def test():
    #Import the classes from the pawpal_system.py file
    from pawpal_system import Schedule, Owner, Pet, Task, Priority
    # Create schedule
    schedule = Schedule()

    # Create one owner (name, age, address)
    owner = Owner("Alice", 30, "123 Main St")

    # Create two pets and assign to owner
    fluffy = Pet("Fluffy", "Cat", 10, "Female")
    lito = Pet("Lito", "Cat", 2, "Female")
    owner.add_pet(fluffy)
    owner.add_pet(lito)

    # Create tasks (title, duration_minutes, priority)
    task1 = Task("Feed Fluffy", 10, Priority.HIGH)
    task2 = Task("Walk Fluffy", 30, Priority.MEDIUM)
    task3 = Task("Feed Lito", 10, Priority.LOW)

    # Add tasks to schedule
    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)

    # Create optimized plan by reordering schedule tasks
    schedule.create_plan()

    print(schedule)


if __name__ == "__main__":
    test()
