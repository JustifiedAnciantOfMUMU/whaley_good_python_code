import matplotlib.pyplot as plt, pandas as pd, openpyxl, sys, os

sys.path.append(os.getcwd())
from Libs.Tools.Done import Done
from Config.import_config import ConfigDict

class ExcelFile ():

    @staticmethod
    def extract_rows_from_sheet(sheet_name, excel_file) -> None:
        data_dict = {}
        excel_file = pd.ExcelFile(excel_file)
        sheet = excel_file.parse(sheet_name)
        for index, row in sheet.iterrows():
            data_dict[index] = row.to_dict()
        return data_dict
    
    @staticmethod
    def extract_rows_from_file(filepath):
        excel_file = pd.ExcelFile(filepath)
        data_dict = {}
        for sheet_name in excel_file.sheet_names:
            sheet = excel_file.parse(sheet_name)
            for index, row in sheet.iterrows():
                data_dict[index] = row.to_dict()
        return data_dict
    
    @staticmethod
    def extract_colum_from_sheet(sheet_name, excel_file_path):
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        # Find columns with non-null entries
        non_empty_columns = df.columns[df.notna().any()]
        # Extract the non-empty columns into a list of arrays
        column_arrays = [df[column_name].tolist() for column_name in non_empty_columns]

        return column_arrays
    
if __name__ == '__main__':
    print(ExcelFile().extract_colum_from_sheet('dataset_tests', r'C:\Users\Jon\Documents\UNI\Thesis\data\graphs.xlsx'))
    Done()