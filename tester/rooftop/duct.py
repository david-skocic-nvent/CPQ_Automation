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
    results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), [x for x in range(12,25)])
    
    #input value for pipe spacing
    if random.choice(EXTRA_CROSS_MEMBER):
        results["extra cross member"] = True
        click_element(driver, (By.CSS_SELECTOR, "input[id*='chkTopBar_CheckBoxElement']"))
    else:
        results["extra cross member"] = False
    
    #input value for snow load
    results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SNOW_LOAD)
    
    #click next 
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']")) #, multiple=True, element_index=1)

#Filling in second page of values
def page2(driver: webdriver.Edge):
    results["shape"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"))
    time.sleep(1)
    if results["shape"] == "Round":
        results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctDia_TextBoxElement']"),[x for x in range(10,51)])
    else:
        results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctWidth_TextBoxElement']"),[x for x in range(10,51)])
        results["height"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctHeight_TextBoxElement']"),[x for x in range(10,51)])
    time.sleep(.5)

    results["gauge"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctGage_ComboBoxElement']"))
    results["insulation thickness"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"))
    results["length"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctSegment_ComboBoxElement']"))
    results["insulation density"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationDensity_ComboBoxElement']"))
    time.sleep(1)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))

def read_values_from_page2(driver: webdriver.Edge):
    results["overall weight"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']"))
    results["cross member width"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']"))
    results["frame spacing"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']"))
    click_element(driver, (By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    
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
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macEditPipeInfo_WebkitOuterClickLayer']"))
    time.sleep(2)
    read_values_from_page2(driver)
    time.sleep(2)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext3_WebkitOuterClickLayer']"))

def page4(driver):
    results["section length"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), [100])
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macAddSectionLength_WebkitOuterClickLayer']"))
    time.sleep(1)
    results["total frames"] = read_value(driver,(By.CSS_SELECTOR, "input[id*='numTotalHFrames_TextBoxElement']"))
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macComplete_WebkitOuterClickLayer']"), multiple=True, element_index=1)
