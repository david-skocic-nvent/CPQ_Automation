import threading
import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from tester_functions import *
from dotenv import load_dotenv
import time
import os
from typing import List
load_dotenv()
USERNAME = os.getenv("TACTON_USERNAME")
PASSWORD = os.getenv("TACTON_PASSWORD")

FIELD_NAMES = ["part number", "configuration", "bar thickness", "bar width", "bar length", "hole pattern", "hole size", "material"]
LINK = "https://nventefs-admin.tactoncpq.com/!tickets%7ET-00000938/solution/list"
HTML_DUMP_FILE_PATH = "C:\\Users\\E2023355\\OneDrive - nVent Management Company\\Documents\\VSCode\\Projects\\CPQ\\CPQ_Automation\\dump.html"

drivers = []
threads: List[threading.Thread] = []
drivers_in_use = []
NUMBER_OF_THREADS = 2

def make_drivers():
    global drivers
    for i in range (NUMBER_OF_THREADS):
        drivers.append(webdriver.Edge())
        drivers[-1].get(LINK)
        login(drivers[-1])

def login (driver):
    # enters username and password
    choose_textbox_value(driver, (By.NAME, "username"), [USERNAME])
    choose_textbox_value(driver, (By.NAME, "password"), [PASSWORD])
    # clicks the login button
    click_element(driver, (By.XPATH, "//button"))

def read_csv ():
    csv_file = open("C:\\Users\\E2023355\\OneDrive - nVent Management Company\\Documents\\VSCode\\Projects\\CPQ\\CPQ_Automation\\tester\\busbar\\parsed_numbers.csv", "r", newline='')
    reader = csv.DictReader(csv_file)
    dict_list = []
    for row in reader:
        dict_list.append(row)
    return dict_list

def write_csv(row):
    csv_file = open("C:\\Users\\E2023355\\OneDrive - nVent Management Company\\Documents\\VSCode\\Projects\\CPQ\\CPQ_Automation\\tester\\busbar\\part_prices.csv", "a", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(row)
    

def click_to_part_number_logic (driver):
    # clicks my project
    click_element(driver, (By.XPATH, '//span[text() = "David Skocic"]'))
    # clicks add product button
    click_element(driver, (By.XPATH, '//*[@id="objectTab-null-overview"]/div[2]/div[1]/section[1]/div[1]/div[2]/div/a'))
    # clicks the busbar button
    click_element(driver, (By.XPATH, '//*[@id="table122206"]/tbody/tr[1]/td[2]'))
    # clicks the electrical ground button
    click_element(driver, (By.XPATH, '//*[@id="config-middle"]/div/div/div[2]/div/div/div[1]'))
    # clicks the part number logic button
    click_element(driver, (By.XPATH, '//*[@id="config-left-column"]/ul/ul/li[2]'))

def try_to_exit_warning (driver):
    if count_existing_elements(driver, (By.XPATH, '//*[@id="conflictForm"]/div[2]/button[1]')):
        click_element(driver, (By.XPATH, '//*[@id="conflictForm"]/div[2]/button[1]'))

def get_out_of_selection (driver: webdriver.Edge):
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.TAB)


def fill_values(driver, values):
    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46e978dfe6-a6a6-4bbf-8d0e-dd802ba7fbac"]'), [values["configuration"]])
    get_out_of_selection(driver)
    time.sleep(2)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46440960ce-4964-4b1d-a59e-df51da1eb862"]'), [values["bar thickness"]])
    get_out_of_selection(driver)
    time.sleep(2)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-460d760aa7-b2b7-4669-baad-b75e692488e6"]'), [values["bar width"]])
    get_out_of_selection(driver)
    time.sleep(2)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46da4742ce-7c9d-4611-96c9-cf3cdc755ba1"]'), [values["bar length"]])
    get_out_of_selection(driver)
    time.sleep(2)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-4603b44eaf-d4e6-4ae2-a9e6-e80e6078a05f"]'), [values["hole pattern"]])
    get_out_of_selection(driver)
    time.sleep(2)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46b473b4b3-47bb-425a-a88e-c844d5983042"]'), [values["hole size"]])
    get_out_of_selection(driver)
    time.sleep(2)
    try_to_exit_warning (driver)

    read_prices(driver, values)

def read_prices (driver, values):
    return_list = []
    return_list.append(values["part number"])
    return_list.append(read_value(driver, (By.XPATH, '//*[@id="PricingEditorTable"]/table/tfoot/tr/th[2]/span/span')))

    number_of_bom_rows = int(count_existing_elements(driver, (By.XPATH, '//*[contains(@id, "bom-item-")]')))
    for i in range(2, number_of_bom_rows+1):
        return_list.append(read_value(driver, (By.XPATH, f'//*[@id="bom-item-{i}"]/td[4]/span/span')))
        return_list.append(read_value(driver, (By.XPATH, f'//*[@id="bom-item-{i}"]/td[5]/span/span')))
        return_list.append(read_value(driver, (By.XPATH, f'//*[@id="bom-item-{i}"]/td[6]/span/span')))

    write_csv(return_list)

def main():
    global drivers
    tests = read_csv()

    make_drivers()

    for i in range(NUMBER_OF_THREADS):
        threads.append(threading.Thread(target=click_to_part_number_logic, args = (drivers[i],)))
        threads[-1].start()
        print(threads[-1].is_alive())

    for i in range(NUMBER_OF_THREADS):
        threads[i].join()

    i = 1

    while len(tests) > 0:
        if tests[0]["hole size"] != "other":
            for i, thread in enumerate(threads):
                if not thread.is_alive():
                    threads[i] = threading.Thread(target=fill_values, args=(drivers[i],tests[0]))
                    threads[i].start()
                    print (f"Started running test {i}")
                    i = i + 1
                    tests.pop(0)
        else:
            tests.pop(0)
        time.sleep(2)

    time.sleep(5)