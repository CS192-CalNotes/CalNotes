from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newtask", views.addNewTask, name="newtask"),
    path("<str:task_id>/deletetask", views.deleteTask, name="deletetask"),
    path("<str:task_id>/toggletask", views.toggleTask, name="toggletask"),
    path("newevent", views.addNewEvent, name="newevent"),
    path("<str:event_id>/deleteEvent", views.deleteEvent, name="deleteEvent"),
    path("newnote", views.addNewNote, name="newnote"),
    path("<str:note_id>/deleteNote", views.deleteNote, name="deleteNote"),
]
