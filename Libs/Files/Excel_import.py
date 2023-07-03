import matplotlib.pyplot as plt, pandas as pd, openpyxl, sys, os

class ExcelFile ():

    @staticmethod
    def extract_rows_from_sheet(sheet_name, excel_file) -> None:
        data_dict = {}
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