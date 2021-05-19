import time
import os
from datetime import datetime
from faker import Faker
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER, logging
from selenium.webdriver.chrome.options import Options
from calnote.models import Task, Event, Note

fake = Faker()


class CreateTaskViewTest(StaticLiveServerTestCase):

    def create_task(self, name, date, isComplete):
        """Utility function for creating task."""

        Task.objects.create(task=name, dueDate=date, isComplete=isComplete)

    def setUp(self):
        """Setup Chrome driver"""

        options = Options()
        if "PY_ENV" in os.environ and os.environ["PY_ENV"] == "test":
            options.add_argument('--headless')
        options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.driver.implicitly_wait(5)

    def test_edit_task(self):
        """Integration test for edit task."""

        # Task to edit
        fakeName = fake.text()[0:100]
        date = datetime.now()
        isComplete = False
        self.create_task(fakeName, date, isComplete)
        time.sleep(2)

        self.driver.get(self.live_server_url)
        self.assertEqual(self.live_server_url + "/",
                         self.driver.current_url, "Link redirects to other routes.")
        time.sleep(2)

        # Go to edit form
        linkButton = self.driver.find_element_by_css_selector("td:nth-of-type(4) > a")
        linkButton.click()
        self.driver.implicitly_wait(10)

        # Form data
        newFakeName = fake.text()[0:100]
        newDueDate = datetime.now()

        # Set Task names
        taskNameField = self.driver.find_element_by_id("id_task")
        dueDateField = self.driver.find_element_by_id("id_dueDate")

        # Clear inputs
        taskNameField.clear()
        dueDateField.clear()

        self.driver.implicitly_wait(10)

        # Fill in task name
        taskNameField.send_keys(newFakeName)
        dueDateField.send_keys(newDueDate.strftime("%Y-%m-%d %H:%M:%S"))

        # Submit Form
        time.sleep(5)
        self.driver.find_element_by_css_selector(
            'input[type="submit"]').click()

        # Verify that the task was saved
        self.assertEqual(self.live_server_url + "/", self.driver.current_url)

        # Get rendered values
        taskName = self.driver.find_element_by_css_selector(
            "td:nth-of-type(2)").get_attribute("innerText").strip()
        self.assertEqual(taskName, newFakeName.strip())

        actualDate = self.driver.find_element_by_css_selector(
            "td:nth-of-type(3)").get_attribute("innerText").strip()
        expectedDate = newDueDate.strftime(
            "%B %#d, %Y, %#I:%M ") + ["p.m.", "a.m."][newDueDate.strftime("%p") == "AM"]
        self.assertEqual(actualDate, expectedDate)

        # Clean Test database
        Task.objects.all().delete()

    def tearDown(self):
        """Close chrome driver"""

        time.sleep(2)
        self.driver.stop_client()
        self.driver.close()


class CreateEventViewTest(StaticLiveServerTestCase):

    def create_event(self, name, date):
        """Utility function for creating event."""

        Event.objects.create(name=name, date=date)

    def setUp(self):
        """Setup Chrome driver"""

        options = Options()

        if "PY_ENV" in os.environ and os.environ["PY_ENV"] == "test":
            options.add_argument('--headless')

        options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.driver.implicitly_wait(5)

    def test_edit_event(self):
        """Integration test for editing of events."""

        # Create event
        fakeName = fake.text()[0:100]
        date = datetime.now()
        self.create_event(fakeName, date)
        time.sleep(2)

        self.driver.get(self.live_server_url)
        self.assertEqual(self.live_server_url + "/",
                         self.driver.current_url, "Link redirects to other routes.")
        time.sleep(2)

        # Get rendered values
        linkButton = self.driver.find_element_by_id("dropdownMenuLink")
        linkButton.click()
        time.sleep(2)

        linkButton2 = self.driver.find_element_by_id("edit-event")
        linkButton2.click()
        self.driver.implicitly_wait(15)

        # Form data
        newFakeName = fake.text()[0:100]
        newDueDate = datetime.now()

        # Set Event fields
        eventNameField = self.driver.find_element_by_id("id_name")
        dueDateField = self.driver.find_element_by_id("id_date")

        # Clear inputs
        eventNameField.clear()
        dueDateField.clear()

        self.driver.implicitly_wait(15)

        # Fill in event details
        eventNameField.send_keys(newFakeName)
        dueDateField.send_keys(newDueDate.strftime("%Y-%m-%d %H:%M:%S"))

        # Submit Form
        time.sleep(10)
        self.driver.find_element_by_css_selector(
            'input[type="submit"]').click()

        # Verify that the event was saved
        self.assertEqual(self.live_server_url + "/", self.driver.current_url)

        # Verify that the event was edited
        eventName = self.driver.find_element_by_id(
            "dropdownMenuLink").get_attribute("innerText").strip()
        self.assertEqual(eventName, newFakeName.strip())

        # Clean Test database
        Event.objects.all().delete()

    def tearDown(self):
        """Close chrome driver"""

        time.sleep(2)
        self.driver.stop_client()
        self.driver.close()


class CreateNoteViewTest(StaticLiveServerTestCase):

    def create_note(self, noteTitle, note, date):
        """Utility function for creating event."""

        Note.objects.create(noteTitle=noteTitle, note=note, date=date)

    def setUp(self):
        """Setup Chrome driver"""

        options = Options()

        if "PY_ENV" in os.environ and os.environ["PY_ENV"] == "test":
            options.add_argument('--headless')

        options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.driver.implicitly_wait(5)

    def test_add_note(self):
        """Integration test for note creation."""

        url = "%s%s" % (self.live_server_url, "/newnote")
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        # Form data
        fakeName = fake.text()[0:100]
        fakeContent = fake.text()[:256]
        date = datetime.now()

        # Set note fields
        noteTitleField = self.driver.find_element_by_id("id_noteTitle")
        noteField = self.driver.find_element_by_id("id_note")
        dateField = self.driver.find_element_by_id("id_date")

        noteTitleField.clear()
        noteField.clear()
        dateField.clear()

        self.driver.implicitly_wait(10)

        noteTitleField.send_keys(fakeName)
        noteField.send_keys(fakeContent)
        dateField.send_keys(date.strftime("%Y-%m-%d %H:%M:%S"))

        # Submit form
        time.sleep(10)
        self.driver.find_element_by_css_selector(
            'input[type="submit"]').click()

        time.sleep(5)

        # Verify that the note was saved
        self.assertEqual(self.live_server_url + "/notes", self.driver.current_url)

        # Get rendered values
        noteName = self.driver.find_element_by_css_selector(
            "td:nth-of-type(1)").get_attribute("innerText").strip()
        self.assertEqual(noteName, fakeName.strip())

        noteDate = self.driver.find_element_by_css_selector(
            "td:nth-of-type(2)").get_attribute("innerText").strip()
        expectedDate = date.strftime(
            "%B %#d, %Y, %#I:%M ") + ["p.m.", "a.m."][date.strftime("%p") == "AM"]
        self.assertEqual(noteDate, expectedDate)

        linkButton = self.driver.find_element_by_css_selector("td:nth-of-type(1)")
        linkButton.click()
        time.sleep(2)

        content = self.driver.find_element_by_tag_name('p').get_attribute(
            "innerText").strip()
        self.assertEqual(content, fakeContent.strip())

        # Clean Test database
        Note.objects.all().delete()

    def test_edit_note(self):
        """Integration test for editing of notes."""

        # Create note
        fakeName = fake.text()[0:100]
        fakeContent = fake.text()[:256]
        date = datetime.now()
        self.create_note(fakeName, fakeContent, date)
        time.sleep(2)

        url = "%s%s" % (self.live_server_url, "/notes")
        self.driver.get(url)
        time.sleep(5)

        linkButton = self.driver.find_element_by_id("edit-test")
        linkButton.click()
        self.driver.implicitly_wait(10)

        # Form data
        newFakeName = fake.text()[0:100]
        newFakeContent = fake.text()[:256]
        newDate = datetime.now()

        # Set note fields
        noteTitleField = self.driver.find_element_by_id("id_noteTitle")
        noteField = self.driver.find_element_by_tag_name("textarea")
        dateField = self.driver.find_element_by_id("id_date")

        noteTitleField.clear()
        noteField.clear()
        dateField.clear()
        
        self.driver.implicitly_wait(10)

        noteTitleField.send_keys(newFakeName)
        noteField.send_keys(newFakeContent)
        dateField.send_keys(newDate.strftime("%Y-%m-%d %H:%M:%S"))

        # Submit form
        time.sleep(5)
        self.driver.find_element_by_css_selector(
            'input[type="submit"]').click()

        time.sleep(5)

        # Verify that the note was saved
        self.assertEqual(self.live_server_url + "/notes", self.driver.current_url)

        # Get rendered values
        noteName = self.driver.find_element_by_css_selector(
            "td:nth-of-type(1)").get_attribute("innerText").strip()
        self.assertEqual(noteName, newFakeName.strip())

        noteDate = self.driver.find_element_by_css_selector(
            "td:nth-of-type(2)").get_attribute("innerText").strip()
        expectedDate = newDate.strftime(
            "%B %#d, %Y, %#I:%M ") + ["p.m.", "a.m."][newDate.strftime("%p") == "AM"]
        self.assertEqual(noteDate, expectedDate)

        linkButton = self.driver.find_element_by_css_selector("td:nth-of-type(1)")
        linkButton.click()
        time.sleep(2)

        content = self.driver.find_element_by_tag_name('p').get_attribute(
            "innerText").strip()
        self.assertEqual(content, newFakeContent.strip())

        # Clean Test database
        Note.objects.all().delete()

    def test_remove_note(self):
        """Integration test for note deletion."""

        # Create note
        fakeName = fake.text()[0:100]
        fakeContent = fake.text()[:256]
        date = datetime.now()
        self.create_note(fakeName, fakeContent, date)
        time.sleep(2)

        url = "%s%s" % (self.live_server_url, "/notes")
        self.driver.get(url)
        time.sleep(5)

        linkButton = self.driver.find_element_by_id("delete-test")
        linkButton.click()
        time.sleep(5)

        # Verify that the note was deleted
        self.assertEqual(self.live_server_url + "/notes", self.driver.current_url)

        message = self.driver.find_element_by_id(
            "test-removed").get_attribute("innerText").strip()
        self.assertEqual(message, "No Notes.")

    def tearDown(self):
        """Close chrome driver"""

        time.sleep(2)
        self.driver.stop_client()
        self.driver.close()
