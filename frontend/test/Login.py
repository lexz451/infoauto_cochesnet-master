# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login(self):
        driver = self.driver
        driver.get("http://gadessrvpru.uca.es/auth/login")
        driver.find_element_by_id("input_0").click()
        driver.find_element_by_id("input_0").clear()
        driver.find_element_by_id("input_0").send_keys("mario@intelligenia.com")
        driver.find_element_by_id("input_1").click()
        driver.find_element_by_id("input_1").clear()
        driver.find_element_by_id("input_1").send_keys("mario1234")
        driver.find_element_by_xpath("//div[@id='login-form']/form/button/ng-transclude/span").click()
        self.assertEqual("mario@intelligenia.com", driver.find_element_by_xpath("//md-menu-bar[@id='user-menu']/md-menu/button/span/span[2]").text)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
