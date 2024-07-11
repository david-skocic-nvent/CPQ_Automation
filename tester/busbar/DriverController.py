from time import sleep
from constants import *

class DriverController():
    def __init__(self, driver_type, currency, test_list, driver_count=1):
        self.driver_type = driver_type
        self.driver_count = driver_count
        self.test_list = test_list
        self.currency = currency

        self.failed_tests = []
        self.drivers = []

    def make_drivers(self, wait_time=0):
        for _ in range(self.driver_count):
            self.drivers.append(self.driver_type(self.currency))
            sleep(wait_time)

    def run_tests(self):
        # loop through all test cases
        while len(self.test_list) > 0:
            if self.start_thread(self.test_list[0]):
                print (f"test started for:\n {self.test_list[0]}\n")
                self.test_list.pop(0)
            else:
                # wait a few seconds if there are no free drivers
                sleep(3)

    def start_thread(self, values):
        # this for loop gets a driver with a dead thread
        for driver in self.drivers:
            if not driver.is_active():
                break
        else:
            # if it doesnt find any inactive drivers, return False
            return False
        # start the inactive thread and return true
        driver.start_thread(values)
        return True