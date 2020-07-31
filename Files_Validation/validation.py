import os
import shutil
import re
import json
import pandas as pd
from Log_Writer.log import logWriter

class FileValidation ():
    
    def __init__(self):
        self.logWriter = logWriter
        self.schemaPath = 'raw_data_schema.json'
        self.trainGoodRawDataPath ='Data/Train/Good_Raw_Data'
        self.trainBadRawDataPath = 'Data/Train/Bad_Raw_Data'
        self.predictionGoodRawDataPath ='Data/Prediction/Good_Raw_Data'
        self.predictionBadRawDataPath = 'Data/Prediction/Bad_Raw_Data'
    
    def schemaValidation (self):
        
        try: 
            with open(self.schemaPath, 'r') as f:
                schema = json.load(f)
                self.lengthOfDateStampInFile = schema['LengthOfDateStampInFile']
                self.lengthOfTimeStampInFile = schema['LengthOfTimeStampInFile']
                self.columnsNumbers = schema['ColumnsNumbers']
                self.columnsNames = schema['ColumnsNames']
                message =  f'LengthOfDateStampInFile: {self.lengthOfDateStampInFile} "LengthOfTimeStampInFile: { self.lengthOfTimeStampInFile}  "ColumnsNumbers: {self.columnsNumbers}'
                with open('Training_Logs/schema_validation_log.txt', 'a+') as file:
                    self.logWriter(file, message)
            
        except Exception as e:
            with open('Training_Logs/schema_validation_log.txt', 'a+') as file:
                logWriter(file, str(e))   
            raise e
    
    # file name regex
    def fileNameRegex (self):
        return "['visibility']+['\_'']+[\d_]+[\d]+\.csv"
    
    # create folder          
    def createDirectory (self, dirPath, dirName):
        try:
            if not os.path.isdir(dirPath) :
                os.makedirs(dirPath)
                with open('Training_Logs/general_logs.txt', 'a+') as file:
                    self.logWriter(file, f'Folder {dirName} has been created.')
                
        except OSError as e:
            with open('Training_Logs/general_logs.txt', 'a+') as file:
                    self.logWriter(file, f'Something went wrong while creating foler {dirName}.')   
            raise e

#delete directory
    def deleteDirectory (self, dirPath, dirName):
        
        try:
            if os.path.isdir(dirPath):
                shutil.rmtree(dirPath)
                with open('Training_Logs/general_logs.txt', 'a+') as file:
                    self.logWriter(file, f'Folder {dirName} has been deleted successfully.')
            
        except OSError as e:
            with open('Training_Logs/general_logs.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while deleting foler {dirName}.')
            raise e
        
#Validate raw file name 
    def fileNameValidation (self, dirPath, datasetType='train'):
        
        goodRawDataPath = self.trainGoodRawDataPath if datasetType=='train' else self.predictionGoodRawDataPath
        badRawDataPath = self.trainBadRawDataPath if datasetType == 'train' else self.predictionBadRawDataPath
        self.deleteDirectory(goodRawDataPath, 'good raw data')
        self.deleteDirectory(badRawDataPath, 'bad raw data')
        
        try:
            self.createDirectory(goodRawDataPath, 'good raw data')
            self.createDirectory(badRawDataPath, 'bad raw data')
            fileNames = [file for file in os.listdir(dirPath) if file not in ['Bad_Raw_Data', 'Good_Raw_Data']]

            for fileName in fileNames:
                reg = self.fileNameRegex()
                isMatch = re.match(reg, fileName)
                nameWithoutExt = fileName.split('.csv')[0].split('_')
                isValidName = len(nameWithoutExt[1]) == self.lengthOfDateStampInFile and len(nameWithoutExt[2]) == self.lengthOfTimeStampInFile
               
                if isMatch and isValidName:
                    shutil.copy(f'{dirPath}/{fileName}', goodRawDataPath)
                    with open('Training_Logs/file_name_validation.txt', 'a+') as file:
                        self.logWriter(file, 'Correct file name provided')
                else:
                    shutil.copy(f'{dirPath}/{fileName}', badRawDataPath)
                    with open('Training_Logs/file_name_validation.txt', 'a+') as file:
                        self.logWriter(file, 'Invalid file name provided')
        
                    
                    
        except Exception as e:
            with open('Training_Logs/file_name_validation.txt', 'a+') as file:
                self.logWriter(file, f'Something wend wrong while validating file name: {e}')
            raise e
            
#Check if the number of column in csv file is equal to the one mentioned in json file.
    def columnsNumbersValidation (self, datasetType ='train'):
        try:
            goodRawDataPath = self.trainGoodRawDataPath if datasetType=='train' else self.predictionGoodRawDataPath
            badRawDataPath = self.trainBadRawDataPath if datasetType == 'train' else self.predictionBadRawDataPath
            fileNames = [file for file in os.listdir(goodRawDataPath)]
            
            for fileName in fileNames:
                df = pd.read_csv(f'{goodRawDataPath}/{fileName}')
                columnNumber = self.columnsNumbers if  datasetType == 'train' else self.columnsNumbers -1
                
                if len(df.columns) == columnNumber:
                    with open('Training_Logs/file_columnnumber_validation.txt', 'a+') as file:
                        self.logWriter(file, 'Column number verified')
                else:
                    shutil.move(f'{goodRawDataPath}/{fileName}', badRawDataPath)
                    with open('Training_Logs/file_columnnumber_validation.txt', 'a+') as file:
                        self.logWriter(file, 'The column number is invalid')
                   
        except Exception as e :
            with open('Training_Logs/file_columnnumber_validation.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while verifying the column number: {e}')
            raise e
           
    # Check if ther is any empty column in csv file from good raw data
    def emptyColumnValidation (self, datasetType ='train'):
        
        try:
            goodRawDataPath = self.trainGoodRawDataPath if datasetType=='train' else self.predictionGoodRawDataPath
            badRawDataPath = self.trainBadRawDataPath if datasetType == 'train' else self.predictionBadRawDataPath
            fileNames = [file for file in os.listdir(goodRawDataPath)]
            
            for fileName in fileNames:
                df = pd.read_csv(f'{goodRawDataPath}/{fileName}')
                
                for column in df:
                    if df[column].count() == 0:
                        shutil.move(f'{goodRawDataPath}/{fileName}', badRawDataPath)
                        with open('Training_Logs/file_column_validation.txt', 'a+') as file:
                            self.logWriter(file, f'There is empty column in file {fileName}')
                        break
                    
                with open('Training_Logs/file_column_validation.txt', 'a+') as file:
                    self.logWriter(file, 'File was verified succefully.')
                    
        except OSError as e:
            with open('Training_Logs/file_column_validation.txt', 'a+') as file: 
                self.logWriter(file, f'Something went wrong while validating the column: {e}')
            raise e
        except Exception as e:
            with open('Training_Logs/file_column_validation.txt', 'a+') as file: 
                self.logWriter(file, f'Something went wrong while validating the column: {e}')
            raise e
            
       

