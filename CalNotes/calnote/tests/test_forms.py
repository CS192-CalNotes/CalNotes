from django.test import TestCase
from django.utils import timezone
from faker import Faker
from calnote.forms import EventForm, NoteForm, TaskForm

fake = Faker()

class TaskFormTest(TestCase):
    def test_empty_form(self):
        """Test form for empty data"""
		
        data = {
            'task': '',
            'dueDate': ''
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty(self):
        """Test form for empty task name"""

        dueDate = timezone.now()
        data = {
            'task': '',
            'dueDate': dueDate.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_dueDate(self):
        """Test form for empty task due date"""

        data = {
            'task': fake.text()[0:100],
            'dueDate': ''
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_wrong_date_format(self):
        """Test form for wrong task date format"""

        dueDate = timezone.now()
        data = {
            'task': fake.text()[0:100],
            'dueDate': "Not A Date Format"
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        """Test form for valid task details"""

        dueDate = timezone.now()
        data = {
            'task':  fake.text()[0:100],
            'dueDate': dueDate.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())
    

class EventFormTest(TestCase):    
    def test_empty_form(self):
        """Test form for empty data"""
		
        data = {
            'name': '',
            'date': ''
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty(self):
        """Test form for empty event name"""

        date = timezone.now()
        data = {
            'name': '',
            'date': date.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_date(self):
        """Test form for empty due date"""

        data = {
            'name': fake.text()[0:100],
            'date': ''
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())

    def test_wrong_date_format(self):
        """Test form for wrong date format"""

        date = timezone.now()
        data = {
            'name': fake.text()[0:100],
            'date': "Not A Date Format"
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        """Test form for valid event details"""

        date = timezone.now()
        data = {
            'name':  fake.text()[0:100],
            'date': date.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())

class NoteFormTest(TestCase):
    def test_empty_form(self):
        """Test form for empty data"""

        data = {
            'noteTitle': '',
            'note': '',
            'date': ''
        }
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_title(self):
        """Test form for empty noteTitle"""

        date = timezone.now()
        data = {
            'noteTitle': '',
            'note': fake.text()[0:100],
            'date': date.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_note(self):
        """Test form for empty note"""

        date = timezone.now()
        data = {
            'noteTitle': fake.text()[0:100],
            'note': '',
            'date': date.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_date(self):
        """Test form for empty date"""

        data = {
            'noteTitle': fake.text()[0:100],
            'note': fake.text()[0:100],
            'date': ''
        }
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_wrong_date_format(self):
        """Test form for wrong date format"""

        data = {
            'noteTitle': fake.text()[0:100],
            'note': fake.text()[0:100],
            'date': "Not A Date Format"
        }
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        """Test form for valid task details"""

        date = timezone.now()
        data = {
            'noteTitle': fake.text()[0:100],
            'note': fake.text()[0:100],
            'date': date.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())
