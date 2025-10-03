import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data
from scipy.stats import randint


import mlflow
import mlflow.sklearn



logger = get_logger(__name__)

class ModelTraining:

    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info("Loading testing data {self.train_path}")
            train_df = load_data(self.train_path)
            
            logger.info("Loading testing data {self.test_path}")
            test_df = load_data(self.test_path)
 

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Successfully loaded and split the data")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error("Error in load_and_split_data", e)
            raise CustomException("Failed to load data", e)
        
    def train_lgbm(self,X_train,y_train):
        try:
            logger.info("initiating training using LightGBM")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("starting RandomizedSearchCV for hyperparameter tuning")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                scoring=self.random_search_params["scoring"],
                cv=self.random_search_params["cv"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                n_jobs=self.random_search_params["n_jobs"]
            )

            logger.info("starting our hyperparameter tuning ")
            random_search.fit(X_train, y_train)

            logger.info("hyperparameter tuning completed")

            best_model = random_search.best_estimator_
            logger.info("Completed RandomizedSearchCV and obtained the best model")


            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"best parameters are : {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            logger.error("Error in train_lightgbm", e)
            raise CustomException("Failed to train LightGBM model", e)
        
    def evaluate_model(self,model,X_test, y_test):
        try:
            logger.info("Evaluating our model")

            y_pred = model.predict(X_test)


            accuracy = accuracy_score(y_test, y_pred)

            precision = precision_score(y_test, y_pred)

            recall = recall_score(y_test, y_pred)

            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy score = {accuracy}")
            logger.info(f"Precision score = {precision}")
            logger.info(f"Recall score = {recall}")
            logger.info(f"F1 score = {f1}")

            return {
                "accuracy" : accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1" : f1 
            }

        except Exception as e:
            logger.error("Error while evaluating the model", e)
            raise CustomException("Failed to evaluate LightGBM model", e)
    
    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)

            logger.info("saving the model")
            joblib.dump(model, self.model_output_path)

            logger.info(f"model saved to {self.model_output_path}")

        except Exception as e:
            logger.error("Error while saving the model", e)
            raise CustomException("Failed to save the LightGBM model", e)
    
    def run(self):
        try:
            with mlflow.start_run():

                logger.info("starting our model training pipeline")

                logger.info("starting our mlflow experimentation ")

                logger.info("logging the training and testing datset to mlflow")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")

                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train,y_train,X_test,y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train,y_train)
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)    
                self.save_model(best_lgbm_model)

                logger.info("Logging the model into MLFLOW")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging Params and metrics to MLFLOW")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model Training sucesfullly completed")

        except Exception as e:
            logger.error("Error while model training pipeline", e)
            raise CustomException("Failed during training of LightGBM model", e)
        

if __name__=="__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_OUTPUT_PATH)
    trainer.run()

