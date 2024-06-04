from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import time

SNOW_LOAD = [0,5,10,20,40,60]
FILL = [31,40,53]
results = {}

# runs all four pages and returns their output dictionary to add to the csv file
# returns to the same place that it started, so it can run continuously
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

#Filling in first page of values
def page1(driver: webdriver.Edge):
    #input value for ground clearance
    results["clearance"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), [x for x in range(12,25)])
    #input value for pipe spacing
    results["spacing"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']"), [x for x in range(2,11)])
    #input value for snow load
    results["snow load"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SNOW_LOAD)
    #click next 
    click_element(driver,(By.CSS_SELECTOR, "div[id*='macNext1_WebkitOuterClickLayer']"), multiple=True, element_index=1)

#Filling in second page of values
def page2(driver: webdriver.Edge):
    results["pipe type"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"))
    time.sleep(1)
    results["diameter"] = choose_combobox_value(driver,(By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"))
    time.sleep(.5)
    results["fill"] = choose_textbox_value(driver,(By.CSS_SELECTOR, "input[id*='numPercentFill_TextBoxElement']"),FILL)

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