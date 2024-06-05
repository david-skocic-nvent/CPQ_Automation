from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import time
import random as rand

AUTO_MATERIAL = ['Water', 'Gas']
AUTO_HOLDER = ["Clamp", "Hanger", "Roller"]
AUTO_SNOW_LOAD = [0,5,10,20,40,60]
AUTO_CLEARANCE = [x for x in range(12,25)]
AUTO_SPACING = [x for x in range(2,11)]
results = {}

def auto(driver, random = True, manual_inputs = {}):
    global results
    global Holder
    global Clearance
    global Spacing
    global SnowLoad
    global PipeType
    global Diameter
    global Insulation
    global PipeCount
    global SectionLength
    global Material
    results = {}
    if random:
        Holder = AUTO_HOLDER
        SnowLoad = AUTO_SNOW_LOAD
        Material = AUTO_MATERIAL
        Clearance = AUTO_CLEARANCE
        Spacing = AUTO_SPACING
        PipeCount = rand.randint(1,10)
        PipeType = []
        Diameter = []
        Insulation = []
        SectionLength = [100]
    else:
        Holder = [manual_inputs['holder']]
        print(Holder)
        SnowLoad = [manual_inputs['snow load']]
        Material = [manual_inputs['material']]
        Clearance = [manual_inputs['clearance']]
        Spacing = [manual_inputs['spacing']]
        PipeCount = int(manual_inputs['pipe count'])
        PipeType = [manual_inputs['pipe type']]
        Diameter = [manual_inputs['diameter']]
        Insulation = [manual_inputs['insulation']]
        SectionLength = [manual_inputs['section length']]

    click_element(driver,(By.CSS_SELECTOR, "div[id*='macPipe_WebkitOuterClickLayer']"))
    time.sleep(3)
    page1(driver, random)
    time.sleep(5)
    page2(driver, random)
    time.sleep(2)
    page3(driver, random)
    time.sleep(3)
    page4(driver, random)
    time.sleep(1)
    return results

# Fills in the first page of values
def page1(driver, random = True):
    #choosing holder button
    holder = rand.choice(Holder)
    match (holder):
        case ("Clamp"):
            click_element(driver,(By.CSS_SELECTOR, "div[id*='optSupport_ImageContainer']"))
        case ("Roller"):
            click_element(driver,(By.CSS_SELECTOR, "div[id*='optRoller_ImageContainer']"))
        case ("Hanger"):
            click_element(driver,(By.CSS_SELECTOR, "div[id*='optHang_ImageContainer']"))
    results['holder'] = holder
    time.sleep(1)
    #input value for ground clearance
    if holder == "Hanger":
        results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDropLength_TextBoxElement']"), Clearance)
    else:
        results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), Clearance)
    #input value for pipe spacing
    results["spacing"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']"), Spacing)
    #input value for snow load
    results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SnowLoad)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']"))
 

# fills in second page of values
def page2(driver: webdriver.Edge, random = True):
    results["pipe type"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"), manual=(not random), manual_values=PipeType)
    time.sleep(1)
    results["diameter"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"), manual=(not random), manual_values=Diameter)
    time.sleep(.5)
    results["insulation"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"), manual=(not random), manual_values=Insulation)
    time.sleep(.5)
    if rand.choice(Material) == "Water":
        results["material"] = "Water"
        click_element(driver,(By.CSS_SELECTOR, "input[id*='optLiquid_OptionElement']"))
    else:
        results["material"] = "Gas"
        click_element(driver,(By.CSS_SELECTOR, "input[id*='optGas_OptionElement']"))
    try:
        slider_element = driver.find_element(By.CSS_SELECTOR, "div[id*='sldNumPipes_SliderTrackElement']")
        actions = ActionChains(driver)
        results["pipe count"] = PipeCount
        print ("Pipe count:" + str(PipeCount))
        for _ in range(int(PipeCount) - 1):
            actions.move_by_offset(slider_element.location['x'] + slider_element.size['width'] - 5, slider_element.location['y'] + 1).click()
            actions.move_by_offset(-(slider_element.location['x'] + slider_element.size['width'] - 5), -(slider_element.location['y'] + 1))
            actions.perform()
            time.sleep(.2)
        time.sleep(1)
    except:
        print("failed when moving slider")
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))

def read_values_from_page2(driver):
    results["overall weight"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']"))
    results["cross member width"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']"))
    results["frame spacing"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']"))
    results["hanger size"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxHangerSize_ComboBoxElement']"))
    click_element(driver, (By.CSS_SELECTOR, "div[id*='macUpdatePipeInfo_WebkitOuterClickLayer']"))
    
def page3(driver: webdriver.Edge, random = True):
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


def page4(driver, random = True):
    results["section length"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), SectionLength)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macAddSectionLength_WebkitOuterClickLayer']"))
    time.sleep(1)
    results["total frames"] = read_value(driver,(By.CSS_SELECTOR, "input[id*='numTotalHFrames_TextBoxElement']"))
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macComplete_WebkitOuterClickLayer']"), multiple=True, element_index=1)