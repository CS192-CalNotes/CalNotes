from django import forms
from .models import Task, Event, Note

#Attributes of forms needed
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

class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['noteTitle','note', 'date']
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
                    "rows":5, 
                    "cols":20}
            ),
            'date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'aria-label': 'Event',
                    'aria-describedby': 'add-btn'}
            )
        }
