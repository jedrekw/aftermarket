# coding=utf-8
import unittest
from selenium import webdriver
from unittestzero import Assert
from pages.home import HomePage
from utils.config import *
from utils.utils import *
from datetime import timedelta, date
from time import sleep
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime
from selenium.common.exceptions import *
from selenium.common.exceptions import WebDriverException
import re

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)
run_locally = True

# @on_platforms(browsers)
class SmokeTest(unittest.TestCase):
    _internal_non_grouped_domain_text = 1

    def test_login_wrong_credentials_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(get_random_string(7), get_random_uuid(6))

        Assert.contains(u"Nieprawidłowy login lub hasło", account_page.get_page_source())

    def test_remind_password_wrong_login_should_succeed(self):

        login = get_random_string(7)

        home_page = HomePage(self.driver).open_home_page()
        remind_page = home_page.header.remind_password(login)

        Assert.contains(u"Podany login nie istnieje", remind_page.get_page_source())

    def test_change_contact_data_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_contact_data_page = settings_page.open_change_contact_data_page()
        settings_page.fill_change_contact_data_form()
        settings_page.save_change_contact_data()

        Assert.contains(u"Poniższe dane wskazują osobę, z którą będziemy mogli skontaktować się w sprawach dotyczących twojego konta.", settings_page.get_page_source())
        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())
        Assert.contains(settings_page._change_contact_data_name_value, settings_page.change_contact_data_name_field_text())
        Assert.contains(settings_page._change_contact_data_address_value, settings_page.change_contact_data_address_field_text())
        Assert.contains(settings_page.change_contact_data_postalcode_field_text(), settings_page._change_contact_data_postalcode_value)
        Assert.contains(settings_page._change_contact_data_city_value, settings_page.change_contact_data_city_field_text())

    def test_change_notification_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_notification_settings_page = settings_page.open_change_email_notification_settings_page()
        settings_page.change_email_notification_settings()
        settings_page.save_change_email_notification_settings()

        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(settings_page._confirmation_result_field, u"Operacja wykonana poprawnie."))

    def test_change_newsletter_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_newsletter_settings_page = settings_page.open_change_newsletter_settings_page()
        settings_page.change_newsletter_settings()
        settings_page.save_change_newsletter_settings()

        Assert.contains(u"Operacja wykonana poprawnie.", settings_page.get_page_source())

    def test_add_email_address_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        add_email_page = settings_page.open_add_email_address_page()
        settings_page.remove_all_email_addresses()
        settings_page.add_email_address()

        Assert.contains(u"Potwierdź adres e-mail", settings_page.get_page_source())

        settings_page.back_to_email_addresses_list()

        Assert.equal(settings_page._add_email_address_value, settings_page.added_email_address_text())
        Assert.equal("Niepotwierdzony", settings_page.added_email_status_text())

        settings_page.remove_all_email_addresses()

        self.not_contains(settings_page._add_email_address_value, settings_page.get_page_source())
        self.not_contains("Niepotwierdzony", settings_page.get_page_source())

    def test_change_SMS_notification_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_sms_notification_page = settings_page.open_sms_notification_settings_page()
        # settings_page.open_first_number_notifications()
        settings_page.change_sms_notification_settings()

        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(settings_page._confirmation_result_field, u"Operacja wykonana poprawnie."))

    def test_add_other_users_to_account_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        add_other_users_page = settings_page.open_add_other_users_page()
        settings_page.remove_all_users()
        settings_page.add_other_user()
        settings_page.add_other_user_change_priviledges()

        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(settings_page._confirmation_result_field, u"Operacja wykonana poprawnie."))
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(settings_page._add_other_user_header, u"Lista loginów"))

        Assert.equal(settings_page._add_other_user_login_value, settings_page.added_user_login_text())
        Assert.equal(settings_page._add_other_user_description_value, settings_page.added_user_description_text())

        settings_page.remove_all_users()

        self.not_contains(settings_page._add_other_user_login_value, settings_page.get_page_source())
        self.not_contains(settings_page._add_other_user_description_value, settings_page.get_page_source())

    def test_change_company_address_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_company_address_page = settings_page.open_change_company_data_page()
        settings_page.edit_company_address()
        sleep(30)
        Assert.contains("Operacja wykonana poprawnie", settings_page.edit_company_data_operation_successful_text())
        Assert.contains(settings_page.edit_company_data_zip_text(), settings_page._change_company_data_zip_value)
        Assert.equal(settings_page._change_company_data_street_value, settings_page.edit_company_data_street_text())
        Assert.equal(settings_page._change_company_data_city_value, settings_page.edit_company_data_city_text())

    def test_change_company_data_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        settings_page = account_page.header.open_settings_page()
        change_company_data_page = settings_page.open_change_company_data_page()
        settings_page.edit_company_data()

        Assert.contains(settings_page.edit_company_data_zip_text(), settings_page._change_company_data_zip_value)
        Assert.equal(settings_page._change_company_data_street_value, settings_page.edit_company_data_street_text())
        Assert.equal(settings_page._change_company_data_city_value, settings_page.edit_company_data_city_text())
        Assert.equal(settings_page._change_company_data_company_name_value, settings_page.edit_company_data_company_name_text())
        Assert.equal(settings_page._change_company_data_nip_value, settings_page.edit_company_data_nip_text())

    def test_add_new_bank_account_should_succeed(self):

        number = "26105014451000002276470461"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        bank_accounts_page = settings_page.open_add_bank_account_page()
        settings_page.remove_all_bank_accounts()
        settings_page.add_bank_account(number)

        Assert.contains(u"Operacja wykonana poprawnie.", settings_page.get_page_source())
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(settings_page._added_bank_account_number, number))
        Assert.contains("Lista kont bankowych", settings_page.get_page_source())
        Assert.contains(u"Na tej liście znajdują się konta bankowe, na które możesz zlecać wypłaty.", settings_page.get_page_source())
        Assert.contains("Oto lista twoich kont bankowych.", settings_page.get_page_source())
        Assert.equal(settings_page._add_bank_account_account_name_value, settings_page.added_bank_account_name_text())

        settings_page.remove_all_bank_accounts()

        Assert.contains("Lista kont bankowych", settings_page.get_page_source())
        Assert.contains(u"Na tej liście znajdują się konta bankowe, na które możesz zlecać wypłaty.", settings_page.get_page_source())
        Assert.contains("Oto lista twoich kont bankowych.", settings_page.get_page_source())
        Assert.contains(u"Brak zdefiniowanych kont bankowych", settings_page.get_page_source())
        self.not_contains(number, settings_page.get_page_source())
        self.not_contains(settings_page._add_bank_account_account_name_value, settings_page.get_page_source())

    def test_change_DNS_servers_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        dns_servers_page = settings_page.open_change_DNS_servers_page()
        settings_page.change_DNS_servers()

        Assert.contains("ns1.aftermarket.pl", settings_page.get_page_source())
        Assert.contains("ns2.aftermarket.pl", settings_page.get_page_source())
        Assert.contains(settings_page._change_DNS_servers_DNS3_value, settings_page.get_page_source())
        Assert.contains(settings_page._change_DNS_servers_DNS4_value, settings_page.get_page_source())
        Assert.equal("Operacja wykonana poprawnie", settings_page.change_DNS_servers_operation_successful_text())

    def test_new_DNS_profile_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        dns_profile_page = settings_page.open_new_DNS_template_page()
        settings_page.delete_all_profiles()
        settings_page.new_DNS_template()

        settings_page.new_DNS_entry()
        Assert.equal("Operacja wykonana poprawnie", settings_page.new_DNS_profile_successful_operation_text())
        Assert.equal(settings_page._new_DNS_profile_name_value, settings_page.new_DNS_profile_successtul_opertation_profile_text())
        Assert.equal(settings_page._new_DNS_profile_host_value, settings_page.new_DNS_profile_successtul_opertation_host_text())
        Assert.equal(settings_page._new_DNS_profile_address_value, settings_page.new_DNS_profile_successtul_opertation_address_text())

        settings_page = account_page.header.open_settings_page()
        dns_profile_page = settings_page.open_new_DNS_template_page()

        Assert.contains(u"Lista szablonów DNS", settings_page.get_page_source())
        Assert.equal(settings_page._new_DNS_profile_name_value, settings_page.new_DNS_profile_name_text())

        settings_page.delete_all_profiles()

        self.not_contains(settings_page._new_DNS_profile_name_value, settings_page.get_page_source())

    def test_notification_about_ending_auctions_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        notification_page = settings_page.open_notifications_about_ending_auctions_page()
        settings_page.change_notifications_about_ending_auctions()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_domain_watching_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        domain_watching_settings__page = settings_page.open_domain_watching_settings_page()
        settings_page.change_domain_watching_settings()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_sellers_watching_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        sellers_watching_settings__page = settings_page.open_sellers_watching_settings_page()
        settings_page.change_sellers_watching_settings()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_change_seller_profile_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_seller_profile__page = settings_page.open_change_seller_profile_page()
        settings_page.change_seller_profile()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())
        Assert.equal(settings_page._change_seller_profile_description_value, settings_page.change_seller_profile_description_text())

    def test_sending_notification_settings_t55should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        sending_notification_settings_page = settings_page.open_sending_notification_settings_page()
        settings_page.change_sending_notification_settings()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_task_list_filtering_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        task_list = account_page.header.open_task_list()
        task_list.get_text_selected_option()
        task_list.select_operation_type()
        try:
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(task_list._first_result, task_list.option_text))
            Assert.contains(u"Rodzaj operacji: <b>%s" % task_list.option_text, task_list.get_page_source())
        except WebDriverException:
            Assert.contains(u"Brak zleconych operacji.", task_list.get_page_source())

    def test_register_domain_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        to_pay_list = account_page.header.open_to_pay_list()
        to_pay_list.remove_all_payments()
        register_domain_page = account_page.header.open_register_domain_page()
        register_domain_page.enter_domain_to_register(register_domain_page._domain_name_value_co_pl)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(register_domain_page._domain_status_field, u"Dostępna do rejestracji"))

        register_domain_page.register_domain()

        WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element(register_domain_page._registration_effect_domain_field, register_domain_page._domain_name_value_co_pl))
        WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element(register_domain_page._registration_effect_text_field, u"Operacja zawieszona, oczekuje na aktywowanie"))
        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, register_domain_page._domain_name_value_co_pl))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Rejestracja domeny"))

        to_pay_list.submit_first_payment()
        # to_pay_list.remove_all_payments()
        #
        # self.not_contains(register_domain_page._domain_name_value_co_pl, to_pay_list.get_page_source())
        # self.not_contains(u"Rejestracja domeny", to_pay_list.get_page_source())

    def test_renew_domain_automatically_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.renew_domain_automatically()

        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena będzie automatycznie odnawiana od"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_renew_domain_manually_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        to_pay_list = account_page.header.open_to_pay_list()
        to_pay_list.remove_all_payments()
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.renew_domain_manually()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._second_stage_text_field, u"Domena zostanie odnowiona"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.second_stage_domain_text())

        registered_domains_page.second_stage_checkboxes_and_submit()

        sleep(3)
        if u"Operacja zawieszona, oczekuje na aktywowanie" in registered_domains_page.result_text():
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena już była odnowiona w ostatnim okresie: "))
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()
        to_pay_list.change_tab_renew()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, registered_domains_page._first_domain_text_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Odnowienie domeny"))

        to_pay_list.remove_all_payments()
        to_pay_list.refresh()

        self.not_contains(registered_domains_page._first_domain_text_value, to_pay_list.get_page_source())
        self.not_contains(u"Odnowienie domeny", to_pay_list.get_page_source())

    def test_change_profile_data_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.change_profile_data()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._second_stage_text_field, u"Profil danych zostanie zmieniony"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.second_stage_domain_text())

        registered_domains_page.change_profile_data_stage_2()

        WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja w toku"))
        if u"Ustawiono profil danych:" in registered_domains_page.result_text():
            Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena jest zablokowana"))
            Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

    def test_privacy_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.privacy_settings_first_stage()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._second_stage_text_field, u"Dane abonenta będą widoczne"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.second_stage_domain_text())

        registered_domains_page.second_stage_checkboxes_and_submit2()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Dane abonenta zostały ujawnione"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_get_authinfo_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.get_authinfo()

        try:
            WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())
        except WebDriverException:
            WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domeny nie można transferować"))
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_move_domain_from_account_should_succeed(self):

        login = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.move_domain_from_account(login)

        WebDriverWait(self.driver, 40).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer domeny został zainicjowany"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_from_account_list()
        transfer_domain_page.cancel_all_domain_transfers_from_account()

        self.not_contains(registered_domains_page._first_domain_text_value, transfer_domain_page.get_page_source())

    def test_change_DNS_servers_for_selected_domain_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.third_domain_text()
        registered_domains_page.select_third_domain()
        registered_domains_page.change_dns_servers_for_selected_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Ustawiono serwery DNS:"))
        Assert.equal(registered_domains_page._third_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_redirection_direct_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_redirection_direct()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Przekierowano na adres: %s"%registered_domains_page._change_redirection_url_value))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_redirection_hidden_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_redirection_hidden()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Przekierowano na adres: %s"%registered_domains_page._change_redirection_url_value))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_redirection_ip_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_redirection_ip()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Przekierowano na adres: %s"%registered_domains_page._change_redirection_ip_value))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_dns_profile_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_dns_profile_stage1()
        registered_domains_page.change_DNS_profile_stage2()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Zastosowano szablon wpisów DNS:"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_new_dns_entry_for_selected_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        sleep(1)
        registered_domains_page.new_dns_entry_for_selected_domain()
        registered_domains_page.delete_all_dns_entries_for_selected_domain()
        registered_domains_page.new_dns_entry_for_selected_domain_details()

        Assert.contains("Operacja wykonana poprawnie", registered_domains_page.get_page_source())

        registered_domains_page.back_from_results_page()

        Assert.contains(registered_domains_page._add_dns_entry_host_name_value, registered_domains_page.get_page_source())
        Assert.contains(registered_domains_page._add_dns_entry_priority_value, registered_domains_page.get_page_source())
        Assert.contains(registered_domains_page._add_dns_entry_address_value, registered_domains_page.get_page_source())

        registered_domains_page.delete_all_dns_entries_for_selected_domain()

        self.not_contains(registered_domains_page._add_dns_entry_host_name_value, registered_domains_page.get_page_source())
        self.not_contains(registered_domains_page._add_dns_entry_address_value, registered_domains_page.get_page_source())

# PRZYCISK POWROTU PO DODANIU WPISU NIE PRZEKIEROWUJE NIGDZIE, zgłoszone


    def test_new_dns_server_in_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.dns_servers_in_domain()

        registered_domains_page.delete_all_dns_servers_in_domain()
        registered_domains_page.new_dns_server_in_domain_details()
        Assert.contains(u"Operacja wykonana poprawnie.", registered_domains_page.get_page_source())
        registered_domains_page.back_from_results_page()

        Assert.contains(registered_domains_page._new_dns_server_in_domain_name_value+"."+registered_domains_page._first_domain_text_value, registered_domains_page.get_page_source())
        Assert.contains(registered_domains_page._new_dns_server_in_domain_ip_value, registered_domains_page.get_page_source())

        registered_domains_page.delete_all_dns_servers_in_domain()

        self.not_contains(registered_domains_page._new_dns_server_in_domain_name_value+"."+registered_domains_page._first_domain_text_value, registered_domains_page.get_page_source())
        self.not_contains(registered_domains_page._new_dns_server_in_domain_ip_value, registered_domains_page.get_page_source())

    def test_change_parking_service_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_parking_service()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Zmieniono serwis parkingu domeny"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_keyword_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_keyword()

        WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja w toku"))

        if "Domena odnowiona poprawnie" in registered_domains_page.result_text():
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page._result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena nie jest zaparkowana"))
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_sell_on_auction_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.delete_all_domain_selling_auctions()
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.third_domain_text()
        sleep(1)
        registered_domains_page.select_third_domain()
        registered_domains_page.sell_on_auction()

        Assert.equal(registered_domains_page._third_domain_text_value, registered_domains_page.sell_on_auction_stage2_domain_text())
        Assert.equal(registered_domains_page._sell_on_auction_description_value, registered_domains_page.sell_on_auction_stage2_description_text())

        registered_domains_page.sell_on_auction_submit()
        sleep(2)
        # Assert.contains("Operacja wykonana poprawnie", registered_domains_page.get_page_source())
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Aukcja została wystawiona z ceną początkową %s"%registered_domains_page._sell_on_auction_price_start_value))
        Assert.equal(registered_domains_page._third_domain_text_value, registered_domains_page.result_domain_text())

        selling_auction_page = account_page.header.open_selling_auction_list()
        Times=0
        while Times < 10:
            try:
                Times+=1
                Assert.contains(registered_domains_page._third_domain_text_value, selling_auction_page.get_page_source())
                break
            except AssertionError:
                self.driver.refresh()
        Assert.contains(str(registered_domains_page._sell_on_auction_price_start_value), selling_auction_page.get_page_source())
        selling_auction_page.delete_all_domain_selling_auctions()

        self.not_contains(registered_domains_page._third_domain_text_value, selling_auction_page.get_page_source())

    def test_sell_on_auction_edit_details_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.delete_all_domain_selling_auctions()
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.third_domain_text()
        sleep(1)
        registered_domains_page.select_third_domain()
        registered_domains_page.sell_on_auction()

        Assert.equal(registered_domains_page._third_domain_text_value, registered_domains_page.sell_on_auction_stage2_domain_text())
        Assert.equal(registered_domains_page._sell_on_auction_description_value, registered_domains_page.sell_on_auction_stage2_description_text())

        registered_domains_page.sell_on_auction_submit()
        sleep(2)
        # Assert.contains("Operacja wykonana poprawnie", registered_domains_page.get_page_source())
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Aukcja została wystawiona z ceną początkową %s"%registered_domains_page._sell_on_auction_price_start_value))
        Assert.equal(registered_domains_page._third_domain_text_value, registered_domains_page.result_domain_text())

        selling_auction_page = account_page.header.open_selling_auction_list()
        Times=0
        while Times < 10:
            try:
                Times+=1
                Assert.contains(registered_domains_page._third_domain_text_value, selling_auction_page.get_page_source())
                break
            except AssertionError:
                self.driver.refresh()
        Assert.contains(str(registered_domains_page._sell_on_auction_price_start_value), selling_auction_page.get_page_source())
        selling_auction_page.first_auction_enter_edit_prices()

        Assert.contains(registered_domains_page._third_domain_text_value, selling_auction_page.get_page_source())
        Assert.contains(str(registered_domains_page._sell_on_auction_price_start_value), selling_auction_page.get_page_source())

        selling_auction_page.edit_auction_prices()
        sleep(2)
        Assert.contains(u"Operacja wykonana poprawnie.", selling_auction_page.get_page_source())
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(selling_auction_page._selling_auctions_header, u"Lista aukcji (sprzedawca)"))

        Assert.contains(registered_domains_page._third_domain_text_value, selling_auction_page.get_page_source())
        Assert.contains(str(selling_auction_page._edit_auction_details_price_start_value), selling_auction_page.get_page_source())

        selling_auction_page.first_auction_enter_edit_description()

        Assert.contains(registered_domains_page._third_domain_text_value, selling_auction_page.get_page_source())
        Assert.contains(str(selling_auction_page._edit_auction_details_price_start_value), selling_auction_page.get_page_source())

        selling_auction_page.edit_auction_description()

        Assert.contains(u"Operacja wykonana poprawnie.", selling_auction_page.get_page_source())
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(selling_auction_page._selling_auctions_header, u"Lista aukcji (sprzedawca)"))
        selling_auction_page.delete_all_domain_selling_auctions()

        self.not_contains(registered_domains_page._third_domain_text_value, selling_auction_page.get_page_source())

    def test_sell_on_escrow_auction_should_succeed(self):

        login_value = "alfa"
        price = get_random_integer(2)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        escrow_auction_page = account_page.header.open_escrow_transactions_seller_list()
        escrow_auction_page.delete_all_escrow_auctions()
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.sell_on_escrow_auction(login_value, price)

        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.sell_on_auction_stage2_domain_text())
        Assert.contains(price, registered_domains_page.get_page_source())
        Assert.equal(login_value, registered_domains_page.sell_on_escrow_auction_stage2_buyer_login_text())

        registered_domains_page.sell_on_escrow_auction_stage2()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._add_escrow_transaction_result_text_field, u"Transakcja Escrow została rozpoczęta"))

        escrow_auction_page = account_page.header.open_escrow_transactions_seller_list()

        Assert.equal(registered_domains_page._first_domain_text_value, escrow_auction_page.first_auction_domain_name_text())
        Assert.contains(price, escrow_auction_page.get_page_source())
        Assert.equal(login_value, escrow_auction_page.first_auction_buyer_login_text())

        escrow_auction_page.delete_all_escrow_auctions()

    def test_search_selling_escrow_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        escrow_auction_page = account_page.header.open_escrow_transactions_seller_list()
        escrow_auction_page.get_text_first_domain_login_and_price()
        escrow_auction_page.search_for_auction(escrow_auction_page.first_domain_text)

        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(escrow_auction_page._first_auction_domain_name_field, escrow_auction_page.first_domain_text))
        Assert.equal(escrow_auction_page.first_domain_login_text, escrow_auction_page.first_auction_buyer_login_text())
        Assert.equal(escrow_auction_page.first_domain_price_text, escrow_auction_page.first_auction_price_text())


# NIE WYŚWIETLA WSZYSTKICH WYNIKÓW, ZGŁOSZONE



    def test_sell_on_escrow_auction_the_same_login_should_succeed(self):

        login_value = USER_DELTA
        price = get_random_integer(2)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.third_domain_text()
        registered_domains_page.select_third_domain()
        registered_domains_page.sell_on_escrow_auction(login_value, price)

        Assert.contains(registered_domains_page._third_domain_text_value, registered_domains_page.get_page_source())
        Assert.contains(price, registered_domains_page.get_page_source())
        Assert.contains(login_value, registered_domains_page.get_page_source())
        Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", registered_domains_page.get_page_source())

    def test_search_buyer_escrow_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        escrow_auction_page = account_page.header.open_escrow_transactions_buyer_list()
        escrow_auction_page.get_text_second_domain_status_and_price()
        escrow_auction_page.search_for_auction(escrow_auction_page.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_auction_page._first_auction_domain_name_field, escrow_auction_page.second_domain_text))
        Assert.equal(escrow_auction_page.second_domain_status_text, escrow_auction_page.first_auction_buyer_status_text())
        Assert.equal(escrow_auction_page.second_domain_price_text, escrow_auction_page.first_auction_price_text())

    def test_add_on_marketplace_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.fourth_domain_text()
        registered_domains_page.select_fourth_domain()
        registered_domains_page.add_on_marketplace()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Cena Kup Teraz: "+registered_domains_page._add_on_marketplace_buynow_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Cena minimalna: "+registered_domains_page._add_on_marketplace_minimum_price_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Dzierżawa: "+registered_domains_page._add_on_marketplace_lease_value))
        Assert.equal(registered_domains_page._fourth_domain_text_value, registered_domains_page.result_domain_text())

    # BŁĄD BAZY DANYCH, zgłoszone

    def test_delete_domain_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        register_domain_page = account_page.header.open_register_domain_page()
        register_domain_page.enter_domain_to_register(register_domain_page._domain_name_value_co_pl)
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._domain_status_field, u"Dostępna do rejestracji"))
        register_domain_page.register_domain_immediately()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._result_text_field, u"Domena zarejestrowana poprawnie"))
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)
        registered_domains_page.wait_until_domain_is_visible()
        registered_domains_page.select_first_searched_auction()
        registered_domains_page.delete_auction()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena została usunięta"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, registered_domains_page.result_domain_text())

        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)

        Assert.contains(u"Brak elementów spełniających warunki wyszukiwania", registered_domains_page.get_page_source())

    def test_transfer_domain_to_the_same_account_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        register_domain_page = account_page.header.open_register_domain_page()
        register_domain_page.enter_domain_to_register(register_domain_page._domain_name_value_co_pl)
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._domain_status_field, u"Dostępna do rejestracji"))
        register_domain_page.register_domain_immediately()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._result_text_field, u"Domena zarejestrowana poprawnie"))
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)
        registered_domains_page.wait_until_domain_is_visible()
        registered_domains_page.select_first_searched_auction()
        registered_domains_page.get_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))

        registered_domains_page.store_authinfo()
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain(register_domain_page._domain_name_value_co_pl, registered_domains_page._authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena już znajduje się na twoim koncie"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, transfer_domain_page.stage2_domain_text())

        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)
        registered_domains_page.select_first_searched_auction()
        registered_domains_page.delete_auction()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena została usunięta"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, registered_domains_page.result_domain_text())

    def test_transfer_domain_to_the_other_account_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        register_domain_page = account_page.header.open_register_domain_page()
        register_domain_page.enter_domain_to_register(register_domain_page._domain_name_value_co_pl)
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._domain_status_field, u"Dostępna do rejestracji"))
        register_domain_page.register_domain_immediately()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._result_text_field, u"Domena zarejestrowana poprawnie"))
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)
        registered_domains_page.wait_until_domain_is_visible()
        registered_domains_page.select_first_searched_auction()
        registered_domains_page.get_authinfo()
        print register_domain_page._domain_name_value_co_pl
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))

        registered_domains_page.store_authinfo()
        print registered_domains_page._authinfo
        account_page = home_page.header.logout()
        account_page = home_page.header.login(USER, PASSWORD)
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain(register_domain_page._domain_name_value_co_pl, registered_domains_page._authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena zostanie przeniesiona z innego konta"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, transfer_domain_page.stage2_domain_text())

        transfer_domain_page.stage2_change_dns_servers_and_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer domeny został zainicjowany"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        Assert.contains(register_domain_page._domain_name_value_co_pl, registered_domains_page.get_page_source())

        transfer_domain_page.cancel_all_domain_transfers()
        self.not_contains(register_domain_page._domain_name_value_co_pl, transfer_domain_page.get_page_source())

        account_page = home_page.header.logout()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        transfer_domains_page = account_page.header.open_transfer_domain_from_account_list()
        self.not_contains(register_domain_page._domain_name_value_co_pl, transfer_domains_page.get_page_source())

        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)
        registered_domains_page.select_first_searched_auction()
        registered_domains_page.delete_auction()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena została usunięta"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, registered_domains_page.result_domain_text())

    def test_transfer_domain_to_the_other_account_and_renew_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        register_domain_page = account_page.header.open_register_domain_page()
        register_domain_page.enter_domain_to_register(register_domain_page._domain_name_value_co_pl)
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._domain_status_field, u"Dostępna do rejestracji"))
        register_domain_page.register_domain_immediately()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._result_text_field, u"Domena zarejestrowana poprawnie"))
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)
        registered_domains_page.wait_until_domain_is_visible()
        registered_domains_page.select_first_searched_auction()
        registered_domains_page.get_authinfo()
        print register_domain_page._domain_name_value_co_pl
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))

        registered_domains_page.store_authinfo()
        print registered_domains_page._authinfo
        account_page = home_page.header.logout()
        account_page = home_page.header.login(USER, PASSWORD)
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain_and_renew(register_domain_page._domain_name_value_co_pl, registered_domains_page._authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena zostanie przeniesiona z innego konta"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, transfer_domain_page.stage2_domain_text())

        transfer_domain_page.stage2_change_dns_servers_and_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer domeny został zainicjowany"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        Assert.contains(register_domain_page._domain_name_value_co_pl, registered_domains_page.get_page_source())

        transfer_domain_page.cancel_all_domain_transfers()
        self.not_contains(register_domain_page._domain_name_value_co_pl, transfer_domain_page.get_page_source())

        account_page = home_page.header.logout()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        transfer_domains_page = account_page.header.open_transfer_domain_from_account_list()
        self.not_contains(register_domain_page._domain_name_value_co_pl, transfer_domains_page.get_page_source())

        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.search_for_auction(register_domain_page._domain_name_value_co_pl)
        registered_domains_page.select_first_searched_auction()
        registered_domains_page.delete_auction()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena została usunięta"))
        Assert.equal(register_domain_page._domain_name_value_co_pl, registered_domains_page.result_domain_text())

    def test_transfer_domain_to_the_other_account_wrong_data_should_succeed(self):

        _wrong_domain = get_random_uuid(10)+".co.pl"
        _wrong_authinfo = get_random_uuid(10)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain(_wrong_domain, _wrong_authinfo)

        WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Trwa sprawdzanie domeny"))

        if u"Niepoprawny kod AuthInfo: %s" % _wrong_domain in transfer_domain_page.stage2_result_text():
            Assert.equal(_wrong_domain, transfer_domain_page.stage2_domain_text())
        else:
            WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena nie istnieje"))
            Assert.equal(_wrong_domain, transfer_domain_page.stage2_domain_text())


    def test_search_expired_options_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        expired_options_page = account_page.header.open_expired_options_list()
        expired_options_page.get_text_sixth_option()
        expired_options_page.search_for_option(expired_options_page.sixth_option_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expired_options_page._first_option_value, expired_options_page.sixth_option_text))

    def test_register_option_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        register_domain_page = account_page.header.open_register_domain_page()
        register_domain_page.enter_domain_to_register(register_domain_page._domain_name_value_waw_pl)
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._domain_status_field, u"Dostępna do rejestracji"))
        register_domain_page.register_domain_immediately()
        WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element(register_domain_page._result_text_field, u"Domena zarejestrowana poprawnie"))
        to_pay_list = account_page.header.open_to_pay_list()
        to_pay_list.remove_all_payments()
        register_option_page = account_page.header.open_register_option_page()
        register_option_page.enter_option_to_register(register_domain_page._domain_name_value_waw_pl)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(register_option_page._stage2_result_field, u"Dostępna."))
        Assert.equal(register_domain_page._domain_name_value_waw_pl, register_option_page.stage2_domain_text())

        register_option_page.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(register_option_page._result_text_field, u"Operacja zawieszona, oczekuje na aktywowanie"))
        Assert.equal(register_domain_page._domain_name_value_waw_pl, register_option_page.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()
        Assert.contains(register_domain_page._domain_name_value_waw_pl, to_pay_list.get_page_source())
        Assert.contains(u"Rejestracja opcji", to_pay_list.get_page_source())

        to_pay_list.remove_all_payments()
        to_pay_list.refresh()
        self.not_contains(register_domain_page._domain_name_value_waw_pl, to_pay_list.get_page_source())
        self.not_contains(u"Rejestracja opcji", to_pay_list.get_page_source())

    def test_register_option_unavailable_should_succeed(self):

        _unavailable_option = get_random_uuid(8)+".unavailabla.pl"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        register_option_page = account_page.header.open_register_option_page()
        register_option_page.enter_option_to_register(_unavailable_option)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(register_option_page._stage2_result_field, u"Niedostępna"))
        Assert.equal(_unavailable_option, register_option_page.stage2_domain_text())

    # W DRUGIM KROKU NAZWA OPCJI WYŚWIETLA SIĘ BEZ PRZEDROSTKA (SAMO UNAVAILABLA.PL), zgłoszone

    def test_change_option_profile_data_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.first_option_text()
        registered_options_list.change_option_profile_data()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Ustawiono profil danych:"))
        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.result_domain_text())

    def test_get_option_authinfo_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.third_option_text()
        registered_options_list.get_option_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Kod AuthInfo:"))
        Assert.equal(registered_options_list._third_option_text_value, registered_options_list.result_domain_text())

    def test_renew_option_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        to_pay_list = account_page.header.open_to_pay_list()
        to_pay_list.remove_all_payments()
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.first_option_text()
        renew_option = registered_options_list.renew_option()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Opcja może być odnowiona"))
        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.stage2_option_text())

        registered_options_list.second_stage_checkboxes_and_submit()

        WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Operacja w toku"))

        if u"Operacja zawieszona, oczekuje na aktywowanie" in registered_options_list.result_text():
            Assert.equal(registered_options_list._first_option_text_value, registered_options_list.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()

        Assert.contains(registered_options_list._first_option_text_value, to_pay_list.get_page_source())
        Assert.contains(u"Odnowienie opcji", to_pay_list.get_page_source())

        to_pay_list.remove_all_payments()
        to_pay_list.refresh()

        self.not_contains(registered_options_list._first_option_text_value, to_pay_list.get_page_source())
        self.not_contains(u"Odnowienie opcji", to_pay_list.get_page_source())

#     def test_transfer_option_from_account_should_succeed(self):
#         login = "alfa"
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
#         internal_option_transfer_list = account_page.header.open_internal_option_transfer_list()
#         internal_option_transfer_list.delete_all_option_transfers()
#         registered_options_list = account_page.header.open_registered_options_list()
#         registered_options_list.third_option_text()
#         transfer_option = registered_options_list.transfer_option_from_account()
#         registered_options_list.transfer_option_enter_login(login)
#         registered_options_list.submit()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer został zainicjowany"))
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.result_domain_text())
#
#         account_page.header.open_internal_option_transfer_list()
#
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.transfer_list_first_domain_text())
#         Assert.contains(u"Oczekujący", registered_options_list.get_page_source())
#
#         registered_options_list.delete_first_transfer()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Transfer zostanie anulowany"))
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.stage2_option_text())
#
#         registered_options_list.submit_and_accept_alert()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer został anulowany"))
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.result_domain_text())
#
#         account_page.header.open_internal_option_transfer_list()
#
#         self.not_contains(registered_options_list._third_option_text_value, registered_options_list.get_page_source())
#         self.not_contains(u"Oczekujący", registered_options_list.get_page_source())


# DOPISAC


    def test_transfer_option_from_account_wrong_login_should_succeed(self):
        wrong_login = get_random_string(10)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_options_list = account_page.header.open_registered_options_list()
        transfer_option = registered_options_list.transfer_option_from_account()
        registered_options_list.transfer_option_enter_login(wrong_login)
        registered_options_list.submit()

        Assert.contains(u"Użytkownik o podanym loginie nie istnieje", registered_options_list.get_page_source())
        Assert.contains(wrong_login, registered_options_list.get_page_source())

#     def test_transfer_option_to_account_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
#         registered_options_list = account_page.header.open_registered_options_list()
#         registered_options_list.third_option_text()
#         registered_options_list.get_option_authinfo()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Kod AuthInfo:"))
#
#         registered_options_list.store_option_authinfo()
#
#         home_page.header.logout()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         transfer_option_list = account_page.header.open_transfer_option_to_account_list()
#         transfer_option_list.new_option_transfer(registered_options_list._third_option_text_value, registered_options_list._option_authinfo)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Opcja zostanie przeniesiona z innego konta"))
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.stage2_option_text())
#
#         registered_options_list.submit_and_accept_alert()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer opcji został zainicjowany"))
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.result_domain_text())
#
#         account_page.header.open_transfer_option_to_account_list()
#
#         Assert.contains(registered_options_list._third_option_text_value, registered_options_list.get_page_source())
#         Assert.contains(strftime("%Y-%m-%d", gmtime()), registered_options_list.get_page_source())
#         Assert.contains(u"Oczekujący", registered_options_list.get_page_source())
#
#         transfer_option_list.remove_first_transfer()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Transfer zostanie anulowany"))
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.stage2_option_text())
#
#         registered_options_list.submit_and_accept_alert()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer został anulowany"))
#         Assert.equal(registered_options_list._third_option_text_value, registered_options_list.result_domain_text())
#
#         account_page.header.open_transfer_option_to_account_list()
#
#         self.not_contains(registered_options_list._third_option_text_value, registered_options_list.get_page_source())
#
    def test_transfer_option_to_account_option_unavailable_should_succeed(self):

        _unavailable_option = get_random_uuid(8)+".unavailable.pl"
        _wrong_authinfo = get_random_uuid(8)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        transfer_option_list = account_page.header.open_transfer_option_to_account_list()
        transfer_option_list.new_option_transfer(_unavailable_option, _wrong_authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_option_list._stage2_result_field, u"Opcja może być przetransferowana"))
        Assert.equal(_unavailable_option, transfer_option_list.stage2_option_text())

    def test_new_hosting_account_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        to_pay_list = account_page.header.open_to_pay_list()
        to_pay_list.remove_all_payments()
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.new_hosting_account(PASSWORD_DELTA)

        Assert.equal("Pakiet Starter", hosting_account_list.get_text_packet_type_stage_2())
        Assert.equal(hosting_account_list._new_hosting_account_login_value, hosting_account_list.get_text_login_stage_2())

        hosting_account_list.new_hosting_account_stage_2()

        WebDriverWait(self.driver, 90).until(EC.text_to_be_present_in_element(hosting_account_list._new_hosting_account_result_text_field, u"Konto hostingowe zostało utworzone i aktywowane na okres próbny 14 dni."))

        to_pay_list = account_page.header.open_to_pay_list()

        Assert.contains(hosting_account_list._new_hosting_account_login_value, to_pay_list.get_page_source())
        Assert.contains(u"Zamówienie serwera", to_pay_list.get_page_source())

        to_pay_list.remove_all_payments()
        to_pay_list.refresh()

        self.not_contains(hosting_account_list._new_hosting_account_login_value, to_pay_list.get_page_source())
        self.not_contains(u"Zamówienie serwera", to_pay_list.get_page_source())

    def test_add_domain_to_hosting_account_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.add_domains_to_hosting_account()
        hosting_account_list.remove_all_all_domains_from_hosting_account()
        hosting_account_list.add_domains_to_hosting_account_stage2(registered_domains_page._first_domain_text_value)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena została dodana do konta:"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

        hosting_account_list.back_from_results_page()

        Assert.contains(registered_domains_page._first_domain_text_value, hosting_account_list.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), hosting_account_list.get_page_source())

        hosting_account_list.remove_all_all_domains_from_hosting_account()

        self.not_contains(registered_domains_page._first_domain_text_value, hosting_account_list.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), hosting_account_list.get_page_source())

    def test_add_domain_to_hosting_account_wrong_domain_name_should_succeed(self):

        _wrong_domain_name = get_random_string(7)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.add_domains_to_hosting_account()
        hosting_account_list.add_domains_to_hosting_account_stage2(_wrong_domain_name)

        Assert.contains(u"Musisz podać poprawne nazwy domen", hosting_account_list.get_page_source())

    def test_renew_hosting_account_manually_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        to_pay_list = account_page.header.open_to_pay_list()
        to_pay_list.remove_all_payments()
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.first_hosting_account_get_text()
        hosting_account_list.renew_first_hosting_account()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hosting_account_list._stage2_result_text_field, u"Konto hostingowe zostanie przedłużone"))
        Assert.equal(hosting_account_list._first_hosting_account_text, hosting_account_list.stage2_result_domain_text())

        hosting_account_list.renew_hosting_account_stage2()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hosting_account_list._result_text_field, u"Operacja zawieszona, oczekuje na aktywowanie"))
        Assert.equal(hosting_account_list._first_hosting_account_text, hosting_account_list.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, hosting_account_list._first_hosting_account_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Przedłużenie hostingu"))

        to_pay_list.remove_all_payments()

        WebDriverWait(self.driver, 5).until_not(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, hosting_account_list._first_hosting_account_text))
        WebDriverWait(self.driver, 5).until_not(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Przedłużenie hostingu"))

    def test_add_offer_on_marketplace_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.open_offers_tab()
        domains_on_marketplace_list.get_text_second_domain()
        domains_on_marketplace_list.add_offer_to_second_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._domain_field_stage1, domains_on_marketplace_list._second_domain_text))

        domains_on_marketplace_list.get_text_price_buynow()
        domains_on_marketplace_list.submit_offer_stage1()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._domain_field_stage1, domains_on_marketplace_list._second_domain_text))
        Assert.contains(domains_on_marketplace_list.price_buynow, domains_on_marketplace_list.get_page_source())
        Assert.contains(domains_on_marketplace_list._price_value, domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.submit_offer_stage2()

        Assert.contains(u"Oferta została złożona", domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.delete_offer_stage1()

        Assert.contains(domains_on_marketplace_list._price_value, domains_on_marketplace_list.get_page_source())
        Assert.contains(domains_on_marketplace_list._second_domain_text, domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.delete_offer_stage2()

        Assert.contains(u"Negocjacje zostały zamknięte", domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.back_to_offers_page()

        self.not_contains(domains_on_marketplace_list._second_domain_text, domains_on_marketplace_list.get_page_source())

# CHROME NIE CHWYTA self._additional_message_field

    def test_search_domains_on_marketplace_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.open_auctions_tab()
        domains_on_marketplace_list.get_text_fourth_domain_and_price()
        domains_on_marketplace_list.search_for_domain(domains_on_marketplace_list._fourth_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._auction_page_domain_name_field, domains_on_marketplace_list._fourth_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._auction_page_price_field, domains_on_marketplace_list._fourth_domain_price_text))

    def test_filter_domains_on_marketplace_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.filter_results_5_characters_com_pl()

        Assert.true(re.compile(r"^\w{5}\.com\.pl$").match(domains_on_marketplace_list.first_domain_text()))

    def test_subscribe_filtered_domains_on_marketplace_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        subscriptions_on_marketplace_list = account_page.header.open_subscriptions_on_marketplace_list()
        subscriptions_on_marketplace_list.delete_all_subscriptions()
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.filter_results_length_com_pl()
        sleep(2)
        domains_on_marketplace_list.subscribe_results()

        Assert.contains(u"Długość:", domains_on_marketplace_list.get_page_source())
        Assert.contains(str(domains_on_marketplace_list._filter_length_from_value), domains_on_marketplace_list.get_page_source())
        Assert.contains(str(domains_on_marketplace_list._filter_length_to_value), domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.subscribe_results_stage2()

        Assert.contains(domains_on_marketplace_list._subscribe_results_subuscription_name_value, domains_on_marketplace_list.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.delete_all_subscriptions()
        Assert.contains(u"Brak subskrypcji domen na giełdzie", domains_on_marketplace_list.get_page_source())
        self.not_contains(domains_on_marketplace_list._subscribe_results_subuscription_name_value, domains_on_marketplace_list.get_page_source())

    def test_watch_new_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        watched_domains_page = account_page.header.open_watched_domains_list()
        watched_domains_page.delete_all_domains()
        watched_domains_page.watch_new_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_domains_page._result_text_field, u"Domena została dodana do obserwacji"))
        Assert.equal(watched_domains_page._domain_name_value, watched_domains_page.result_domain_text())

        account_page.header.open_watched_domains_list()

        Assert.contains(watched_domains_page._domain_name_value, watched_domains_page.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), watched_domains_page.get_page_source())

        watched_domains_page.first_domain_change_watch_settings()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_domains_page._result_text_field, u"Ustawienia obserwacji domeny zostały zmienione"))
        Assert.equal(watched_domains_page._domain_name_value, watched_domains_page.result_domain_text())

        account_page.header.open_watched_domains_list()
        watched_domains_page.delete_all_domains()

        self.not_contains(watched_domains_page._domain_name_value, watched_domains_page.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), watched_domains_page.get_page_source())

    def test_watch_new_seller_should_succeed(self):

        seller_name = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        watched_sellers_page = account_page.header.open_watched_sellers_list()
        watched_sellers_page.delete_all_sellers()
        watched_sellers_page.watch_new_seller(seller_name)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_sellers_page._watched_sellers_header, u"Lista obserwowanych sprzedawców"))
        Assert.contains(seller_name, watched_sellers_page.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), watched_sellers_page.get_page_source())

        watched_sellers_page.change_first_seller_settings()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_sellers_page._result_text_field, u"Ustawienia obserwacji sprzedawcy zostały zmienione"))

        account_page.header.open_watched_sellers_list()
        watched_sellers_page.delete_all_sellers()

        self.not_contains(seller_name, watched_sellers_page.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), watched_sellers_page.get_page_source())

    def test_watch_new_seller_the_same_login_should_succeed(self):

        seller_name = USER_DELTA

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        watched_sellers_page = account_page.header.open_watched_sellers_list()
        watched_sellers_page.watch_new_seller(seller_name)

        Assert.contains(u"Nie możesz obserwować samego siebie", watched_sellers_page.get_page_source())

    def test_new_option_auction_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.delete_all_domain_selling_auctions()
        new_option_auction_page = account_page.header.open_new_option_auction_page()
        new_option_auction_page.new_option_auction_enter_details()

        Assert.contains(new_option_auction_page._option_name, new_option_auction_page.get_page_source())
        Assert.contains(str(new_option_auction_page._price_start_value), new_option_auction_page.get_page_source())
        Assert.contains(str(new_option_auction_page._price_minimum_value), new_option_auction_page.get_page_source())
        Assert.contains(str(new_option_auction_page._price_buynow_value), new_option_auction_page.get_page_source())
        # Assert.contains(new_option_auction_page._description_value, new_option_auction_page.get_page_source())

        new_option_auction_page.new_option_auction_stage_2_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(new_option_auction_page._result_text_field, u"Aukcja opcji została wystawiona z ceną początkową "+str(new_option_auction_page._price_start_value)))
        Assert.equal(new_option_auction_page._option_name, new_option_auction_page.result_domain_text())

        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.delete_all_domain_selling_auctions()

        self.not_contains(new_option_auction_page._option_name, selling_auction_page.get_page_source())

#CHROME NIE CHWYTA self._description_field

    def test_search_seller_ended_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        ended_auctions_list = account_page.header.open_seller_ended_auctions_list()
        ended_auctions_list.get_second_domain_and_price_text()
        ended_auctions_list.search_for_domain(ended_auctions_list._second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_checkbox, ended_auctions_list._second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_price_field, ended_auctions_list._second_domain_price_text))

    def test_search_buyer_ended_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        ended_auctions_list = account_page.header.open_buyer_ended_auctions_list()
        ended_auctions_list.get_third_domain_and_price_text()
        ended_auctions_list.search_for_domain(ended_auctions_list._third_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_checkbox, ended_auctions_list._third_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_price_field, ended_auctions_list._third_domain_price_text))

#     def test_new_escrow_option_transaction_should_succeed(self):
#
#         login = "alfa"
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         escrow_option_transaction_page = account_page.header.open_escrow_option_selling_transaction_list()
#         escrow_option_transaction_page.filter_new()
#         escrow_option_transaction_page.delete_all_auctions()
#         escrow_option_transaction_page.add_escrow_option_transaction(login)
#
#         Assert.equal(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.stage2_option_text())
#         Assert.equal(login, escrow_option_transaction_page.stage2_login_text())
#         Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())
#
#         escrow_option_transaction_page.add_description()
#         escrow_option_transaction_page.stage2_submit_and_accept_alert()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._added_transaction_result_text_field, u"Transakcja escrow została rozpoczęta."))
#
#         account_page.header.open_escrow_option_selling_transaction_list()
#
#         Assert.contains(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.get_page_source())
#         Assert.contains(login, escrow_option_transaction_page.get_page_source())
#         Assert.contains("Nowa", escrow_option_transaction_page.get_page_source())
#         Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())
#
#         escrow_option_transaction_page.delete_first_auction()
#
#         Assert.equal(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.stage2_option_text())
#         Assert.equal(login, escrow_option_transaction_page.stage2_login_text())
#         Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())
#
#         escrow_option_transaction_page.stage2_submit_and_accept_alert()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._added_transaction_result_text_field, u"Transakcja escrow została anulowana."))
#
#         account_page.header.open_escrow_option_selling_transaction_list()
#         escrow_option_transaction_page.filter_new()
#
#         self.not_contains(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.get_page_source())
#         self.not_contains(login, escrow_option_transaction_page.get_page_source())
#         self.not_contains(strftime("%Y-%m-%d", gmtime()), escrow_option_transaction_page.get_page_source())
#
# #Błąd podczas wykonywania operacji, zgłoszone
#
#     def test_search_escrow_option_selling_transactions_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         escrow_option_transaction_page = account_page.header.open_escrow_option_selling_transaction_list()
#         escrow_option_transaction_page.get_text_third_domain_login_and_price()
#         escrow_option_transaction_page.search_for_auction(escrow_option_transaction_page.third_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_field, escrow_option_transaction_page.third_domain_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_login_field, escrow_option_transaction_page.third_domain_login_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_price_field, escrow_option_transaction_page.third_domain_price_text))
#
#     def test_new_escrow_option_transaction_the_same_login_should_succeed(self):
#
#         login = USER_BETA
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
#         escrow_option_transaction_page = account_page.header.open_escrow_option_selling_transaction_list()
#         escrow_option_transaction_page.add_escrow_option_transaction(login)
#
#         Assert.contains(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.get_page_source())
#         Assert.contains(login, escrow_option_transaction_page.get_page_source())
#         Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())
#         Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", escrow_option_transaction_page.get_page_source())
#
#     def test_search_escrow_option_buying_transactions_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         escrow_option_transaction_page = account_page.header.open_escrow_option_buying_transaction_list()
#         escrow_option_transaction_page.get_text_second_domain_status_and_price()
#         escrow_option_transaction_page.search_for_auction(escrow_option_transaction_page.second_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_field, escrow_option_transaction_page.second_domain_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_status_field, escrow_option_transaction_page.second_domain_status_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_price_field, escrow_option_transaction_page.second_domain_price_text))
#
#     def test_search_rental_buyer_transactions_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_buyer_list = account_page.header.open_rental_buyer_list()
#         rental_buyer_list.get_text_second_domain_status_and_price()
#         rental_buyer_list.search_for_domain(rental_buyer_list.second_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_buyer_list._first_domain_field, rental_buyer_list.second_domain_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_buyer_list._first_domain_status_field, rental_buyer_list.second_domain_status_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_buyer_list._first_domain_price_field, rental_buyer_list.second_domain_price_text))
#
#     def test_rental_buyer_transaction_details_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_buyer_list = account_page.header.open_rental_buyer_list()
#         rental_buyer_list.get_text_second_domain_status_and_price()
#         rental_buyer_list.enter_second_domain_details()
#
#         Assert.contains(rental_buyer_list.second_domain_text, rental_buyer_list.get_page_source())
#         Assert.contains(rental_buyer_list.second_domain_price_text, rental_buyer_list.get_page_source())
#
#     def test_rental_buyer_transaction_add_note_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_buyer_list = account_page.header.open_rental_buyer_list()
#         rental_buyer_list.get_text_second_domain_status_and_price()
#         rental_buyer_list.second_domain_enter_add_note()
#
#         Assert.contains(rental_buyer_list.second_domain_text, rental_buyer_list.get_page_source())
#
#         rental_buyer_list.add_note()
#         rental_buyer_list.second_domain_enter_add_note()
#
#         Assert.contains(rental_buyer_list._add_note_value, rental_buyer_list.get_page_source())
#
#     def test_search_rental_seller_transactions_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
#         rental_seller_list = account_page.header.open_rental_seller_list()
#         rental_seller_list.get_text_second_domain_login_status_and_price()
#         rental_seller_list.search_for_domain(rental_seller_list.second_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_field, rental_seller_list.second_domain_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_login_field, rental_seller_list.second_domain_login_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_status_field, rental_seller_list.second_domain_status_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_price_field, rental_seller_list.second_domain_price_text))
#
#     def test_rental_seller_transaction_details_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_seller_list = account_page.header.open_rental_seller_list()
#         rental_seller_list.get_text_second_domain_login_status_and_price()
#         rental_seller_list.enter_second_domain_details()
#
#         Assert.contains(rental_seller_list.second_domain_text, rental_seller_list.get_page_source())
#         Assert.contains(rental_seller_list.second_domain_login_text, rental_seller_list.get_page_source())
#         Assert.contains(rental_seller_list.second_domain_price_text, rental_seller_list.get_page_source())
#
#     def test_rental_seller_transaction_add_note_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_seller_list = account_page.header.open_rental_seller_list()
#         rental_seller_list.get_text_second_domain_login_status_and_price()
#         rental_seller_list.second_domain_enter_add_note()
#
#         Assert.contains(rental_seller_list.second_domain_text, rental_seller_list.get_page_source())
#         Assert.contains(rental_seller_list.second_domain_login_text, rental_seller_list.get_page_source())
#
#         rental_seller_list.add_note()
#         rental_seller_list.second_domain_enter_add_note()
#
#         Assert.contains(rental_seller_list._add_note_value, rental_seller_list.get_page_source())
#
#     def test_new_rental_seller_transaction_should_succeed(self):
#
#         login= "alfa"
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
#         rental_seller_list = account_page.header.open_rental_seller_list()
#         rental_seller_list.add_rental_transaction(login)
#
#         Assert.contains(rental_seller_list._rental_domain_name_text, rental_seller_list.get_page_source())
#         Assert.contains(login, rental_seller_list.get_page_source())
#         Assert.contains(rental_seller_list._add_rental_transaction_monthly_rent_value, rental_seller_list.get_page_source())
#         Assert.contains(str(rental_seller_list._add_rental_transaction_rent_duration_value)+" miesi", rental_seller_list.get_page_source())
#         Assert.contains(u"Wydzierżawiający może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
#         Assert.contains(u"Dzierżawca może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
#         Assert.contains(str(rental_seller_list._add_rental_transaction_notice_period_value)+" miesi", rental_seller_list.get_page_source())
#         Assert.contains(str(rental_seller_list._add_rental_transaction_preemption_price_value), rental_seller_list.get_page_source())
#
#         rental_seller_list.add_rental_transaction_submit()
#         WebDriverWait(self.driver, 40).until_not(EC.text_to_be_present_in_element(rental_seller_list._add_rental_transaction_performing_text_field, "Trwa wykonywanie operacji..."))
#         account_page.header.open_rental_seller_list()
#
#         Assert.contains(rental_seller_list._rental_domain_name_text, rental_seller_list.get_page_source())
#         Assert.contains(login, rental_seller_list.get_page_source())
#         Assert.contains(rental_seller_list._add_rental_transaction_monthly_rent_value, rental_seller_list.get_page_source())
#
#         rental_seller_list.cancel_first_rental_transaction()
#
#         Assert.contains(rental_seller_list._rental_domain_name_text, rental_seller_list.get_page_source())
#         Assert.contains(login, rental_seller_list.get_page_source())
#         Assert.contains(rental_seller_list._add_rental_transaction_monthly_rent_value, rental_seller_list.get_page_source())
#         Assert.contains(str(rental_seller_list._add_rental_transaction_rent_duration_value)+" miesi", rental_seller_list.get_page_source())
#         Assert.contains(u"Wydzierżawiający może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
#         Assert.contains(u"Dzierżawca może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
#         Assert.contains(str(rental_seller_list._add_rental_transaction_notice_period_value)+" miesi", rental_seller_list.get_page_source())
#         Assert.contains(str(rental_seller_list._add_rental_transaction_preemption_price_value), rental_seller_list.get_page_source())
#
#         rental_seller_list.cancel_first_rental_transaction_submit()
#
#         Assert.contains(u"Transakcja dzierżawy została anulowana.", rental_seller_list.get_page_source())
#
# #TRWA WYKONYWANIE OPERACJI, zgłoszone
#
#     def test_new_rental_seller_transaction_wrong_login_should_succeed(self):
#
#         login= get_random_string(10)
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_seller_list = account_page.header.open_rental_seller_list()
#         rental_seller_list.add_rental_transaction(login)
#
#         Assert.contains(u"Użytkownik o podanym loginie nie istnieje", rental_seller_list.get_page_source())
#
#     def test_new_rental_seller_transaction_the_same_login_should_succeed(self):
#
#         login = USER_DELTA
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_seller_list = account_page.header.open_rental_seller_list()
#         rental_seller_list.add_rental_transaction(login)
#
#         Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", rental_seller_list.get_page_source())
#
#     def test_new_rental_seller_transaction_wrong_domain_name_should_succeed(self):
#
#         login = "alfa"
#         domain_name = get_random_string(10)
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         rental_seller_list = account_page.header.open_rental_seller_list()
#         rental_seller_list.add_rental_transaction_wrong_domain_name(login, domain_name)
#
#         Assert.contains(u"Domena nie jest zarejestrowana", rental_seller_list.get_page_source())
#
#     def test_search_hire_buyer_transactions_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_buyer_list = account_page.header.open_hire_buyer_list()
#         hire_buyer_list.get_text_second_domain_status_price_and_installments()
#         hire_buyer_list.search_for_domain(hire_buyer_list.second_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_field, hire_buyer_list.second_domain_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_status_field, hire_buyer_list.second_domain_status_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_price_field, hire_buyer_list.second_domain_price_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_installments_field, hire_buyer_list.second_domain_installments_text))
#
#     def test_hire_buyer_transaction_details_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_buyer_list = account_page.header.open_hire_buyer_list()
#         hire_buyer_list.get_text_second_domain_status_price_and_installments()
#         hire_buyer_list.enter_second_domain_details()
#
#         Assert.contains(hire_buyer_list.second_domain_text, hire_buyer_list.get_page_source())
#         Assert.contains(hire_buyer_list.second_domain_price_text, hire_buyer_list.get_page_source())
#         Assert.contains(hire_buyer_list.second_domain_installments_text, hire_buyer_list.get_page_source())
#
#     def test_hire_buyer_transaction_add_note_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_buyer_list = account_page.header.open_hire_buyer_list()
#         hire_buyer_list.get_text_second_domain_status_price_and_installments()
#         hire_buyer_list.second_domain_enter_add_note()
#
#         Assert.contains(hire_buyer_list.second_domain_text, hire_buyer_list.get_page_source())
#
#         hire_buyer_list.add_note()
#         hire_buyer_list.second_domain_enter_add_note()
#
#         Assert.contains(hire_buyer_list._add_note_value, hire_buyer_list.get_page_source())
#
#     def test_search_hire_seller_transactions_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
#         hire_seller_list = account_page.header.open_hire_seller_list()
#         hire_seller_list.get_text_second_domain_login_status_price_and_installments()
#         hire_seller_list.search_for_domain(hire_seller_list.second_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_field, hire_seller_list.second_domain_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_login_field, hire_seller_list.second_domain_login_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_status_field, hire_seller_list.second_domain_status_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_price_field, hire_seller_list.second_domain_price_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_installments_field, hire_seller_list.second_domain_installments_text))
#
#     def test_hire_seller_transaction_details_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_seller_list = account_page.header.open_hire_seller_list()
#         hire_seller_list.get_text_second_domain_login_status_price_and_installments()
#         hire_seller_list.enter_second_domain_details()
#
#         Assert.contains(hire_seller_list.second_domain_text, hire_seller_list.get_page_source())
#         Assert.contains(hire_seller_list.second_domain_login_text, hire_seller_list.get_page_source())
#         Assert.contains(hire_seller_list.second_domain_price_text, hire_seller_list.get_page_source())
#         Assert.contains(hire_seller_list.second_domain_installments_text, hire_seller_list.get_page_source())
#
#     def test_hire_seller_transaction_add_note_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_seller_list = account_page.header.open_hire_seller_list()
#         hire_seller_list.get_text_second_domain_login_status_price_and_installments()
#         hire_seller_list.second_domain_enter_add_note()
#
#         Assert.contains(hire_seller_list.second_domain_text, hire_seller_list.get_page_source())
#         Assert.contains(hire_seller_list.second_domain_login_text, hire_seller_list.get_page_source())
#
#         hire_seller_list.add_note()
#         hire_seller_list.second_domain_enter_add_note()
#
#         Assert.contains(hire_seller_list._add_note_value, hire_seller_list.get_page_source())
#
#     def test_new_hire_seller_transaction_should_succeed(self):
#
#         login = "alfa"
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_seller_list = account_page.header.open_hire_seller_list()
#         hire_seller_list.add_hire_transaction_stage1()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._add_hire_transaction_domain_name_second_checkbox, ".pl"))
#
#         hire_seller_list.add_hire_transaction_stage2(login)
#
#         Assert.contains(hire_seller_list._hire_domain_name_text, hire_seller_list.get_page_source())
#         Assert.contains(login, hire_seller_list.get_page_source())
#         Assert.contains(hire_seller_list._add_hire_transaction_monthly_installment_value, hire_seller_list.get_page_source())
#         Assert.contains(str(hire_seller_list._add_hire_transaction_number_of_installments_value)+" miesi", hire_seller_list.get_page_source())
#         Assert.contains(str(int(hire_seller_list._add_hire_transaction_monthly_installment_value) * int(hire_seller_list._add_hire_transaction_number_of_installments_value)), hire_seller_list.get_page_source())
#
#         hire_seller_list.add_hire_transaction_submit()
#         WebDriverWait(self.driver, 40).until_not(EC.text_to_be_present_in_element(hire_seller_list._add_hire_transaction_performing_text_field, "Trwa wykonywanie operacji..."))
#         account_page.header.open_hire_seller_list()
#
#         Assert.contains(hire_seller_list._hire_domain_name_text, hire_seller_list.get_page_source())
#         Assert.contains(login, hire_seller_list.get_page_source())
#         Assert.contains(str(int(hire_seller_list._add_hire_transaction_monthly_installment_value) * int(hire_seller_list._add_hire_transaction_number_of_installments_value)), hire_seller_list.get_page_source())
#
#         hire_seller_list.cancel_first_hire_transaction()
#
#         Assert.contains(hire_seller_list._hire_domain_name_text, hire_seller_list.get_page_source())
#         Assert.contains(login, hire_seller_list.get_page_source())
#         Assert.contains(hire_seller_list._add_hire_transaction_monthly_installment_value, hire_seller_list.get_page_source())
#         Assert.contains(str(hire_seller_list._add_hire_transaction_number_of_installments_value)+" miesi", hire_seller_list.get_page_source())
#         Assert.contains(str(int(hire_seller_list._add_hire_transaction_monthly_installment_value) * int(hire_seller_list._add_hire_transaction_number_of_installments_value)), hire_seller_list.get_page_source())
#
#         hire_seller_list.cancel_first_hire_transaction_submit()
#
#         Assert.contains(u"Transakcja sprzedaży na raty została anulowana.", hire_seller_list.get_page_source())
#
# #TRWA WYKONYWANIE OPERACJI, zgłoszone
#
#     def test_new_hire_seller_transaction_wrong_login_should_succeed(self):
#
#         login = get_random_string(9)
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_seller_list = account_page.header.open_hire_seller_list()
#         hire_seller_list.add_hire_transaction_stage1()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._add_hire_transaction_domain_name_second_checkbox, ".pl"))
#
#         hire_seller_list.add_hire_transaction_stage2(login)
#
#         Assert.contains(u"Użytkownik o podanym loginie nie istnieje", hire_seller_list.get_page_source())
#
#     def test_new_hire_seller_transaction_the_same_login_should_succeed(self):
#
#         login = USER_DELTA
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_seller_list = account_page.header.open_hire_seller_list()
#         hire_seller_list.add_hire_transaction_stage1()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._add_hire_transaction_domain_name_second_checkbox, ".pl"))
#
#         hire_seller_list.add_hire_transaction_stage2(login)
#
#         Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", hire_seller_list.get_page_source())
#
#     def test_new_hire_seller_transaction_wrong_domain_name_should_succeed(self):
#
#         login = "alfa"
#         domain_name = get_random_string(9)
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         hire_seller_list = account_page.header.open_hire_seller_list()
#         hire_seller_list.add_hire_transaction_wrong_domain_name(login, domain_name)
#
#         Assert.contains(u"Domena nie jest zarejestrowana", hire_seller_list.get_page_source())
#
#     def test_block_seller_should_succeed(self):
#
#         seller_name = "alfa"
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         blocked_sellers_page = account_page.header.open_blocked_sellers_list()
#         blocked_sellers_page.block_seller(seller_name)
#
#         Assert.contains(u"Operacja wykonana poprawnie.", blocked_sellers_page.get_page_source())
#         sleep(7)
#         Assert.contains(seller_name, blocked_sellers_page.get_page_source())
#         Assert.contains(strftime("%Y-%m-%d", gmtime()), blocked_sellers_page.get_page_source())
#
#         blocked_sellers_page.delete_first_seller()
#
#         Assert.contains(seller_name, blocked_sellers_page.get_page_source())
#         Assert.contains(blocked_sellers_page._note_value, blocked_sellers_page.get_page_source())
#
#         blocked_sellers_page.delete_first_seller_submit()
#
#         Assert.contains(u"Operacja wykonana poprawnie.", blocked_sellers_page.get_page_source())
#         sleep(7)
#         self.not_contains(seller_name, blocked_sellers_page.get_page_source())
#         self.not_contains(strftime("%Y-%m-%d", gmtime()), blocked_sellers_page.get_page_source())
#
#     def test_block_seller_wrong_login_should_succeed(self):
#
#         seller_name = get_random_string(10)
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         blocked_sellers_page = account_page.header.open_blocked_sellers_list()
#         blocked_sellers_page.block_seller(seller_name)
#
#         Assert.contains(seller_name, blocked_sellers_page.get_page_source())
#         Assert.contains(u"Użytkownik o podanym loginie nie istnieje", blocked_sellers_page.get_page_source())
#
#     def test_search_selling_history_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         selling_history_page = account_page.header.open_selling_history_list()
#         selling_history_page.get_second_domain_text()
#         selling_history_page.search_for_domain(selling_history_page._second_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(selling_history_page._first_domain_checkbox, selling_history_page._second_domain_text))
#
#     def test_catch_domain_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         expiring_domains_list = account_page.header.open_expiring_domains_list()
#         expiring_domains_list.first_domain_text()
#         expiring_domains_list.catch_first_domain()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expiring_domains_list._result_text_field, u"Domena dodana do przechwycenia"))
#         Assert.equal(expiring_domains_list._first_domain_text_value, expiring_domains_list.result_domain_text())
#
#         domains_to_catch = account_page.header.open_domains_to_catch_list()
#
#         Assert.contains(expiring_domains_list._first_domain_text_value, domains_to_catch.get_page_source())
#         Assert.contains(strftime("%Y-%m-%d", gmtime()), domains_to_catch.get_page_source())
#
#         domains_to_catch.delete_first_domain()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expiring_domains_list._result_text_field, u"Operacja wykonana poprawnie"))
#         Assert.equal(expiring_domains_list._first_domain_text_value, expiring_domains_list.result_domain_text())
#
#         account_page.header.open_domains_to_catch_list()
#
#         self.not_contains(expiring_domains_list._first_domain_text_value, domains_to_catch.get_page_source())
#         self.not_contains(strftime("%Y-%m-%d", gmtime()), domains_to_catch.get_page_source())
#
#     def test_search_domains_to_catch_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         expiring_domains_list = account_page.header.open_expiring_domains_list()
#         expiring_domains_list.sixth_domain_text()
#         expiring_domains_list.search_for_domain_to_catch(expiring_domains_list._sixth_domain_text_value)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expiring_domains_list._first_domain_checkbox, expiring_domains_list._sixth_domain_text_value))
#
#     def test_filter_domains_to_catch_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         expiring_domains_list = account_page.header.open_expiring_domains_list()
#         expiring_domains_list.filter_results_4_characters_com_pl()
#
#         Assert.true(re.compile(r"^\w{4}\.com\.pl$").match(expiring_domains_list.first_domain_text()))
#
#     def test_subscribe_filtered_domains_to_catch_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
#         expiring_domains_list = account_page.header.open_expiring_domains_list()
#         expiring_domains_list.filter_results_length_and_pl()
#         expiring_domains_list.subscribe_results()
#
#         Assert.contains("Rozszerzenie:", expiring_domains_list.get_page_source())
#         Assert.contains(".pl", expiring_domains_list.get_page_source())
#         Assert.contains(u"Długość:", expiring_domains_list.get_page_source())
#         Assert.contains(str(expiring_domains_list._filter_length_from_value), expiring_domains_list.get_page_source())
#         Assert.contains(str(expiring_domains_list._filter_length_to_value), expiring_domains_list.get_page_source())
#
#         expiring_domains_list.enter_subscription_name_and_submit()
#         subscriptions_list = account_page.header.open_expiring_domains_subscriptions_list()
#
#         Assert.contains(expiring_domains_list._subscription_name_value, expiring_domains_list.get_page_source())
#         Assert.contains(strftime("%Y-%m-%d", gmtime()), expiring_domains_list.get_page_source())
#
#         expiring_domains_list.delete_added_subscription_1_stage()
#
#         Assert.contains(expiring_domains_list._subscription_name_value, expiring_domains_list.get_page_source())
#         Assert.contains("Rozszerzenie:", expiring_domains_list.get_page_source())
#         Assert.contains(".pl", expiring_domains_list.get_page_source())
#         Assert.contains(u"Długość:", expiring_domains_list.get_page_source())
#         Assert.contains(str(expiring_domains_list._filter_length_from_value), expiring_domains_list.get_page_source())
#         Assert.contains(str(expiring_domains_list._filter_length_to_value), expiring_domains_list.get_page_source())
#
#         expiring_domains_list.delete_added_subscription_2_stage()
#
#         self.not_contains(expiring_domains_list._subscription_name_value, expiring_domains_list.get_page_source())
#
# # BŁĄD PRZY DWUKROTNYM DODAWANIU SUBSKRYPCJI, zgłoszone
#
#     def test_search_monitor_domains_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         monitor_domains_list = account_page.header.open_monitor_domains_list()
#         monitor_domains_list.get_text_second_domain_and_status()
#         monitor_domains_list.search_for_domain(monitor_domains_list.second_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_field, monitor_domains_list.second_domain_text))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_status_field, monitor_domains_list.second_domain_status_text))
#
#     def test_change_first_monitored_domain_settings_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         monitor_domains_list = account_page.header.open_monitor_domains_list()
#         monitor_domains_list.get_text_first_domain()
#         monitor_domains_list.change_first_domain_settings()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Opcje monitorowania zmienione"))
#         Assert.equal(monitor_domains_list.first_domain_text, monitor_domains_list.result_domain_text())
#
#     def test_monitor_new_domain_should_succeed(self):
#
#         domain_name = "aaaaaa"+get_random_string(6)+".waw.pl"
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         monitor_domains_list = account_page.header.open_monitor_domains_list()
#         monitor_domains_list.monitor_new_domain(domain_name)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Monitorowanie domeny włączone"))
#         Assert.equal(domain_name, monitor_domains_list.result_domain_text())
#
#         account_page.header.open_monitor_domains_list()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_field, domain_name))
#
#         monitor_domains_list.remove_first_monitored_domain()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Monitorowanie domeny wyłączone"))
#         Assert.equal(domain_name, monitor_domains_list.result_domain_text())
#
#         account_page.header.open_monitor_domains_list()
#
#         self.not_contains(domain_name, monitor_domains_list.get_page_source())
#
#     def test_monitor_new_domain_already_monitored_domain_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         monitor_domains_list = account_page.header.open_monitor_domains_list()
#         monitor_domains_list.get_text_first_domain()
#         monitor_domains_list.monitor_new_domain(monitor_domains_list.first_domain_text)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Już monitorujesz tę domenę"))
#         Assert.equal(monitor_domains_list.first_domain_text, monitor_domains_list.result_domain_text())
#
#     def test_filter_monitored_domains_available_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         monitor_domains_list = account_page.header.open_monitor_domains_list()
#         monitor_domains_list.filter_available()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_status_field, u"Dostępna"))
#
#     def test_filter_monitored_domains_registered_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         monitor_domains_list = account_page.header.open_monitor_domains_list()
#         monitor_domains_list.filter_registered()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_status_field, u"Zarejestrowana"))
#
#     def test_add_domain_catalog_should_succeed(self):
#
#         catalog_name = "aaaaaaaa"+get_random_string(5)
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         domain_catalog_list = account_page.header.open_domain_catalog_list()
#         domain_catalog_list.add_catalog_stage1(catalog_name)
#
#         Assert.contains(catalog_name, domain_catalog_list.get_page_source())
#
#         domain_catalog_list.add_catalog_stage2()
#
#         WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element(domain_catalog_list._result_text_field, u"Operacja w toku"))
#
#         if u"Domena nie jest wystawiona na sprzedaż" in domain_catalog_list.result_text():
#             Assert.equal(domain_catalog_list.domain_name, domain_catalog_list.result_domain_text())
#         else:
#             WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._result_text_field, u"Domena dodana do katalogu"))
#             Assert.equal(domain_catalog_list.domain_name, domain_catalog_list.result_domain_text())
#
#         domain_catalog_list.back_to_domains_in_catalog()
#
#         Assert.contains(domain_catalog_list.domain_name, domain_catalog_list.get_page_source())
#
#         domain_catalog_list.remove_first_domain_in_catalog()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._result_text_field, u"Domena usunięta z katalogu"))
#         Assert.equal(domain_catalog_list.domain_name, domain_catalog_list.result_domain_text())
#
#         domain_catalog_list.back_to_domains_in_catalog()
# 2
#         self.not_contains(domain_catalog_list.domain_name, domain_catalog_list.get_page_source())
#
#         account_page.header.open_domain_catalog_list()
#
#         domain_catalog_list.remove_first_catalog()
#
#         sleep(2)
#         Assert.contains(u"Operacja wykonana poprawnie.", domain_catalog_list.get_page_source())
#
#         sleep(7)
#         self.not_contains(catalog_name, domain_catalog_list.get_page_source())
#
#     def test_add_domain_to_catalog_already_added_domain_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
#         domain_catalog_list = account_page.header.open_domain_catalog_list()
#         domain_catalog_list.add_already_existing_domain_to_catalog()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._result_text_field, u"Domena już znajduje się w katalogu"))
#         Assert.equal(domain_catalog_list.first_domain_value, domain_catalog_list.result_domain_text())
#
#     def test_search_domain_in_catalog_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
#         domain_catalog_list = account_page.header.open_domain_catalog_list()
#         domain_catalog_list.search_second_domain_in_catalog()
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._first_domain_in_catalog_field, domain_catalog_list.second_domain_value))
#
#     def test_search_appraisal_list_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         appraisal_list = account_page.header.open_appraisal_list()
#         appraisal_list.get_fourth_appraisal_domain_time_type_and_status()
#         appraisal_list.search_for_appraisal(appraisal_list.fourth_appraisal_domain)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_domain_field, appraisal_list.fourth_appraisal_domain))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_time_field, appraisal_list.fourth_appraisal_time))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_type_field, appraisal_list.fourth_appraisal_type))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_status_field, appraisal_list.fourth_appraisal_status))
#
# #BŁĄD BRAK WYNIKÓW, zgłoszone
#
#     def test_search_active_appraisals_list_should_succeed(self):
#
#         home_page = HomePage(self.driver).open_home_page()
#         account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
#         appraisal_list = account_page.header.open_active_appraisals_list()
#         appraisal_list.get_fourth_appraisal_domain_time_and_propositions()
#         appraisal_list.search_for_appraisal(appraisal_list.fourth_appraisal_domain)
#
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_domain_field, appraisal_list.fourth_appraisal_domain))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_time_field, appraisal_list.fourth_appraisal_time))
#         WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_propositions_field, appraisal_list.fourth_appraisal_propositions))
#
# #BŁĄD BRAK WYNIKÓW, zgłoszone

    def tally(self):
        return len(self._resultForDoCleanups.errors) + len(self._resultForDoCleanups.failures)

    def setUp(self):
        self.timeout = 30
        if run_locally:
            sr_args = ["--verbose", "--log-path=chromedriver.log"]
            self.driver = webdriver.Chrome(executable_path='C:\Downloads\chromedriver.exe',  service_args=sr_args)
            # self.driver = webdriver.Firefox()
            self.driver.set_window_size(1024,768)
            # self.driver.maximize_window()
            # self.driver.implicitly_wait(self.timeout)
            self.errors_and_failures = self.tally()
        else:
            self.desired_capabilities['name'] = self.id()
            sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"

            self.driver = webdriver.Remote(
                desired_capabilities=self.desired_capabilities,
                command_executor=sauce_url % (USERNAME, ACCESS_KEY)
            )

            self.driver.implicitly_wait(self.timeout)

    def tearDown(self):
        if run_locally:
                if self.tally() > self.errors_and_failures:
                    if not os.path.exists(SCREEN_DUMP_LOCATION):
                        os.makedirs(SCREEN_DUMP_LOCATION)
                    for ix, handle in enumerate(self.driver.window_handles):
                        self._windowid = ix
                        self.driver.switch_to.window(handle)
                        # self.take_screenshot()
                        # self.dump_html()
                self.driver.quit()

    def not_contains(self, needle, haystack, msg=''):
        try:
            assert not needle in haystack
        except AssertionError:
            raise AssertionError('%s is found in %s. %s' % (needle, haystack, msg))

if __name__ == '__main__':
     unittest.main()
