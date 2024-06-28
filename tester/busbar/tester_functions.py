import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


def login(driver: webdriver.Edge, username, password):
    choose_textbox_value(driver,(By.ID, 'username'),[username])
    choose_textbox_value(driver,(By.NAME, 'Password'),[password])
    click_element(driver, (By.ID, "login-button"))

# a simple decorator that will retry a function 20 times with a one second break until it returns true
def repeat_until_successful(func):
    def wrapper(*args, **kwargs):
        for _ in range(20):
            ret = func(*args, **kwargs)
            if ret:
                return ret
            time.sleep(1)
        else:
            return False
    return wrapper

def count_existing_elements(driver: webdriver.Edge, selection):
    try:
        elements = driver.find_elements(*selection)
        return len(elements)
    except:
        return 0

# chooses a combobox value. Can be from all possible options or from a list of user-defined options
@repeat_until_successful
def choose_combobox_value(driver: webdriver.Edge, selection, allow_empty_value = False, manual_values: list = None):
    try:
        dropdown_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(selection))
        dropdown = Select(dropdown_element)

        if not manual_values:
            choice = random.choice(dropdown.options).text
            if not allow_empty_value:
                while choice == "":
                    choice = random.choice(dropdown.options).text
        else:
            choice = random.choice(manual_values)

        dropdown.select_by_visible_text(choice)
        return choice
    except:
        print("No combobox value could be chosen for " + str(selection))
        return None

#Chooses a random value from the list argument to put into the textbox.
#A list with only one element can be used for a direct input value
@repeat_until_successful
def choose_textbox_value(driver: webdriver.Edge, selection, list):
    try:
        choice = random.choice(list)
        textbox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(selection))
        textbox.click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        textbox.send_keys(choice)
        return choice
    except:
        print("No textbox value could be chosen for "+ str(selection))
        return None

@repeat_until_successful
def read_value(driver: webdriver.Edge, selection):
    try:
        element = driver.find_element(*selection)
        if element.get_attribute('value') is None:
            return element.text
        return element.get_attribute("value")
    except:
        print("value from " + str(selection) + " could not be read")
        return None

@repeat_until_successful
def click_element(driver: webdriver.Edge, selection, multiple = False, element_index = 0):
    try:
        if multiple:
            elements = driver.find_elements(selection[0], selection[1])
            selection = (By.ID, elements[element_index].get_attribute("id"))
        
        element = WebDriverWait(driver,5).until(EC.element_to_be_clickable(selection))
        element.click()
        return True
    except:
        print(str(selection) + " could not be clicked")
        return None

def dump_html_to_file(driver: webdriver.Edge, filename):
    with open(filename, 'w', errors='replace') as f:
        f.write(driver.page_source)