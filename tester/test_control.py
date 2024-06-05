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
                "material", "pipe count", "section length", "overall weight", "cross member width",
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

    a = input("Press enter to begin: ")

    if a == "debug":
        while a != "end":
            a = input("<debug> what would you like to run?: ")
            args = a.split()
            match args[0]:
                case "p":
                    match args[1]:
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
                case "c":
                    match args[1]:
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
                case "d":
                    match args[1]:
                        case "p1":
                            duct.page1(driver)
                        case "p2":
                            duct.page2(driver)
                        case "rp2":
                            duct.read_values_from_page2(driver)
                        case "p3":
                            duct.page3(driver)
                        case "p4":
                            duct.page4(driver)
    else:
        while (a != "end"):
            a = input("what would you like to run?: ")
            args = a.split()
            if len(args) != 3:
                continue
            args[2] = int(args[2])
            match args[0]:
                case "p":
                    match args[1]:
                        case "--direct" | "d":
                            dictreader = csvin("pipe")
                            results = []
                            for d in dictreader:
                                results.append(d)
                            print(pipe.auto(driver, random=False, manual_inputs=results[args[2]]))
                        case "--random" | "r":
                            for _ in range(args[2]):
                                results = pipe.auto(driver)
                                csvout(field_names=PIPE_FIELD_NAMES, dict = results, toolname = "pipe")
                case "c":
                    match args[1]:
                        case "--direct" | "d":
                            dictreader = csvin("conduit")
                            results = []
                            for d in dictreader:
                                results.append(d)
                            print(conduit.auto(driver, random=False, manual_inputs=results[args[2]]))
                        case "--random" | "r":
                            for _ in range(args[2]):
                                results = conduit.auto(driver)
                                csvout(field_names=CONDUIT_FIELD_NAMES, dict = results, toolname = "conduit")
                case "d":
                    match args[1]:
                        case "--direct" | "d":
                            dictreader = csvin("duct")
                            results = []
                            for d in dictreader:
                                results.append(d)
                            print(duct.auto(driver, random=False, manual_inputs=results[args[2]]))
                        case "--random" | "r":
                            for _ in range(args[2]):
                                results = duct.auto(driver)
                                csvout(field_names=DUCT_FIELD_NAMES, dict = results, toolname = "duct")