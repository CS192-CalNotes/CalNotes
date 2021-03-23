from faker import Faker
from django.utils import timezone
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.remote.remote_connection import LOGGER, logging
from selenium.webdriver.chrome.options import Options
import time

fake = Faker()

class TaskViewTest(StaticLiveServerTestCase):
    def setUp(self):
        """Setup Chrome driver"""
        options = Options()
        # options.add_argument('--headless')
        options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.driver.implicitly_wait(5)

    def test_create_task(self):
        """Integration test for task creation."""
        url = "%s%s" % (self.live_server_url, "/newtask")
        self.driver.get(url)
        
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
        time.sleep(1)
        self.driver.find_element_by_css_selector('input[type="submit"]').click()
        
        # Verify that the task was saved

        self.assertEqual(self.live_server_url + "/",self.driver.current_url)
        
        # get first child list
        innerText = self.driver.find_element_by_css_selector("li.list-group-item.list-group-item-action:first-of-type").get_attribute("innerText").strip()
        parsedDate = dueDate.strftime("%B %#d, %Y, %#H:%M ") + ["p.m.","a.m."][dueDate.strftime("%p") == "AM"]
        self.assertEqual( ("%s | %s" % (fakeName,parsedDate) ),innerText)


    def tearDown(self):
        """Close chrome driver"""
        time.sleep(2)
        self.driver.close()
        