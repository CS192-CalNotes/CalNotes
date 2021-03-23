from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Task #imports class Task from models.py
from .forms import AddTaskForm #imports class AddTaskForm from forms.py

# Create your views here.

def index(request):
    task_list = Task.objects.order_by('taskID')
    context = {
        'task_list': task_list, 
        'empty_task_list': len(task_list) == 0
    }
    return render(request, "calnote/index.html", context)

def addNewTask(request):
    if request.method == "POST":
        addtaskform = AddTaskForm(request.POST)
        if addtaskform.is_valid():
            new_addtask = addtaskform.save() #new addtask object
        return redirect(index)
    elif request.method == "GET":
        addtaskform = AddTaskForm(instance=Task())
        context = {
            'taskform': addtaskform
        }
        return render(request, "calnote/taskform.html", context)
