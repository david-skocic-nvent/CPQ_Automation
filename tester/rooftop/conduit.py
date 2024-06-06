from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import threading
from fileout import csvout
import time
import random as rand

TOOLNAME = "conduit"
FIELD_NAMES = ["clearance", "spacing", "snow load", "pipe type", "diameter", "fill", "pipe count",
                       "section length", "overall weight", "cross member width", "frame spacing", "total frames"]

AUTO_SNOW_LOAD = [0,5,10,20,40,60]
AUTO_FILL = [31,40,53]
AUTO_CLEARANCE = [x for x in range(12,25)]
AUTO_SPACING = [x for x in range(2,11)]
PIPE_COUNT = [x for x in range(1,11)]

# runs all four pages and returns their output dictionary to add to the csv file
# returns to the same place that it started, so it can run continuously
def auto(driver, executions, random = True, manual_inputs = {}):
    global SnowLoad
    global Clearance
    global Spacing
    global Fill
    global PipeCount
    global PipeType
    global Diameter
    global SectionLength
    #Saving values as default auto values for textbox fills and empty lists for comboboxes
    if random:
        SnowLoad = AUTO_SNOW_LOAD
        Clearance = AUTO_CLEARANCE
        Spacing = AUTO_SPACING
        Fill = AUTO_FILL
        PipeCount = PIPE_COUNT
        PipeType = []
        Diameter = []
        SectionLength = [100]
    #saving values from manual input dict. saved as lists of one item to work with tester_functions
    else:
        PipeCount = int(manual_inputs['pipe count'])
        Clearance = [manual_inputs['clearance']]
        Spacing = [manual_inputs['spacing']]
        SnowLoad = [manual_inputs['snow load']]
        Fill = [manual_inputs['fill']]
        PipeType = [manual_inputs['pipe type']]
        Diameter = [manual_inputs["diameter"]]
        SectionLength = [manual_inputs['section length']]
    
    for i in range(executions):
        results = {}
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macConduit_WebkitOuterClickLayer']"))
        time.sleep(3)
        page1(driver, results, random)
        time.sleep(5)
        page2(driver, results, random)
        time.sleep(2)
        page3(driver, results, random)
        time.sleep(3)
        page4(driver, results, random)
        time.sleep(1)
        csvout(field_names=FIELD_NAMES, dict_to_write=results, toolname=TOOLNAME)
        print(f"thread {threading.current_thread().name} finished test execution {i + 1}")

#Filling in first page of values
def page1(driver: webdriver.Edge, results, random = True):
    choose_combobox_value(driver, (By.CSS_SELECTOR, "select[id*='cboCrossMemberType_ComboBoxElement']"), manual=True, manual_values=["Double Sided A12A Strut"])
    choose_combobox_value(driver, (By.CSS_SELECTOR, "select[id*='cboFootType_ComboBoxElement']"), manual=True, manual_values=["Heavy Duty"])
    time.sleep(1)
    #input value for ground clearance
    results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), Clearance)
    #input value for pipe spacing
    results["spacing"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']"), Spacing)
    #input value for snow load
    results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SnowLoad)
    #click next 
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext1_WebkitOuterClickLayer']"), multiple=True, element_index=1)

#Filling in second page of values
def page2(driver: webdriver.Edge, results, random = True):
    results["pipe type"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"), manual=(not random), manual_values=PipeType)
    time.sleep(1)
    results["diameter"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"), manual=(not random), manual_values=Diameter)
    time.sleep(.5)
    results["fill"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPercentFill_TextBoxElement']"), Fill)

    try:
        pipe_count = rand.choice(PipeCount)
        slider_element = driver.find_element(By.CSS_SELECTOR, "div[id*='sldNumPipes_SliderTrackElement']")
        actions = ActionChains(driver)
        results["pipe count"] = pipe_count
        for _ in range(pipe_count - 1):
            actions.move_by_offset(slider_element.location['x'] + slider_element.size['width'] - 5, slider_element.location['y'] + 1).click()
            actions.move_by_offset(-(slider_element.location['x'] + slider_element.size['width'] - 5), -(slider_element.location['y'] + 1))
            actions.perform()
            time.sleep(.2)
        time.sleep(1)
    except:
        print("failed when moving slider")

    click_element(driver,(By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))

def read_values_from_page2(driver: webdriver.Edge, results):
    results["overall weight"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']"))
    results["cross member width"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']"))
    results["frame spacing"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']"))
    click_element(driver, (By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    
def page3(driver: webdriver.Edge, results, random = True):
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

def page4(driver, results, random = True):
    results["section length"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), SectionLength)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macAddSectionLength_WebkitOuterClickLayer']"))
    time.sleep(2)
    results["total frames"] = read_value(driver,(By.CSS_SELECTOR, "input[id*='numTotalHFrames_TextBoxElement']"))
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macComplete_WebkitOuterClickLayer']"), multiple=True, element_index=1)