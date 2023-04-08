import argparse
import os
import logging
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from src.pressureBrakePrediction.utils import read_yaml


STAGE = "split_data_&_pca" ## <<< change stage name 

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
    processed_data_dir = os.path.join(artifacts_dir, artifacts["PROCESSED_DATA_DIR"])
    input_features = os.path.join(processed_data_dir, artifacts["INPUT_FEATURE"])
    output_feature = os.path.join(processed_data_dir, artifacts["OUTPUT_FEATURE"]) 

    split = params["prepare"]["split"] # split ratio
    state = params["prepare"]["state"]
    seed = params["prepare"]["seed"]
    tag = params["prepare"]["tag"]

    random.seed(seed)

    X = pd.read_csv(input_features)
    Y = pd.read_csv(output_feature)

    
    X_train, X_val, y_train,y_val = train_test_split(X, Y, test_size=split, random_state=state)

    



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        print(">>>>> stage Prepare_data Started <<<<<")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed! <<<<<\n")
        print(">>>>> stage Prepare_data completed <<<<<")
    except Exception as e:
        logging.exception(e)
        raise 