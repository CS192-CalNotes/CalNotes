from django import forms
from .models import Task, Event

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


class AddEventForm(forms.ModelForm):
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
