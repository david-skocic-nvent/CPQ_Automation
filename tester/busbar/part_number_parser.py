import csv
from constants import *


egb_configurations = {
    'A': "(A) Busbar, Insulators and Brackets",
    'B': "(B) Busbar and Brackets",
    'C': "(C) Busbar Only",
    'D': "(D) Busbar and Insulators",
    'F': "(F) Busbar, Insulators, Brackets and Plexiglass Cover"
}

bar_thicknesses = {
    '14': "14 - 1/4",
    '38': "38 - 3/8",
    '12': "12 - 1/2"
}

hole_sizes = {
    'G': "1/2 in",
    'F': "1/4 in",
    'C': "3/8 in",
    'D': "5/16 in",
    'A': "5/8 in",
    'E': "7/16 in",
    'B': "9/16 in",
}

telecom_configuration = {
    'A':"(A) Busbar, Insulators and Brackets",
    'C':"(C) Busbar Only",
    'F':"(F) Busbar, Insulators, Brackets and Plexiglass Cover"
}

telecom_lengths = [
    "06L",
    "12L",
    "16L",
    "18L",
    "20L",
    "24L",
    "29L"
]

telecom_number_of_holes = [
    "18P", 
    "41P",
    "02P",
    "06P",
    "08P",
    "10P",
    "12P",
    "14P",
    "15P",
    "19P",
    "23P",
    "27P",
    "33P"
]

other_count = 0

def parse_ground(s):
    global other_count
    configuration = None
    thickness = None
    width = None
    length = None
    hole_pattern = None
    hole_size = None
    material = None
    return_dict = {}

    return_dict["part number"] = s

    if s[0:3] != "EGB":
        #print("Bad part number")
        return False
    s = s[3:]
    temp_string = ""
    while (len(s)) > 0:
        temp_string += s[0]
        
        if configuration == None:
            configuration = egb_configurations[temp_string]
            temp_string = ""
            #print(configuration)
            return_dict["configuration"] = configuration
        elif thickness == None:
            if len(temp_string) == 2:
                thickness = temp_string
                temp_string = ""
                #print(thickness)
                return_dict["bar thickness"] = thickness
        elif width == None:
            width = temp_string
            temp_string = ""
            #print(width)
            return_dict["bar width"] = width
        elif length == None:
            if not s[1].isnumeric():
                length = temp_string
                temp_string = "" 
                #print(length)
                return_dict["bar length"] = length
        elif hole_pattern == None:
            hole_pattern = temp_string
            temp_string = ""
            return_dict["hole pattern"] = hole_pattern
            #print(hole_pattern)
        elif hole_size == None:
            if temp_string == hole_pattern:
                if hole_pattern != 'N':
                    hole_size = "7/16 in"
                else:
                    hole_size = "No Hole Pattern"
                return_dict["hole size"] = hole_size
            else:
                hole_size = "other"
                other_count += 1
                return_dict["hole size"] = hole_size
                #print(hole_size)
        else:
            break
        s = s[1:]
    if s == "":
        material = "Copper"
    elif s[0] == 'T':
        material = "Tinned Copper"
        s = s[1:]
    if len(s) > 0 : 
        #print("unable to process this part number")
        return False
    
    return_dict["material"] = material
    #print(material)

    return return_dict

def parse_telecom(s):
    global other_count
    prefix = None
    configuration = None
    length = None
    material = None
    number_of_holes = None
    return_dict = {}

    return_dict["part number"] = s

    temp_string = ""
    while (len(s)) > 0:
        temp_string += s[0]
        if prefix == None:
            if (len(temp_string) == 3 and temp_string == "TGB") or (len(temp_string) == 4):
                    prefix = temp_string
                    temp_string = ""
                    return_dict["prefix"] = prefix
        elif configuration == None:
            configuration = telecom_configuration[temp_string]
            temp_string = ""
            return_dict["configuration"] = configuration
        elif length == None:
            if len(temp_string) == 3:
                length = temp_string
                if length not in telecom_lengths:
                    return False
                temp_string = "" 
                return_dict["length"] = length
        elif number_of_holes == None:
            if len(temp_string) == 3:
                number_of_holes = temp_string
                if number_of_holes not in telecom_number_of_holes:
                    return False
                temp_string = ""
                return_dict["number of holes"] = number_of_holes
        else:
            break
        s = s[1:]
    if s == "":
        material = "Copper"
    elif s[0] == 'T':
        material = "Tinned Copper"
        s = s[1:]
    if len(s) > 0 : 
        return False
    
    return_dict["material"] = material

    print(return_dict)
    return return_dict


def run_parser (tool):
    if tool == "ground":
        raw_part_number_path = RAW_PART_NUMBERS_FILE_PATH_GROUND
        parsed_part_number_path = PARSED_NUMBERS_FILE_PATH_GROUND
        field_names = FIELD_NAMES_GROUND
        parse = parse_ground
    elif tool == "telecom":
        raw_part_number_path = RAW_PART_NUMBERS_FILE_PATH_TELECOM
        parsed_part_number_path = PARSED_NUMBERS_FILE_PATH_TELECOM
        field_names = FIELD_NAMES_TELECOM
        parse = parse_telecom

    f = open(raw_part_number_path, "r")
    part_numbers = f.read().split()
    f.close()

    dict_list = []

    # add parsed numbers to the parsed
    for num in part_numbers:
        parsed_num = parse(num)
        if parsed_num not in dict_list:
            dict_list.append(parsed_num)
        if dict_list[-1] == False:
            dict_list.pop(-1)
    print(len(dict_list))
    
    # write parsed parts to parsed number file
    csv_file = open(parsed_part_number_path, "w", newline='')
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(dict_list)
    csv_file.close()

run_parser(TELECOM)