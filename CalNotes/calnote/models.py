from django.db import models
from datetime import datetime

class Task(models.Model):
	taskID = models.AutoField(primary_key = True)
	task = models.CharField(max_length = 100)
	dueDate = models.DateTimeField(default = datetime.now, blank = True)
	isComplete = models.BooleanField(default = False)

	def __str__(self):
		return self.task
