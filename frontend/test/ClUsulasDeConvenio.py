# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ClUsulasDeConvenio(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_cl_usulas_de_convenio(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='horizontal-navigation']/div/ms-navigation-horizontal/ul/li[10]/ul/li[2]/div/a/span").click()
        self.assertEqual(u"Cláusulas de convenios", driver.find_element_by_xpath("//div[@id='conditionsTemplates']/div[2]/div/div/div/span").text)
        driver.find_element_by_xpath("//div[@id='conditionsTemplates']/div[2]/div[2]/md-content/div/div/div/div/div/div[2]/button/md-icon").click()
        self.assertEqual(u"Editar cláusula de convenio", driver.find_element_by_xpath("//md-toolbar/div/span").text)
        driver.find_element_by_xpath("//md-toolbar/div/button/md-icon").click()
        self.assertNotEqual(u"Editar cláusula de convenio", driver.find_element_by_xpath("//md-toolbar/div/span").text)
    
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
