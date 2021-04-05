from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from datetime import datetime
from calendar import monthrange
from math import ceil

from .models import Task			# Imports class Task from models.py
from .forms import AddTaskForm 		# Imports class AddTaskForm from forms.py


def index(request):
    """Main view: shows the task listing by default."""

    # Parse date URL query
    date_query = request.GET.get('date')
    if date_query == None:
        selected_date = datetime.today()
    else:
        selected_date = datetime.strptime(date_query, "%Y-%m-%d")
    
    calendar_month_str = selected_date.strftime("%B")
    calendar_year_str = selected_date.strftime("%Y")
    _, calendar_days = monthrange(selected_date.year, selected_date.month)
    offset = datetime.strptime(
        "%d-%d-1" % (selected_date.year, selected_date.month),
        "%Y-%m-%d"
    ).weekday()
    
    calendar_month_range = [
        [
            (week*7+day-offset+1)
            for day in range(7)
        ]
        for week in range(ceil((offset+calendar_days)/7))
    ]

    task_list = Task.objects.order_by('taskID')
    context = {
        'task_list': task_list,
        'empty_task_list': len(task_list) == 0,
        'len_incomplete_task_list': len([task for task in task_list if not task.isComplete]),
        'len_complete_task_list': len([task for task in task_list if task.isComplete]),

        # Calendar contexts
        'calendar_month_str': calendar_month_str,
        'calendar_year_str': calendar_year_str,
        'calendar_month_range': calendar_month_range,
        'calendar_days': calendar_days,
        'calendar_selected': selected_date.day
    }
    return render(request, "calnote/taskview.html", context)


def addNewTask(request):
    """View to add a new task"""

    # Save task inputs; adds a task to the database
    if request.method == "POST":
        addtaskform = AddTaskForm(request.POST)
        if addtaskform.is_valid():
            new_addtask = addtaskform.save()		# New addtask object
        return redirect(index)

        # Display task input form
    elif request.method == "GET":
        addtaskform = AddTaskForm(instance=Task())
        context = {
            'taskform': addtaskform
        }
        return render(request, "calnote/taskform.html", context)


def deleteTask(request, task_id):
    """View to remove an existing task"""

    task = Task.objects.get(taskID=task_id)
    task.delete()									# Remove from database
    return redirect(index)


def toggleTask(request, task_id):
    """View to mark or unmark task as complete"""

    task = Task.objects.get(taskID=task_id)
    if not task.isComplete:
        task.isComplete = True
    else:
        task.isComplete = False
    task.save()
    return redirect(index)
