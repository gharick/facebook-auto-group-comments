from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from locators import LoginPageLocators, PostToGroupsLocators

import time
import re


class FacebookBot:
    drive = None
    URL = 'https://mbasic.facebook.com'

    def __init__(self, driver):
        """
        :param driver: The selenium driver
        :type driver: object
        """
        self.driver = driver

    def login(self, username, password):
        """ Login at facebook

        :param username: account username
        :type username: str
        :param password: account password
        :type password: str
        """
        self.driver.get(self.URL)

        # Login to facebook
        print("Logging into facebook...")
        usr_elem = self.driver.find_element(*LoginPageLocators.USR_ELEM)
        pwd_elem = self.driver.find_element(*LoginPageLocators.PWD_ELEM)

        usr_elem.send_keys(username)
        pwd_elem.send_keys(password)
        pwd_elem.send_keys(Keys.RETURN)
        time.sleep(2)  # We'll wait 2 seconds for the page to load completely

    def collect_groups(self):
        """List of groups a user belongs to

        :returns: list
        """

        print("Collecting groups in profile...")
        self.driver.get(self.URL + '/groups/?seemore&refid=27')

        groups = []
        source = self.driver.page_source
        soup = BeautifulSoup(source, "html.parser")

        for group in soup.find_all("a", href=re.compile(r"groups/\d")):
            groups.append(self.URL + group['href'])

        print("{} groups found in profile.".format(len(groups)))

        return groups

    def post_to_groups(self, post, interval, groups):
        """ Creates a post in a given list of groups

        :param post:
        :type post: str
        :param interval: the amount of time between posts at the groups
        :type interval: int
        :param groups:
        :type groups: list
        """
        for i, group in enumerate(groups):
            self.driver.get(group)
            try:
                post_elem = self.driver.find_element(*PostToGroupsLocators.POST_ELEM)
                sub_elem = self.driver.find_element(*PostToGroupsLocators.SUB_ELEM)

                post_elem.send_keys(post)
                sub_elem.click()

                print("Sucessfully posted in group #{}.".format(i))
                time.sleep(interval)
            except NoSuchElementException:
                print("Can't post in group #{}.".format(i))
                continue
