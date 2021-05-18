from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newtask", views.addNewTask, name="newtask"),
    path("<str:task_id>/deletetask", views.deleteTask, name="deletetask"),
    path("<str:task_id>/toggletask", views.toggleTask, name="toggletask"),
    path("<str:task_id>/edittask", views.editTask, name="edittask"),
    path("newevent", views.addNewEvent, name="newevent"),
    path("<str:event_id>/deleteEvent", views.deleteEvent, name="deleteEvent"),
    path("<str:event_id>/editEvent", views.editEvent, name="editEvent"),
    path("newnote", views.addNewNote, name="newnote"),
    path("<str:note_id>/deleteNote", views.deleteNote, name="deleteNote"),
    path("notes", views.viewNotes, name="viewnotes"),
    path("notes/<str:note_id>", views.openNote, name="opennote"),
    path("<str:note_id>/editNote", views.editNote, name="editNote"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout")
]
