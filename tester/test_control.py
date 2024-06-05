from selenium import webdriver
from fileout import *
from tester_functions import login
import rooftop.pipe as pipe
import rooftop.conduit as conduit
import rooftop.duct as duct
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("CPQ_USERNAME")
PASSWORD = os.getenv("CPQ_PASSWORD")

PIPE_FIELD_NAMES = ["holder", "clearance", "spacing", "snow load", "pipe type", "diameter", "insulation",
                "material", "pipe count", "section length", "pressure", "overall weight", "cross member width",
                "frame spacing", "hanger size", "total frames"]

CONDUIT_FIELD_NAMES = ["clearance", "spacing", "snow load", "pipe type", "diameter", "fill", "pipe count",
                       "section length", "overall weight", "cross member width", "frame spacing", "total frames"]

DUCT_FIELD_NAMES = ["clearance", "extra cross member", "snow load", "shape", "width", "height", "gauge", "insulation thickness",
                    "length", "insulation density", "overall weight", "cross member width", "frame spacing", "section length", "total frames"]

LINK = "http://10.4.75.133:8020/Apps/Rooftop_1_MNL/"

if __name__ == '__main__':
    driver = 1
    driver = webdriver.Edge()
    driver.get(LINK)

    login(driver, USERNAME, PASSWORD)

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
                    case "write results":
                        csvout(field_names=PIPE_FIELD_NAMES, dict=pipe.results)
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
                    case "write results":
                        csvout(field_names=PIPE_FIELD_NAMES, dict=pipe.results)
                a = input("a: ")
    elif a == "auto":
        while (a != "end"):
            match (a):
                case "pipe":
                    dictreader = csvin("pipe")
                    results = []
                    for d in dictreader:
                        results.append(d)
                    print(results[0])
                    print(pipe.auto(driver, random=False, manual_inputs=results[0]))
                    #for _ in range(8):
                    #    results = pipe.auto(driver)
                    #    csvout(field_names=PIPE_FIELD_NAMES, dict = results, toolname = "pipe")
                case "conduit1":
                    dictreader = csvin("conduit")
                    results = []
                    for d in dictreader:
                        results.append(d)
                    print(results[0])
                    print(conduit.auto(driver, random=False, manual_inputs=results[0]))

                    #for _ in range(10):
                    #    results = conduit.auto(driver)
                    #    csvout(field_names=CONDUIT_FIELD_NAMES, dict = results, toolname = "conduit") 
                case "conduit2":
                    results = conduit.auto(driver)
                    print(results)
                case "duct":
                    dictreader = csvin("duct")
                    results = []
                    for d in dictreader:
                        results.append(d)
                    print(results[0])
                    print(duct.auto(driver, random=False, manual_inputs=results[0]))
                    #results = duct.auto(driver)
                    #print(results)
                    #csvout(DUCT_FIELD_NAMES, results, "duct")
            a = input("tool?: ")