import sys, os

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Graphing.plot import plot_performance
from Libs.Tools.Done import Done
from Libs.Files.Excel_import import ExcelFile

columns = ExcelFile().extract_colum_from_sheet('dataset_tests', r'C:\Users\Jon\Documents\UNI\Thesis\data\graphs.xlsx')

plot_performance([columns[0][1:], columns[0][1:]], [columns[1][1:], columns[2][1:]], ['Accuracy', 'Val_accuracy'], ['Accuracy', 'Epoch'], 'Dataset Performance')

plot_performance([columns[0][1:], columns[0][1:]], [columns[3][1:], columns[4][1:]], ['Accuracy', 'Val_accuracy'], ['Accuracy', 'Epoch'], 'Dataset Performance')

Done()
