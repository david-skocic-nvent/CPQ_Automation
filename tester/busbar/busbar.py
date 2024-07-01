import threading
import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from tester_functions import *
from dotenv import load_dotenv
import time
import os
from typing import List
from constants import *
load_dotenv()
USERNAME = os.getenv("TACTON_USERNAME")
PASSWORD = os.getenv("TACTON_PASSWORD")

drivers: List[webdriver.Edge] = []
threads: List[threading.Thread] = []
drivers_in_use = []
NUMBER_OF_THREADS = 1

def main(tool):
    global drivers

    make_drivers()

    # get to part number logic part of the program
    for i in range(NUMBER_OF_THREADS):
        threads.append(threading.Thread(target=click_to_part_number_logic, args = (drivers[i],)))
        threads[-1].start()
        print(threads[-1].is_alive())

    # wait for threads to finish
    for i in range(NUMBER_OF_THREADS):
        threads[i].join()

    # loop through the remaining tests, removing one every time 
    while len(tests) > 0:
        for i, thread in enumerate(threads):
            if not thread.is_alive():
                threads[i] = threading.Thread(target=run_test, args=(drivers[i],tests[0]))
                threads[i].start()
                print (f"Started running test for {tests[0]["part number"]}")
                i = i + 1
                tests.pop(0)
        time.sleep(2)

    time.sleep(5)

main(TELECOM)