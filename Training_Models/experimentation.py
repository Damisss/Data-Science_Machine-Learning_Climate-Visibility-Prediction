from Training_Models.grid_params  import GridParams
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Log_Writer.log import logWriter

#neg_mean_squared_error

class FindBestModels (GridParams):
    
    def __init__ (self):
        super().__init__()
        self.logWriter = logWriter
        self.models  = {
                        'Svc': make_pipeline(StandardScaler(), SVR()),
                        'Kneighbors':  make_pipeline(StandardScaler(), KNeighborsRegressor()),
                        'RandomForest': make_pipeline(StandardScaler(), RandomForestRegressor(random_state=42)),
                        'ExtraTrees': make_pipeline(StandardScaler(), ExtraTreesRegressor(random_state=42)),
                        #'AdaBoost': make_pipeline(StandardScaler(),AdaBoostRegressor(random_state=42)),
                        'GradientBoosting': make_pipeline(StandardScaler(), GradientBoostingRegressor(random_state=42)),
                        'Xgboost':make_pipeline(StandardScaler(), XGBRegressor(random_state=42))
                         }
    
    def experimentations (self, X, y, cv, scoring):
        try:
            results ={}
            for name, model in self.models.items():
               # perform  both feature and target scalling
               wrapped_model = TransformedTargetRegressor(regressor=model, transformer=StandardScaler())
               mse = cross_val_score(wrapped_model, X, y, cv=cv, scoring=scoring)
               results[name] = np.sqrt(-np.mean(mse))
               
            promisingModelName = list(filter(lambda x : results[x] == min(results.values()), results))[0]
             
            with open('Training_Logs/find_best_model_logs.txt', 'a+') as file:
                self.logWriter(file, f'Experimentation has been completed successfully. Model selected is {promisingModelName}')
        
            
            return {promisingModelName: self.models[promisingModelName]}
            
        except Exception as e:
            with open('Training_Logs/find_best_model_logs.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while taining: {e}')
            raise e
    
    def hyperparametersTuning (self, modelObject, X, y, cv):
        try:
            name, model = [(name, model) for name, model in modelObject.items()][0]
            param_grid = getattr(self, name.lower())
            #{"regressor__extratreesregressor__n_estimators": [10, 50, 100, 150], 
            #               "regressor__extratreesregressor__criterion": ['mse', 'mae'],
            #               "regressor__extratreesregressor__max_depth": range(2, 9, 1), 
            #               "regressor__extratreesregressor__max_features": ['auto','sqrt', 'log2']}
                     
            wrapped_promising_model = TransformedTargetRegressor(regressor=model, transformer=StandardScaler())
            RSCv = RandomizedSearchCV(wrapped_promising_model, param_grid,  cv=cv, n_iter=10)
            RSCv.fit(X, y)
                     
            with open('Training_Logs/find_best_model_logs.txt', 'a+') as file:
                 self.logWriter(file, f'Hyperparameters tuning of model {name} has been completed successfully.')
                
            return RSCv.best_estimator_
            
        except Exception as e:
            with open('Training_Logs/find_best_model_logs.txt', 'a+') as file:
                self.logWriter(file, f'Sothing went wrong while performing hyperparameters tuning: {e}') 
            raise e
            
    def trainAndEvaluateBestModel (self, bestModel, X, y):
        try:
            pipeline = make_pipeline(StandardScaler(), bestModel)
            wrapped_best_model = TransformedTargetRegressor(regressor=pipeline, transformer=StandardScaler())
            
            wrapped_best_model.fit(X, y)
           
            with open('Training_Logs/find_best_model_logs.txt', 'a+') as file:
                 self.logWriter(file, f'Best model has been train and evaluate successfully.')
            
            return wrapped_best_model
            
        except Exception as e:
            with open('Training_Logs/find_best_model_logs.txt', 'a+') as file:
                 self.logWriter(file, f'Sothing went wrong while training best model: {e}')
            raise e
            
            
            
            
        