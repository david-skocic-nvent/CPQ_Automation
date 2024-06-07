from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import threading
from fileout import csvout
import time
import random as rand

TOOLNAME = "duct"
FIELD_NAMES = ["clearance", "extra cross member", "snow load", "shape", "width", "height", "gauge", "insulation thickness",
                    "length", "insulation density","section length", "overall weight", "cross member width", "frame spacing",  "total frames"]

AUTO_SNOW_LOAD = [0,5,10,20,40,60]
AUTO_EXTRA_CROSS_MEMBER = [True, False]
AUTO_CLEARANCE = [x for x in range(12,25)]
AUTO_WIDTH = [6,12,24,36,48]
AUTO_HEIGHT = [6,12,24,36,48]
AUTO_GAUGE = []
AUTO_SHAPE = []
AUTO_INSULATION_THICKNESS = []
AUTO_LENGTH = []
AUTO_INSULATION_DENSITY = []
AUTO_SECTION_LENGTH = [100]


# runs all four pages and returns their output dictionary to add to the csv file
# returns to the same place that it started, so it can run continuously
def auto(driver, executions, random=True, manual_inputs={}):
    for i in range(executions):
        results = {}
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macDuct_WebkitOuterClickLayer']"))
        time.sleep(3)
        page1(driver, results, random, manual_inputs)
        time.sleep(5)
        page2(driver, results, random, manual_inputs)
        time.sleep(2)
        page3(driver, results, random)
        time.sleep(3)
        page4(driver, results, random, manual_inputs)
        time.sleep(1)
        csvout(field_names=FIELD_NAMES, dict_to_write=results, toolname=TOOLNAME)
        print(f"thread {threading.current_thread().name} finished test execution {i + 1}")

#Filling in first page of values
def page1(driver: webdriver.Edge, results, random=True, inputs = {}):
    if random:
        clearance = AUTO_CLEARANCE
        extra_cross_member = AUTO_EXTRA_CROSS_MEMBER
        snow_load = AUTO_SNOW_LOAD
    else:
        clearance = [inputs['clearance']]
        extra_cross_member = [inputs['extra cross member']]
        snow_load = [inputs['snow load']]
    
    #choose_combobox_value(driver, (By.CSS_SELECTOR, "select[id*='cboCrossMemberType_ComboBoxElement']"), manual=True, manual_values=["Double Sided A12A Strut"])
    #choose_combobox_value(driver, (By.CSS_SELECTOR, "select[id*='cboFootType_ComboBoxElement']"), manual=True, manual_values=["Heavy Duty"])
    time.sleep(1)
    #input value for ground clearance
    results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), clearance)
    
    #input value for pipe spacing
    if rand.choice(extra_cross_member):
        results["extra cross member"] = True
        click_element(driver, (By.CSS_SELECTOR, "input[id*='chkTopBar_CheckBoxElement']"))
    else:
        results["extra cross member"] = False
    
    #input value for snow load
    results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), snow_load)
    
    #click next 
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']")) #, multiple=True, element_index=1)

#Filling in second page of values
def page2(driver: webdriver.Edge, results, random=True, inputs={}):
    if random:
        shape = AUTO_SHAPE
        width = AUTO_WIDTH
        height = AUTO_HEIGHT
        length = AUTO_LENGTH
        insulation_thickness = AUTO_INSULATION_THICKNESS
        insulation_density = AUTO_INSULATION_DENSITY
        gauge = AUTO_GAUGE
    else:
        shape = [inputs['shape']]
        if shape[0] == "Rectangle":
            height = [inputs['height']]
        width = [inputs['width']]
        length = [inputs['length']]
        insulation_density = [inputs['insulation density']]
        insulation_thickness = [inputs['insulation thickness']]
        gauge = [inputs['gauge']]
    results["shape"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"), manual=(not random), manual_values=shape)
    time.sleep(1)
    if results["shape"] == "Round":
        results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctDia_TextBoxElement']"),width)
    else:
        results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctWidth_TextBoxElement']"),width)
        results["height"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctHeight_TextBoxElement']"),height)
    time.sleep(1)
    results["length"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctSegment_ComboBoxElement']"), manual=(not random), manual_values=length)
    time.sleep(.1)
    results["insulation thickness"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"), manual=(not random), manual_values=insulation_thickness)
    time.sleep(.1)
    results["insulation density"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationDensity_ComboBoxElement']"), manual=(not random), manual_values=insulation_density)
    time.sleep(1)
    results["gauge"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctGage_ComboBoxElement']"), manual=(not random), manual_values=gauge)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))

def read_values_from_page2(driver: webdriver.Edge, results):
    results["overall weight"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']"))
    results["cross member width"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']"))
    results["frame spacing"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']"))
    click_element(driver, (By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    
def page3(driver: webdriver.Edge, results, random=True):
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
    read_values_from_page2(driver, results)
    time.sleep(2)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext3_WebkitOuterClickLayer']"))

def page4(driver, results, random=True, inputs={}):
    if random:
        section_length = AUTO_SECTION_LENGTH
    else:
        section_length = [inputs['section length']]
    results["section length"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), section_length)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macAddSectionLength_WebkitOuterClickLayer']"))
    time.sleep(2)
    results["total frames"] = read_value(driver,(By.CSS_SELECTOR, "input[id*='numTotalHFrames_TextBoxElement']"))
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macComplete_WebkitOuterClickLayer']"), multiple=True, element_index=1)
