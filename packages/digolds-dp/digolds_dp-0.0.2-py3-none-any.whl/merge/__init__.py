from merge import csv_to_xlsx
from merge import multi_csv_to_single_csv
from merge import multi_csv_to_single_xlsx

sub_command_map = {
    'multi-csv2xlsx' : [multi_csv_to_single_xlsx.multiple_csv_to_single_xlsx, multi_csv_to_single_xlsx.parse],
    'csv2csv' : [multi_csv_to_single_csv.multiple_csv_to_single_csv, multi_csv_to_single_csv.parse],
    'csv2xlsx' : [csv_to_xlsx.csv_to_xlsx, csv_to_xlsx.parse]
}

def handle(args):
    sub_command = args[0]
    if sub_command in sub_command_map:
        command_set = sub_command_map[sub_command]
        handler = command_set[0]
        parser = command_set[1]
        ordered_args = parser(args[1])
        handler(*ordered_args)