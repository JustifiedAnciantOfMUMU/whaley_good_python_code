import matplotlib.pyplot as plt, pandas as pd, openpyxl, sys, os

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict

def ExtractRows(filepath):
    excel_file = pd.ExcelFile(filepath)
    data_dict = {}
    for sheet_name in excel_file.sheet_names:
        sheet = excel_file.parse(sheet_name)
        for index, row in sheet.iterrows():
            data_dict[index] = row.to_dict()
    return data_dict

class KirsebomDatabase():
    def __init__(self, path) -> None:
        pass

if __name__ == '__main__':
    ## Kirsebom
    pass