import csv

FIELD_NAMES = ["part number", "configuration", "bar thickness", "bar width", "bar length", "hole pattern", "hole size", "material"]

configurations = {
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

other_count = 0

def parse(s):
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
            configuration = configurations[temp_string]
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


f = open("C:\\Users\\E2023355\\OneDrive - nVent Management Company\\Documents\\VSCode\\Projects\\CPQ\\CPQ_Automation\\tester\\busbar\\part_numbers_from_sheet.txt", "r")

part_numbers = f.read().split()

f.close()

dict_list = []

for num in part_numbers:
    dict_list.append(parse(num))
    if dict_list[-1] == False:
        dict_list.pop(-1)
print(dict_list)

csv_file = open("C:\\Users\\E2023355\\OneDrive - nVent Management Company\\Documents\\VSCode\\Projects\\CPQ\\CPQ_Automation\\tester\\busbar\\parsed_numbers.csv", "w", newline='')

writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
writer.writeheader()
writer.writerows(dict_list)
csv_file.close()