# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Expedientes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_expedientes(self):
        driver = self.driver
        driver.find_element_by_link_text("Expedientes").click()
        driver.find_element_by_xpath("//div[@id='dossiers']/div[2]/div[2]/md-content/div/div/div/div/div/div/div[2]").click()
        self.assertEqual("Expediente", driver.find_element_by_xpath("//div[@id='dossier-edit']/div[2]/div/div[2]/div[2]/span/span").text)
        driver.find_element_by_xpath("//md-sidenav[@id='dossiers-sidenav']/md-content/div/a[2]/div/span").click()
        self.assertEqual("Interrupciones", driver.find_element_by_xpath("//div[@id='dossierInterruptions']/div[2]/div/div/div/span").text)
        driver.find_element_by_link_text(u"Prórrogas").click()
        self.assertEqual(u"Prórrogas", driver.find_element_by_xpath("//div[@id='dossierExtensions']/div[2]/div/div/div/span").text)
        driver.find_element_by_link_text("Cancelaciones").click()
        self.assertEqual("Cancelaciones", driver.find_element_by_xpath("//div[@id='dossierResignations']/div[2]/div/div/div/span").text)
        driver.find_element_by_link_text(u"Documentación").click()
        self.assertEqual("Documentos", driver.find_element_by_xpath("//div[@id='dossierDocuments']/div[2]/div/div/div/span").text)
    
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
