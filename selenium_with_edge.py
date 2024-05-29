from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
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
    dropdown = Select(driver.find_element(selection[0],selection[1]))
    choice = random.choice(dropdown.options).text
    if not allow_empty_value:
        while choice == "":
            choice = random.choice(dropdown.options).text
    dropdown.select_by_visible_text(choice)

def auto_rooftop_pipe():
    #click on the pipe button
    #select hanger/support type button
    #fill ground clearance field
    #fill spacing field
    #fill snow load field
    #click next                             
    #fill material field
    #fill size field
    #fill insulation field
    #fill material in pipe field            <<<<<< Here
    #move quantity slider
    #click complete
    #read off weight per foot, cross member length, and pressure on each H frame
    #click on the pipe row in the table 
    #click edit pipe type
    #click the little gray square
    #read off weight per foot, width of cross member, hanger size, minimum max pipe spacing, and max spacing between H frames
        #while max spacing is not filled, choose between (move slider to a lower number, reduce size of pipes)
    #click complete
    #click next
    #enter length of 100
    #click add to table
    #read Total number of H frames
    #click complete
    #select the row just created
    #click delete line

    #start again at the top of the list

    try:
        # Select the pipe button
        button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='macPipe_WebkitOuterClickLayer']")))
        button.click()
    except:
        print("Couldn't press Pipe button")

def page1():
#--------------------------------------------------------------------------------
#Filling in first page of values

    #choosing holder button
    try:
        holder = random.choice(HOLDER)
        match (holder):
            case ("Clamp"):
                button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='optSupport_ImageContainer']")))
                button.click()
            case ("Roller"):
                button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='optHang_ImageContainer']")))
                button.click()
            case ("Hanger"):
                button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='optRoller_ImageContainer']")))
                button.click()
    except:
        print ("Failed when selecting a holder button")

    time.sleep(2)
    #input value for ground clearance
    try:
        clearance = random.randrange(12,37,1)
        if holder == "Hanger":
            clearnace_textbox = driver.find_element(By.CSS_SELECTOR, "input[id*='numDropLength_TextBoxElement']")
            clearnace_textbox.clear()
            clearnace_textbox.send_keys(clearance)
        else:
            clearnace_textbox = driver.find_element(By.CSS_SELECTOR, "input[id*='numGndClearance_TextBoxElement']")
            clearnace_textbox.clear()
            clearnace_textbox.send_keys(clearance)
    except:
        print("Failed when filling ground clearance field")
    
    #input value for pipe spacing
    try:
        spacing = random.randrange(6,11,1)
        spacing_textbox = driver.find_element(By.CSS_SELECTOR, "input[id*='numPipeSpacing_TextBoxElement']")
        spacing_textbox.clear()
        spacing_textbox.send_keys(spacing)
    except:
        print("Failed when filling pipe spacing field")

    #input value for snow load
    try:
        snow_load = random.choice(SNOW_LOAD)
        snow_load_textbox = driver.find_element(By.CSS_SELECTOR, "input[id*='numSnowLoad_TextBoxElement']")
        snow_load_textbox.clear()
        snow_load_textbox.send_keys(snow_load)
    except:
        print("Failed when filling snow load field")

    try:
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id*='macNext2_WebkitOuterClickLayer']")))
        next_button.click()
    except:
        print("Failed when Clicking next button")
#--------------------------------------------------------------------------------

def page2():
#--------------------------------------------------------------------------------
#Filling in second page of values
    try:
        choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboPipeType_ComboBoxElement']"))
    except:
        print("Failed when filling pipe material field")
    
    time.sleep(0.5)

    try:
        choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboPipeDia_ComboBoxElement']"))
    except:
        print("Failed when filling pipe diameter field")

    time.sleep(0.5)

    try:
        choose_random_combobox_value((By.CSS_SELECTOR, "select[id*='cboInsulationThickness_ComboBoxElement']"))
    except:
        print("Failed when filling pipe diameter field")

    time.sleep(0.5)

    try:
        if random.choice(MATERIAL) == "Water":
            material_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id*='optLiquid_OptionElement']")))
        else:
            material_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id*='optGas_OptionElement']")))
        material_button.click()
    except:
        print("Failed when pressing material in pipe button")



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
        print(driver.page_source)
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



