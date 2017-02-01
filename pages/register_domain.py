# coding=utf-8
from selenium.webdriver.common.by import By
from pages.base import BasePage
from utils.utils import *
from random import randint
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class RegisterDomainPage(BasePage):
    _title = "Register domain"

    _domain_name_field = (By.NAME, "domains")
    _domain_name_value = get_random_uuid(10)+".waw.pl"
    _check_domain_availability_button = (By.XPATH, "//div[2]/button")
    _first_domain_checkbox = (By.XPATH, "/html/body/div[7]/div/div/form/div[1]/table/tbody/tr[1]/td[1]/div/label/input")
    _stop_realization_until_manual_activation_radio = (By.XPATH, "//label[2]/span[2]")
    _register_domain_button = (By.XPATH, "//div[18]/div/div[2]/div[2]/button")
    _register_domain_submit = (By.XPATH, "//div[3]/button")
    _registration_effect_text_field = (By.XPATH, "//td[3]")
    _registration_effect_domain_field = (By.XPATH, "//div/span")
    _first_domain = (By.XPATH, "//input[@value='%s']" %_domain_name_value)
    _domain_status_field = (By.XPATH, "//label/div")

    def __init__(self, driver):
        super(RegisterDomainPage, self).__init__(driver, self._title)

    def enter_domain_to_register(self):
        self.clear_field_and_send_keys(self._domain_name_value, self._domain_name_field)
        self.click(self._check_domain_availability_button)

    def register_domain(self):
        # self.check(self._first_domain_checkbox)
        self.click(self._stop_realization_until_manual_activation_radio)
        sleep(2)
        self.click(self._register_domain_button)
        sleep(2)
        self.click(self._register_domain_submit)





