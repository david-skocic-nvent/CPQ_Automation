from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import threading
from fileout import csvout
import time
import random as rand

AUTO_MATERIAL = ['Water', 'Gas']
AUTO_HOLDER = ["Clamp", "Hanger", "Roller"]
AUTO_SNOW_LOAD = [0,5,10,20,40,60]
AUTO_CLEARANCE = [x for x in range(12,25)]
AUTO_SPACING = [x for x in range(2,11)]
AUTO_PIPE_COUNT = [x for x in range(1,11)]
AUTO_PIPE_TYPE = []
AUTO_DIAMETER = []
AUTO_INSULATION = []
AUTO_SECTION_LENGTH = [100]

TOOLNAME = "pipe"
FIELD_NAMES = ["holder", "clearance", "spacing", "snow load", "pipe type", "diameter", "insulation", "material", "pipe count", 
                "section length", "overall weight", "cross member width", "frame spacing", "hanger size", "total frames"]

def auto(driver, executions, random = True, manual_inputs = {}):
    for i in range(executions):
        results = {}
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macPipe_WebkitOuterClickLayer']"))
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

# Fills in the first page of values
def page1(driver, results, random = True, inputs = {}):
    #choose_combobox_value(driver, (By.CSS_SELECTOR, "select[id*='cboCrossMemberType_ComboBoxElement']"), manual=True, manual_values=["Double Sided A12A Strut"])
    #choose_combobox_value(driver, (By.CSS_SELECTOR, "select[id*='cboFootType_ComboBoxElement']"), manual=True, manual_values=["Heavy Duty"])
    time.sleep(1)
    if random:
        holder = AUTO_HOLDER
        clearance = AUTO_CLEARANCE
        spacing = AUTO_SPACING
        snow_load = AUTO_SNOW_LOAD
    else:
        holder = [inputs['holder']]
        clearance = [inputs['clearance']]
        spacing = [inputs['spacing']]
        snow_load = [inputs['snow load']]
    #choosing holder button
    holder_choice = rand.choice(holder)
    match (holder_choice):
        case ("Clamp"):
            click_element(driver,(By.CSS_SELECTOR, "div[id*='optSupport_ImageContainer']"))
        case ("Roller"):
            click_element(driver,(By.CSS_SELECTOR, "div[id*='optRoller_ImageContainer']"))
        case ("Hanger"):
            click_element(driver,(By.CSS_SELECTOR, "div[id*='optHang_ImageContainer']"))
    results['holder'] = holder_choice
    time.sleep(1)
    #input value for ground clearance
    if holder_choice == "Hanger":
        results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numDropLength_TextBoxElement']"), clearance)
    else:
        results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), clearance)
    #input value for pipe spacing
    results["spacing"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']"), spacing)
    #input value for snow load
    results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), snow_load)
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']"))
 

# fills in second page of values
def page2(driver: webdriver.Edge, results, random = True, inputs={}):
    if random:
        pipe_type = AUTO_PIPE_TYPE
        diameter = AUTO_DIAMETER
        insulation = AUTO_INSULATION
        material = AUTO_MATERIAL
        pipe_count = AUTO_PIPE_COUNT
    else:
        pipe_type = [inputs["pipe type"]]
        diameter = [inputs["diameter"]]
        insulation = [inputs["insulation"]]
        material = [inputs["material"]]
        pipe_count = [inputs["pipe count"]]

    results["pipe type"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"), manual=(not random), manual_values=pipe_type)
    time.sleep(1)
    results["diameter"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"), manual=(not random), manual_values=diameter)
    time.sleep(.5)
    results["insulation"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"), manual=(not random), manual_values=insulation)
    time.sleep(.5)
    if rand.choice(material) == "Water":
        results["material"] = "Water"
        click_element(driver,(By.CSS_SELECTOR, "input[id*='optLiquid_OptionElement']"))
    else:
        results["material"] = "Gas"
        click_element(driver,(By.CSS_SELECTOR, "input[id*='optGas_OptionElement']"))
    try:
        pipe_count_choice = rand.choice(pipe_count)
        slider_element = driver.find_element(By.CSS_SELECTOR, "div[id*='sldNumPipes_SliderTrackElement']")
        actions = ActionChains(driver)
        results["pipe count"] = pipe_count_choice
        print ("Pipe count:" + str(pipe_count_choice))
        for _ in range(int(pipe_count_choice) - 1):
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
    results["hanger size"] = read_value(driver,(By.CSS_SELECTOR, "select[id*='cboMaxHangerSize_ComboBoxElement']"))
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