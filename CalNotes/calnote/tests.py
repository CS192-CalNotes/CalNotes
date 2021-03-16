from django.test import TestCase
from calnote.models import Task
from faker import Faker
from datetime import datetime
from random import randint

fake = Faker()

class TaskTest(TestCase):
    def create_task(self, name, date, isComplete):
        """Utility function for creating task."""
        Task.objects.create(task=name,dueDate=date,isComplete=isComplete)

    def test_create_task(self):
        """Test for task model creation."""
        fakeName = fake.text()[0:100]
        date = datetime.now()
        isComplete = (True,False)[randint(0,1)]

        self.create_task(fakeName,date,isComplete)

        task = Task.objects.get(task=fakeName)
        self.assertTrue(isinstance(task,Task))
        self.assertNotEqual(getattr(task,"taskID",False),False)
        self.assertEqual(task.task,fakeName)
        self.assertEqual(task.dueDate.timestamp(), date.timestamp()+8*60*60 )
        self.assertEqual(task.isComplete,isComplete)