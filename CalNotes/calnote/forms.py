from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, Event, Note

# Attributes of forms needed


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'dueDate']
        widgets = {
            'task': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter task here',
                    'aria-label': 'Task',
                    'aria-describedby': 'add-btn'}
            ),
            'dueDate': forms.DateTimeInput()
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter event here',
                    'aria-label': 'Event',
                    'aria-describedby': 'add-btn'}
            ),
            'date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'aria-label': 'Event',
                    'aria-describedby': 'add-btn'}
            )
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['noteTitle', 'note', 'date']
        widgets = {
            'noteTitle': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter task here',
                    'aria-label': 'Note',
                    'aria-describedby': 'add-btn'}
            ),
            'note': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter note here',
                    'aria-label': 'Note',
                    'aria-describedby': 'add-btn',
                    "rows": 5,
                    "cols": 20}
            ),
            'date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'aria-label': 'Note',
                    'aria-describedby': 'add-btn'}
            )
        }

class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['noteTitle', 'note', 'date']
        widgets = {
            'noteTitle': forms.TextInput(
                attrs={
                    'class': 'title-input',
                    'placeholder': 'Enter note here',
                    'aria-label': 'Note',
                    'aria-describedby': 'add-btn'}
            ),
            'note': forms.Textarea(
                attrs={
                    'id': 'note-editor',
                    'class': 'note-input',
                    'placeholder': 'Enter note here',
                    'aria-label': 'Note',
                    'aria-describedby': 'add-btn',
                }
            ),
            'date': forms.DateTimeInput(
                attrs={
                    'class': 'date-input',
                    'aria-label': 'Event',
                    'aria-describedby': 'add-btn'}
            )
        }
        
#new user form
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        #password2 is password confirmation

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user