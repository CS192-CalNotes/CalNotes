from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newtask", views.addNewTask, name="newtask"),
    path("addtask", views.addTask, name="addtask")
]
