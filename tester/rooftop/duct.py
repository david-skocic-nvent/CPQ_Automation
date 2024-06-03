from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import time
import random

SNOW_LOAD = [0,5,10,20,40,60]
EXTRA_CROSS_MEMBER = [True, False]
results = {}

# runs all four pages and returns their output dictionary to add to the csv file
# returns to the same place that it started, so it can run continuously
def auto(driver):
    global results
    results = {}
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macDuct_WebkitOuterClickLayer']"))
    time.sleep(3)
    page1(driver)
    time.sleep(5)
    page2(driver)
    time.sleep(2)
    page3(driver)
    time.sleep(3)
    page4(driver)
    time.sleep(1)
    return results

#Filling in first page of values
def page1(driver: webdriver.Edge):
    #input value for ground clearance
    try:
        results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), [x for x in range(12,25)])
    except:
        print("Failed when filling ground clearance field")
    
    #input value for pipe spacing
    try:
        if random.choice(EXTRA_CROSS_MEMBER):
            results["extra cross member"] = True
            click_element(driver, (By.CSS_SELECTOR, "input[id*='chkTopBar_CheckBoxElement']"))
        else:
            results["extra cross member"] = False
    except:
        print("Failed when clicking extra cross member field")
    
    #input value for snow load
    try:
        results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SNOW_LOAD)
    except:
        print("Failed when filling snow load field")
    
    #click next 
    try:
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']")) #, multiple=True, element_index=1)
    except:
        print("failed to click next button")

#Filling in second page of values
def page2(driver: webdriver.Edge):
    try:
        results["shape"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"))
    except:
        print("Failed when filling shape field")
    time.sleep(1)
    try:
        if results["shape"] == "Round":
            results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctDia_TextBoxElement']"),[x for x in range(10,51)])
        else:
            results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctWidth_TextBoxElement']"),[x for x in range(10,51)])
            results["height"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctHeight_TextBoxElement']"),[x for x in range(10,51)])
    except:
        print("Failed when filling size field(s)")
    time.sleep(.5)

    try:
        results["gauge"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctGage_ComboBoxElement']"))
    except:
        print("Failed when filling gauge field")

    try:
        results["insulation thickness"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"))
    except:
        print("Failed when filling insulation thickness field") 

    try:
        results["length"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctSegment_ComboBoxElement']"))
    except:
        print("Failed when filling insulation density field")

    try:
        results["insulation density"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationDensity_ComboBoxElement']"))
    except:
        print("Failed when filling insulation density field")

    time.sleep(1)

    try:
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    except:
        print("failed to click complete button")

def read_values_from_page2(driver: webdriver.Edge):
    try:
        results["overall weight"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']"))
    except:
        print("failed to read Overall Weight")
    try:
        results["cross member width"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']"))
    except:
        print("failed to read Cross Member length")
    try:
        results["frame spacing"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']"))
    except:
        print("failed to read maximum H frame spacing")

    try:
        click_element(driver, (By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    except:
        print("failed to click complete button")
    
def page3(driver: webdriver.Edge):
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
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macEditPipeInfo_WebkitOuterClickLayer']"))
    except:
        print("failed to click edit pipe type button")
    time.sleep(2)
    read_values_from_page2(driver)
    time.sleep(2)
    try:
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext3_WebkitOuterClickLayer']"))
    except:
        print("failed to click next button")

def page4(driver):
    try:
        results["section length"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), [100])
    except:
        print("failed when entering section length")
    try:
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macAddSectionLength_WebkitOuterClickLayer']"))
    except:
        print("failed to click add to table button")
    time.sleep(1)
    try:
        results["total frames"] = read_value(driver,(By.CSS_SELECTOR, "input[id*='numTotalHFrames_TextBoxElement']"))
    except:
        print("failed when reading total number of H frames")
    try:
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macComplete_WebkitOuterClickLayer']"), multiple=True, element_index=1)
    except:
        print("failed to click complete button")