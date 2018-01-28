from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    USR_ELEM = (By.CSS_SELECTOR, '#m_login_email')
    PWD_ELEM = (By.CSS_SELECTOR, '#login_form > ul > li:nth-child(2) > div > input')