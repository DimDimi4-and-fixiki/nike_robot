from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NikeBot(object):
    """
    class of the bot
    Fills form with accounts data
    And makes an order of shoes automatically
    """
    def __init__(self, **kwargs):
        self.user_login = kwargs.get("login", None)  # user login
        self.user_password = kwargs.get("password", None)  # user password
        self.main_page_link = kwargs.get("main_page", None)  # main page SNKRS
        self.last_name = kwargs.get("last_name", "Евгеньевич")
        self.gay_link = kwargs.get("special_link", None)  # link for fast filling
        self.user_address = kwargs.get("address", None)  # user house address

        # Chrome options:
        options = Options()
        options.add_argument("window-size=1400,800")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")

        # Opens browser:
        self.browser = webdriver.Chrome("/home/dimdimi4/Documents/nike_robot/chromedriver",
                                        options=options)
        self.browser.get(self.main_page_link)  # opens main page in the browser window
        self.submit_time = kwargs.get("submit_time", None)
        self.submit_button = None  # button to click on time
        self.log_in_user()
        self.go_by_special_link()
        self.fill_form()
        self.wait_for_time(self.submit_time)

    def log_in_user(self):
        sleep(5)
        enter_button = self.browser.find_element_by_css_selector("button[data-qa='top-nav-join-or-login-button']")
        enter_button.click()
        sleep(5)
        email_input = self.browser.find_element_by_css_selector("input[type='email']")
        password_input = self.browser.find_element_by_css_selector("input[type='password']")
        email_input.send_keys(self.user_login)
        password_input.send_keys(self.user_password)

        sleep(3)
        log_in_button = self.browser.find_element_by_css_selector("input[type='button'][value='ВОЙТИ']")
        log_in_button.click()
        sleep(3)

    def go_by_special_link(self):
        """
        opens a tab with a form for shoes order
        Delays before and after opening
        """
        sleep(1)
        self.browser.get(self.gay_link)
        sleep(4)

    def fill_form(self):
        """
        Fills the form with all the data
        """
        sleep(10)
        try:  # fills middle name
            middle_name_input = self.browser.find_element_by_css_selector("input[id='middleName']")
            middle_name_input.send_keys(self.last_name)
        except Exception:  # middle name is not found
            pass
        sleep(2)

        # Fills address data:
        address_input = self.browser.find_element_by_css_selector("input[id='addressLine1']")
        address_input.clear()
        address_input.send_keys(self.user_address)
        sleep(2)
        
        try:  # fills phone input
            phone_input = self.browser.find_element_by_css_selector("input[placeholder='Номер телефона']")
            cur_phone = phone_input.get_attribute(name="value")
            phone = cur_phone[1:]
            phone_input.clear()
            phone_input.send_keys(phone)
        except Exception:  # phone field os not found
            pass
        sleep(3)
        save_button = self.browser.find_element_by_css_selector("button[class='button-continue']")
        save_button.click()
        sleep(4)
        save_iframe = self.browser.find_element_by_css_selector("iframe[title='payment']")
        save_iframe.click()
        sleep(5)

    def submit(self):
        """
        clicks submit button
        :return:
        """
        self.submit_button.click()
        sleep(300000)

    def is_time(self) -> bool:
        """
        Checks if it is time to click the button
        :return: bool
        """
        eps = 0.0003
        cur_full_time = str(datetime.now())
        cur_time = cur_full_time.split(" ")[-1]
        seconds = float(cur_time.split(":")[-1])
        submit_seconds = float(self.submit_time.split(":")[-1])
        if seconds >= submit_seconds or abs(submit_seconds-seconds) <= eps:
            self.submit()
            return True
        return False

    def wait_for_time(self, t):
        """
        waits for moment t
        when it is near t it starts to check every 0.001s
        :param t: moment of time in format hh:mm:ss.ms
        """

        # Button to click:
        self.submit_button = self.browser.find_element_by_css_selector("button[class='button-submit']")

        # Firstly, checks slowly
        sleep_interval = 0.1
        near = False
        while(True):
            if near:
                self.is_time()

            cur_full_time = str(datetime.now())
            cur_time = cur_full_time.split(" ")[-1]
            sleep(sleep_interval)

            if not near and self.check_time(cur_time, t):  # Checks fast
                sleep_interval = 0.0001
                near = True

    def check_time(self, x, y):
        """
        checks if x and y moments are near
        :return: bool
            True if x and y are near
            False if x and y are not near
        """
        x_hours = float(x.split(":")[0])
        x_minutes = float(x.split(":")[1])
        x_seconds = float(x.split(":")[-1])
        y_hours = float(y.split(":")[0])
        y_minutes = float(y.split(":")[1])
        y_seconds = float(y.split(":")[-1])
        if x_hours == y_hours and x_minutes == y_minutes and abs(x_seconds - y_seconds) <= 1:
            return True
        return False



    @staticmethod
    def get_cur_time(self):
        """
        gets current time in format hh:mm:ss.ms
        :return: str  current time
        """
        cur_full_time = str(datetime.now())
        cur_time = cur_full_time.split(" ")[-1]
        return cur_time
