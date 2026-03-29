#!/usr/bin/env python3
"""
Performance comparison of overlap detection algorithms
"""

from pawpal_system import Schedule, Task, Priority
from datetime import time
import time as time_module

def create_test_schedule(num_tasks: int) -> Schedule:
    """Create a schedule with many tasks for performance testing"""
    schedule = Schedule()

    for i in range(num_tasks):
        task = Task(
            title=f"Task {i}",
            duration_minutes=30,
            priority=Priority.MEDIUM
        )
        # Assign random start times to create potential overlaps
        hour = (i * 7) % 24  # Spread tasks throughout the day
        task.start_time = time(hour, 0)
        schedule.add_task(task)

    return schedule

def performance_test():
    print("⚡ Overlap Detection Performance Test")
    print("=" * 40)

    test_sizes = [10, 50, 100, 200]

    for num_tasks in test_sizes:
        print(f"\n🧪 Testing with {num_tasks} tasks:")

        # Create test schedule
        schedule = create_test_schedule(num_tasks)

        # Time the overlap detection
        start_time = time_module.time()
        for _ in range(10):  # Run multiple times for better measurement
            overlaps = schedule.detect_overlaps()
        end_time = time_module.time()

        avg_time = (end_time - start_time) / 10
        conflicts_found = len(overlaps)

        print(".6f")
        print(f"   Conflicts detected: {conflicts_found}")

        # Test warning system performance
        start_time = time_module.time()
        for _ in range(10):
            warnings = schedule.get_warnings()
            has_conflicts = schedule.has_conflicts()
        end_time = time_module.time()

        avg_warning_time = (end_time - start_time) / 10
        print(".6f")

if __name__ == "__main__":
    performance_test()