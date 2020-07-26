from flask import Flask, request
from Training_Files_Validation.validation import  FileValidation
from Training_Data_Transformation.data_transformation import TransformData
from Put_Training_Data_To_Db.dbOperation import DB
from TrainingModels import TrainingModels
#from Training_Models.gridParams import GridPrarams

# a = FileValidation()
# a.schemaValidation()
# a.fileNameValidation('Training_Raw_Data')

# a.columnsNumbersValidation()
# a.emptyColumnValidation()
# a = TransformData()
# a.transform()

#a = DB()
#a.createTable('DataBase/Training_Db/training.db')
#a.putDataIntoTable('DataBase/Training_Db/training.db')
#a.fetchAllToCsv('DataBase/Training_Db/training.db')
# app = Flask(__name__)

# @app.route('/train', methods=['Post'])
# def modelTraining ():
#     print(request.json['filePath'])
training = TrainingModels()
training.run()
#     return 'ok'


# if __name__ == '__main__':
#     app.run()
    

    
    
    