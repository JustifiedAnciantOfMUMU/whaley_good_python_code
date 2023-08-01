import scipy.io, pandas as pd, time

def load_mat_file(file_path):
    data_dict = scipy.io.loadmat(file_path)
    return data_dict

def NOPP_mat_import(file_path):
    annots = scipy.io.loadmat(file_path)
    
    feild = [field for field in annots if not field.startswith('__')]
    con_list = [[element for element in upperElement] for upperElement in annots[feild[0]][0][0]]
    #x=con_list[10][0]
    _dict = {}
    duration_max=0

    for i in range(len(con_list[10][0])):
        start = time.strftime("%H:%M:%S", time.gmtime(con_list[10][0][i][6][0][0]))

        _dict[con_list[10][0][i][0][0][0]] = start
        duration_max = max(duration_max, con_list[10][0][i][8][0][0])

    return _dict, duration_max


if __name__ == '__main__':
    file_path = r"E:\Thesis\Datasets\NOPP_Gunshot_data\NOPP1_20080124_RW_gunshots.mat"
    data_dict = NOPP_mat_import(file_path)

print('done')