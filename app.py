import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
# --- Session State Setup (App Memory) ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Abigail")  # you can change name later

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

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
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

# If user changes owner name, keep the same Owner object but update its name
st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=50, value=2)

if st.button("Add pet"):
    if pet_name.strip() == "":
        st.error("Please enter a pet name.")
    else:
        new_pet = Pet(name=pet_name.strip(), species=species, age=int(age))
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet: {new_pet.name}")

st.markdown("### Your Pets")
if not st.session_state.owner.pets:
    st.info("No pets added yet.")
else:
    for p in st.session_state.owner.pets:
        st.write(f"• {p.name} ({p.species}, age {p.age})")


pets = st.session_state.owner.pets
selected_pet = None

if pets:
    pet_names = [p.name for p in pets]
    selected_pet_name = st.selectbox("Assign tasks to which pet?", pet_names, key="task_pet_selector")

    selected_pet = next(p for p in pets if p.name == selected_pet_name)
else:
    st.warning("Add a pet first to assign tasks.")
pets = st.session_state.owner.pets
selected_pet = None

if pets:
    pet_names = [p.name for p in pets]
    selected_pet_name = st.selectbox("Assign tasks to which pet?", pet_names)
    selected_pet = next(p for p in pets if p.name == selected_pet_name)
else:
    st.warning("Add a pet first to assign tasks.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not st.session_state.owner.pets:
        st.error("Please add at least one pet first.")
    elif not st.session_state.tasks:
        st.error("Please add at least one task first.")
    elif selected_pet is None:
        st.error("Please select a pet to assign tasks to.")
    else:
        # Prevent duplicate tasks every time you click generate
        selected_pet.tasks = []

        # Convert UI dict tasks into Task objects
        for i, t in enumerate(st.session_state.tasks):
            # simple times: 09:00, 09:30, 10:00...
            hour = 9 + (i // 2)
            minute = "00" if i % 2 == 0 else "30"
            time_str = f"{hour:02d}:{minute}"

            task_obj = Task(
                description=f"{t['title']} (priority: {t['priority']}, {t['duration_minutes']} min)",
                time=time_str,
                frequency="once",
            )
            selected_pet.add_task(task_obj)

        # Run scheduler
        all_tasks = st.session_state.scheduler.get_today_tasks(st.session_state.owner)
        sorted_tasks = st.session_state.scheduler.sort_tasks(all_tasks)
        conflicts = st.session_state.scheduler.detect_conflicts(sorted_tasks)

        st.subheader("Generated Schedule")
        for task in sorted_tasks:
            status = "✅" if task.completed else "⬜"
            st.write(f"{status} {task.time} — {task.description} [{task.frequency}]")

        if conflicts:
            st.warning("Conflicts detected:")
            for t1, t2 in conflicts:
                st.write(f"• {t1.time}: {t1.description} ↔ {t2.description}")
        else:
            st.success("No conflicts detected.")
