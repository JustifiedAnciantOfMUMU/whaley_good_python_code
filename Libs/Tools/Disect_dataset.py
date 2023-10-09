import os, sys, random


def copy_file(source_path, destination_path, label):
    path = destination_path[:45] + label
    if not os.path.exists(path):
        # Create the directory
        os.makedirs(path)
    try:
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as destination_file:
                destination_file.write(source_file.read())
        print(f"File copied from {source_path} to {destination_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def split_folder(_in, _out, lable):
    files = os.listdir(_in)
    i=0
    while i < (len(files)*split):
        random_index = random.randint(0, len(files) - 1)
        random_file = files.pop(random_index)
        copy_file(_in + '/' + random_file, _out + r'/val' + lable + '/' + random_file, lable)
        i+=1
    
    for file in files:
        copy_file(_in + '/' + file, _out + r'/train'+ lable + '/' + file, 'n' + lable)

if __name__ == '__main__':
    split = 0.1
    out = r'E:\Thesis\Datasets\051023_DCLDE2024\D2\gs'
    print(out + r'\train' + r'\call\\')
    #split_folder(out + r'/call', out, r'\call') #call
    split_folder(out + r'/nocall', out, r'\nocall') #call
