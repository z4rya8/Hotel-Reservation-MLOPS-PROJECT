import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

#what is the purpose of this class and how does it fit into the overall project?
# The DataProcessor class is designed to handle data loading, preprocessing, and saving of processed data for a machine learning project. It fits into the overall project by ensuring that the data is clean, well-structured, and ready for model training and evaluation.
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    def preprocess(self, df):
        try:
            logger.info("starting preprocessing")

            logger.info("Droppign the columns which are not required")
            df.drop(columns= ['Unnamed: 0', 'Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

             
            logger.info("Appling label encoding") 

            label_encoders = LabelEncoder()

            mappings = {}

            for col in cat_cols:
                df[col] = label_encoders.fit_transform(df[col])
                #what happened above?
                #   The above code applies label encoding to each categorical column in the cat_cols list.
                #   It transforms the categorical values into numerical labels, which can be used in machine learning

                mappings[col] = {label:code for label, code in zip(label_encoders.classes_, label_encoders.transform(label_encoders.classes_))}
                # explain the above line of code? with its syntax too? 
            
            logger.info("Label mappings are :")
            for col, mapping in mappings.items():
                logger.info(f"Mapping for {col}: {mapping}")


            logger.info("SKEWNESS Handling")

            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness>skew_threshold].index:
                df[column] = np.log1p(df[column])
            
            return df

        except Exception as e:
            logger.error(f"error during preprocess step {e}")
            raise CustomException("Error while preprocess data",e)

    def balance_data(self, df):
        try:
            logger.info("handling imbalanced data")
            X = df.drop(columns='booking_status')
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            # Correct way to rebuild the DataFrame
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("Data balancing completed")
            return balanced_df

        except Exception as e:
            logger.error(f"error during balancing data step {e}")
            raise CustomException("Error while balancing data", e)


    def select_features(self,df):
        try:
            logger.info("starting our feature selection step")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

# what does above code do?
# The above code initializes a RandomForestClassifier model with a specified random state for reproducibility.
# It then fits the model to the feature set X and target variable y, training the model to learn the relationship between the features and the target.
# This trained model can then be used for making predictions or evaluating feature importance.  

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                        'feature': X.columns,
                        'importance': feature_importance
                            })


            top_features_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)

            num_featuers_to_select = self.config["data_processing"]["no_of_features"]

            top_10_features = top_features_importance_df["feature"].head(num_featuers_to_select).values
            
            logger.info(f"Top {num_featuers_to_select} features are : {top_10_features}")
            

            top_10_df = df[top_10_features.tolist() + ['booking_status']]


#what does above code do?
# The above code selects the top 10 most important features based on their importance scores from the feature_importance_df DataFrame.
# It then creates a new DataFrame top_10_df that includes only these top 10 features along with the target variable 'booking_status'.
# This new DataFrame can be used for further analysis or modeling, focusing on the most relevant features.

            logger.info("Feature selection completed")

            return top_10_df
        
        except Exception as e:
            logger.error(f"error during feature selection step {e}")
            raise CustomException("Error while selecting features",e)
        

    def save_data(self,df, file_path):
        try:
            logger.info("saving our data in processed folder")

            df.to_csv(file_path,   index = False)

            logger.info(f"data saved successfully to {file_path}") 

        except Exception as e:
             logger.error(f"Error during save data {e }")
             raise CustomException("error while saving data ", e)


    def process(self):
        try: 
            logger.info("Loading data from raw directory ")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            train_df = self.preprocess(train_df)
            test_df = self.preprocess(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error during preprocessing pipelines {e }")
            raise CustomException("error while saving data ",e)


if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()

   

