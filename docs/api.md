# PawPal System API Documentation

## Task

Represents a pet care task

---

## Schedule

Manages pet care tasks

### add_priority(self, task_id: int, priority: pawpal_system.Priority) -> None

Update the priority of a task

### add_task(self, task: pawpal_system.Task) -> None

Add a task to the schedule

### create_plan(self) -> None

Create an optimized plan in-place for this schedule

### mark_task_complete(self, task_id: int) -> None

Mark a task as complete by index

### mark_task_incomplete(self, task_id: int) -> None

Mark a task as incomplete by index

### modify_task(self, task_id: int, new_task: pawpal_system.Task) -> None

Modify an existing task by index

### remove_task(self, task_id: int) -> None

Remove a task from the schedule

---

## Owner

Represents a pet owner

### add_pet(self, pet: 'Pet') -> None

Assign a pet to this owner

### add_schedule(self, schedule: pawpal_system.Schedule) -> None

Assign a schedule to this owner

### delete_info(self) -> None

Delete owner information (reset to defaults)

### edit_info(self, name: str = None, age: int = None, address: str = None) -> None

Edit owner information

### enter_info(self) -> None

Enter owner information

### remove_pet(self, pet: 'Pet') -> None

Remove a pet from this owner

### remove_schedule(self, schedule: pawpal_system.Schedule) -> None

Remove schedule from this owner

---

## Pet

Represents a pet

### add_task(self, task: pawpal_system.Task) -> None

Add a care task associated to this pet

### delete_info(self) -> None

Delete pet information (reset to defaults)

### edit_info(self, name: str = None, breed: str = None, age: int = None, gender: str = None) -> None

Edit pet information

### enter_info(self) -> None

Enter pet information

### remove_task(self, task: pawpal_system.Task) -> None

Remove task from this pet

---
