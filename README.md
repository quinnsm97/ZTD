# ZTD- CLI Task Manager

ZTD is a command-line to-do list manager based on the **Zen To Done (ZTD)** methodology developed by Leo Babauta. This tool is designed for productivity and simplicity, with support for priorities, categories, recurring tasks, and more. 

---

## Features

The app runs in the Command Line Interface (CLI) and has the following features: 

* Add tasks with categories (`@category`), priorities (`!urgent`), and recurrence (`~daily`)
* View/sort tasks by category
* Mark tasks as done 
* Delete single or multiple tasks
* Set or update priorities, categories, recurrence
* Save/load tasks from JSON file
* Natural language date parsing for scheduling
* For recurring tasks, automatically re-adds recurring tasks (daily/weekly/monthly) on the appropriate date  
* When a new task is added, blank [category] and (-) priority spaces are retained. This is intentional to prompt the user to manually add category and priority.
---

## Installation

Prior to running the app, the following third party tools should be installed by using the following code in the terminal: 
    
    `pip install schedule dateparser rich
    `

---

## Usage

To run the app for the first time, run the following code: 
    
    `python ztd_cli.py  
    `

Then interact using commands like: 
    
    `add email boss @work !urgent ~daily  
    list  
    done 2  
    category 1 2 work  
    recur 1 daily  
    priority 1 urgent  
    `delete 1,2

These commands have been designed to be as shorthand as possible to maximise speed and efficiency. For this reason, it is important that the commands are written accurately with no errors.

---

## Commands
Command
Description
`add`
Add tasks with optional `@category`, `!priority`, and `~recurrence `
list
Show all tasks
`done <task#>`
Mark task(s) as complete
`undo <task#>`
Undo completed task(s)
`delete <task#>`
Delete task(s)
`category <#> <category>`
Assign task(s) to a category
`priority <#> <priority>`
Set priority (`urgent`, `today`, etc.)
`recur <#> <interval>`
Set task recurrence (`daily`, `weekly`, `monthly`)
`categories`
Show tasks by category
`showdone`
Show completed tasks
`help`
Show help menu
`save`
Save task files manually
`exit`
Save and exit the app

---

## File Structure

* `tasks.json`: stores active tasks
* `done_tasks.json`: stores completed tasks

---

## Dependencies

These are three third party software that have their own license. 

### 1\. [`schedule`](https://pypi.org/project/schedule/)
Copyright: © 2015–present Dan Bader

* **Purpose:** Handles recurring task scheduling.
* **License:** MIT License 
* **Summary:** Allows free use, distribution, and modification with attribution.

### 2\. [`dateparser`](https://pypi.org/project/dateparser/)
Copyright: © 2014–present Scrapinghub

* **Purpose:** Parses natural language dates like "next Friday".
* **License:** BSD 3-Clause License 
* **Summary:** Permits redistribution and modification with credit; no endorsement allowed.

### 3\. [`rich`](https://pypi.org/project/rich/)
Copyright: © 2020–present Will McGugan

* **Purpose:** Enhances terminal output with colors, tables, and styled text for improved readability and accessibility.
* **License:** MIT License 
* **Summary:** Permits reuse, modification, and distribution with attribution. Encourages ethical open-source contribution and improves user experience in CLI applications.

---

## Ethical and Legal Considerations

Here are some of the main ethical and legal considerations for the third party licenses/software used for this tool. 

* **Open Source Attribution:** All third-party libraries selected for this project are open-source and included under valid licenses (MIT, BSD).
* **Usage Boundaries:** Third party Libraries are used non-commercially and legally, without modification or redistribution outside this project.
* **Transparency:** This README file includes full disclosure of dependencies and license compliance. This is intended to foster Transparency which is an important ethical principle. 

---

## Thank you

This software was created by Vikashan Thayanithy as part of the CoderAcademy Web Development Bootcamp-  Python Module.