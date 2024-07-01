from drivers import GroundBarDriver, TelecomBarDriver
from parsers import GroundParser, TelecomParser
from DriverController import DriverController
import csv
from constants import *

def read_csv_dict_list (file_path):
    csv_file = open(file_path, "r", newline='')
    reader = csv.DictReader(csv_file)
    dict_list = []
    for row in reader:
        dict_list.append(row)
    return dict_list

def read_csv_list (file_path):
    csv_file = open(file_path, "r", newline='')
    reader = csv.reader(csv_file)
    return_list = []
    for row in reader:
        return_list.append(row)
    return return_list

def remove_completed_tests():
    # get a list of the completed part numbers
    completed_part_numbers = []
    for row in completed_tests:
        completed_part_numbers.append(row[0])
    tests_to_remove = []

    # find all completed tests in tests list and add them to a remove list
    for test in tests:
        if test["part number"] in completed_part_numbers:
            completed_part_numbers.remove(test["part number"])
            tests_to_remove.append(test)

    # remove all completed tests from tests
    for test in tests_to_remove:
        tests.remove(test)

if __name__ == '__main__':

    number_of_threads = int(input("How many threads?: "))
    tool = input("Which tool to use?: ")

    if tool == GROUND:
        tests = read_csv_dict_list(PARSED_NUMBERS_FILE_PATH_GROUND)
        completed_tests = read_csv_list(COMPLETED_PARTS_FILE_PATH_GROUND)
        driver_type = GroundBarDriver
        parser = GroundParser()
    elif tool == TELECOM:
        tests = read_csv_dict_list(PARSED_NUMBERS_FILE_PATH_TELECOM)
        completed_tests = read_csv_list(COMPLETED_PARTS_FILE_PATH_TELECOM)
        driver_type = TelecomBarDriver
        parser = TelecomParser()
    
    parser.parse_all()
    parser.write_csv()
   
    remove_completed_tests()
    
    controller = DriverController(driver_type=driver_type, driver_count=number_of_threads, test_list=tests)
    controller.make_drivers(wait_time=1)

    controller.run_tests()
