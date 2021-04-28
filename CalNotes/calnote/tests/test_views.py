import os
from faker import Faker
from datetime import datetime
from calnote.models import Task, Event
from random import randint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.remote.remote_connection import LOGGER, logging
from selenium.webdriver.chrome.options import Options

import time
fake = Faker()


# class CreateTaskViewTest(StaticLiveServerTestCase):

#     def create_task(self, name, date, isComplete):
#         """Utility function for creating task."""

#         Task.objects.create(task=name, dueDate=date, isComplete=isComplete)

#     def setUp(self):
#         """Setup Chrome driver"""

#         options = Options()
#         if "PY_ENV" in os.environ and os.environ["PY_ENV"] == "test":
#             options.add_argument('--headless')
#         options.add_argument("--log-level=OFF")
#         self.driver = webdriver.Chrome(
#             ChromeDriverManager().install(), chrome_options=options)
#         self.driver.implicitly_wait(5)

#     def test_create_task(self):
#         """Integration test for task creation."""

#         url = "%s%s" % (self.live_server_url, "/newtask")
#         self.driver.get(url)
#         time.sleep(2)

#         # Form data
#         fakeName = fake.text()[0:10]
#         dueDate = datetime.now()

#         # Set Task names
#         taskNameField = self.driver.find_element_by_id("id_task")
#         dueDateField = self.driver.find_element_by_id("id_dueDate")

#         # Clear inputs
#         taskNameField.clear()
#         dueDateField.clear()

#         # Fill in task name
#         taskNameField.send_keys(fakeName)
#         dueDateField.send_keys(dueDate.strftime("%Y-%m-%d %H:%M:%S"))

#         # Submit Form
#         time.sleep(10)
#         self.driver.find_element_by_css_selector(
#             'input[type="submit"]').click()

#         # Verify that the task was saved
#         self.assertEqual(self.live_server_url + "/", self.driver.current_url)

#         # Get rendered values
#         taskName = self.driver.find_element_by_css_selector(
#             "td:nth-of-type(2)").get_attribute("innerText").strip()
#         self.assertEqual(taskName, fakeName.strip())

#         actualDate = self.driver.find_element_by_css_selector(
#             "td:nth-of-type(3)").get_attribute("innerText").strip()
#         expectedDate = dueDate.strftime(
#             "%B %-d, %Y, %-H:%M ") + ["p.m.", "a.m."][dueDate.strftime("%p") == "AM"]
#         self.assertEqual(actualDate, expectedDate)

#         # Clean Test database
#         Task.objects.all().delete()

#     def test_mark_task(self):
#         """Integration test for mark task."""

#         fakeName = fake.text()[0:100]
#         date = datetime.now()
#         isComplete = False
#         self.create_task(fakeName, date, isComplete)
#         time.sleep(2)

#         self.driver.get(self.live_server_url)
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")

#         time.sleep(2)

#         # Get rendered values
#         linkButton = self.driver.find_element_by_css_selector(
#             "td:first-of-type > a")
#         linkButton.click()
#         time.sleep(2)

#         # Verify that the task was marked complete
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")
#         message = self.driver.find_element_by_id(
#             "marked-test").get_attribute("innerText").strip()
#         self.assertEqual(message, "You have no incomplete tasks.")

#     def test_unmark_task(self):
#         """Integration test for mark task."""

#         fakeName = fake.text()[0:100]
#         date = datetime.now()
#         isComplete = True
#         self.create_task(fakeName, date, isComplete)
#         time.sleep(2)

#         self.driver.get(self.live_server_url)
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")

#         time.sleep(2)

#         # Get rendered values
#         linkButton = self.driver.find_element_by_id("test-click")
#         linkButton.click()
#         time.sleep(2)

#         # Verify that the task was marked complete
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")
#         message = self.driver.find_element_by_id(
#             "marked-test").get_attribute("innerText").strip()
#         self.assertEqual(message, "You have 1 incomplete task/s.")

#     def test_remove_task(self):
#         """Integration test for task deletion."""

#         fakeName = fake.text()[0:100]
#         date = datetime.now()
#         isComplete = False
#         self.create_task(fakeName, date, isComplete)
#         time.sleep(2)

#         self.driver.get(self.live_server_url)
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")

#         time.sleep(2)

#         # Get rendered values
#         linkButton = self.driver.find_element_by_css_selector(
#             "td:nth-of-type(4) > a")
#         linkButton.click()
#         time.sleep(2)

#         # Verify that the task was removed
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")
#         message = self.driver.find_element_by_id(
#             "test-removed").get_attribute("innerText").strip()
#         self.assertEqual(message, "No active tasks.")

#     def tearDown(self):
#         """Close chrome driver"""

#         time.sleep(2)
#         self.driver.stop_client()
#         self.driver.close()


# class CreateEventViewTest(StaticLiveServerTestCase):

#     def create_event(self, name, date):
#         """Utility function for creating event."""

#         Event.objects.create(name=name, date=date)

#     def setUp(self):
#         """Setup Chrome driver"""

#         options = Options()

#         if "PY_ENV" in os.environ and os.environ["PY_ENV"] == "test":
#             options.add_argument('--headless')

#         options.add_argument("--log-level=OFF")
#         self.driver = webdriver.Chrome(
#             ChromeDriverManager().install(), chrome_options=options)
#         self.driver.implicitly_wait(5)

#     def test_create_event(self):
#         """Integration test for event creation."""

#         url = "%s%s" % (self.live_server_url, "/newevent")
#         self.driver.get(url)
#         time.sleep(2)

#         # Form data
#         fakeName = fake.text()[0:10]
#         date = datetime.now()

#         # Set Event names
#         eventNameField = self.driver.find_element_by_id("id_name")
#         dateField = self.driver.find_element_by_id("id_date")

#         # Clear inputs
#         eventNameField.clear()
#         dateField.clear()

#         # Fill in event name
#         eventNameField.send_keys(fakeName)
#         dateField.send_keys(date.strftime("%Y-%m-%d %H:%M:%S"))

#         # Submit Form
#         time.sleep(5)

#         self.driver.find_element_by_id('eventSubmit').click()

#         # Verify that the task was saved
#         self.assertEqual(self.live_server_url + "/", self.driver.current_url)

#         # Get rendered values
#         eventName = self.driver.find_element_by_id(
#             "dropdownMenuLink").get_attribute("innerText").strip()
#         self.assertEqual(eventName, fakeName.strip())

#         # Event date not displayed
#         # actualDate = self.driver.find_element_by_css_selector(
#         #     "td:nth-of-type(3)").get_attribute("innerText").strip()
#         # expectedDate = date.strftime(
#         #     "%B %-d, %Y, %-H:%M ") + ["p.m.", "a.m."][date.strftime("%p") == "AM"]
#         # self.assertEqual(actualDate, expectedDate)

#         # Clean Test database
#         Event.objects.all().delete()

#     def test_remove_event(self):
#         """Integration test for event deletion."""

#         fakeName = fake.text()[0:100]
#         date = datetime.now()
#         self.create_event(fakeName, date)
#         time.sleep(2)

#         self.driver.get(self.live_server_url)
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")

#         time.sleep(2)

#         # Get rendered values
#         linkButton = self.driver.find_element_by_id("dropdownMenuLink")
#         linkButton.click()
#         time.sleep(2)

#         linkButton2 = self.driver.find_element_by_id("remove-event")
#         linkButton2.click()
#         time.sleep(2)

#         # Verify that the task was removed
#         self.assertEqual(self.live_server_url + "/",
#                          self.driver.current_url, "Link redirects to other routes.")
#         message = self.driver.find_element_by_id(
#             "test-marker").get_attribute("innerText").strip()
#         self.assertEqual(message, "+")

#     def tearDown(self):
#         """Close chrome driver"""

#         time.sleep(2)
#         self.driver.stop_client()
#         self.driver.close()


class CalendarViewTest(StaticLiveServerTestCase):

    def create_event(self, date):
        """Utility function for creating event."""
        fakeName = fake.text()[0:10]
        Event.objects.create(name=fakeName, date=date)

    def setUp(self):
        """Setup Chrome driver"""

        options = Options()

        if "PY_ENV" in os.environ and os.environ["PY_ENV"] == "test":
            options.add_argument('--headless')

        options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.driver.implicitly_wait(5)

        # Add events
        eventDate = datetime.now()
        self.create_event(eventDate.replace(day=1, month=1))
        self.create_event(eventDate.replace(day=3, month=1))
        self.create_event(eventDate.replace(day=1, month=2))

    def test_today(self):
        """ Test if calendar highlights the correct day """
        url = self.live_server_url
        self.driver.get(url)
        time.sleep(2)

        selected_day = self.driver.find_element_by_css_selector(
            ".calendar td.selected").get_attribute("innerText").strip()
        self.assertEqual(selected_day, "%d" % datetime.now().day)

    def test_day(self):
        """ Test if calendar highlights the correct arbitrary day """
        url = "%s%s" % (self.live_server_url, "?date=2021-05-02")
        self.driver.get(url)
        time.sleep(2)

        selected_day = self.driver.find_element_by_css_selector(
            "div.calendar td.selected").get_attribute("innerText").strip()
        self.assertEqual(selected_day, "2")

    def tearDown(self):
        """Close chrome driver"""

        time.sleep(2)
        self.driver.stop_client()
        self.driver.close()
