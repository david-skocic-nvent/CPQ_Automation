import csv
from pathlib import Path

def output_results_to_csv(field_names, dict):
    dict_list = [dict]
    root_dir = Path(__file__).resolve().parent.parent
    csv_file = open(root_dir / "testing_outputs" / "website_test_values.csv", "a" ,newline='')
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writerows(dict_list)
    csv_file.close()
