import csv
from pathlib import Path

def csvout(field_names, dict, toolname):
    dict_list = [dict]
    root_dir = Path(__file__).resolve().parent.parent
    csv_file = open(root_dir / "output" / csv_from_tool(toolname), "a" ,newline='')
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writerows(dict_list)
    csv_file.close()

def csv_from_tool(toolname):
    match toolname:
        case "pipe":
            return "pipe.csv"
        case "duct":
            return "duct.csv"
        case "conduit":
            return "conduit.csv"
    return toolname + ".csv"