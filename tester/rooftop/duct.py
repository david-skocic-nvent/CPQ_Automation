from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import time
import random as rand

AUTO_SNOW_LOAD = [0,5,10,20,40,60]
AUTO_EXTRA_CROSS_MEMBER = [True, False]
AUTO_CLEARANCE = [x for x in range(12,25)]
AUTO_WIDTH = [x for x in range(10,51)]
AUTO_HEIGHT = [x for x in range(10,51)]
results = {}

# runs all four pages and returns their output dictionary to add to the csv file
# returns to the same place that it started, so it can run continuously
def auto(driver, random=True, manual_inputs={}):
    global results
    global Clearance
    global SnowLoad
    global ExtraCrossMember
    global Width
    global Height
    global Gauge
    global Shape
    global InsulationThickness
    global Length
    global InsulationDensity
    global SectionLength
    if random:
        Clearance = AUTO_CLEARANCE
        SnowLoad = AUTO_SNOW_LOAD
        ExtraCrossMember = AUTO_EXTRA_CROSS_MEMBER
        Width = AUTO_WIDTH
        Height = AUTO_HEIGHT
        Gauge = []
        Shape = []
        InsulationThickness = []
        Length = []
        InsulationDensity = []
        SectionLength = [100]
    else:
        Clearance = [manual_inputs['clearance']]
        SnowLoad = [manual_inputs['snow load']]
        ExtraCrossMember = [bool(manual_inputs['extra cross member'])]
        Width = [manual_inputs['width']]
        Height = [manual_inputs['height']]
        Gauge = [manual_inputs['gauge']]
        Shape = [manual_inputs['shape']]
        InsulationThickness = [manual_inputs['insulation thickness']]
        Length = [manual_inputs['length']]
        InsulationDensity = [manual_inputs['insulation density']]
        SectionLength = [manual_inputs['section length']]

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
def page1(driver: webdriver.Edge, random=True):
    #input value for ground clearance
    results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), Clearance)
    
    #input value for pipe spacing
    if rand.choice(ExtraCrossMember):
        results["extra cross member"] = True
        click_element(driver, (By.CSS_SELECTOR, "input[id*='chkTopBar_CheckBoxElement']"))
    else:
        results["extra cross member"] = False
    
    #input value for snow load
    results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SnowLoad)
    
    #click next 
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']")) #, multiple=True, element_index=1)

#Filling in second page of values
def page2(driver: webdriver.Edge, random=True):
    results["shape"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"), manual=(not random), manual_values=Shape)
    time.sleep(1)
    if results["shape"] == "Round":
        results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctDia_TextBoxElement']"),Width)
    else:
        results["width"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctWidth_TextBoxElement']"),Width)
        results["height"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDuctHeight_TextBoxElement']"),Height)
    time.sleep(.5)

    results["gauge"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctGage_ComboBoxElement']"), manual=(not random), manual_values=Gauge)
    time.sleep(.5)
    results["insulation thickness"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"), manual=(not random), manual_values=InsulationThickness)
    time.sleep(.5)
    results["length"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboDuctSegment_ComboBoxElement']"), manual=(not random), manual_values=Length)
    time.sleep(.5)
    results["insulation density"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationDensity_ComboBoxElement']"), manual=(not random), manual_values=InsulationDensity)
    time.sleep(1)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))

def read_values_from_page2(driver: webdriver.Edge):
    results["overall weight"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']"))
    results["cross member width"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']"))
    results["frame spacing"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']"))
    click_element(driver, (By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    
def page3(driver: webdriver.Edge, random=True):
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

def page4(driver,random=True):
    results["section length"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), SectionLength)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macAddSectionLength_WebkitOuterClickLayer']"))
    time.sleep(1)
    results["total frames"] = read_value(driver,(By.CSS_SELECTOR, "input[id*='numTotalHFrames_TextBoxElement']"))
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macComplete_WebkitOuterClickLayer']"), multiple=True, element_index=1)
