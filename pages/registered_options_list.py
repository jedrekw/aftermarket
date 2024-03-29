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
from pages.home import HomePage

class RegisteredOptionsListPage(BasePage):
    _title = "Registered options"

    _first_option_checkbox = (By.XPATH, "//div/label/span")
    _second_option_checkbox = (By.XPATH, "//tbody[2]/tr/td[3]/div/label/span")
    _third_option_checkbox = (By.XPATH, "//tbody[3]/tr/td[3]/div/label/span")
    _renew_first_option_button = (By.XPATH, "//td/div/a[2]")
    _change_profile_data_button = (By.XPATH, "//tr[3]/td/div/a")
    _change_profile_data_dropdown = (By.NAME, "id")
    _change_profile_data_dropdown_index = randint(1,7)
    _stage2_result_field = (By.XPATH, "//label/div")
    _stage2_option_name_field = (By.XPATH, "//td[2]/div/label/span")
    _submit_button = (By.XPATH, "//div[2]/button")
    _confirmation_alert_yes = (By.XPATH, "//div[3]/button")
    _result_domain_name_field = (By.XPATH, "//div/span")
    _result_text_field = (By.XPATH, "//td[3]")
    _transfer_first_option_button = (By.XPATH, "//button[4]")
    _transfer_button = (By.XPATH, "//div[2]/div[2]/a[4]")
    _transfer_option_login_field = (By.NAME, "login")
    _transfer_list_first_option_field = (By.XPATH, "//td[3]/div/span/label/span")
    _transfer_list_first_option_cancel_button = (By.XPATH, "//td/div/button")
    _get_option_authinfo_button = (By.XPATH, "//div[2]/div[2]/a[3]")
    _second_stage_send_email_after_oparation_radio = (By.XPATH, "//label/span[2]")
    _second_stage_stop_realization_until_manual_activation_radio = (By.XPATH, "//div[4]/div/div[2]/div/label[2]/span[2]")
    _back_from_results_page = (By.XPATH, "//button")
    _base_url = HomePage._url

    def __init__(self, driver):
        super(RegisteredOptionsListPage, self).__init__(driver, self._title)

    def first_option_text(self):
        self._first_option_text_value = self.get_text(self._first_option_checkbox)

    def second_option_text(self):
        self._second_option_text_value = self.get_text(self._second_option_checkbox)

    def third_option_text(self):
        self._third_option_text_value = self.get_text(self._third_option_checkbox)

    def change_option_profile_data(self):
        self.click(self._first_option_checkbox)
        self.click(self._change_profile_data_button)
        self.select_index_from_dropdown(self._change_profile_data_dropdown_index, self._change_profile_data_dropdown)
        self.click(self._submit_button)

    def renew_option(self):
        self.click(self._first_option_checkbox)
        self.click(self._renew_first_option_button)

    def stage2_option_text(self):
        return self.get_text(self._stage2_option_name_field)

    def submit_and_accept_alert(self):
        sleep(3)
        self.click(self._submit_button)
        sleep(3)
        self.accept_alert()

    def result_domain_text(self):
        return self.get_text(self._result_domain_name_field)

    def result_text(self):
        return self.get_text(self._result_text_field)

    def transfer_option_from_account(self):
        self.click(self._third_option_checkbox)
        self.click(self._transfer_button)

    def transfer_option_enter_login(self, login):
        self.clear_field_and_send_keys(login, self._transfer_option_login_field)

    def submit(self):
        self.click(self._submit_button)

    def transfer_list_first_domain_text(self):
        return self.get_text(self._transfer_list_first_option_field)

    def delete_first_transfer(self):
        self.click(self._transfer_list_first_option_field)
        self.click(self._transfer_list_first_option_cancel_button)

    def get_option_authinfo(self):
        self.click(self._third_option_checkbox)
        self.click(self._get_option_authinfo_button)
        self.click(self._submit_button)

    def store_option_authinfo(self):
        self._result_text = self.get_text(self._result_text_field)
        self._option_authinfo = self._result_text[14:]

    def second_stage_checkboxes_and_submit(self):
        self.click(self._second_stage_stop_realization_until_manual_activation_radio)
        self.click(self._submit_button)
        self.click(self._confirmation_alert_yes)

    def delete_all_option_transfers(self):
        while True:
            if "/assets/img/table/row/delete.png" in self.get_page_source():
                self.click(self._transfer_list_first_option_field)
                self.click(self._transfer_list_first_option_cancel_button)
                sleep(3)
                self.click(self._submit_button)
                sleep(3)
                self.accept_alert()
                WebDriverWait(self.get_driver(), 30).until(EC.text_to_be_present_in_element(self._result_text_field, u"Transfer został anulowany"))
                self.get(self._base_url + "Intransferfuture/List/")
            else:
                break

