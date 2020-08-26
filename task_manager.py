# This program manages tasks entered by the user and are stored in external files

# Built in modules used in the program
from datetime import datetime
from collections import Counter
   
# User defined functions for activities in the task management system

# Register user function - checks if the user exists, stores password and writes to user file
def reg_user():

    user_file = open("user.txt", "r+")
    new = False

    while new == False:
        new_user = input("Please enter the new username: ")
            
        if new_user not in (user_list):
            new = True
        if new_user in (user_list) :
            print("That username is already taken, try another.")
            new = False
        user_file.seek(0)                     
    new_password1 = input("Please enter a password: ")
    new_password2 = input("Please re-enter the password: ")
    while new_password1 != new_password2:
        print("The passwords did not match.")
        new_password1 = input("Please enter a password: ")
        new_password2 = input("Please re-enter the password: ")
    
    user_file = open("user.txt", "a")

    if new_password1 == new_password2:
        user_file.write(f"\n{new_user}, {new_password1}")
    user_file.close()

# Add task function - appends a task entered by the user to the existing task file
def add_task():
    task_file = open("tasks.txt", "a+")
    user = input("Enter the username: ")
    task = input("Enter the name of the task: ")
    task_descrip = input("Enter a description of the task: ")
    day = input("Please enter today's date in the format DD MMM YYYY: ")
    due_date = input("Enter the date that the task is due in the format DD MMM YYYY: ")
    completed = "No"

    task_file.write(f"\n{user}, {task}, {task_descrip}, {day}, {due_date}, {completed}")
    task_file.close()

# View all tasks function - prints out all tasks in the task file by username
def view_all():
    task_file = open("tasks.txt", "r+")
    for line in task_file:
        user, task, task_descrip, today, due_date, completed = line.split(", ")
        print(f"""Username: {user}
Task: {task}
Task Description: {task_descrip}
Start Date: {today}
Due Date: {due_date}
Completed: {completed}""")
    task_file.close()

# View mine function - prints out tasks for one user
def view_mine():
    task_file = open("tasks.txt", "r+")      
    
    for i, line in enumerate(task_file, 1):
        user_task, task, task_descrip, today, due_date, completed = line.split(", ")
        if username == user_task:    
            print(f"""          
Task {i}: {task}
Task Description: {task_descrip}
Start Date: {today}
Due Date: {due_date}
Completed: {completed}""") 

    # For a user selected task edit and write to the task file
    inputNum = int(input("Please enter a task (by number) you'd like to update: "))
    j = inputNum - 1
        
    edit_task = input("""
You can choose to:
c - Mark Task as completed
et - Edit Task

Enter your choice: """)
    edit_task = edit_task.lower()
    edit_task = edit_task.strip(" ")  
    if edit_task == "c":
        completed_list[j] = "Yes"
        print("The task has been marked as completed")
    elif edit_task == "et":
        edit_choice = input("""
Would you like to: 
rt - Reassign this task to a new user
nd - Assign a new due_date to the task: 
""")
        edit_choice = edit_choice.lower()
        edit_choice = edit_choice.strip(" ")
        if edit_choice == "rt":
            user_change = input("Enter the user to which you want to reassign this task: ")
            user_task_list[j] = user_change
        elif edit_choice == "nd":
            due_date_change = input("Enter a new due date for this task in the format DD MMM YYYY: ")
            due_date_list[j] = due_date_change         

    output = ""
    for num in range(total_tasks):
            entry = (f"{user_task_list[num]}, {task_list[num]}, {task_descrip_list[num]}, {today_list[num]}, {due_date_list[num]}, {completed_list[num]}")
            output += entry + "\n"

    task_file = open("tasks.txt", "w+")
    task_file.write(output)  
    
    task_file.close()

# User defined function for generating task and user overview text reports
def gen_rep():  
    task_report = open("task_overview.txt", "w+")
    user_report = open("user_overview.txt", "w+")

    # This calculates elements for the Task Overview file
    total_comp = 0
    total_incomp = 0
    
    today = datetime.now()
    due_dateListformat = [datetime.strptime(day, "%d %b %Y") for day in due_date_list]

    for element in completed_list:
        if element == "Yes":
            total_comp += 1
        else:
            total_incomp += 1       
                
    for completed in completed_list:
        overdue = 0
        for day in due_dateListformat:
            if day < today and completed == "No":
                overdue += 1
    per_overdue = (overdue/total_tasks* 100)
    per_incomplete = (total_incomp/ total_tasks * 100)

    task_report.write(f"""Statistical Task Report (Generated {today})
Total number of tasks: {total_tasks}
Total number of completed tasks: {total_comp}
Total number of incomplete tasks: {total_incomp}
Total number of incompleted tasks that are overdue: {overdue}
Percentage of tasks that are overdue: {round(per_overdue, 2)}%
Percentage of tasks that are incomplete: {round(per_incomplete, 2)}%
""")
        
    # This determines the elements for the User Overview Report
        
    # Determines percentage of user tasks that are (in)completed, overdue using a counter stored in dictionaries
    userNum = len(user_list)
    user_report.write(f"""Statistical User Report (Generated {today})
Total number of users: {userNum}
Total number of tasks: {total_tasks}\n""")     
        
    user_taskNum = Counter(user_task_list)                
    compltDict = {}
    overdDict = {}
    incompltDict = {}

    for i in user_taskNum:
        compltCount = 0
        overdCount = 0
        incompltCount = 0
        for j in range(total_tasks):
            if user_task_list[j] == i and completed_list[j] == "No":
                incompltCount +=1
                if due_dateListformat[j] < today:
                    overdCount += 1
            if user_task_list[j] == i and completed_list[j] == "Yes":
                compltCount += 1

        compltDict[i] = compltCount
        overdDict[i] = overdCount
        incompltDict[i] = incompltCount
    
    for key in user_taskNum and compltDict and overdDict and incompltDict:
        user_report.write(f"""
For {key}:
Total number of tasks: {user_taskNum[key]} 
Percentage of total tasks: {round((user_taskNum[key] / total_tasks * 100), 2)}%
Percentage of tasks completed: {round((compltDict[key] / user_taskNum[key] * 100), 2)}%
Percentage of tasks incomplete: {round((incompltDict[key] / user_taskNum[key] * 100), 2)}%
Percentage of tasks incomplete and overdue: {round ((overdDict[key] / user_taskNum[key] * 100), 2)}%
""")  
    task_report.close()
    user_report.close()
    print("Task and User Overview Reports have been generated!")

# User defined function for display of statistics 
def display():
    # Generate user and task overview reports
    reports = gen_rep()
    
    task_report = open("task_overview.txt", "r+")
    user_report = open("user_overview.txt", "r+")
    
    # Displays contents of the user and task overview reports
    taskContents = ""
    for line in task_report:
        taskContents += line
    print(taskContents)
        
    userContents = ""
    for line in user_report:
        userContents += line
    print(userContents)

# Creates lists for each item in entry in the tasks and user files
task_file = open("tasks.txt", "r+")
user_file = open("user.txt", "r+")

user_task_list = []
task_list = []
task_descrip_list = []
today_list = []
due_date_list = []
completed_list = []
user_list = []

for line in task_file:
    line = line.split(", ")
    user_task = line[0]
    user_task_list.append(user_task)
    task = line[1]
    task_list.append(task)
    task_descrip = line[2]
    task_descrip_list.append(task_descrip)
    today = line[3]
    today_list.append(today)
    due_date = line[4]
    due_date_list.append(due_date)
    completed = line[5]
    completed = completed.strip("\n")
    completed_list.append(completed)
    
total_tasks = len(task_list)
for line in user_file:
    line = line.split(", ")
    user = line[0]
    user_list.append(user)

# Requests a user to login and checks if details match username and password from user file
# Three incorrect entries of username or password will terminate the program
attempts = 0
login = False

while login == False:
    user_file = open("user.txt", "r+")

    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    
    for line in user_file:
        valid_user, valid_password = line.split(", ")
        valid_password = valid_password.rstrip("\n")
        if username == valid_user and password == valid_password: 
            login = True
    if login == False:
        print("Incorrect details")    
        attempts += 1
    if attempts == 3:
        print("You have reached maximum attempts. The program will be terminated.")
        quit()
    user_file.seek(0)
user_file.close()

# Main menu where the user is requested to make a choice as below

# Once the options in the main menu have been completed or an input incorrectly entered, the user will
# be returned to the main menu
option = True

while option == True:
    if username != "admin":
        choice = input(""" 
From the menu below
r - Register a new user
a - Add new task(s)
va - View all tasks
vm - View my tasks
gr - Generate reports
e - Exit

Please enter a letter(s) corresponding to the options: """)
    
    # A modified menu is displayed if 'admin' is logged in
    if username == "admin":
        choice = input(""" 
From the menu below
r - Register a new user
a - Add new task(s)
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display Statistics
e - Exit

Please enter letter(s) corresponding to one of the options: """)
        choice = choice.lower()
        choice = choice.strip(" ")   
    if choice not in ("r", "a", "va", "vm", "gr", "e") and choice == "ds" and user == "admin":
        print("Your response has not been recognised, please re-enter a choice.")
        continue  

# If an option is enter, the following calls the appropriate user defined function
    if choice == "r":
        reg_user()

    elif choice == "a":
        add_task()
       
    elif choice == "va":    
        view_all()

    elif choice == "vm":
        view_mine()

    elif choice == "gr":
        gen_rep()

    elif choice == "ds":
        display()
    
    else:
        quit()












