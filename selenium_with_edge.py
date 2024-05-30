from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("CPQ_USERNAME")
PASSWORD = os.getenv("CPQ_PASSWORD")
TOOL = "RoofTop"
LINK = "http://10.4.75.133:8020/Apps/Rooftop_1_MNL/" #"http://10.4.75.133:8020/Login"

TOOL_HREFS = {"RoofTop": "/Apps/Rooftop"}

HEIGHT_ABOVE_ROOF = [12, 18, 24, 30, 36]
SNOW_LOAD = [0, 10, 20, 40, 60]
PIPE_SPACING = [6, 8, 10, 12, 14]
PIPE_TYPE = ['Iron - Schedule 40', 'Iron - Schedule 80', 'Copper - type K', 'Copper - type L', 'CPVC - Schedule 40', 'CPVC - Schedule 80']
DIAMETERS = [2, 4, 6, 8, 10]
PIPE_INSULATION = [.5, 1, 1.5, 2.5, 3, 4]
NUMBER_OF_PIPES = [x for x in range(1,11)]
MATERIAL = ['Water', 'Gas']
HOLDER = ["Clamp", "Hanger", "Roller"]

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
    

    try:
        # Select the pipe button
        button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='macPipe_WebkitOuterClickLayer']")))
        button.click()
    except:
        print("Couldn't press Pipe button")

def click_element(selection):
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
    except:
        print ("Failed when selecting a holder button")

    time.sleep(1)
    #input value for ground clearance
    try:
        if holder == "Hanger":
            choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numDropLength_TextBoxElement']"), [x for x in range(12,25)])
        else:
            choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']"), [x for x in range(12,25)])
    except:
        print("Failed when filling ground clearance field")
        write_html_to_temp_file()
    
    #input value for pipe spacing
    try:
        choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']"), [x for x in range(2,25)])
    except:
        print("Failed when filling pipe spacing field")
    
    #input value for snow load
    try:
        choose_random_textbox_value((By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']"), SNOW_LOAD)
    except:
        print("Failed when filling snow load field")
    
    '''try:
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']")))
        next_button.click()
    except:
        print("Failed when Clicking next button")'''
#--------------------------------------------------------------------------------

def page2():
#--------------------------------------------------------------------------------
#Filling in second page of values
    try:
        choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"))
    except:
        print("Failed when filling pipe material field")

    try:
        choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"))
    except:
        print("Failed when filling pipe diameter field")

    try:
        choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"))
    except:
        print("Failed when filling pipe diameter field")

    try:
        if random.choice(MATERIAL) == "Water":
            click_element((By.CSS_SELECTOR, "input[id*='optLiquid_OptionElement']"))
        else:
            click_element((By.CSS_SELECTOR, "input[id*='optGas_OptionElement']"))
    except:
        print("Failed when pressing material in pipe button")

    try:
        slider_element = driver.find_element(By.CSS_SELECTOR, "div[id*='sldNumPipes_SliderTrackElement']" )
        actions = ActionChains(driver)
        for i in range(random.randint(0,9)):
            actions.move_by_offset(slider_element.location['x'] + slider_element.size['width'] - 5, slider_element.location['y'] + 1).click()
            actions.perform()
            actions.move_by_offset(-(slider_element.location['x'] + slider_element.size['width'] - 5), -(slider_element.location['y'] + 1))
            actions.perform()
    except:
        print("failed when moving slider")

def read_values_from_page2():
    try:
        print(read_value((By.CSS_SELECTOR, "select[id*='cboSumWeight_ComboBoxElement']")))
    except:
        print("failed to read Overall Weight")
    try:
        print(read_value((By.CSS_SELECTOR, "select[id*='cboWidthCrossMember_ComboBoxElement']")))
    except:
        print("failed to read Cross Member length")
    try:
        print(read_value((By.CSS_SELECTOR, "select[id*='cboMaxSpacingtoUse_ComboBoxElement']")))
    except:
        print("failed to read maximum H frame spacing")
    try:
        print(read_value((By.CSS_SELECTOR, "select[id*='cboMaxHangerSize_ComboBoxElement']")))
    except:
        print("failed to read max hanger size")
    
def page3():
    try:
        print(read_value((By.CSS_SELECTOR, "input[id*='numOverallPSI_TextBoxElement']")))
    except:
        print("failed to read PSI")
    try:
        table = driver.find_element(By.CSS_SELECTOR, "div[data-id*='dw-listview-body_']")
        print("here")
        actions = ActionChains(driver)
        actions.move_by_offset(table.location['x'] + 5, table.location['y'] + 5).click()
        actions.move_by_offset(-(table.location['x'] + 5),-(table.location['y'] + 5))
        actions.perform()
    except:
        print("failed to select table row")
    try:
        click_element((By.CSS_SELECTOR, "div[id*='macEditPipeInfo_WebkitOuterClickLayer']"))
    except:
        print("failed to click edit pipe type button")
    time.sleep(2)
    read_values_from_page2()






#--------------------------------------------------------------------------------
'''
    try:

        button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']")))
        button.click()
        time.sleep(1)

        dropdownelement = driver.find_element(By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']")
        dropdown = Select(dropdownelement)
        print("here")
        dropdown.click()
        visible_options = dropdown.options
        for option in visible_options:
            print(option.text)
        dropdown.select_by_visible_text("abc") #throws an error when there isnt the option
        print("here")


        
    except:
        print("failed.")'''

def write_html_to_temp_file():
    with open("html_output.txt", 'w') as f:
        f.write(driver.page_source)

def random_params():
    #choose random value between 12 and 36 (inclusive) for ground clearance
    #choose random value between 6 and 15 (inclusive) for required spacing between pipes
    #choose random value from [0,10,20,40,60] for snow load
    #choose random value from pipe material list
    #choose random diameter from the size dropdown
    #choose random insulation thickness from the thickness dropdown (must intersect with the list from the excel)
    #choose water/gas
    #choose a random quantity
    pass

if __name__ == '__main__':
    driver = webdriver.Edge()
    driver.get(LINK)

    login()
    #enter_tool("RoofTop")

    a = input("a: ")

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
        a = input("a: ")


    '''login()
    enter_tool(TOOL)
    time.sleep(3)
    rooftop_pipe()'''
    #time.sleep(3)
    
    #leave browser open when done
    #driver.quit()



