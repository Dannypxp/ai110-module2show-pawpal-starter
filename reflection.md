# PawPal+ Project Reflection

## 1. System Design

Three Core actions
1. Add pet info
2. Add Owner Info
3. Make a task with time and priority

Objects Needed 
1. Owner
    A - Name, Age, Address
    M - Enter info, Edit info, Delete info
2. Pet
    A - Name, Breed, Age, Gender
    M - Enter info, Edit info, Delete info
3. Schedule
    A - Task
    M - Add Task, Modify Task, Remove Task, Add Priority, create plan
4. Task
    A - Title, Priority, duration
    M - 
**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design contains 4 classes (Owner, Pet, Schedule, Task) Pet belongs to owner, schedule belongs to owner, task belongs to schedule
- What classes did you include, and what responsibilities did you assign to each?
4 Classes
Owner class holds basic info about the owner and lets them edit or add their info to their profile in the app
Pet class holds basic info about the owners pet and allows the owner to change or add info
Schedule class allows for tasks to be created and edited, included are priorities on those tasks, and a plan can be created
Task class hold the name, duration and priority of those tasl
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
