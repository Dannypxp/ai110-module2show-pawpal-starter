

def test():
    #Import the classes from the pawpal_system.py file
    from pawpal_system import Schedule, Owner, Pet, Task, Priority, Frequency
    from datetime import time
    
    # Create schedule
    schedule = Schedule()

    # Create one owner (name, age, address)
    owner = Owner("Alice", 30, "123 Main St")

    # Create two pets and assign to owner
    fluffy = Pet("Fluffy", "Cat", 10, "Female")
    lito = Pet("Lito", "Cat", 2, "Female")
    owner.add_pet(fluffy)
    owner.add_pet(lito)

    # Create tasks that will cause overlaps
    morning_feeding = Task("Morning feeding", 15, Priority.HIGH, frequency=Frequency.DAILY)
    morning_walk = Task("Morning walk", 30, Priority.HIGH, frequency=Frequency.DAILY)  # Will overlap with feeding
    grooming = Task("Grooming", 45, Priority.MEDIUM, frequency=Frequency.WEEKLY)
    playtime = Task("Playtime", 20, Priority.LOW, frequency=Frequency.DAILY)

    # Add tasks to pets
    fluffy.add_task(morning_feeding)
    lito.add_task(morning_walk)
    fluffy.add_task(grooming)
    lito.add_task(playtime)

    # Add tasks to schedule
    schedule.add_task(morning_feeding)
    schedule.add_task(morning_walk)
    schedule.add_task(grooming)
    schedule.add_task(playtime)

    print("=== TASKS WITHOUT SCHEDULED TIMES ===")
    for i, task in enumerate(schedule.tasks, 1):
        pet_name = task.pet.name if task.pet else "No pet"
        freq = task.frequency.value
        print(f"{i}. {task.title} - {task.duration_minutes}m ({task.priority.value}) - {freq} - Pet: {pet_name}")

    print("\n=== ASSIGNING START TIMES (8:00 AM) ===")
    schedule.assign_start_times(8, 0)  # Start at 8:00 AM
    
    for i, task in enumerate(schedule.tasks, 1):
        pet_name = task.pet.name if task.pet else "No pet"
        time_str = task.start_time.strftime("%H:%M") if task.start_time else "Unscheduled"
        end_str = task.end_time.strftime("%H:%M") if task.end_time else "Unscheduled"
        freq = task.frequency.value
        print(f"{i}. {time_str}-{end_str}: {task.title} ({task.duration_minutes}m, {task.priority.value}) - {freq} - Pet: {pet_name}")

    print("\n=== DETECTING OVERLAPS ===")
    overlaps = schedule.detect_overlaps()
    
    if overlaps:
        print(f"Found {len(overlaps)} scheduling conflicts:")
        for task1, task2, conflict_type in overlaps:
            t1_time = f"{task1.start_time.strftime('%H:%M')}-{task1.end_time.strftime('%H:%M')}" if task1.start_time else "Unscheduled"
            t2_time = f"{task2.start_time.strftime('%H:%M')}-{task2.end_time.strftime('%H:%M')}" if task2.start_time else "Unscheduled"
            print(f"   ⚠️  {conflict_type}: '{task1.title}' ({t1_time}) overlaps with '{task2.title}' ({t2_time})")
    else:
        print("✅ No overlaps detected")

    print("\n=== ATTEMPTING TO RESOLVE OVERLAPS ===")
    success, resolution_warnings = schedule.resolve_overlaps()
    
    print(f"Resolution {'✅ SUCCESSFUL' if success else '❌ FAILED'}")
    for warning in resolution_warnings:
        print(f"   {warning.severity.upper()}: {warning.message}")
    
    if success:
        print("New schedule after resolution:")
        for i, task in enumerate(schedule.tasks, 1):
            pet_name = task.pet.name if task.pet else "No pet"
            time_str = task.start_time.strftime("%H:%M") if task.start_time else "Unscheduled"
            end_str = task.end_time.strftime("%H:%M") if task.end_time else "Unscheduled"
            freq = task.frequency.value
            print(f"{i}. {time_str}-{end_str}: {task.title} ({task.duration_minutes}m, {task.priority.value}) - {freq} - Pet: {pet_name}")
    else:
        remaining_overlaps = schedule.detect_overlaps()
        print(f"Remaining conflicts: {len(remaining_overlaps)}")

    print("\n=== SCHEDULE SUMMARY ===")
    warnings = schedule.get_warnings()
    if warnings:
        print("Schedule warnings:")
        for warning in warnings:
            print(f"  {warning.severity.upper()}: {warning.message}")
    else:
        print("✅ Schedule has no warnings")

    print(f"\nQuick conflict check: {'❌ Has conflicts' if schedule.has_conflicts() else '✅ No conflicts'}")
    conflict_summary = schedule.get_conflict_summary()
    if conflict_summary:
        print("Conflict details:")
        print(conflict_summary)

    # Test with manual time assignment to create specific overlaps
    print("\n=== TESTING MANUAL TIME ASSIGNMENT ===")
    # Manually set overlapping times
    schedule.tasks[0].start_time = time(9, 0)   # Morning feeding at 9:00
    schedule.tasks[1].start_time = time(9, 10)  # Morning walk at 9:10 (overlaps with feeding)
    schedule.tasks[2].start_time = time(10, 0)  # Grooming at 10:00
    schedule.tasks[3].start_time = time(9, 5)   # Playtime at 9:05 (overlaps with both feeding and walk)

    overlaps = schedule.detect_overlaps()
    print(f"Manual overlaps created: {len(overlaps)} conflicts")
    for task1, task2, conflict_type in overlaps:
        t1_time = f"{task1.start_time.strftime('%H:%M')}-{task1.end_time.strftime('%H:%M')}" if task1.start_time else "Unscheduled"
        t2_time = f"{task2.start_time.strftime('%H:%M')}-{task2.end_time.strftime('%H:%M')}" if task2.start_time else "Unscheduled"
        print(f"   ⚠️  {conflict_type}: '{task1.title}' ({t1_time}) vs '{task2.title}' ({t2_time})")

    # Test: Two tasks at exactly the same time
    print("\n=== TESTING SAME TIME CONFLICTS ===")
    test_schedule = Schedule()
    
    # Create two tasks that start at exactly the same time
    task_a = Task("Task A", 30, Priority.HIGH, frequency=Frequency.ONCE)
    task_b = Task("Task B", 20, Priority.MEDIUM, frequency=Frequency.ONCE)
    
    # Manually set them to start at the same time
    same_time = time(10, 0)  # Both start at 10:00 AM
    task_a.start_time = same_time
    task_b.start_time = same_time
    
    test_schedule.add_task(task_a)
    test_schedule.add_task(task_b)
    
    print("Created two tasks starting at exactly the same time (10:00 AM)")
    print(f"Task A: {task_a.start_time.strftime('%H:%M')}-{task_a.end_time.strftime('%H:%M')}")
    print(f"Task B: {task_b.start_time.strftime('%H:%M')}-{task_b.end_time.strftime('%H:%M')}")
    
    # Check for conflicts
    same_time_overlaps = test_schedule.detect_overlaps()
    print(f"\nSchedule detected {len(same_time_overlaps)} conflicts:")
    
    if same_time_overlaps:
        for task1, task2, conflict_type in same_time_overlaps:
            print(f"   🚨 {conflict_type.upper()}: '{task1.title}' and '{task2.title}' start at the same time!")
            print(f"      Both start at {task1.start_time.strftime('%H:%M')}")
    else:
        print("   ❌ ERROR: Schedule should have detected conflicts but didn't!")
    
    # Test warnings system for same time conflicts
    print("\nWarnings for same time conflicts:")
    warnings = test_schedule.get_warnings()
    for warning in warnings:
        if warning.severity in ['error', 'warning']:
            print(f"   {warning.severity.upper()}: {warning.message}")
    
    # Verify has_conflicts returns True
    has_conflicts = test_schedule.has_conflicts()
    print(f"\nhas_conflicts() result: {'✅ CORRECT - detected conflicts' if has_conflicts else '❌ ERROR - missed conflicts'}")
    
    # Test conflict summary
    conflict_summary = test_schedule.get_conflict_summary()
    if conflict_summary:
        print(f"\nConflict summary:\n{conflict_summary}")
    else:
        print("\n❌ ERROR: No conflict summary generated!")


if __name__ == "__main__":
    test()
