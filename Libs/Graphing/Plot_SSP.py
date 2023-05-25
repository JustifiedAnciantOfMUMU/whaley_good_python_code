import matplotlib.pyplot as plt, pandas as pd, openpyxl

class _SoundSpeedProfileBase():
    @staticmethod
    def plot(x, y, title):
        plt.figure()
        plt.plot(x, y, label= 'Sound Speed Profile')
        plt.title(title), plt.xlabel('Speed of Sound (m/s)'), plt.ylabel('Depth (m)')

class SoundSpeedProfileExcel(_SoundSpeedProfileBase):
    def __init__(self, filepath) -> None:
        excel_file = pd.ExcelFile(filepath)
        column_data = {}
        for sheet_name in excel_file.sheet_names:
            sheet_data = excel_file.parse(sheet_name, usecols=[0, 1, 2])
            column_data[sheet_name] = { sheet_data.columns[0] : sheet_data.iloc[:, 0].values, sheet_data.columns[1]: sheet_data.iloc[:, 1].values, sheet_data.columns[2]: sheet_data.iloc[:, 2].values}

        for i in column_data.items():
            self.plot(i[1]['sound_speed'], i[1]['depth'],i[0])

if __name__ == '__main__':
    ssp = SoundSpeedProfileExcel(r'C:\Users\Jon\Documents\UNI\Thesis\SSP.xlsx')
    plt.show()
    print('done')
