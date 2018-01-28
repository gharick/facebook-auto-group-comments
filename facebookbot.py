from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import re

from locators import LoginPageLocators, PostToGroupsLocators

class FacebookBot:
    drive = None

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.get("https://mbasic.facebook.com")

        # Login to facebook
        print("Logging into facebook...")
        usr_elem = self.driver.find_element(*LoginPageLocators.USR_ELEM)
        pwd_elem = self.driver.find_element(*LoginPageLocators.PWD_ELEM)

        usr_elem.send_keys(username)
        pwd_elem.send_keys(password)
        pwd_elem.send_keys(Keys.RETURN)
        time.sleep(2)  # We'll wait 2 seconds for the page to load completely

    def collect_groups(self):
        print("Collecting groups in profile...")
        self.driver.get('https://mbasic.facebook.com/groups/?seemore&refid=27')

        groups = []
        source = self.driver.page_source
        soup = BeautifulSoup(source, "html.parser")

        for group in soup.find_all("a", href=re.compile(r"groups/\d")):
            groups.append("https://mbasic.facebook.com" + group['href'])

        print(f"{len(groups)} groups found in profile.")

        return groups

    def post_to_groups(self, post, interval, groups):
        # Go to each group and post
        for i, group in enumerate(groups):
            self.driver.get(group)
            try:
                post_elem = self.driver.find_element(*PostToGroupsLocators.POST_ELEM)
                sub_elem = self.driver.find_element(*PostToGroupsLocators.SUB_ELEM)

                post_elem.send_keys(post)
                sub_elem.click()

                print(f"Sucessfully posted in group #{i}.")
                time.sleep(interval)
            except NoSuchElementException:
                print(f"Can't post in group #{i}.")
                continue
