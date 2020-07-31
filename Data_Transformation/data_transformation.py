import pandas as pd
import os
from Log_Writer.log import logWriter

class TransformData ():
    def __init__ (self, dirPath):
        self.dirPath = dirPath
        self.logWriter = logWriter
    
    def transform (self, datasetType='train'):
        try:
            dirPrefix = 'Training' if datasetType =='train' else 'Prediction'
            files = [file for file in os.listdir(self.dirPath)]

            for fileName in files:
                df = pd.read_csv(f'{self.dirPath}/{fileName}', parse_dates=['DATE'])
                
                df['Year'] = df['DATE'].dt.year
                df['Month'] = df['DATE'].dt.month
                df['Day'] = df['DATE'].dt.day
                df['DayOfMonth'] = df['DATE'].dt.dayofyear
                df['DayOfWeek'] = df['DATE'].dt.dayofweek
                df = df.drop('DATE', axis=1)

                df.to_csv(f'{self.dirPath}/{fileName}', index=None, header=True)
                with open(f'{dirPrefix}_Logs/data_transformation.txt', 'a+') as f:
                    self.logWriter(f, f'Data has been transformed successfuly')
                
        except Exception as e:
            with open(f'{dirPrefix}_Logs/data_transformation.txt', 'a+') as f:
                self.logWriter(f, f'Something went wrong while transforming data: {e}')
            raise e