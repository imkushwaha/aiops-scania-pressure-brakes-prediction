import os 
from pathlib import Path
import zipfile
import shutil
from tqdm import tqdm
from pressure_brake_prediction.entity import DataIngestionConfig
from pressure_brake_prediction import logger

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def copy_data_to_project_and_extract(self):
        if not os.path.exists(self.config.local_data_file):
            shutil.copy(self.config.source_data_file, self.config.local_data_file)


        if not os.path.exists(self.config.unzip_dir):
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(self.config.unzip_dir)


