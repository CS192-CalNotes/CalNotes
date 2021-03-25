from django import forms
from .models import Task					# Class Task from models.py

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task','dueDate']
        widgets = {
            'task': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Enter task here',
                    'aria-label':'Task',
                    'aria-describedby':'add-btn'}
            ),
            'dueDate': forms.DateTimeInput()
        }