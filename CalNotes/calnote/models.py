from django.db import models
from django.utils import timezone

class Task(models.Model):
	"""Task object fields"""

	taskID = models.AutoField(primary_key = True)
	task = models.CharField(max_length = 100)

	# dueDate for the task. Should default to time of task creation
	dueDate = models.DateTimeField(default = timezone.now, blank = True)
	isComplete = models.BooleanField(default = False)

	def __str__(self):
		return self.task
