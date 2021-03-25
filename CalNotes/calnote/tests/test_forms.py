from django.test import TestCase
from django.utils import timezone
from calnote.forms import AddTaskForm
from faker import Faker

fake = Faker()


class TaskFormTest(TestCase):

    def test_empty_form(self):
        """Test form for empty data"""
		
        data = {
            'task': '',
            'dueDate': ''
        }
        form = AddTaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_task(self):
        """Test form for empty task name"""

        dueDate = timezone.now()
        data = {
            'task': '',
            'dueDate': dueDate.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = AddTaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_dueDate(self):
        """Test form for empty due date"""

        data = {
            'task': fake.text()[0:100],
            'dueDate': ''
        }
        form = AddTaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_wrong_date_format(self):
        """Test form for wrong date format"""

        dueDate = timezone.now()
        data = {
            'task': fake.text()[0:100],
            'dueDate': "Not A Date Format"
        }
        form = AddTaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        """Test form for valid task details"""

        dueDate = timezone.now()
        data = {
            'task':  fake.text()[0:100],
            'dueDate': dueDate.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = AddTaskForm(data=data)
        self.assertTrue(form.is_valid())
