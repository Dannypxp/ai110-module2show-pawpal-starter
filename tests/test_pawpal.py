import pytest

from pawpal_system import Schedule, Owner, Pet, Task, Priority


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
