from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Task #imports class Task from models.py
from .forms import AddTaskForm #imports class AddTaskForm from forms.py

# Create your views here.

def index(request):
    return render(request, "calnote/index.html")


def addNewTask(request):
    return render(request, "calnote/index.html")
    task_list = Task.objects.order_by('taskID')
    addtaskform = AddTaskForm()
    context = {'task_list': task_list, 'form': addtaskform}
    return render(request, "calnote/index.html", context)

@require_POST
def addTask(request):
    addtaskform = AddTaskForm(request.POST)
    if addtaskform.is_valid():
        new_addtask = addtaskform.save() #new addtask object
    return redirect('index')
