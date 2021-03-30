from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newtask", views.addNewTask, name="newtask"),
    path("<str:task_id>/deletetask", views.deleteTask, name="deletetask"),
	path("<str:task_id>/toggletask", views.toggleTask, name="toggletask")
]
