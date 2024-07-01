import csv
from constants import *


ground_configurations = {
    'A': "(A) Busbar, Insulators and Brackets",
    'B': "(B) Busbar and Brackets",
    'C': "(C) Busbar Only",
    'D': "(D) Busbar and Insulators",
    'F': "(F) Busbar, Insulators, Brackets and Plexiglass Cover"
}

ground_bar_thicknesses = {
    '14': "14 - 1/4",
    '38': "38 - 3/8",
    '12': "12 - 1/2"
}

ground_hole_sizes = {
    'A': {
        'A': "7/16 in",
        'B': "5/8 in",
        'C': "9/16 in",
        'D': "3/8 in",
        'E': "5/16 in",
        'F': "1/4 in",
    },
    'B': {
        'A': "5/8 in",
        'B': "7/16 in",
        'C': "9/16 in",
        'D': "3/8 in",
        'E': "5/16 in",
        'F': "1/4 in",
        'G': "1/2 in",
    },
    'C': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "7/16 in",
        'D': "3/8 in",
        'E': "5/16 in",
        'F': "1/4 in",
        'G': "1/2 in",
    },
    'D': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "3/8 in",
        'D': "7/16 in",
        'E': "5/16 in",
        'F': "1/4 in",
        'G': "1/2 in",
    },
    'E': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "3/8 in",
        'D': "5/16 in",
        'E': "7/16 in",
        'F': "1/4 in",
        'G': "1/2 in",
    },
    'G': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "3/8 in",
        'D': "5/16 in",
        'E': "1/4 in",
        'F': "1/2 in",
        'G': "7/16 in",
    },
    'H': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "3/8 in",
        'D': "5/16 in",
        'E': "1/4 in",
        'F': "1/2 in",
        'H': "7/16 in",
    },
    'J': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "3/8 in",
        'D': "5/16 in",
        'E': "1/4 in",
        'F': "1/2 in",
        'G': "9/32 in",
        'J': "7/16 in",
    },
    'K': {
        'A': "3/8 in",
        'K': "7/16 in",
    },
    'L': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "3/8 in",
        'D': "5/16 in",
        'E': "1/4 in",
        'F': "1/2 in",
        'L': "7/16 in",
    },
    'M': {
        'M': "7/16 in",
    },
    'Q': {
        'A': "3/8 in",
        'Q': "7/16 in",
    },
    'R': {
        'A': "5/8 in",
        'B': "9/16 in",
        'C': "3/8 in",
        'D': "5/16 in",
        'E': "1/4 in",
        'F': "1/2 in",
        'R': "7/16 in",
    },
    'S': {
        'A': "3/8 in",
        'S': "7/16 in",
    },
    'N': {
        'N': "No Hole Pattern",
    }
}

ground_pigtail_codes = {
    '1G': "#6 Solid Copper Wire",
    '1T': "#2 Solid Copper Wire, Tinned",
    '1K': "#4 Solid Copper Wire, Tinned",
    '1V': "#2 Concentric Copper Cable, 7 Strand",
    '1L': "#4 Concentric Copper Cable, 7 Strand",
    '2C': "1/0 Concentric Copper Cable, 7 Strand",
    '2G': "2/0 Concentric Copper Cable, 7 Strand",
    '2L': "3/0 Concentric Copper Cable, 19 Strand",
    '2Q': "4/0 Concentric Copper Cable, 7 Strand",
    '2V': "250 KCM Concentric Copper Cable, 19 Strand",
    '3D': "350 KCM Concentric Copper Cable, 37 Strand",
    '3Q': "500 KCM Concentric Copper Cable, 37 Strand",
    '4L': "750 KCM Concentric Copper Cable, 61 Strand",
}

ground_pigtail_lengths = {
    'A': "1 ft",
    'B': "2 ft",
    'C': "3 ft",
    'D': "4 ft",
    'E': "5 ft",
    'F': "6 ft",
    'G': "7 ft",
    'H': "8 ft",
    'J': "9 ft",
    'K': "10 ft",
    'L': "12 ft",
    'M': "14 ft",
    'N': "16 ft",
    'P': "18 ft",
    'Q': "20 ft",
    'R': "22 ft",
    'S': "24 ft",
    'T': "26 ft",
    'U': "28 ft",
    'V': "30 ft",
    'W': "32 ft",
    'X': "34 ft",
    'Y': "36 ft",
    'Z': "38 ft",
}

telecom_configurations = {
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

def parse_ground(s):
    return_dict = {}

    return_dict["part number"] = s
    try:
        # filter out any non-EGB
        if s[0:3] != "EGB":
            return False
        s = s[3:]

        # get configuration, thickness and width from the string
        return_dict["configuration"] = ground_configurations[s[0]]
        return_dict["bar thickness"] = ground_bar_thicknesses[s[1:3]]
        return_dict["bar width"] = s[3]
        s = s[4:]

        # check if bar length is 2 or 3 digits and add it accordingly
        if s[2].isnumeric():
            return_dict["bar length"] = s[0:3]
            s = s[3:]
        else:
            return_dict["bar length"] = s[0:2]
            s = s[2:]
        # get hole pattern from the next character, then base hole size on said hole pattern       
        return_dict["hole pattern"] = s[0]
        return_dict["hole size"] = ground_hole_sizes[return_dict["hole pattern"]][s[1]]
        s = s[2:]

        # if the part number is over, then it is just copper, otherwise if theres a T, its tinned copper
        if s == "":
            return_dict["material"] = "Copper"
        elif s[0] == 'T':
            return_dict["material"] = "Tinned Copper"
            s = s[1:]
        
        # if string is empty, the part is done. Otherwise get the pigtail code from the remaining characters
        if len(s) > 0: 
            return_dict["pigtail code"] = ground_pigtail_codes[s[0:2]]
            return_dict["pigtail length"] = ground_pigtail_lengths[s[2]]
            s = s[3:]
            if len(s) > 0:
                return False
        else:
            return_dict["pigtail code"] = '-'
            return_dict["pigtail length"] = '-'
            
        return return_dict
    
    # if a value was not in any of the dictionaries, the part is invalid (at least to enter into the website)
    except KeyError:
        return False

def parse_telecom(s):
    return_dict = {}

    try:
        # set prefix and filter out parts that arent telecom
        return_dict["part number"] = s
        if s[0:3] == "TGB":
            return_dict["prefix"] = "TGB"
            s = s[3:]
        elif s[0:4] == "TMGB":
            return_dict["prefix"] = "TMGB"
            s = s[4:]
        else:
            return False

        # fill in next few values based on string if they are allowed
        return_dict["configuration"] = telecom_configurations[s[0]]
        if s[1:4] not in telecom_lengths:
            return False
        return_dict["length"] = s[1:4]
        if s[4:7] not in telecom_number_of_holes:
            return False
        return_dict["number of holes"] = s[4:7]
        s = s[7:]

        # if there is anything left in the string then it is indicating tinned copper or is incorrect
        if len(s) > 0:
            if s[0] == 'T':
                return_dict["material"] = "Tinned Copper"
            else:
                return False
        else:
            return_dict["material"] = "Copper"

        return return_dict
    
    # if something wasnt in a dictionary then its not on the website
    except KeyError:
        return False



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
    print(len(part_numbers))
    for num in part_numbers:
        parsed_num = parse(num)
        if parsed_num not in dict_list:
            dict_list.append(parsed_num)
        if dict_list[-1] == False:
            dict_list.pop(-1)
    print(dict_list)
    
    # write parsed parts to parsed number file
    csv_file = open(parsed_part_number_path, "w", newline='')
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(dict_list)
    csv_file.close()

run_parser(GROUND)