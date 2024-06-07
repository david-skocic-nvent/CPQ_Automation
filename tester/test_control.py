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

VALID_TOOLS = ["p", "pipe", "d", "duct", "c", "conduit"]

# creates and returns a list of webdrivers and logs them into the CPQ website
# there are NUMBER_OF_THREADS drivers in the list so each thread can execute one driver
def make_drivers():
    drivers = []
    for i in range (NUMBER_OF_THREADS):
        drivers.append(webdriver.Edge())
        drivers[i].get(LINK)
        login(drivers[i], USERNAME, PASSWORD)
    return drivers

# finds and returns the number of tests each thread has to execute based on the total number of tests desired
# This is not simply division because with 35 tests and 3 threads you need 12, 12, and 11 tests for the respective threads
def get_thread_execution_counts(total_execution_count):
    thread_run_counts = []
    threads_left = NUMBER_OF_THREADS
    while threads_left > 0:
        thread_run_counts.append(math.ceil(total_execution_count / threads_left))
        threads_left -= 1
        total_execution_count -= thread_run_counts[-1]
    return thread_run_counts

# a basic cli that allows the user to debug and run the tool
# to get into debug mode, type debug when it says "Press enter to begin"
def run_cli():
    global drivers
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
            out = process_args(args)
            if out is not None:
                print(out)

'''
case "--direct" | "d":
dictreader = csvin("pipe")
results = []
for d in dictreader:
    results.append(d)'''   

def process_args(args: list):
    random_test = True
    execution_count = 1
    tool = args.pop(0)
    
    if tool not in VALID_TOOLS:
        return "Invalid tool entered"
    
    while len(args) > 0:
        arg = args.pop(0)
        if arg[0] == '-':
            match arg:
                case "-r" | "--random":
                    random_test = True
                case "-c":
                    if len(args) == 0:
                        return "Usage: -c <number_of_executions>"
                    count = args.pop(0)
                    if not (count.isnumeric()):
                        return "Usage: -c <number_of_executions>"
                    else:
                        execution_count = int(count)
                case "-d" | "--direct":
                    random_test = False
    
    match tool:
        case "p" | "pipe":
            run_tool(pipe.auto, random_test=random_test, execution_count=execution_count)
        case "d" | "duct":
            run_tool(duct.auto, random_test=random_test, execution_count=execution_count)
        case "c" | "conduit":
            run_tool(conduit.auto, random_test=random_test, execution_count=execution_count)
    
def run_tool (tool_target, random_test=True, execution_count=1, direct_inputs = {}):
    if random_test:
        execution_counts = get_thread_execution_counts(execution_count)
        threads = []
        for i in range(NUMBER_OF_THREADS):
            threads.append(threading.Thread(target=tool_target, args=(drivers[i], execution_counts[i]), name=f"thread {i+1}"))

        for i in range (NUMBER_OF_THREADS):
            threads[i].start()
        
        for i in range(NUMBER_OF_THREADS):
            threads[i].join()

if __name__ == '__main__':
    run_cli()