from merge import csv_to_xlsx
from merge import multi_csv_to_single_csv
import os

def parse(args):
    src_path = args.get('--src-path', '.')
    xlsx_file = args.get('--xlsx-file', 'data.xlsx')
    sheet_name = args.get('--sheet-name', 'daily')
    return (src_path, xlsx_file, sheet_name)

def multiple_csv_to_single_xlsx(src_path, xlsx_file, sheet_name):
    dest_path = '.'
    output_name = 'digolds-dp.csv'
    csv_file = multi_csv_to_single_csv.multiple_csv_to_single_csv(src_path, dest_path, output_name)
    output = csv_to_xlsx.csv_to_xlsx(csv_file, xlsx_file, sheet_name)
    file_name = os.path.join(dest_path,output_name)
    if os.path.exists(file_name):
        os.remove(file_name)
    return output

if __name__ == "__main__":
    pass