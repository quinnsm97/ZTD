# ZTD - CLI Task Manager

ZTD is a command-line to-do list manager based on the **Zen To Done (ZTD)** methodology developed by **Leo Babauta**.  
This tool is designed for **productivity** and **simplicity**, with support for priorities, categories, recurring tasks, and more.

---

## Features

The app runs in the Command Line Interface (CLI) and has the following features:

- Add tasks with categories (`@category`), priorities (`!urgent`), and recurrence (`~daily`)
- View/sort tasks by category
- Mark tasks as done
- Delete single or multiple tasks
- Set or update priorities, categories, recurrence
- Save/load tasks from JSON file
- Natural language date parsing for scheduling
- For recurring tasks, automatically re-adds recurring tasks (daily/weekly/monthly) on the appropriate date
- When a new task is added, blank `[category]` and `(-)` priority spaces are retained to prompt the user to manually add them

---

## System Requirements

- **Python** 3.10 or later  
- **Operating System:** macOS, Windows, or Linux  
- **Interface:** Command Line (Terminal or PowerShell)

---

## Installation

1. **Clone the repository** or download the source code.
2. Ensure you have **Python 3.10+** installed.
3. *(Optional but recommended)* Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
4. Install required third-party tools:
   ```bash
   pip install schedule dateparser rich
   ```

---

## Usage

To run the app for the first time:

```bash
python 'ZTD_APP_CODE.py'
```

Example commands:

```bash
add email boss @work !urgent ~daily
list
done 2
category 1 2 work
recur 1 daily
priority 1 urgent
delete 1,2
```

Commands are designed to be shorthand for speed and efficiency.  
They must be typed accurately to work correctly.

---

## Commands

### Task Management
- `add <task description>` — Add a new task. Add multiple with commas.  
  Example:  
  ```bash
  add email boss @work !urgent ~daily ^tomorrow
  ```
- `list` — Show all tasks.  
- `done <task_id#>` — Mark a task as completed.  
- `delete <task_id#> <task_id#> ...` — Delete one or more tasks.  
- `move <from> <to>` — Move a task from one position to another.

### Task Details
- `priority <task_id#> <priority>` — Set priority (`urgent`, `today`, `tomorrow`, `later`).  
- `category <task_id#> <category>` — Set category.  
- `recur <task_id#> <frequency>` — Set recurrence (`daily`, `weekly`, `monthly`).  
- `duedate <task_id#> <due date>` — Set or update due date.  
  Example:  
  ```bash
  duedate 2 4/9/25
  ```

### Filtering & Views
- `showdone` — View completed tasks.  
- `categories` — View tasks grouped by category.

### Other
- `save` — Save tasks manually.  
- `help` — Show help message.  
- `exit` — Save and exit the program.

---

## Notes
- Tasks are saved to `tasks.json`  
- Completed tasks are saved to `done_tasks.json`  
- Recurring tasks reappear based on the **last completed date**  
- Supports natural language due dates like `^tomorrow` or `^06/10/25`

---

## File Structure
- **tasks.json** — Stores active tasks  
- **done_tasks.json** — Stores completed tasks  

---

## Dependencies

This project uses the following third-party libraries:

### 1\. [`schedule`](https://pypi.org/project/schedule/)
   - **Copyright:** © 2015–present Dan Bader  
   - **Purpose:** Handles recurring task scheduling.  
   - **License:** MIT License  
   - **Summary:** Allows free use, distribution, and modification with attribution.

### 2\. [`dateparser`](https://pypi.org/project/dateparser/)
   - **Copyright:** © 2014–present Scrapinghub  
   - **Purpose:** Parses natural language dates like `"next Friday"`.  
   - **License:** BSD 3-Clause License  
   - **Summary:** Permits redistribution and modification with credit; no endorsement allowed.

### 3\. [`rich`](https://pypi.org/project/rich/)
   - **Copyright:** © 2020–present Will McGugan  
   - **Purpose:** Enhances terminal output with colors, tables, and styled text.  
   - **License:** MIT License  
   - **Summary:** Permits reuse, modification, and distribution with attribution. Improves user experience in CLI apps.

---

## Ethical and Legal Considerations

Here are some of the main ethical and legal considerations for the third party licenses/software used for this tool. 

* **Open Source Attribution:** All third-party libraries selected for this project are open-source and included under valid licenses (MIT, BSD).
* **Usage Boundaries:** Third party Libraries are used non-commercially and legally, without modification or redistribution outside this project.
* **Transparency:** This README file includes full disclosure of dependencies and license compliance. This is intended to foster Transparency which is an important ethical principle. 

---

## Additional Documentation

For more details on privacy and security practices for ZTD, please refer to:

- [SECURITY.md](./SECURITY.md) — Information about data storage, limitations, and how to encrypt your task data.
- [PRIVACY.md](./PRIVACY.md) — Details on how ZTD stores, deletes, and backs up your data.

---

## Thank You

This software was created by **Vikashan Thayanithy** as part of the *CoderAcademy Web Development Bootcamp — Python Module*.
