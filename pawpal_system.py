from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    """Priority levels for tasks"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Represents a pet care task"""
    title: str
    duration_minutes: int
    priority: Priority
    completed: bool = False
    
    def __post_init__(self):
        """Validate task data"""
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be positive")


@dataclass
class Schedule:
    """Manages pet care tasks"""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule"""
        self.tasks.append(task)

    def modify_task(self, task_id: int, new_task: Task) -> None:
        """Modify an existing task by index"""
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id] = new_task

    def remove_task(self, task_id: int) -> None:
        """Remove a task from the schedule"""
        if 0 <= task_id < len(self.tasks):
            self.tasks.pop(task_id)

    def add_priority(self, task_id: int, priority: Priority) -> None:
        """Update the priority of a task"""
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].priority = priority

    def create_plan(self) -> None:
        """Create an optimized plan in-place for this schedule"""
        priority_order = {Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}
        self.tasks = sorted(
            self.tasks,
            key=lambda t: (-priority_order[t.priority], t.duration_minutes)
        )

    def mark_task_complete(self, task_id: int) -> None:
        """Mark a task as complete by index"""
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].completed = True

    def mark_task_incomplete(self, task_id: int) -> None:
        """Mark a task as incomplete by index"""
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].completed = False


@dataclass
class Owner:
    """Represents a pet owner"""
    name: str
    age: int
    address: str
    
    pets: List['Pet'] = field(default_factory=list)
    schedules: List[Schedule] = field(default_factory=list)

    def enter_info(self) -> None:
        """Enter owner information"""
        # data is provided through constructor in this domain model
        return
    
    def edit_info(self, name: str = None, age: int = None, address: str = None) -> None:
        """Edit owner information"""
        if name:
            self.name = name
        if age is not None:
            self.age = age
        if address:
            self.address = address
    
    def delete_info(self) -> None:
        """Delete owner information (reset to defaults)"""
        self.name = ""
        self.age = 0
        self.address = ""
        self.pets.clear()
        self.schedules.clear()

    def add_pet(self, pet: 'Pet') -> None:
        """Assign a pet to this owner"""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet: 'Pet') -> None:
        """Remove a pet from this owner"""
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def add_schedule(self, schedule: Schedule) -> None:
        """Assign a schedule to this owner"""
        self.schedules.append(schedule)

    def remove_schedule(self, schedule: Schedule) -> None:
        """Remove schedule from this owner"""
        if schedule in self.schedules:
            self.schedules.remove(schedule)


@dataclass
class Pet:
    """Represents a pet"""
    name: str
    breed: str
    age: int
    gender: str
    owner: Optional[Owner] = None
    tasks: List[Task] = field(default_factory=list)
    
    def enter_info(self) -> None:
        """Enter pet information"""
        pass
    
    def edit_info(self, name: str = None, breed: str = None, age: int = None, gender: str = None) -> None:
        """Edit pet information"""
        if name:
            self.name = name
        if breed:
            self.breed = breed
        if age is not None:
            self.age = age
        if gender:
            self.gender = gender

    def add_task(self, task: Task) -> None:
        """Add a care task associated to this pet"""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove task from this pet"""
        if task in self.tasks:
            self.tasks.remove(task)

    @property
    def task_counter(self) -> int:
        """Return number of tasks assigned to this pet"""
        return len(self.tasks)
    
    def delete_info(self) -> None:
        """Delete pet information (reset to defaults)"""
        self.name = ""
        self.breed = ""
        self.age = 0
        self.gender = ""
        self.owner = None

