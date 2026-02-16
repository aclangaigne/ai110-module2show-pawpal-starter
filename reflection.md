# PawPal+ Project Reflection

## 1. System Design
Add a pet: User can create a pet profile (name/species/age) and store it under their owner account.

Schedule a task: User can add a task (walk, feeding, meds, appointment) to a specific pet with a time + frequency.

View today’s schedule: User can generate a sorted list of all tasks due today across all pets, so they know what to do next.

### Building Blocks (Objects)

**Owner**
- Attributes: name, pets (list of Pet)
- Methods: add_pet(pet), get_all_tasks()

**Pet**
- Attributes: name, species, age, tasks (list of Task)
- Methods: add_task(task), get_tasks()

**Task**
- Attributes: description, time, frequency, completed
- Methods: mark_complete()

**Scheduler**
- Attributes: none required (logic-only)
- Methods: get_today_tasks(owner), sort_tasks(tasks), detect_conflicts(tasks)

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
