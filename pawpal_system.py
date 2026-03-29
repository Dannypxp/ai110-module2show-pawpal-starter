from dataclasses import dataclass, field
from typing import List
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
    
    def __post_init__(self):
        """Validate task data"""
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be positive")


@dataclass
class Owner:
    """Represents a pet owner"""
    name: str
    age: int
    address: str
    
    def enter_info(self) -> None:
        """Enter owner information"""
        pass
    
    def edit_info(self, name: str = None, age: int = None, address: str = None) -> None:
        """Edit owner information"""
        if name:
            self.name = name
        if age:
            self.age = age
        if address:
            self.address = address
    
    def delete_info(self) -> None:
        """Delete owner information (reset to defaults)"""
        self.name = ""
        self.age = 0
        self.address = ""


@dataclass
class Pet:
    """Represents a pet"""
    name: str
    breed: str
    age: int
    gender: str
    owner: Owner = None
    
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
    
    def delete_info(self) -> None:
        """Delete pet information (reset to defaults)"""
        self.name = ""
        self.breed = ""
        self.age = 0
        self.gender = ""


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


@dataclass
class Plan:
    """Creates and manages optimized schedules"""
    tasks: List[Task] = field(default_factory=list)
    
    def create_plan(self, schedule: Schedule) -> None:
        """Create an optimized plan from a schedule"""
        # Sort tasks by priority (high > medium > low) and then by duration
        priority_order = {Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}
        self.tasks = sorted(
            schedule.tasks,
            key=lambda t: (-priority_order[t.priority], t.duration_minutes)
        )
