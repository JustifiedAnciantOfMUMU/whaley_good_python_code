import matplotlib.pyplot as plt, pandas as pd, openpyxl

def ExtractRows(filepath):
    excel_file = pd.ExcelFile(filepath)
    data_dict = {}
    for sheet_name in excel_file.sheet_names:
        sheet = excel_file.parse(sheet_name)
        for index, row in sheet.iterrows():
            data_dict[index] = row.to_dict()
    return data_dict



if __name__ == '__main__':
    annotations = ExtractRows(r'C:\Users\Jon\Documents\UNI\Thesis\annotations.xlsx')
    bouy_id     = ExtractRows(r'C:\Users\Jon\Documents\UNI\Thesis\buoydata.xlsx')
    print('done :)')