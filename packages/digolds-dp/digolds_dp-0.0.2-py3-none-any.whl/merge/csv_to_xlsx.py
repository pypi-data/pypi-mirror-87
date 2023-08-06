from pandas.io.excel import ExcelWriter
import pandas

def parse(args):
    csv_file = args.get('--csv-file', 'data.csv')
    xlsx_file = args.get('--xlsx-file', 'data.xlsx')
    sheet_name = args.get('--sheet-name', 'daily')
    return (csv_file, xlsx_file, sheet_name)

def csv_to_xlsx(csv_file, xlsx_file, sheet_name):
    with ExcelWriter(xlsx_file) as ew:
        pandas.read_csv(csv_file).to_excel(ew, sheet_name=sheet_name, index=False)
        return xlsx_file

if __name__ == "__main__":
    csv_file = './tests/final_result.csv'
    xlsx_file = './tests/final_result.xlsx'
    sheet_name = 'daily'
    csv_to_xlsx(csv_file, xlsx_file, sheet_name)

# https://stackoverflow.com/questions/39099008/how-to-write-csv-files-into-xlsx-using-python-pandas
# https://www.codegrepper.com/code-examples/r/pandas+to+excel+no+index