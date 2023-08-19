import json, os

def create_config_file():
    file_path = "/Config/config.json"

    # Define the configuration data
    config_data = {
        "dataset_from_kiresbom": r"E:/Thesis/Datasets/Kiresbom_dataset",
        "dataset_from_kiresbom_cropped_snr": r"E:/Thesis/Datasets/Kiresbom_dataset_cropped",  
        "kirsebom_data": r"E:/Thesis/Datasets/Kiresbom_data/data", # https://www.frdr-dfdr.ca/repo/dataset/4a3113e6-1d58-6bb4-aaf2-a9adf75165be
        "resnet50_features_from_kiresbom": r"E:/Thesis/Datasets/Kiresbom_resnet50_features",
        "NOPP_Gunshot_data": r"E:/Thesis/Datasets/NOPP_Gunshot_data",
        "Gunshot_dataset": r"E:/Thesis/Datasets/Gunshot_dataset"
        
    }

    # Write the configuration data to the file
    with open(os.getcwd() + file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)


if __name__ == '__main__':
    print("Current Dir: " + os.getcwd()) 
    # Call the function to create the config file
    create_config_file()