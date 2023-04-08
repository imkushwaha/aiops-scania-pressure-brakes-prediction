import argparse
import os
import logging
import random
import zipfile
import pandas as pd
from src.pressureBrakePrediction.utils import read_yaml, create_directories, change_dtype, target_label_encoding


STAGE = "Prepare_data" ## <<< change stage name 

logging.basicConfig(filename=os.path.join("logs", 'running_logs.log'), 
                    level=logging.INFO, 
                    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
                    filemode="a")


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    #params = read_yaml(params_path)
    
    artifacts = config["artifacts"]

    artifacts_dir = artifacts["ARTIFACTS_DIR"]
    extracted_data_dir = os.path.join(artifacts_dir, artifacts["EXTRACTED_DATA_DIR"])
    processed_data_dir = os.path.join(artifacts_dir, artifacts["PROCESSED_DATA_DIR"])

    raw_data_dir = artifacts["RAW_DATA_DIR"]
    raw_data_file = artifacts["RAW_DATA"]
    raw_data_path = os.path.join(raw_data_dir, raw_data_file)

    # split = params["prepare"]["split"] # split ratio
    # seed = params["prepare"]["seed"]
    # tag = params["prepare"]["tag"]

    # random.seed(seed)

    create_directories([artifacts_dir, extracted_data_dir, processed_data_dir])

    input_feature_path = os.path.join(processed_data_dir, artifacts["INPUT_FEATURE"])
    output_feature_path = os.path.join(processed_data_dir, artifacts["OUTPUT_FEATURE"])

    if os.path.exists(raw_data_path):
        with zipfile.ZipFile(raw_data_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_data_dir)
    else:
        logging.info("Raw data dir does not exists")

    train_data_path = os.path.join(extracted_data_dir, artifacts["TRAINING_DATA"])

    # Read train_data
    train_data = pd.read_csv(train_data_path)
    
    # Changing the data type of object column and replacing "na" with np.nan
    all_input_columns = list(train_data.columns)[1:]
    for input_col in all_input_columns:
        if train_data[input_col].dtype =='O':
            train_data[input_col] = train_data[input_col].apply(change_dtype)
        else:
            pass
    
    # Input Feature
    X = train_data.drop(columns=["class"], axis=0)

    # Output Label
    Y = train_data["class"]

    # Imputing missing values with medina values of respective attribute
    X = X.apply(lambda x: x.fillna(x.median()), axis=0)

    Y = Y.apply(target_label_encoding)
    
   # save processed input and output
    X.to_csv(input_feature_path, index=False)
    Y.to_csv(output_feature_path, index=False)
    logging.info("Processed input & output files saved successfully!!")


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    # args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        print(">>>>> stage Prepare_data Started <<<<<")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed! <<<<<\n")
        print(">>>>> stage Prepare_data completed <<<<<")
    except Exception as e:
        logging.exception(e)
        raise 