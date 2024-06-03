from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from write_to_output import output_results_to_csv
from pathlib import Path
import rooftop.pipe as pipe
import rooftop.conduit as conduit
import time
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("CPQ_USERNAME")
PASSWORD = os.getenv("CPQ_PASSWORD")

PIPE_FIELD_NAMES = ["holder", "clearance", "spacing", "snow load", "pipe type", "diameter", "insulation",
                "material", "pipe count", "section length", "pressure", "overall weight", "cross member width",
                "frame spacing", "hanger size", "total frames"]

LINK = "http://10.4.75.133:8020/Apps/Rooftop_1_MNL/"


def login(driver: webdriver.Edge):
    element = driver.find_element(By.ID, 'username')
    element.send_keys(USERNAME)
    element = driver.find_element(By.NAME, 'Password')
    element.send_keys(PASSWORD)
    button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "login-button")))
    button.click()

def write_html_to_temp_file():
    with open("html_output.txt", 'w') as f:
        f.write(driver.page_source)

if __name__ == '__main__':
    driver = webdriver.Edge()
    driver.get(LINK)

    login(driver)

    a = input("How do you want to run tests?: ")

    if a == "debug":
        a = input("what tool are you using?: ")
        if a == "pipe":
            while (a != "end"):
                match (a):
                    case "p1":
                        pipe.page1(driver)
                    case "p2":
                        pipe.page2(driver)
                    case "rp2":
                        pipe.read_values_from_page2(driver)
                    case "p3":
                        pipe.page3(driver)
                    case "p4":
                        pipe.page4(driver)
                    case "dump":
                        write_html_to_temp_file(driver)
                    case "write results":
                        output_results_to_csv(field_names=PIPE_FIELD_NAMES, dict=pipe.results)
                a = input("a: ")
        elif a == "conduit":
            while (a != "end"):
                match (a):
                    case "p1":
                        conduit.page1(driver)
                    case "p2":
                        conduit.page2(driver)
                    case "rp2":
                        conduit.read_values_from_page2(driver)
                    case "p3":
                        conduit.page3(driver)
                    case "p4":
                        conduit.page4(driver)
                    case "dump":
                        write_html_to_temp_file()
                    case "write results":
                        output_results_to_csv(field_names=PIPE_FIELD_NAMES, dict=pipe.results)
                a = input("a: ")
    elif a == "auto":
        while (a != "end"):
            match (a):
                case "pipe":
                    for _ in range(8):
                        results = pipe.auto(driver)
                        output_results_to_csv(field_names=PIPE_FIELD_NAMES, dict = results) 
                case "conduit":
                    for _ in range(2):
                        results = conduit.auto(driver)
            a = input("tool?: ")