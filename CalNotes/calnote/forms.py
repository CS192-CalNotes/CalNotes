from django import forms
from .models import Task #class Task from models.py

# Insert form classes here
class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task','dueDate']
        widgets = {
            'task': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter task here',
                    'aria-label':'Task',
                    'aria-describedby':'add-btn'}
            ),
            'dueDate': forms.DateTimeField()
        }