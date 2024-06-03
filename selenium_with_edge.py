from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from write_to_output import output_results_to_csv
from pathlib import Path
import random
import time
import csv
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("CPQ_USERNAME")
PASSWORD = os.getenv("CPQ_PASSWORD")
TOOL = "RoofTop"
LINK = "http://10.4.75.133:8020/Apps/Rooftop_1_MNL/" #"http://10.4.75.133:8020/Login"

TOOL_HREFS = {"RoofTop": "/Apps/Rooftop"}

MATERIAL = ['Water', 'Gas']
HOLDER = ["Clamp", "Hanger", "Roller"]
SNOW_LOAD = [0,5,10,20,40,60]
FIELD_NAMES = ["holder", "clearance", "spacing", "snow load", "pipe type", "diameter", "insulation",
                "material", "pipe count", "section length", "pressure", "overall weight", "cross member width",
                "frame spacing", "hanger size", "total frames"]
results = {}


def login():
    element = driver.find_element(By.ID, 'username')
    element.send_keys(USERNAME)
    element = driver.find_element(By.NAME, 'Password')
    element.send_keys(PASSWORD)
    button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "login-button")))
    button.click()

def enter_tool(toolName):
    button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains (@href, '%s')]" % TOOL_HREFS[toolName])))
    button.click()

def choose_random_combobox_value(selection, allow_empty_value = False):
    dropdown_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selection))
    dropdown = Select(dropdown_element)
    choice = random.choice(dropdown.options).text
    if not allow_empty_value:
        while choice == "":
            choice = random.choice(dropdown.options).text
    dropdown.select_by_visible_text(choice)
    return choice

def choose_random_textbox_value(selection, list):
    choice = random.choice(list)
    textbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selection))
    textbox.click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
    textbox.send_keys(choice)
    return choice

def read_value(selection):
    element = driver.find_element(selection[0], selection[1])
    return element.get_attribute("value")

def auto_rooftop_pipe():
    pass

def click_element(selection, multiple = False, element_index = 0):
    if multiple:
        elements = driver.find_elements(selection[0], selection[1])
        selection = (By.ID, elements[element_index].get_attribute("id"))
        
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable(selection))
    element.click()

def page1():
#--------------------------------------------------------------------------------
#Filling in first page of values

    #choosing holder button
    try:
        holder = random.choice(HOLDER)
        match (holder):
            case ("Clamp"):
                click_element((By.CSS_SELECTOR, "div[id*='optSupport_ImageContainer']"))
            case ("Roller"):
                click_element((By.CSS_SELECTOR, "div[id*='optRoller_ImageContainer']"))
            case ("Hanger"):
                click_element((By.CSS_SELECTOR, "div[id*='optHang_ImageContainer']"))
        results["holder"] = holder
    except:
        print ("Failed when selecting a holder button")

    time.sleep(1)
    #input value for ground clearance
    try:
        if holder == "Hanger":
            results["clearance"] = choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numDropLength_TextBoxElement']"), [x for x in range(12,25)])
        else:
            results["clearance"] = choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), [x for x in range(12,25)])
    except:
        print("Failed when filling ground clearance field")
    
    #input value for pipe spacing
    try:
        results["spacing"] = choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']"), [x for x in range(2,11)])
    except:
        print("Failed when filling pipe spacing field")
    
    #input value for snow load
    try:
        results["snow load"] = choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SNOW_LOAD)
    except:
        print("Failed when filling snow load field")
    
    try:
        click_element((By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']"))
    except:
        print("failed to click next button")
#--------------------------------------------------------------------------------

def page2():
#--------------------------------------------------------------------------------
#Filling in second page of values
    try:
        results["pipe type"] = choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"))
    except:
        print("Failed when filling pipe material field")
    time.sleep(.5)
    try:
        results["diameter"] = choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"))
    except:
        print("Failed when filling pipe diameter field")
    time.sleep(.5)
    try:
        results["insulation"] = choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"))
    except:
        print("Failed when filling pipe diameter field")

    try:
        if random.choice(MATERIAL) == "Water":
            results["material"] = "Water"
            click_element((By.CSS_SELECTOR, "input[id*='optLiquid_OptionElement']"))
        else:
            results["material"] = "Gas"
            click_element((By.CSS_SELECTOR, "input[id*='optGas_OptionElement']"))
    except:
        print("Failed when pressing material in pipe button")

    try:
        slider_element = driver.find_element(By.CSS_SELECTOR, "div[id*='sldNumPipes_SliderTrackElement']" )
        actions = ActionChains(driver)
        pipe_count = random.randint(1,10)
        results["pipe count"] = pipe_count
        print ("Pipe count:" + str(pipe_count))
        for _ in range(pipe_count - 1):
            actions.move_by_offset(slider_element.location['x'] + slider_element.size['width'] - 5, slider_element.location['y'] + 1).click()
            actions.move_by_offset(-(slider_element.location['x'] + slider_element.size['width'] - 5), -(slider_element.location['y'] + 1))
            actions.perform()
            time.sleep(.2)
        time.sleep(.5)
    except:
        print("failed when moving slider")

    try:
        click_element((By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    except:
        print("failed to click complete button")

def read_values_from_page2():
    try:
        results["overall weight"] = read_value((By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']"))
    except:
        print("failed to read Overall Weight")
    try:
        results["cross member width"] = read_value((By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']"))
    except:
        print("failed to read Cross Member length")
    try:
        results["frame spacing"] = read_value((By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']"))
    except:
        print("failed to read maximum H frame spacing")
    try:
        results["hanger size"] = read_value((By.CSS_SELECTOR, "select[id*='cboMaxHangerSize_ComboBoxElement']"))
    except:
        print("failed to read max hanger size")
    try:
        click_element((By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    except:
        print("failed to click complete button")
    
def page3():
    try:
        results["pressure"] = read_value((By.CSS_SELECTOR, "input[id*='numOverallPSI_TextBoxElement']"))
    except:
        print("failed to read PSI")
    try:
        table = driver.find_elements(By.CSS_SELECTOR, "div[data-id*='dw-listview-bodyScroller_']")
        for element in table:
            if "tblPipeType_ListView" in element.get_attribute("data-id"):
                actions = ActionChains(driver)
                actions.move_by_offset(element.location['x'] + 5, element.location['y'] + 5).click()
                actions.move_by_offset(-(element.location['x'] + 5),-(element.location['y'] + 5))
                actions.perform()
    except:
        print("failed to select table row")
    try:
        click_element((By.CSS_SELECTOR, "div[id*='macEditPipeInfo_WebkitOuterClickLayer']"))
    except:
        print("failed to click edit pipe type button")
    time.sleep(2)
    read_values_from_page2()
    time.sleep(2)
    try:
        click_element((By.CSS_SELECTOR, "div[id*='macNext3_WebkitOuterClickLayer']"))
    except:
        print("failed to click next button")
#--------------------------------------------------------------------------------

def page4():
    try:
        results["section length"] = choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), [100])
    except:
        print("failed when entering section length")
    try:
        click_element((By.CSS_SELECTOR, "div[id*='macAddSectionLength_WebkitOuterClickLayer']"))
    except:
        print("failed to click add to table button")
    time.sleep(1)
    try:
        results["total frames"] = read_value((By.CSS_SELECTOR, "input[id*='numTotalHFrames_TextBoxElement']"))
    except:
        print("failed when reading total number of H frames")
    try:
        click_element((By.CSS_SELECTOR, "div[id*='macComplete_WebkitOuterClickLayer']"), multiple=True, element_index=1)
    except:
        print("failed to click complete button")


def write_html_to_temp_file():
    with open("html_output.txt", 'w') as f:
        f.write(driver.page_source)

if __name__ == '__main__':
    driver = webdriver.Edge()
    driver.get(LINK)

    login()

    a = input("a: ")

    if a == "control":
        while (a != "end"):
            match (a):
                case "manual":
                    pass
                case "page1":
                    page1()
                case "page2":
                    page2()
                case "rp2":
                    read_values_from_page2()
                case "page3":
                    page3()
                case "reset":
                    driver.get(LINK)
                case "page4":
                    page4()
                case "results":
                    print(results)
                case "dump":
                    write_html_to_temp_file()
                case "write results":
                    output_results_to_csv(field_names=FIELD_NAMES, dict=results)
                case "all":
                    page1()
                    time.sleep(5)
                    page2()
                    time.sleep(2)
                    page3()
                    time.sleep(3)
                    page4()
            a = input("a: ")
    elif a == "auto pipe":
        for _ in range(5):
            click_element((By.CSS_SELECTOR, "div[id*='macPipe_WebkitOuterClickLayer']"))
            time.sleep(3)
            page1()
            time.sleep(5)
            page2()
            time.sleep(2)
            page3()
            time.sleep(3)
            page4()
            time.sleep(1)
            output_results_to_csv(field_names=FIELD_NAMES, dict = results)
            results = {}



