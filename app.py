import streamlit as st
from pawpal_system import Pet, Task, Schedule, Priority, Owner, Frequency
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialize session state for owner, pet, and tasks
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, 30, "123 Main St")

if "pet" not in st.session_state:
    st.session_state.pet = Pet(pet_name, species, 5, "Unknown")
    st.session_state.owner.add_pet(st.session_state.pet)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "schedule" not in st.session_state:
    st.session_state.schedule = None

# Update owner/pet if names change
st.session_state.owner.name = owner_name
st.session_state.pet.name = pet_name
st.session_state.pet.breed = species

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

if st.button("Add task"):
    priority_val = Priority.HIGH if priority == "high" else Priority.MEDIUM if priority == "medium" else Priority.LOW
    freq_val = Frequency.ONCE if frequency == "once" else Frequency.DAILY if frequency == "daily" else Frequency.WEEKLY
    new_task = Task(task_title, int(duration), priority_val, frequency=freq_val)
    st.session_state.pet.add_task(new_task)
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority, "frequency": frequency}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    
    # Sorting and filtering controls
    col_sort, col_filter = st.columns(2)
    
    with col_sort:
        st.subheader("Sort Tasks")
        sort_by = st.selectbox("Sort by:", ["None", "Priority", "Duration", "Frequency"], key="sort_by")
        sort_order = st.radio("Order:", ["Ascending", "Descending"], key="sort_order", horizontal=True)
    
    with col_filter:
        st.subheader("Filter Tasks")
        filter_priority = st.multiselect("Priority:", ["low", "medium", "high"], default=["low", "medium", "high"], key="filter_priority")
        filter_frequency = st.multiselect("Frequency:", ["once", "daily", "weekly"], default=["once", "daily", "weekly"], key="filter_frequency")
    
    # Process tasks for display
    display_tasks = st.session_state.tasks.copy()
    
    # Apply filters
    if filter_priority:
        display_tasks = [t for t in display_tasks if t["priority"] in filter_priority]
    if filter_frequency:
        display_tasks = [t for t in display_tasks if t["frequency"] in filter_frequency]
    
    # Apply sorting
    if sort_by != "None":
        reverse = sort_order == "Descending"
        if sort_by == "Priority":
            priority_order = {"low": 1, "medium": 2, "high": 3}
            display_tasks.sort(key=lambda x: priority_order[x["priority"]], reverse=reverse)
        elif sort_by == "Duration":
            display_tasks.sort(key=lambda x: x["duration_minutes"], reverse=reverse)
        elif sort_by == "Frequency":
            freq_order = {"once": 1, "daily": 2, "weekly": 3}
            display_tasks.sort(key=lambda x: freq_order[x["frequency"]], reverse=reverse)
    
    # Display filtered and sorted tasks
    if display_tasks:
        st.table(display_tasks)
        st.success(f"Showing {len(display_tasks)} of {len(st.session_state.tasks)} tasks")
    else:
        st.warning("No tasks match the current filters.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    # Create schedule and add pet tasks
    schedule = Schedule()
    for task in st.session_state.pet.tasks:
        schedule.add_task(task)
    
    # Generate optimized plan (sort by priority then duration)
    schedule.create_plan()
    
    # Assign start times starting from 8:00 AM
    assignment_warnings = schedule.assign_start_times(8, 0)
    
    # Check for conflicts and warnings
    warnings = schedule.get_warnings()
    
    st.session_state.schedule = schedule
    st.session_state.owner.add_schedule(schedule)
    
    st.success(f"Schedule generated for {st.session_state.pet.name}!")
    
    # Display schedule details
    st.write("### Optimized Schedule")
    st.write(f"**Pet:** {st.session_state.pet.name} ({st.session_state.pet.breed})")
    st.write(f"**Total Tasks:** {st.session_state.pet.task_counter}")
    
    # Schedule sorting and filtering controls
    col_sched_sort, col_sched_filter = st.columns(2)
    
    with col_sched_sort:
        schedule_sort = st.selectbox("Sort schedule by:", ["Default (Priority)", "Duration", "Start Time"], key="schedule_sort")
    
    with col_sched_filter:
        schedule_filter_status = st.multiselect("Show tasks:", ["Pending", "Completed"], default=["Pending", "Completed"], key="schedule_filter")
        schedule_filter_priority = st.multiselect("Priority:", ["HIGH", "MEDIUM", "LOW"], default=["HIGH", "MEDIUM", "LOW"], key="schedule_filter_priority")
    
    # Prepare schedule data for display
    schedule_data = []
    for i, task in enumerate(schedule.tasks, 1):
        start_str = task.start_time.strftime("%H:%M") if task.start_time else "Not scheduled"
        end_str = task.end_time.strftime("%H:%M") if task.end_time else "N/A"
        freq_str = task.frequency.value
        status = "Completed" if task.completed else "Pending"
        
        schedule_data.append({
            "Task": task.title,
            "Duration (min)": task.duration_minutes,
            "Priority": task.priority.name,
            "Frequency": freq_str,
            "Start Time": start_str,
            "End Time": end_str,
            "Status": status
        })
    
    # Apply filters
    if schedule_filter_status:
        schedule_data = [t for t in schedule_data if t["Status"] in schedule_filter_status]
    if schedule_filter_priority:
        schedule_data = [t for t in schedule_data if t["Priority"] in schedule_filter_priority]
    
    # Sort schedule data
    if schedule_sort == "Duration":
        schedule_data.sort(key=lambda x: x["Duration (min)"])
    elif schedule_sort == "Start Time":
        # Sort by start time, handling "Not scheduled"
        schedule_data.sort(key=lambda x: (x["Start Time"] == "Not scheduled", x["Start Time"]))
    
    # Display as table
    if schedule_data:
        st.table(schedule_data)
        st.success(f"Showing {len(schedule_data)} scheduled tasks")
    else:
        st.warning("No tasks match the current schedule filters.")
    
    # Display warnings and conflicts
    if warnings:
        st.write("### Schedule Warnings")
        for warning in warnings:
            if warning.severity == "error":
                st.error(f"🚫 {warning.message}")
            elif warning.severity == "warning":
                st.warning(f"⚠️ {warning.message}")
            else:
                st.info(f"ℹ️ {warning.message}")
    
    # Show conflict summary
    conflict_summary = schedule.get_conflict_summary()
    if conflict_summary:
        st.write("### Conflict Summary")
        st.code(conflict_summary, language="text")
    
    # Option to resolve conflicts if any
    if schedule.has_conflicts():
        if st.button("Resolve Conflicts"):
            success, resolve_warnings = schedule.resolve_overlaps()
            if success:
                st.success("Conflicts resolved! Schedule updated.")
                # Re-display the updated schedule
                st.rerun()
            else:
                st.error("Could not fully resolve conflicts. Manual adjustment needed.")
                for w in resolve_warnings:
                    if w.severity == "error":
                        st.error(f"🚫 {w.message}")
                    elif w.severity == "warning":
                        st.warning(f"⚠️ {w.message}")
                    else:
                        st.info(f"ℹ️ {w.message}")

st.divider()

st.subheader("Mark Tasks Complete")
st.caption("Mark completed tasks to handle recurring ones.")

if st.session_state.schedule and st.session_state.schedule.tasks:
    incomplete_tasks = [i for i, task in enumerate(st.session_state.schedule.tasks) if not task.completed]
    if incomplete_tasks:
        # Show pending tasks in a table
        pending_data = []
        for idx in incomplete_tasks:
            task = st.session_state.schedule.tasks[idx]
            start_str = task.start_time.strftime("%H:%M") if task.start_time else "Not scheduled"
            end_str = task.end_time.strftime("%H:%M") if task.end_time else "N/A"
            pending_data.append({
                "Task": task.title,
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority.name,
                "Frequency": task.frequency.value,
                "Start Time": start_str,
                "End Time": end_str
            })
        
        st.write("Pending tasks:")
        st.table(pending_data)
        
        # Completion interface
        task_options = [f"{i+1}. {st.session_state.schedule.tasks[i].title}" for i in incomplete_tasks]
        selected_task = st.selectbox("Select task to mark complete:", task_options, key="complete_task")
        if selected_task and st.button("Mark Complete", key="mark_complete"):
            task_index = incomplete_tasks[int(selected_task.split('.')[0]) - 1]
            st.session_state.schedule.mark_task_complete(task_index)
            st.success(f"Task '{st.session_state.schedule.tasks[task_index].title}' marked complete!")
            if st.session_state.schedule.tasks[task_index].frequency != Frequency.ONCE:
                st.info("Recurring task: Next occurrence created.")
            st.rerun()
    else:
        st.success("All tasks are completed!")
else:
    st.info("Generate a schedule first.")
