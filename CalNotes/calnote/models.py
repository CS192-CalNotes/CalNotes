from django.db import models
from django.utils import timezone


class Task(models.Model):
    """Task object fields"""

    taskID = models.AutoField(primary_key=True)
    task = models.CharField(max_length=100)

    # dueDate for the task. Should default to time of task creation
    dueDate = models.DateTimeField(default=timezone.now, null=True, blank=True)
    isComplete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.task)
        

class Event(models.Model):
    """Event object fields"""

    eventID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class Note(models.Model):
    """Note object fields"""

    noteID = models.AutoField(primary_key=True)
    note = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now, null=True,blank=True)

    def __str__(self):
        return str(self.note)