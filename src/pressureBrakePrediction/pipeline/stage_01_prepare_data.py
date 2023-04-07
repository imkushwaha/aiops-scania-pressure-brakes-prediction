import argparse
import os
import logging
import random
import zipfile
from src.pressureBrakePrediction.utils import read_yaml, create_directories, get_df


STAGE = "Prepare_data" ## <<< change stage name 

logging.basicConfig(filename=os.path.join("logs", 'running_logs.log'), 
                    level=logging.INFO, 
                    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
                    filemode="a")


def main(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    artifacts = config["artifacts"]

    artifacts_dir = artifacts["ARTIFACTS_DIR"]
    extracted_data_dir = os.path.join(artifacts_dir, artifacts["EXTRACTED_DATA_DIR"])
    processed_data_dir = os.path.join(artifacts_dir, artifacts["PROCESSED_DATA_DIR"])

    raw_data_dir = artifacts["RAW_DATA_DIR"]
    raw_data_file = artifacts["RAW_DATA"]
    raw_data_path = os.path.join(raw_data_dir, raw_data_file)

    split = params["prepare"]["split"] # split ratio
    seed = params["prepare"]["seed"]
    tag = params["prepare"]["tag"]

    random.seed(seed)

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
    train_data = get_df(path_to_data=train_data_path)
    
    def change_dtype(x):
        """This function is used to change data type of feature
           and to make NaN where it find "na".
        """
        if x == "na":
            return float('nan')
        else:
            return float(x)

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

    def target_label_encoding(y):

        """This functions helps to encode target feature into
        0 or 1 depending upon the label "neg" or "pos".

        args:
                y: target or output feature

        return:
                integer: 0 or 1 depending upon the "neg" or "pos"
        """
        if y == "neg":
            return 0
        else:
            return 1

    Y = Y.apply(target_label_encoding)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise 