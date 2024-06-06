import csv
from pathlib import Path

def csvout(field_names, dict_to_write, toolname='', file_path=""):
    root_dir = Path(__file__).resolve().parent.parent
    if file_path == "":
        csv_file = open(root_dir / "output" / csv_from_tool(toolname), "a" ,newline='')
    else:
        csv_file = open(file_path, "a", newline = '')
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writerow(dict_to_write)
    csv_file.close()

def csvin(toolname, file_path=""):
    root_dir = Path(__file__).resolve().parent.parent
    if file_path == "":
        csv_file = open(root_dir / "output" / csv_from_tool(toolname), "r" ,newline='')
    else:
        csv_file = open(file_path, "r")
    reader = csv.DictReader(csv_file)
    return reader

def csv_from_tool(toolname):
    return toolname + ".csv"