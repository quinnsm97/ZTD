# ZTD APP - a Zen to Done Command Line Interface app
# Before running, pip install -r requirements.txt
# run python from virtual environment where packages are installed
import os
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
import dateparser
from rich import print
from rich.console import Console
from rich.table import Table
import schedule
import threading
import time

TASKS_FILE = "tasks.json"
DONE_FILE = "done_tasks.json"

tasks = []
completed_tasks = []
console = Console()

# === CLEAR TERMINAL ===
def clear_terminal():
	"""
	Clears the terminal.

    This function clears all prior output displayed in the terminal, providing a clean space to load the CLI Task manager.

    On windows, the function runs 'cls' command.
    On MacOS/Linux/WSL, the function runs 'clear' command.
    """

	os.system('cls' if os.name == 'nt' else 'clear')
clear_terminal()

# === LOAD AND SAVE TASKS ===
def load_tasks():
    """
    Load tasks and completed tasks - from JSON files.

    Loads data from TASKS_FILE into a global 'tasks' list
    and from DONE_FILE into a global 'completed_tasks' list.
    If the files do not exist or if they contain invalid data, lists are reset to empty.
    """

    global tasks, completed_tasks
    try:
        with open(TASKS_FILE, "r") as f:
            tasks = json.load(f)
    except:
        tasks = []
    try:
        with open(DONE_FILE, "r") as f:
            completed_tasks = json.load(f)
    except:
        completed_tasks = []

def save_tasks():
    """
    Save the current lists of tasks and completed tasks to the JSON files in the main folder.

    Side Effects:
        Overwrites the TASKS_FILE and DONE_FILE with current in-memory task data.
    """

    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
    with open(DONE_FILE, "w") as f:
        json.dump(completed_tasks, f, indent=2)

# === FUNCTIONS ABOUT DISPLAY ===
def show_tasks():
    """
    Display all current active tasks in a formatted table.

    Shows task number, category, description, priority,
    recurrence, and due date for each task.

    If a column is left blank it will display '-' 
    """
          
    table = Table(title="Your Tasks")
    table.add_column("#", style="cyan")
    table.add_column("Category", style="green")
    table.add_column("Description", style="white")
    table.add_column("Priority", style="magenta")
    table.add_column("Recurring", style="yellow")
    table.add_column("Due", style="red")

    for idx, task in enumerate(tasks, start=1):
        cat = task['category'] if task['category'] else "-"
        desc = task['description']
        prio = task['priority'] if task['priority'] else "-"
        recur = task['recurring'] if task.get('recurring') else "-"
        due = task['due'] if task.get('due') else "-"
        table.add_row(str(idx), cat, desc, prio, recur, due)
    console.print(table)

def show_done_tasks():
    """
    Display all completed tasks in a formatted table.

    Shows:
        - Task number
        - Category (or '-' if none)
        - Description
        - Priority (or '-' if none)

    Application currently uses rich to colour-code the sections. 
    """

    table = Table(title="Completed Tasks")
    table.add_column("#", style="cyan")
    table.add_column("Category", style="green")
    table.add_column("Description", style="white")
    table.add_column("Priority", style="magenta")

    for idx, task in enumerate(completed_tasks, start=1):
        cat = task['category'] if task['category'] else "-"
        prio = task['priority'] if task['priority'] else "-"
        table.add_row(str(idx), cat, task['description'], prio)
    console.print(table)

def show_tasks_by_category():
    """
    Display active tasks grouped by category in formatted tables.

    Groups tasks by their category field, defaulting to "Uncategorized"
    when no category is set.
    """

    grouped = defaultdict(list)
    for task in tasks:
        grouped[task.get("category", "").strip() or "Uncategorized"].append(task)

    for cat, cat_tasks in grouped.items():
        print(f"\n[bold underline green]{cat}[/bold underline green]")
        table = Table()
        table.add_column("#", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Priority", style="magenta")
        table.add_column("Recurring", style="yellow")
        table.add_column("Due", style="red")

        for idx, task in enumerate(cat_tasks, start=1):
            desc = task['description']
            prio = task.get('priority', '-') or "-"
            recur = task.get('recurring', '-') or "-"
            due = task.get('due', '-') or "-"
            table.add_row(str(idx), desc, prio, recur, due)
        console.print(table)

# === FN FOR ADDING TASKS ===
def add_task_with_category(input_str):
    """
    Parse and add one or more tasks from a single input string.

    The input can include optional inline metadata:
        @category   → task category
        !priority   → urgency (urgent, today, tomorrow, later)
        ~recurring  → recurrence pattern (daily, weekly, monthly)
        ^due date   → natural language date (parsed via dateparser - currently only supports DD/MM/YYYY Format

    Example:    "Buy milk @Groceries !today ^22/10/2025, Write report @Work !urgent ~weekly"

    Side Effects:
        Adds parsed tasks to the global 'tasks' list and saves changes to file. 
    """

    tasks_raw = [t.strip() for t in input_str.split(",") if t.strip()]
    pattern = r"(?P<desc>.+?)(?:\s+@(?P<cat>[^!~^]+))?(?:\s*!\s*(?P<prio>urgent|today|tomorrow|later))?(?:\s*~\s*(?P<recur>daily|weekly|monthly))?(?:\s*\^\s*(?P<due>.+))?$"

    for task_raw in tasks_raw:
        match = re.match(pattern, task_raw.strip(), re.IGNORECASE)
        if match:
            desc = match.group("desc").strip()
            cat = (match.group("cat") or "").strip()
            prio = (match.group("prio") or "").strip()
            recur = (match.group("recur") or "").strip()
            due_text = (match.group("due") or "").strip()
        else:
            desc = task_raw.strip()
            cat = ""
            prio = ""
            recur = ""
            due_text = ""

        due = None
        if due_text:
            parsed = dateparser.parse(due_text)
            if parsed:
                due = parsed.strftime("%Y-%m-%d")

        task = {
            "description": desc,
            "category": cat,
            "priority": prio,
            "recurring": recur,
            "due": due
        }
        print(f"[bold green]Added:[/bold green] [{cat or '-'}] {desc} ({prio or '-'}){' ~ ' + recur if recur else ''}{' ^ ' + due if due else ''}")
        tasks.append(task)
        save_tasks()

# === FN FOR DELETING TASKS ===
def delete_tasks(input_str):
    """
    Delete one or more tasks by their numeric index.

    Side Effects:
        Removes specified tasks from the global 'tasks' list and saves changes.
    """

    try:
        indices = sorted({int(i) for i in input_str.strip().split()}, reverse=True)
        for i in indices:
            if 1 <= i <= len(tasks):
                removed = tasks.pop(i - 1)
                print(f"[red]Deleted:[/red] {removed['description']}")
            else:
                print(f"[yellow]Task {i} does not exist.[/yellow]")
        save_tasks()
    except ValueError:
        print("[red]Please enter valid task numbers separated by spaces.[/red]")

# === FN FOR MARKING TASKS AS DONE ===
def mark_done(input_str):
    """
    Mark one or more tasks as completed.

    Moves specified tasks from 'tasks' to 'completed_tasks'.
    For recurring tasks, records the date they were last completed.
    """

    try:
        indices = sorted({int(i) for i in input_str.strip().split()}, reverse=True)
        for i in indices:
            if 1 <= i <= len(tasks):
                task = tasks.pop(i - 1)
                if task.get("recurring"):
                    task["last_done"] = datetime.today().strftime("%Y-%m-%d")
                completed_tasks.append(task)
                print(f"[bold green]Marked as done:[/bold green] {task['description']}")
            else:
                print(f"[yellow]Task {i} does not exist.[/yellow]")
        save_tasks()
    except ValueError:
        print("[red]Please enter valid task numbers separated by spaces.[/red]")

# === MOVING TASKS ===
def move_task(input_str):
    """
    Move a task from one position in the task list to another.

    Expects two integers: the current position (task number) and the target position (what you want the task number to be). 
    """

    try:
        from_pos, to_pos = map(int, input_str.strip().split())
        if 1 <= from_pos <= len(tasks) and 1 <= to_pos <= len(tasks):
            task = tasks.pop(from_pos - 1)
            tasks.insert(to_pos - 1, task)
            print(f"[green]Moved task from position {from_pos} to {to_pos}.[/green]")
            save_tasks()
        else:
            print("[red]Invalid task numbers.[/red]")
    except ValueError:
        print("[red]Usage: move <from_position> <to_position>[/red]")

# === FN TO SET PRIORITY ON TASKS ===
def set_priority_command(input_str):
    """
    Set the priority of one or more tasks.

    Expects: the task number and the priority it should be - for example, 'priority <task_numbers> <priority_level>'.
    """

    try:
        parts = input_str.split()
        priority = parts[-1].lower()
        indices = [int(i) for i in parts[1:-1]]
        for i in indices:
            if 1 <= i <= len(tasks):
                tasks[i - 1]['priority'] = priority
                print(f"[bold green]Set priority:[/bold green] Task {i} -> {priority}")
            else:
                print(f"[yellow]Task {i} not found.[/yellow]")
        save_tasks()
    except Exception:
        print("[red]Usage: priority <task_id#> <priority>[/red]")

#== FN TO UPDATE DUE DATE OF TASKS
def set_due_date_command(input_str):
    """
    Set or update the due date for a specific task.

    Parses natural language dates using the dateparser library.
    """

    try:
        parts = input_str.strip().split()
        task_id = int(parts[0])
        due_text = " ".join(parts[1:])
        parsed = dateparser.parse(due_text)

        if not parsed:
            print(f"[red]Could not parse due date from: '{due_text}'[/red]")
            return

        due_date = parsed.strftime("%Y-%m-%d")

        if 1 <= task_id <= len(tasks):
            tasks[task_id - 1]["due"] = due_date
            print(f"[bold green]Set due date:[/bold green] Task {task_id} -> {due_date}")
        else:
            print(f"[yellow]Task {task_id} not found.[/yellow]")
        save_tasks()
    except Exception as e:
        print(f"[red]Usage: duedate <task_id#> <due date>[/red]")

# === FN TO SET CATEGORY ON TASKS ===
def set_category_command(input_str):
    """
    Assign a category to one or more tasks.

    Expects: 'category <task_numbers> <category>'.
    """

    try:
        parts = input_str.split()
        category = parts[-1]
        indices = [int(i) for i in parts[1:-1]]
        for i in indices:
            if 1 <= i <= len(tasks):
                tasks[i - 1]['category'] = category
                print(f"[bold green]Set category:[/bold green] Task {i} -> {category}")
            else:
                print(f"[yellow]Task {i} not found.[/yellow]")
        save_tasks()
    except Exception:
        print("[red]Usage: category <task_id#> <category>[/red]")

# === FN TO SET RECURRENCE ON TASKS ===
def set_recur_command(input_str):
    """
    Set the recurrence pattern for one or more tasks.

    Expects: 'recur <task_numbers> <daily|weekly|monthly>'.
    """

    try:
        parts = input_str.split()
        recurrence = parts[-1].lower()
        indices = [int(i) for i in parts[1:-1]]
        for i in indices:
            if 1 <= i <= len(tasks):
                tasks[i - 1]['recurring'] = recurrence
                print(f"[bold green]Set recurrence:[/bold green] Task {i} -> {recurrence}")
            else:
                print(f"[yellow]Task {i} not found.[/yellow]")
        save_tasks()
    except Exception:
        print("[red]Usage: recur <task_id#> <daily|weekly|monthly>[/red]")

# === FN TO SHOW TASKS BY CATEGORY ===
def show_tasks_by_category():
    """
    Print a simple list of tasks grouped by category.

    Displays category headers followed by numbered tasks with priorities.
    """

    category_map = defaultdict(list)
    for i, task in enumerate(tasks, start=1):
        category = task.get("category") or "-"
        category_map[category].append((i, task))

    for cat, entries in category_map.items():
        print(f"\n[bold cyan]Category: {cat}[/bold cyan]")
        for idx, task in entries:
            prio = task.get("priority") or "-"
            desc = task['description']
            print(f"{idx}. {desc} ({prio})")

# === FNs FOR SCHEDULED REMINDER ===
def scheduled_reminder():
    """
    Display a reminder message in the console.
    """

    print("[bold blue]\U0001F4A1 Reminder: Don't forget to review your tasks today![/bold blue]")

def start_scheduler():
    """
    Start a background scheduler that triggers reminders periodically.

    Side Effects:
        Runs an infinite loop in a background thread to execute scheduled jobs.

        Currently set to default of 86400 seconds or 24 hours. 
    """

    schedule.every(86400).seconds.do(scheduled_reminder)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduler in background
threading.Thread(target=start_scheduler, daemon=True).start()

# === HELP MENU CLASS ===

class HelpMenu:
    """
    This class stores the name of the app and displays the CLI help menu for the ZTD Task Manager 
    when requested(by entering `help` into the command line).
    """

    def __init__(self, app_name="Zen To Done (ZTD) CLI Task Manager"):
        self.app_name = app_name
        """
        Initialises HelpMenu class with custom application name
        """

    def show(self):
        """
        Print's help command text in the terminal. Help commands are listed with an explanation
        """
        
        print(f"""
Welcome to the {self.app_name}!
        
Commands:
---------
Task Management:
- add <task description>                  : Add a new task. Add multiple with commas. Example: add email boss @work !urgent ~daily ^tomorrow
- list                                    : Show all tasks.
- done <task_id#>                         : Mark a task as completed.
- delete <task_id#> <task_id#> ...        : Delete one or more tasks.
- move <from> <to>                        : Move task from one position to another.

Task Details:
- priority <task_id#> <priority>          : Set priority (urgent, today, tomorrow, later).
- category <task_id#> <category>          : Set category.
- recur <task_id#> <frequency>            : Set recurrence (daily, weekly, monthly).
- duedate <task_id#> <due date>           : Set or update due date (e.g., duedate 2 next Friday)

Filtering & Views:
- showdone                                : View completed tasks.
- categories                              : View tasks grouped by category
- later <task_id# ...>                    : Move task to Later list.
- showlater                               : View tasks saved for later.

Other:
- save                                    : Save tasks manually.
- help                                    : Show this help message.
- exit                                    : Save and exit the program.

Notes:
- Tasks are saved to tasks.json, done_tasks.json, and later_tasks.json
- Recurring tasks reappear based on last completed date
- Supports natural language due dates using ^tomorrow, ^next Friday, etc.
- Sends periodic reminders to review your task list
""")

# === RUN MAIN LOOP ===
help_menu = HelpMenu()

def run_cli():
    """
    This is the main run loop, it launches the interactive CLI for the Zen to Done Task Manager.

    Currently includes the commands for adding, listing, modifying, deleting,
    and completing tasks. 
    
    Runs until 'exit' is entered.
    """

    load_tasks()
    print("[bold cyan]ZTD CLI Task Manager (type 'help' for options)[/bold cyan]")
    while True:
        console.print("> ", style="bold", end="")
        user_input = input().strip()
        if user_input.lower() == "exit":
            save_tasks()
            print("[bold red]Goodbye![/bold red]")
            break
        elif user_input.lower() == "list":
            show_tasks()
        elif user_input.lower().startswith("add "):
            add_task_with_category(user_input[4:])
        elif user_input.lower() == "showdone":
            show_done_tasks()
        elif user_input.lower().startswith("delete "):
            delete_tasks(user_input[7:])
        elif user_input.lower().startswith("done "):
            mark_done(user_input[5:])
        elif user_input.lower().startswith("move "):
            move_task(user_input[5:])
        elif user_input.lower().startswith("priority "):
            set_priority_command(user_input)
        elif user_input.lower().startswith("category "):
            set_category_command(user_input)
        elif user_input.lower().startswith("duedate "):
            set_due_date_command(user_input[8:])
        elif user_input.lower().startswith("recur "):
            set_recur_command(user_input)
        elif user_input.lower() == "categories":
            show_tasks_by_category()
        elif user_input.lower() == "help":
            help_menu.show()   # Uses the HelpMenu class method
        else:
            print("[yellow]Unknown command. Try: add, list, delete, done, move, priority, category, recur, categories, showdone, help, exit[/yellow]")

def move_task(input_str):
    """
    Move a task from one position in the active task list to another.

    Expects:
        input_str (str): Two integers separated by a space, representing
        the current position of the task and the new desired position.
        Example: "3 1" moves the task at position 3 to position 1.

    Side Effects:
        Reorders the global 'tasks' list and saves the updated order to file.
        Prints a confirmation message or an error if indices are invalid.
    """

    try:
        parts = input_str.strip().split()
        if len(parts) != 2:
            raise ValueError
        from_idx, to_idx = int(parts[0]) - 1, int(parts[1]) - 1
        if 0 <= from_idx < len(tasks) and 0 <= to_idx < len(tasks):
            task = tasks.pop(from_idx)
            tasks.insert(to_idx, task)
            print(f"[bold cyan]Moved:[/bold cyan] {task['description']} from {from_idx+1} to {to_idx+1}")
            save_tasks()
        else:
            print("[red]Invalid indices. Use valid task numbers.[/red]")
    except ValueError:
        print("[red]Usage: move <from> <to>. Example: move 3 1[/red]")

if __name__ == "__main__":
    run_cli()
