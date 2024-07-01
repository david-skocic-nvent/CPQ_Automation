from abc import ABC, abstractmethod
from selenium import webdriver
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from threading import Thread

# a simple decorator that will retry a function 20 times with a one second break until it returns true
# exits thread or program if true is never received
def repeat_until_successful(func):
    def wrapper(*args, **kwargs):
        for _ in range(20):
            ret = func(*args, **kwargs)
            if ret:
                return ret
            time.sleep(1)
        else:
            exit(0)
            #return False
    return wrapper

class CustomDriver(webdriver.Edge, ABC):

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def run_test_case(self):
        pass

    def is_active(self):
        if self.thread is None:
            return False
        elif self.thread.is_alive():
            return True
        return False

    def start_thread(self, target, args):
        self.thread = Thread(target=target, args=args)
        self.thread.start()

    #******************************************************************
    def count_existing_elements(self, selection):
        try:
            elements = self.find_elements(*selection)
            return len(elements)
        except:
            return 0

    # chooses a combobox value. Can be from all possible options or from a list of user-defined options
    @repeat_until_successful
    def choose_combobox_value(self, selection, allow_empty_value = False, manual_values: list = None):
        try:
            dropdown_element = WebDriverWait(self, 5).until(EC.element_to_be_clickable(selection))
            dropdown = Select(dropdown_element)

            if manual_values is None:
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
    def choose_textbox_value(self, selection, list):
        try:
            choice = random.choice(list)
            textbox = WebDriverWait(self, 5).until(EC.element_to_be_clickable(selection))
            textbox.click()
            ActionChains(self).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
            textbox.send_keys(choice)
            return choice
        except:
            print("No textbox value could be chosen for "+ str(selection))
            return None

    @repeat_until_successful
    def read_value(self, selection):
        try:
            element = self.find_element(*selection)
            if element.get_attribute('value') is None:
                return element.text
            return element.get_attribute("value")
        except:
            print("value from " + str(selection) + " could not be read")
            return None

    @repeat_until_successful
    def click_element(self, selection, multiple = False, element_index = 0):
        try:
            if multiple:
                elements = self.find_elements(*selection)
                selection = (By.ID, elements[element_index].get_attribute("id"))
            
            element = WebDriverWait(self,5).until(EC.element_to_be_clickable(selection))
            element.click()
            return True
        except:
            print(str(selection) + " could not be clicked")
            return None

    def dump_html_to_file(self, filename):
        with open(filename, 'w', errors='replace') as f:
            f.write(self.page_source)

    def tabout (self):
        body = self.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.TAB)


