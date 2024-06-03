from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import time

MATERIAL = ['Water', 'Gas']
HOLDER = ["Clamp", "Hanger", "Roller"]
SNOW_LOAD = [0,5,10,20,40,60]
results = {}

def auto(driver):
    global results
    results = {}
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macConduit_WebkitOuterClickLayer']"))
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


def page1(driver: webdriver.Edge):
#--------------------------------------------------------------------------------
#Filling in first page of values

    time.sleep(1)
    #input value for ground clearance
    try:
        results["clearance"] = choose_random_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), [x for x in range(12,25)])
    except:
        print("Failed when filling ground clearance field")
    
    #input value for pipe spacing
    try:
        results["spacing"] = choose_random_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']"), [x for x in range(2,11)])
    except:
        print("Failed when filling pipe spacing field")
    
    #input value for snow load
    try:
        results["snow load"] = choose_random_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SNOW_LOAD)
    except:
        print("Failed when filling snow load field")
    
    try:
        click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext1_WebkitOuterClickLayer']"), multiple=True, element_index=1)
    except:
        print("failed to click next button")
#--------------------------------------------------------------------------------

def page2(driver: webdriver.Edge):
#--------------------------------------------------------------------------------
#Filling in second page of values
    try:
        results["pipe type"] = choose_random_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"))
    except:
        print("Failed when filling pipe material field")
    time.sleep(1)
    try:
        results["diameter"] = choose_random_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"))
    except:
        print("Failed when filling pipe diameter field")
    time.sleep(.5)
    try:
        results["fill"] = choose_random_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPercentFill_TextBoxElement']"),[31,40,53])
    except:
        print("Failed when filling wire fill field")

    try:
        slider_element = driver.find_element(By.CSS_SELECTOR, "div[id*='sldNumPipes_SliderTrackElement']")
        actions = ActionChains(driver)
        pipe_count = random.randint(1,10)
        results["pipe count"] = pipe_count
        print ("Pipe count:" + str(pipe_count))
        for _ in range(pipe_count - 1):
            actions.move_by_offset(slider_element.location['x'] + slider_element.size['width'] - 5, slider_element.location['y'] + 1).click()
            actions.move_by_offset(-(slider_element.location['x'] + slider_element.size['width'] - 5), -(slider_element.location['y'] + 1))
            actions.perform()
            time.sleep(.2)
        time.sleep(1)
    except:
        print("failed when moving slider")

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
#--------------------------------------------------------------------------------

def page4(driver):
    try:
        results["section length"] = choose_random_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSectionLength_TextBoxElement']"), [100])
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