from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import threading
from fileout import csvout
import time
import random as rand
import re

SUPPORTING = ["Conduits", "Cables", "CablePath", "Ebox", "MetalFraming", "ThreadedRods", "WireChain"]
NUMBER_OF_CONDUITS = ['1','2','3']
CONDUIT_DIAMETER = ["16", "20", '25', '32', '40', '50', '60', '63']
PRIMARY_CONDUIT_MATERIAL = ["Plastic", "Metal"]
LINK = "http://10.4.75.133:8020/Apps/Fasteners_1_MNL/"

results = {}


def read_From_table (driver: webdriver.Edge, page_number):
    #columns = []
    #rows = []
    names = []
    column_count = len(driver.find_elements(By.XPATH, "//div[contains(@id, 'DataTableControl9_MainElement')]//div[contains(@data-id,'dw-listview-header_')]//span[@class='dw-listview-valueContainer']"))
    table_entries = driver.find_elements(By.XPATH, "//div[contains(@id, 'DataTableControl9_MainElement')]//span[@class='dw-listview-valueContainer']")
    for i in range(column_count, len(table_entries), column_count):
        names.append(table_entries[i].text)
    results[f"page {page_number} names"] = names
"""        if i // column_count > len(rows):
            rows.append({})
        if i < column_count:
            columns.append(entry.text)
        else:
            rows[-1][columns[i % column_count]] = entry.text
    for row in rows:
        print (row)"""
    #    print(entry.text)
#    for i, thing in enumerate(things):
 #       substring = re.search('>(.*?)<', thing.get_attribute("outerHTML")).group(1)
  #      print(substring)

def auto (driver, executions):
    page1(driver)

def page1 (driver: webdriver.Edge):
    driver.get(LINK)
    time.sleep(2)
    supporting = rand.choice(SUPPORTING)
    supporting = "Conduits"
    choose_combobox_value(driver,selection=(By.XPATH, "//select[contains(@id, 'Application_ComboBoxElement')]"), manual=True, manual_values=[supporting])
    match supporting:
        case "Conduits":
            results["number of conduits"] = choose_combobox_value(driver,selection=(By.XPATH, "//select[contains(@id, 'ConduitQuantity_ComboBoxElement')]"))
            time.sleep(.5)
            results["diameter"] = choose_combobox_value(driver,selection=(By.XPATH, "//select[contains(@id, 'ConduitDiameter_ComboBoxElement')]"))
            time.sleep(.5)
            results["primary material"] = choose_combobox_value(driver,selection=(By.XPATH, "//select[contains(@id, 'PrimaryConduitMaterial_ComboBoxElement')]"))
            time.sleep(.5)
            results["certification"] = choose_combobox_value (driver, (By.XPATH, "//select[contains(@id, 'Certification_ComboBoxElement')]"))
            time.sleep(2)

    read_From_table(driver, 1)
    print(results)
    click_element (driver, selection=(By.XPATH, "//a[contains(@href, 'javascript:window.ActiveSpecification.next();')]"))

def page2 (driver: webdriver.Edge, supporting):
    match supporting:
        case "Conduits":
            results["environment"] = choose_combobox_value (driver, (By.XPATH, "//select[contains(@id, 'Environment_ComboBoxElement')]"))
            time.sleep(.5)
            results["environment"] = choose_combobox_value (driver, (By.XPATH, "//select[contains(@id, 'InstallationOrientation_ComboBoxElement')]"))
            time.sleep(.5)
            results["environment"] = choose_combobox_value (driver, (By.XPATH, "//select[contains(@id, 'ClosingMechanism_ComboBoxElement')]"))
            time.sleep(.5)
    

    read_From_table(driver, 1)
    print(results)
    click_element (driver, selection=(By.XPATH, "//a[contains(@href, 'javascript:window.ActiveSpecification.next();')]"))

def page3(driver: webdriver.Edge, supporting):
    match supporting:
        case "Conduits":
            