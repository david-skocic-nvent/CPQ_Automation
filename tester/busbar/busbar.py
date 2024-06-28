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
from constants import *
load_dotenv()
USERNAME = os.getenv("TACTON_USERNAME")
PASSWORD = os.getenv("TACTON_PASSWORD")

drivers: List[webdriver.Edge] = []
threads: List[threading.Thread] = []
drivers_in_use = []
NUMBER_OF_THREADS = 1

def configure_tool (tool):
    global completed_parts_path
    global tool_button_xpath
    global run_test
    global parsed_numbers_path
    if tool == GROUND:
        completed_parts_path = COMPLETED_PARTS_FILE_PATH_GROUND
        parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_GROUND
        tool_button_xpath = '//*[@id="config-middle"]/div/div/div[2]/div/div/div[1]'
        run_test = run_test_ground
    elif tool == TELECOM:
        completed_parts_path = COMPLETED_PARTS_FILE_PATH_TELECOM
        parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_TELECOM
        tool_button_xpath = '//*[@id="config-middle"]/div/div/div[2]/div/div/div[2]'
        run_test = run_test_telecom

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

def read_csv_dict_list (file_path):
    csv_file = open(file_path, "r", newline='')
    reader = csv.DictReader(csv_file)
    dict_list = []
    for row in reader:
        dict_list.append(row)
    return dict_list

def read_csv_list (file_path):
    csv_file = open(file_path, "r", newline='')
    reader = csv.reader(csv_file)
    return_list = []
    for row in reader:
        return_list.append(row)
    return return_list

def write_csv(file_path, row):
    csv_file = open(file_path, "a", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(row)

def click_to_part_number_logic (driver):
    # clicks my project
    click_element(driver, (By.XPATH, '//span[text() = "David Skocic"]'))
    # clicks add product button
    click_element(driver, (By.XPATH, '//*[@id="objectTab-null-overview"]/div[2]/div[1]/section[1]/div[1]/div[2]/div/a'))
    # clicks the busbar button
    click_element(driver, (By.XPATH, '//*[@id="table122206"]/tbody/tr[1]/td[2]'))
    # clicks the button for the right tool
    click_element(driver, (By.XPATH, tool_button_xpath))
    # clicks the part number logic button
    click_element(driver, (By.XPATH, '//*[@id="config-left-column"]/ul/ul/li[2]'))

def try_to_exit_warning (driver):
    if count_existing_elements(driver, (By.XPATH, '//*[@id="conflictForm"]/div[2]/button[1]')):
        click_element(driver, (By.XPATH, '//*[@id="conflictForm"]/div[2]/button[1]'))

def get_out_of_selection (driver: webdriver.Edge):
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.TAB)

def run_test_telecom(driver, values):
    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-4609c11402-752f-4449-95d2-850a398973a8"]'), [values["prefix"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46427860a6-e530-4307-b69e-b748fed3471b"]'), [values["configuration"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46eb578ade-85e5-4036-81f5-2700316724ee"]'), [values["length"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-461605fd72-2d71-41a3-b471-d108a1d77bb6"]'), [values["number of holes"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46bc4bc784-be3a-4cd2-a046-f5daf217323c"]'), ["a\b" + values["material"]])
    get_out_of_selection(driver)
    time.sleep(3)
    try_to_exit_warning (driver)

    read_prices(driver, values)

def run_test_ground(driver, values):
    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46e978dfe6-a6a6-4bbf-8d0e-dd802ba7fbac"]'), [values["configuration"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46440960ce-4964-4b1d-a59e-df51da1eb862"]'), [values["bar thickness"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-460d760aa7-b2b7-4669-baad-b75e692488e6"]'), [values["bar width"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46da4742ce-7c9d-4611-96c9-cf3cdc755ba1"]'), [values["bar length"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-4603b44eaf-d4e6-4ae2-a9e6-e80e6078a05f"]'), [values["hole pattern"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46b473b4b3-47bb-425a-a88e-c844d5983042"]'), [values["hole size"]])
    get_out_of_selection(driver)
    time.sleep(1)
    try_to_exit_warning (driver)

    choose_textbox_value(driver, (By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46028e1b03-2f59-4b5d-ab93-a5fe5903969c"]'), ["a\b" + values["material"]])
    time.sleep(0.5)
    get_out_of_selection(driver)
    time.sleep(3)
    try_to_exit_warning(driver)

    read_prices(driver, values)

def read_prices(driver, values):
    return_list = []
    return_list.append(values["part number"])
    return_list.append(read_value(driver, (By.XPATH, '//*[@id="PricingEditorTable"]/table/tfoot/tr/th[2]/span/span')))

    number_of_bom_rows = int(count_existing_elements(driver, (By.XPATH, '//*[contains(@id, "bom-item-")]')))
    for i in range(2, number_of_bom_rows+1):
        return_list.append(read_value(driver, (By.XPATH, f'//*[@id="bom-item-{i}"]/td[4]/span/span')))
        return_list.append(read_value(driver, (By.XPATH, f'//*[@id="bom-item-{i}"]/td[5]/span/span')))
        return_list.append(read_value(driver, (By.XPATH, f'//*[@id="bom-item-{i}"]/td[6]/span/span')))

    # a last check to see if the part number is put in correctly
    part_number_on_site = read_value (driver, (By.XPATH, '//*[@id="widget-null-90a80895-c989-4fe3-8d3e-8f141408f9b9-4616533bf9-3595-470c-9006-a4615b24d6dd-row"]/div[2]/div/div/input')) 

    if return_list[0] != part_number_on_site:
        print (f"Part number {[return_list[0]]} was entered incorrectly. {part_number_on_site} was entered instead")
    else:
        write_csv(completed_parts_path, return_list)

def main(tool):
    global drivers

    configure_tool(tool)

    tests = read_csv_dict_list(parsed_numbers_path)
    completed_tests = read_csv_list(completed_parts_path)

    # get a list of the completed part numbers
    completed_part_numbers = []
    for row in completed_tests:
        completed_part_numbers.append(row[0])

    tests_to_remove = []

    # find all completed tests in tests list and add them to a remove list
    for test in tests:
        if test["part number"] in completed_part_numbers:
            completed_part_numbers.remove(test["part number"])
            tests_to_remove.append(test)

    # remove all completed tests from tests
    for test in tests_to_remove:
        tests.remove(test)

    # 
    for test in tests:
        print(test["part number"])

    make_drivers()

    # get to part number logic part of the program
    for i in range(NUMBER_OF_THREADS):
        threads.append(threading.Thread(target=click_to_part_number_logic, args = (drivers[i],)))
        threads[-1].start()
        print(threads[-1].is_alive())

    # wait for threads to finish
    for i in range(NUMBER_OF_THREADS):
        threads[i].join()

    # loop through the remaining tests, removing one every time 
    while len(tests) > 0:
        for i, thread in enumerate(threads):
            if not thread.is_alive():
                threads[i] = threading.Thread(target=run_test, args=(drivers[i],tests[0]))
                threads[i].start()
                print (f"Started running test for {tests[0]["part number"]}")
                i = i + 1
                tests.pop(0)
        time.sleep(2)

    time.sleep(5)

main(TELECOM)