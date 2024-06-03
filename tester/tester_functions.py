import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def choose_random_combobox_value(driver: webdriver.Edge, selection, allow_empty_value = False):
    dropdown_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selection))
    dropdown = Select(dropdown_element)
    choice = random.choice(dropdown.options).text
    if not allow_empty_value:
        while choice == "":
            choice = random.choice(dropdown.options).text
    dropdown.select_by_visible_text(choice)
    return choice

def choose_random_textbox_value(driver: webdriver.Edge, selection, list):
    choice = random.choice(list)
    textbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selection))
    textbox.click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
    textbox.send_keys(choice)
    return choice

def read_value(driver: webdriver.Edge, selection):
    element = driver.find_element(selection[0], selection[1])
    return element.get_attribute("value")

def click_element(driver: webdriver.Edge, selection, multiple = False, element_index = 0):
    if multiple:
        elements = driver.find_elements(selection[0], selection[1])
        selection = (By.ID, elements[element_index].get_attribute("id"))
    
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable(selection))
    element.click()