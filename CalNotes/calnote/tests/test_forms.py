from django.test import TestCase
from django.utils import timezone
from faker import Faker
from calnote.forms import EventForm, NoteForm

fake = Faker()


class NoteFormTest(TestCase):
    def test_empty_form(self):
        """Test form for empty data"""

        data = {
            'noteTitle': '',
            'note': '',
            'date': ''
        }
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        """Test form for empty noteTitle"""

        date = timezone.now()
        data = {
            'noteTitle': '',
            'note': fake.text()[0:100],
            'date': date.strftime("%Y-%m-%d %H:%M:%S")
        }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())

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
