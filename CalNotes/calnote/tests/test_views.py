from faker import Faker
from django.utils import timezone
from calnote.models import Task
from random import randint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.remote.remote_connection import LOGGER, logging
from selenium.webdriver.chrome.options import Options

import time
fake = Faker()


class CreateTaskViewTest(StaticLiveServerTestCase):

    def create_task(self, name, date, isComplete):
        """Utility function for creating task."""
        Task.objects.create(task=name, dueDate=date, isComplete=isComplete)

    def setUp(self):
        """Setup Chrome driver"""
        options = Options()
        # options.add_argument('--headless')
        options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.driver.implicitly_wait(5)

    def test_create_task(self):
        """Integration test for task creation."""
        url = "%s%s" % (self.live_server_url, "/newtask")
        self.driver.get(url)
        time.sleep(2)

        # Form data
        fakeName = fake.text()[0:100]
        dueDate = timezone.now()

        # Set Task names
        taskNameField = self.driver.find_element_by_id("id_task")
        dueDateField = self.driver.find_element_by_id("id_dueDate")

        # Clear inputs
        taskNameField.clear()
        dueDateField.clear()

        # Fill in task name
        taskNameField.send_keys(fakeName)
        dueDateField.send_keys(dueDate.strftime("%Y-%m-%d %H:%M:%S"))

        # Submit Form
        time.sleep(2)
        self.driver.find_element_by_css_selector(
            'input[type="submit"]').click()

        # Verify that the task was saved

        self.assertEqual(self.live_server_url + "/", self.driver.current_url)

        # Get rendered values
        taskName = self.driver.find_element_by_css_selector(
            "td:first-of-type").get_attribute("innerText").strip()
        self.assertEqual(taskName, fakeName)

        actualDate = self.driver.find_element_by_css_selector(
            "td:nth-of-type(2)").get_attribute("innerText").strip()
        expectedDate = dueDate.strftime(
            "%B %#d, %Y, %#H:%M ") + ["p.m.", "a.m."][dueDate.strftime("%p") == "AM"]
        self.assertEqual(actualDate, expectedDate)

        # Clean Test database
        Task.objects.all().delete()

    def test_remove_task(self):
        """Integration test for task deletion."""
        fakeName = fake.text()[0:100]
        date = timezone.now()
        isComplete = (True, False)[randint(0, 1)]
        self.create_task(fakeName, date, isComplete)
        time.sleep(2)

        self.driver.get(self.live_server_url)
        self.assertEqual(self.live_server_url + "/",
                         self.driver.current_url, "Link redirects to other routes.")

        time.sleep(2)
        # Get rendered values
        linkButton = self.driver.find_element_by_css_selector(
            "td:nth-of-type(3) > a")
        linkButton.click()
        time.sleep(2)

        # Verify that the task was removed
        self.assertEqual(self.live_server_url + "/",
                         self.driver.current_url, "Link redirects to other routes.")
        message = self.driver.find_element_by_css_selector(
            "tr").get_attribute("innerText").strip()
        self.assertEqual(message, "")

    def tearDown(self):
        """Close chrome driver"""
        time.sleep(2)
        self.driver.stop_client()
        self.driver.close()
