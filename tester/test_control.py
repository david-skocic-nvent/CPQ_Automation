from selenium import webdriver
from fileout import *
from tester_functions import login
import rooftop.pipe as pipe
import rooftop.conduit as conduit
import rooftop.duct as duct
import threading
import math
from dotenv import load_dotenv
import os
load_dotenv()
USERNAME = os.getenv("CPQ_USERNAME")
PASSWORD = os.getenv("CPQ_PASSWORD")

NUMBER_OF_THREADS = 1

LINK = "http://10.4.75.133:8020/Apps/Rooftop_1_MNL/"

def make_drivers():
    drivers = []
    for i in range (NUMBER_OF_THREADS):
        drivers.append(webdriver.Edge())
        drivers[i].get(LINK)
        login(drivers[i], USERNAME, PASSWORD)
    return drivers

def get_thread_execution_counts(total_execution_count):
    thread_run_counts = []
    threads_left = NUMBER_OF_THREADS
    while threads_left > 0:
        thread_run_counts.append(math.ceil(total_execution_count / threads_left))
        threads_left -= 1
        total_execution_count -= thread_run_counts[-1]
    return thread_run_counts

if __name__ == '__main__':
    a = input("Press enter to begin: ")

    if a == "debug":
        driver = webdriver.Edge()
        driver.get(LINK)
        login(driver, USERNAME, PASSWORD)
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
        drivers = make_drivers()
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
                            #print(pipe.auto(driver, random=False, manual_inputs=results[args[2]]))
                        case "--random" | "r":
                            execution_counts = get_thread_execution_counts(args[2])
                            threads = []
                            for i in range(NUMBER_OF_THREADS):
                                threads.append(threading.Thread(target=pipe.auto, args=(drivers[i], execution_counts[i]), name=f"thread {i+1}"))

                            for i in range (NUMBER_OF_THREADS):
                                threads[i].start()
                            
                            for i in range(NUMBER_OF_THREADS):
                                threads[i].join()
                case "c":
                    match args[1]:
                        case "--direct" | "d":
                            dictreader = csvin("conduit")
                            results = []
                            for d in dictreader:
                                results.append(d)
                            #print(conduit.auto(driver, random=False, manual_inputs=results[args[2]]))
                        case "--random" | "r":
                            execution_counts = get_thread_execution_counts(args[2])
                            threads = []
                            for i in range(NUMBER_OF_THREADS):
                                threads.append(threading.Thread(target=conduit.auto, args=(drivers[i], execution_counts[i]), name=f"thread {i+1}"))

                            for i in range (NUMBER_OF_THREADS):
                                threads[i].start()
                            
                            for i in range(NUMBER_OF_THREADS):
                                threads[i].join()
                case "d":
                    match args[1]:
                        case "--direct" | "d":
                            dictreader = csvin("duct")
                            results = []
                            for d in dictreader:
                                results.append(d)
                            print(duct.auto(random=False, manual_inputs=results[args[2]]))
                        case "--random" | "r":
                            execution_counts = get_thread_execution_counts(args[2])
                            threads = []
                            for i in range(NUMBER_OF_THREADS):
                                threads.append(threading.Thread(target=duct.auto, args=(drivers[i], execution_counts[i]), name=f"thread {i+1}"))

                            for i in range (NUMBER_OF_THREADS):
                                threads[i].start()
                            
                            for i in range(NUMBER_OF_THREADS):
                                threads[i].join()