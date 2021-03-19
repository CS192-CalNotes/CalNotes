from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "calnote/index.html")


def addNewTask(request):
    return render(request, "calnote/index.html")