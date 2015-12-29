# coding=utf-8
from selenium.webdriver.common.by import By
from pages.base import BasePage
from utils.utils import *
from random import randint
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from random import randint

class WatchedDomainsListPage(BasePage):
    _title = "Watched domains"

    _watch_new_domain_button = (By.XPATH, "//button")
    _domain_name_field = (By.NAME, "domains")
    _domain_name_value = get_random_string(8)+".waw.pl"
    _watch_new_domain_submit = (By.XPATH, "//button[2]")
    _result_domain_name_field = (By.XPATH, "/html/body/div[7]/div/div/form/div[2]/table/tbody/tr[1]/td[2]/span")
    _result_text_field = (By.XPATH, "/html/body/div[7]/div/div/form/div[2]/table/tbody/tr[1]/td[3]")
    _delete_first_domain_button = (By.XPATH, "//div/span/img")
    _back_from_results_page_button = (By.XPATH, "//button")


    def __init__(self, driver):
        super(WatchedDomainsListPage, self).__init__(driver, self._title)

    def watch_new_domain(self):
        self.click(self._watch_new_domain_button)
        self.clear_field_and_send_keys(self._domain_name_value, self._domain_name_field)
        self.click(self._watch_new_domain_submit)

    def result_domain_text(self):
        return self.get_text(self._result_domain_name_field)

    def delete_first_domain(self):
        self.click(self._delete_first_domain_button)
        self.accept_alert()

    def back_from_results_page(self):
        self.click(self._back_from_results_page_button)