import pandas as pd
from sklearn.preprocessing import StandardScaler
from Log_Writer.log import logWriter

class DataPreprocessing ():
    
    def __init__ (self):
        self.logWriter = logWriter
        
    # remove columns as discused in EDA section.
    def removeColumn (self, dataPath, listOfColumns):
        try:
            df = pd.read_csv(dataPath)
            df = df.drop(listOfColumns, axis=1)
            
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, 'Columns removed successfully')
            return df
            
        except Exception as e:
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'Somthing went wrong while removing columns :{e}')
            raise e
            
    def separateFeaturesFromTarget (self, data, targetName):
        try:
            X = data.drop(targetName, axis =1)
            y = data[targetName]
            
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, 'Independante variables and Dependant variable were separated Successfully')
            return X, y
        
        except Exception as e:
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'Somthing went wrong while separating features from target :{e}')
            raise e
        
   
    def featureScaling (self, data):
        try:
            X_scalled = StandardScaler().fit_transform(data)
            
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, 'Features were scalled successfully')
                
            return X_scalled
        except Exception as e:
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'Somthing went wrong while performing data scalling :{e}')
            raise e
    
    def preprocess (self, dataPath, listOfColumns, targetName=None):
        
        try:
            df = self.removeColumn(dataPath, listOfColumns)
            if targetName:
                X, y = self.separateFeaturesFromTarget(df, targetName)
                
                with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                        self.logWriter(file, 'Done. The data is ready to be passed to a model.')
                return X, y
            
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, 'Done. The data is ready to be passed to a model.')
            return df

        except Exception as e:
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'Somthing went wrong while preprocessing the data:{e}')
            raise e
            
            
            
            