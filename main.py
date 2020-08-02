import os
from flask import Flask, request, Response
#from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from Files_Validation.validation import  FileValidation
from Data_Transformation.data_transformation import TransformData
from Put_Data_To_Db.dbOperation import DB
from TrainingModels import TrainingModels
from Prediction import Predict
#from Training_Models.gridParams import GridPrarams

app = Flask(__name__)
#dashboard.bind(app)
#CORS(app)


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['csv'])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/train", methods=['POST'])
#@cross_origin()
def trainRouteClient():

    try:
        # upload training data file or files.
          UPLOAD_DIRECTORY = 'Data/Train'
          app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY
          
          if not os.path.exists(UPLOAD_DIRECTORY):
              os.makedirs(UPLOAD_DIRECTORY)
        
          if request.method == 'POST':
        # check if the post request has the files part
              if 'files[]' not in request.files:
                  return Response('No file found')
              files = request.files.getlist('files[]')

              for file in files:
                  if file and allowed_file(file.filename):
                      filename = secure_filename(file.filename)
                      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         
          # Validate training data files
          fileValidation = FileValidation()
          fileValidation.schemaValidation()
          fileValidation.fileNameValidation('Data/Train')
          fileValidation.columnsNumbersValidation()
          fileValidation.emptyColumnValidation()
         
        # transform Date column in each training file
          transformDateTime = TransformData('Data/Train/Good_Raw_Data')
          transformDateTime.transform()
        
        # Perform database operation (save all data in sqlite db and then fecth all into a single csv file)
          db = DB()
          #create db
          db.createTable('DataBase/Training_Db/training.db')
          #put data into db
          db.putDataIntoTable('DataBase/Training_Db/training.db')
          #fetch data and save it into csv
          db.fetchAllToCsv('DataBase/Training_Db/training.db')
         
         #Model training
          trainModel = TrainingModels()
         # run training
          trainModel.run()


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    
    return Response("Models training has been completed successfully!")



@app.route("/prediction", methods=['POST'])
#@cross_origin()
def predictRouteClient():

    try:
          UPLOAD_DIRECTORY = 'Data/Prediction'
          app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY
          
          if not os.path.exists(UPLOAD_DIRECTORY):
              os.makedirs(UPLOAD_DIRECTORY)
        # upload training data file or files.
          if request.method == 'POST':
        # check if the post request has the files part
              if 'files[]' not in request.files:
                  return Response('No file found')
              files = request.files.getlist('files[]')

              for file in files:
                  if file and allowed_file(file.filename):
                      filename = secure_filename(file.filename)
                      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         
          # Validate training data files
          fileValidation = FileValidation()
          fileValidation.schemaValidation()
          fileValidation.fileNameValidation('Data/Prediction', 'prediction')
          fileValidation.columnsNumbersValidation('prediction')
          fileValidation.emptyColumnValidation('prediction')
         
        # transform Date column in each training file
          transformDateTime = TransformData('Data/Prediction/Good_Raw_Data')
          transformDateTime.transform('prediction')
        
        # Perform database operation (save all data in sqlite db and then fecth all into a single csv file)
          db = DB()
          #create db
          db.createTable('DataBase/Prediction_Db/prediction.db', 'prediction')
          #put data into db
          db.putDataIntoTable('DataBase/Prediction_Db/prediction.db', 'prediction')
          #fetch data and save it into csv
          db.fetchAllToCsv('DataBase/Prediction_Db/prediction.db', 'prediction')
         
          # Perform prediction
          predict = Predict()
          # run training
          predict.run()


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    
    return Response("Prediction has been completed successfully!")

    

  
if __name__ == '__main__':
 app.run(debug=True)
    
    