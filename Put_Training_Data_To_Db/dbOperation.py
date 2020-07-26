import json
import sqlite3
import csv
import shutil
import os
from Log_Writer.log import logWriter
#'DataBase/Training_Db/training.db'

class DB ():
    def __init__(self):
        self.logWriter = logWriter
        self.schemaPath = "table_schema.json"
        self.goodRawData = 'Training_Raw_Data_Separated/good_raw_data'
        self.badRawData = 'Training_Raw_Data_Separated/good_raw_data'
        self.fileFromDb = 'Training_Set_From_Db'
        self.trainingSet = 'training_set.csv'
        
    def dbConnection (self, dbName):
        try:
            connect = sqlite3.connect(dbName)
            with open('Db_Logs/training_db.txt', 'a+') as file:
                self.logWriter(file, '{dbName} was connected successfully')

        except ConnectionError as e:
            with open('Db_Logs/training_db.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while connecting {dbName} : e')
            raise e
        return connect
   
    def createTable(self, dbName):
        
        try:
            conn = self.dbConnection('DataBase/Training_Db/training.db')
            c = conn.cursor()
            with open(self.schemaPath, 'r') as f:
                schema = json.load(f)
                
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] == 1:
                conn.close()
                with open('Db_Logs/training_db.txt', 'a+') as file:
                    self.logWriter(file, 'Table already exist. db is closed ('')')
            else:
                for column_name, dtype in schema.items():
                    
                    try:
                        # if table is created then add the reste of columns.
                        conn.execute(f'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dtype}')
                    except:
                        #create the table with only one column.
                        conn.execute(f'CREATE TABLE  Good_Raw_Data ({column_name} {dtype})')
                    with open('Db_Logs/training_db.txt', 'a+') as file:
                         self.logWriter(file, 'Table already exist. db is closed')
            conn.close()          
        except Exception as e:
            with open('Db_Logs/training_db.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while creating table.')
            conn.close()
            raise e
    
    def putDataIntoTable (self, bdName):
        try:
            conn = self.dbConnection(bdName)
            files =[file for file in os.listdir(self.goodRawData)]
            
            for file in files:
                
                with open(f'{self.goodRawData}/{file}', 'r') as f:
                    next(f)
                    csvFile = csv.reader(f, delimiter="\n")
                    
                    for row in csvFile:
                        try:
                            conn.execute(f'INSERT INTO Good_Raw_Data values ({row[0]})')
                            conn.commit()
                            
                            with open('Db_Logs/training_db.txt', 'a+') as file:
                                 self.logWriter(file, f'Data was inserted to Good_Raw_Data table successfully.')

                        except Exception as e:
                             with open('Db_Logs/training_db.txt', 'a+') as file:
                                 self.logWriter(file, f'Something went wrong while inserting data to the table.')
                             conn.close()
                             raise e
            conn.close()        
            with open('Db_Logs/training_db.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong ')
                
        except Exception as e:
            conn.rollback()
            with open('Db_Logs/training_db.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while inserting data to the table.')
            conn.close()
            raise e
            
    def fetchAllToCsv (self, dbName):
        
        try:
            conn = self.dbConnection(dbName)
            c= conn.cursor()
            query = 'SELECT * FROM Good_Raw_Data'
            c.execute(query)
            results = c.fetchall()
            
            headers = [(i[0]).lower() for i in c.description]
            
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)
            
        # Open CSV file for writing.
            csvFile = csv.writer(open(f'{self.fileFromDb}/{self.trainingSet}', 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

        # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)
            
            with open('Db_Logs/training_db.txt', 'a+') as file:
                self.logWriter(file, f'Traingset file exported successfully.')
                
            conn.close()
            
        
        except Exception as e:

            with open('Db_Logs/training_db.txt', 'a+') as file:
                 self.logWriter(file, f'Something went wrong while fecthing data from db to csv file: {e}.')
            conn.close()
            raise e
            
            
            
            
            
            
            
            