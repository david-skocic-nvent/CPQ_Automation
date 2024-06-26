from pathlib import Path
import os

# Get the path of the current file
BUSBAR_FOLDER_PATH = Path(os.path.abspath(__file__)).parent

PARSED_NUMBERS_FILE_PATH_GROUND = BUSBAR_FOLDER_PATH / "data\\parsed_numbers_ground.csv"
PARSED_NUMBERS_FILE_PATH_TELECOM = BUSBAR_FOLDER_PATH / "data\\parsed_numbers_telecom.csv"
COMPLETED_PARTS_FILE_PATH_GROUND = BUSBAR_FOLDER_PATH / "data\\part_prices_ground.csv"
COMPLETED_PARTS_FILE_PATH_TELECOM = BUSBAR_FOLDER_PATH / "data\\part_prices_telecom.csv"
RAW_PART_NUMBERS_FILE_PATH_GROUND = BUSBAR_FOLDER_PATH / "data\\raw_part_numbers_ground.txt"
RAW_PART_NUMBERS_FILE_PATH_TELECOM = BUSBAR_FOLDER_PATH / "data\\raw_part_numbers_telecom.txt"

TELECOM = "telecom"
GROUND = "ground"

FIELD_NAMES_GROUND = ["part number", "configuration", "bar thickness", "bar width", "bar length", "hole pattern", "hole size", "material", "pigtail code", "pigtail length"]
FIELD_NAMES_TELECOM = ["part number", "prefix", "configuration", "length", "number of holes", "material"]

LINK = "https://nventefs-admin.tactoncpq.com/!tickets%7ET-00000938/solution/list"
