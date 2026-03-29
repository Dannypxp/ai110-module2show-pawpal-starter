import pytest
from datetime import time

from pawpal_system import Schedule, Owner, Pet, Task, Priority, Frequency, ScheduleWarning


def test_schedule_create_plan_sorts_by_priority_then_duration():
	schedule = Schedule()
	schedule.add_task(Task("Low1", 10, Priority.LOW))
	schedule.add_task(Task("High", 20, Priority.HIGH))
	schedule.add_task(Task("Medium", 15, Priority.MEDIUM))
	schedule.add_task(Task("HighShort", 5, Priority.HIGH))

	schedule.create_plan()

	titles = [t.title for t in schedule.tasks]
	assert titles == ["HighShort", "High", "Medium", "Low1"]


def test_owner_pet_relationships_work():
	owner = Owner("Alice", 30, "123 Main St")
	pet = Pet("Fluffy", "Cat", 10, "Female")

	owner.add_pet(pet)

	assert pet.owner is owner
	assert pet in owner.pets

	owner.remove_pet(pet)

	assert pet.owner is None
	assert pet not in owner.pets


def test_schedule_mark_task_complete_and_incomplete():
	schedule = Schedule()
	task = Task("Feed", 10, Priority.HIGH)
	schedule.add_task(task)

	schedule.mark_task_complete(0)
	assert schedule.tasks[0].completed is True

	schedule.mark_task_incomplete(0)
	assert schedule.tasks[0].completed is False


def test_pet_task_counter_increments_when_task_added():
	pet = Pet("Fluffy", "Cat", 10, "Female")

	assert pet.task_counter == 0
	pet.add_task(Task("Feed", 10, Priority.HIGH))
	assert pet.task_counter == 1


# Sorting Correctness Tests
def test_schedule_sort_by_duration():
	schedule = Schedule()
	schedule.add_task(Task("Short", 5, Priority.MEDIUM))
	schedule.add_task(Task("Long", 30, Priority.MEDIUM))
	schedule.add_task(Task("Medium", 15, Priority.MEDIUM))

	schedule.sort_by_duration()

	durations = [t.duration_minutes for t in schedule.tasks]
	assert durations == [5, 15, 30]


def test_schedule_create_plan_empty_schedule():
	schedule = Schedule()
	schedule.create_plan()  # Should not crash
	assert len(schedule.tasks) == 0


def test_schedule_create_plan_single_task():
	schedule = Schedule()
	task = Task("Single", 10, Priority.HIGH)
	schedule.add_task(task)
	schedule.create_plan()
	assert schedule.tasks[0] == task


def test_schedule_create_plan_same_priority_sort_by_duration():
	schedule = Schedule()
	schedule.add_task(Task("Long", 30, Priority.HIGH))
	schedule.add_task(Task("Short", 5, Priority.HIGH))
	schedule.add_task(Task("Medium", 15, Priority.HIGH))

	schedule.create_plan()

	durations = [t.duration_minutes for t in schedule.tasks]
	assert durations == [5, 15, 30]


def test_schedule_create_plan_mixed_priorities():
	schedule = Schedule()
	schedule.add_task(Task("LowLong", 30, Priority.LOW))
	schedule.add_task(Task("HighShort", 5, Priority.HIGH))
	schedule.add_task(Task("Medium", 15, Priority.MEDIUM))
	schedule.add_task(Task("HighLong", 20, Priority.HIGH))

	schedule.create_plan()

	priorities = [t.priority for t in schedule.tasks]
	assert priorities == [Priority.HIGH, Priority.HIGH, Priority.MEDIUM, Priority.LOW]


# Recurrence Logic Tests
def test_mark_task_complete_creates_daily_recurrence():
	schedule = Schedule()
	task = Task("Daily Feed", 10, Priority.HIGH, frequency=Frequency.DAILY)
	schedule.add_task(task)

	initial_count = len(schedule.tasks)
	schedule.mark_task_complete(0)

	assert len(schedule.tasks) == initial_count + 1
	assert schedule.tasks[0].completed is True
	assert schedule.tasks[1].completed is False
	assert schedule.tasks[1].title == "Daily Feed"
	assert schedule.tasks[1].frequency == Frequency.DAILY


def test_mark_task_complete_creates_weekly_recurrence():
	schedule = Schedule()
	task = Task("Weekly Bath", 30, Priority.MEDIUM, frequency=Frequency.WEEKLY)
	schedule.add_task(task)

	schedule.mark_task_complete(0)

	assert len(schedule.tasks) == 2
	assert schedule.tasks[1].frequency == Frequency.WEEKLY


def test_mark_task_complete_no_recurrence_for_once():
	schedule = Schedule()
	task = Task("One-time Vet", 60, Priority.HIGH, frequency=Frequency.ONCE)
	schedule.add_task(task)

	initial_count = len(schedule.tasks)
	schedule.mark_task_complete(0)

	assert len(schedule.tasks) == initial_count
	assert schedule.tasks[0].completed is True


def test_recurring_task_added_to_pet():
	owner = Owner("Alice", 30, "123 Main St")
	pet = Pet("Fluffy", "Cat", 10, "Female")
	owner.add_pet(pet)

	schedule = Schedule()
	task = Task("Daily Feed", 10, Priority.HIGH, frequency=Frequency.DAILY, pet=pet)
	schedule.add_task(task)

	schedule.mark_task_complete(0)

	assert len(pet.tasks) == 1  # New recurring task added to pet
	assert pet.tasks[0].completed is False


def test_multiple_recurrences():
	schedule = Schedule()
	task = Task("Daily Walk", 20, Priority.MEDIUM, frequency=Frequency.DAILY)
	schedule.add_task(task)

	# Complete multiple times
	schedule.mark_task_complete(0)  # Creates task 1
	schedule.mark_task_complete(1)  # Creates task 2

	assert len(schedule.tasks) == 3
	assert all(t.title == "Daily Walk" for t in schedule.tasks)
	assert all(t.frequency == Frequency.DAILY for t in schedule.tasks)


# Conflict Detection Tests
def test_detect_overlaps_same_pet():
	pet = Pet("Fluffy", "Cat", 10, "Female")
	schedule = Schedule()

	task1 = Task("Feed", 30, Priority.HIGH, pet=pet)
	task1.start_time = time(9, 0)  # 9:00 - 9:30

	task2 = Task("Play", 30, Priority.MEDIUM, pet=pet)
	task2.start_time = time(9, 15)  # 9:15 - 9:45

	schedule.add_task(task1)
	schedule.add_task(task2)

	overlaps = schedule.detect_overlaps()
	assert len(overlaps) == 1
	assert overlaps[0][2] == "same_pet"


def test_detect_overlaps_different_pets():
	pet1 = Pet("Fluffy", "Cat", 10, "Female")
	pet2 = Pet("Spot", "Dog", 5, "Male")
	schedule = Schedule()

	task1 = Task("Feed Cat", 30, Priority.HIGH, pet=pet1)
	task1.start_time = time(9, 0)

	task2 = Task("Walk Dog", 30, Priority.MEDIUM, pet=pet2)
	task2.start_time = time(9, 15)

	schedule.add_task(task1)
	schedule.add_task(task2)

	overlaps = schedule.detect_overlaps()
	assert len(overlaps) == 1
	assert overlaps[0][2] == "owner_capacity"


def test_detect_overlaps_no_overlap():
	schedule = Schedule()

	task1 = Task("Task1", 30, Priority.HIGH)
	task1.start_time = time(9, 0)  # 9:00 - 9:30

	task2 = Task("Task2", 30, Priority.MEDIUM)
	task2.start_time = time(9, 30)  # 9:30 - 10:00 (adjacent, no overlap)

	schedule.add_task(task1)
	schedule.add_task(task2)

	overlaps = schedule.detect_overlaps()
	assert len(overlaps) == 0


def test_detect_overlaps_overnight():
	schedule = Schedule()

	task1 = Task("Late Task", 60, Priority.HIGH)  # 1 hour
	task1.start_time = time(23, 0)  # 23:00 - 24:00

	task2 = Task("Early Task", 60, Priority.MEDIUM)
	task2.start_time = time(23, 30)  # 23:30 - 00:30

	schedule.add_task(task1)
	schedule.add_task(task2)

	overlaps = schedule.detect_overlaps()
	assert len(overlaps) == 1


def test_detect_overlaps_unscheduled_tasks():
	schedule = Schedule()

	task1 = Task("Scheduled", 30, Priority.HIGH)
	task1.start_time = time(9, 0)

	task2 = Task("Unscheduled", 30, Priority.MEDIUM)  # No start_time

	schedule.add_task(task1)
	schedule.add_task(task2)

	overlaps = schedule.detect_overlaps()
	assert len(overlaps) == 0  # Unscheduled task shouldn't cause overlaps


def test_get_warnings_includes_overlaps():
	pet = Pet("Fluffy", "Cat", 10, "Female")
	schedule = Schedule()

	task1 = Task("Feed", 30, Priority.HIGH, pet=pet)
	task1.start_time = time(9, 0)

	task2 = Task("Play", 30, Priority.MEDIUM, pet=pet)
	task2.start_time = time(9, 15)

	schedule.add_task(task1)
	schedule.add_task(task2)

	warnings = schedule.get_warnings()
	conflict_warnings = [w for w in warnings if w.severity in ['error', 'warning']]
	assert len(conflict_warnings) == 1
	assert "Same pet conflict" in conflict_warnings[0].message


def test_has_conflicts():
	pet = Pet("Fluffy", "Cat", 10, "Female")
	schedule = Schedule()

	task1 = Task("Feed", 30, Priority.HIGH, pet=pet)
	task1.start_time = time(9, 0)

	task2 = Task("Play", 30, Priority.MEDIUM, pet=pet)
	task2.start_time = time(9, 15)

	schedule.add_task(task1)
	schedule.add_task(task2)

	assert schedule.has_conflicts() is True


def test_resolve_overlaps_success():
	schedule = Schedule()

	task1 = Task("Task1", 30, Priority.HIGH)
	task2 = Task("Task2", 30, Priority.MEDIUM)

	schedule.add_task(task1)
	schedule.add_task(task2)

	# Manually set overlapping times
	task1.start_time = time(9, 0)
	task2.start_time = time(9, 15)

	success, warnings = schedule.resolve_overlaps()

	assert success is True
	assert len(schedule.get_warnings()) == 0  # No conflicts after resolution
