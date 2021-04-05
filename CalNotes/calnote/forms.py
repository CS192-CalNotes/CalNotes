from django import forms
from .models import Task, Event


class AddTaskForm(forms.ModelForm):
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


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter task here',
                    'aria-label': 'Task',
                    'aria-describedby': 'add-btn'}
            ),
            'date': forms.DateTimeInput()
        }
