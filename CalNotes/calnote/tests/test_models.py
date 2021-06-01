from random import randint
from django.test import TestCase
from django.utils import timezone
from faker import Faker
from calnote.models import Task, Event, Note
from django.contrib.auth.models import User

# Start a faker instance
fake = Faker()


class TaskModelTest(TestCase):

    def create_task(self, name, date, isComplete, user_id):
        """Utility function for creating task."""

        Task.objects.create(task=name, dueDate=date, isComplete=isComplete, user_id=user_id)

    def test_create_task(self):
        """Test for task model creation."""

        fakeName = fake.text()[0:100]
        date = timezone.now()
        isComplete = (True, False)[randint(0, 1)]
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.create_task(fakeName, date, isComplete, user.id)

        task = Task.objects.get(task=fakeName)
        self.assertTrue(isinstance(task, Task))
        self.assertNotEqual(getattr(task, "taskID", False), False)
        self.assertEqual(task.task, fakeName)
        self.assertEqual(task.dueDate.timestamp(), date.timestamp())
        self.assertEqual(task.isComplete, isComplete)

class EventModelTest(TestCase):

    def create_event(self, name, date, user_id):
        """Utility function for creating event."""

        Event.objects.create(name=name, date=date, user_id=user_id)

    def test_create_event(self):
        """Test for event model creation."""

        fakeName = fake.text()[0:100]
        date = timezone.now()

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.create_event(fakeName, date, user.id)

        event = Event.objects.get(name=fakeName)
        self.assertTrue(isinstance(event, Event))
        self.assertNotEqual(getattr(event, "eventID", False), False)
        self.assertEqual(event.name, fakeName)
        self.assertEqual(event.date.timestamp(), date.timestamp())

class NoteModelTest(TestCase):

    def create_note(self, name, content, date, user_id):
        """Utility function for creating note."""

        Note.objects.create(noteTitle=name, note=content, date=date, user_id=user_id)

    def test_create_note(self):
        """Test for note model creation."""

        fakeName = fake.text()[0:100]
        fakeContent = fake.text()
        date = timezone.now()

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.create_note(fakeName, fakeContent, date, user.id)

        note = Note.objects.get(noteTitle=fakeName)
        self.assertTrue(isinstance(note, Note))
        self.assertNotEqual(getattr(note, "noteID", False), False)
        self.assertEqual(note.noteTitle, fakeName)
        self.assertEqual(note.note, fakeContent)
        self.assertEqual(note.date.timestamp(), date.timestamp())
