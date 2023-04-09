from pressure_brake_prediction.logger import logging
from pressure_brake_prediction.exception import CustomException
from pressure_brake_prediction.entity import DataTransformationConfig
from pressure_brake_prediction.utils import save_bin
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import RandomOverSampler



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_data_transformer_object(self):

        "This function is reponsible for data transformation."

        try:
        
            num_pipeline= Pipeline(
                    steps=[
                    ("imputer",SimpleImputer(strategy="mean")),
                    ("scaler",StandardScaler()),
                    ("pca", PCA(n_components=65, random_state=42))
                    ]
            )

            return num_pipeline
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_transformer(self):

        try:

            train_data = pd.read_csv(self.config.raw_train_data, na_values="na")
            test_data = pd.read_csv(self.config.raw_test_data, na_values = "na")

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            X_train_data = train_data.drop(columns=[self.config.target_column], axis=0)
            y_train_data = train_data[self.config.target_column]

            X_test_data = test_data.drop(columns=[self.config.target_column], axis=0)
            y_test_data = test_data[self.config.target_column]

            logging.info("Checking for data imbalance in Train data.")

            logging.info(str(y_train_data.value_counts()))

            # data is highly balance doing oversampling for getting a balanced data

            oversample_obj = RandomOverSampler(random_state=42)

            oversampled_X_train_data, oversampled_y_train_data = oversample_obj.fit_resample(X_train_data, y_train_data)

            # data is oversampled now check if it is balanced.
            logging.info(f"Data after transformation {oversampled_y_train_data.value_counts()}")

            # initiating the pipeline for data transformatoin
            logging.info(
                    f"Applying preprocessing object on training dataframe and testing dataframe."
                )

            processed_train_data = preprocessing_obj.fit_transform(oversampled_X_train_data)
            processed_test_data = preprocessing_obj.transform(X_test_data)


            train_arr = np.c_[
                    processed_train_data, np.array(oversampled_y_train_data)]
            test_arr = np.c_[
                    processed_test_data, np.array(y_test_data)]
            
            logging.info("Saved preprocessing object.")
            save_bin(

                    path=self.config.preprocessor_obj_file_path,
                    data=preprocessing_obj

                )
            
            save_bin(

                    path=self.config.train_data,
                    data=train_arr

                )
            save_bin(

                    path=self.config.test_data,
                    data=test_arr

                )

            return (train_arr,
                    test_arr,
                    self.config.preprocessor_obj_file_path)
        except Exception as e:
            raise CustomException(e,sys)
        