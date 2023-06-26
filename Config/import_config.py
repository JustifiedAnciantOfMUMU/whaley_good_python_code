import json, os, sys

sys.path.append(os.getcwd())
from Libs.Tools.Create_config_file import create_config_file

class ConfigDict():
    config_filepath = os.getcwd() + r"/Config/config.json"

    def __init__(self) -> None:
        self.check_file_exists()
        self.import_config()
    
    def check_file_exists(self):
        # Check if the file exists
        if os.path.exists(self.config_filepath):
            pass
        else:
            create_config_file()
        
    def import_config(self):
        with open(self.config_filepath, 'r') as json_file:
            # Load the JSON data into a dictionary
            self.dict = json.load(json_file)

if __name__ == '__main__':
    _ConfigDict = ConfigDict()
    print(_ConfigDict.dict)